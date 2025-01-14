import tkinter as tk
from tkinter import scrolledtext
import re

# Function to correct Python code and provide error details
def correct_code(code_snippet):
    lines = code_snippet.split('\n')
    corrected_lines = []
    errors = []
    expected_indentation = 0  # Track the expected level of indentation

    for line_no, line in enumerate(lines, start=1):
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            corrected_lines.append('')
            continue

        # Rule 1: Check Indentation
        actual_indentation = len(line) - len(stripped_line)
        if actual_indentation % 4 != 0 or actual_indentation != expected_indentation:
            errors.append(f"Line {line_no}: Incorrect or inconsistent indentation.")
            actual_indentation = expected_indentation
            line = ' ' * expected_indentation + stripped_line

        # Rule 2: Missing colons in control statements or function definitions
        if re.match(r'^(if|for|while|def|class)\s+.*[^:]$', stripped_line):
            errors.append(f"Line {line_no}: Missing colon after control statement or function definition.")
            stripped_line += ':'
            line = ' ' * actual_indentation + stripped_line

        # Rule 3: Equality operator for conditions
        if re.match(r'^\s*if\s+.*=.*:', stripped_line) and '==' not in stripped_line:
            errors.append(f"Line {line_no}: '=' used instead of '==' in condition.")
            stripped_line = re.sub(r'(if\s+.*?)(=)([^=].*):', r'\1==\3:', stripped_line)
            line = ' ' * actual_indentation + stripped_line

        # Rule 4: Replace printf with print
        if re.match(r'^\s*printf', stripped_line):
            errors.append(f"Line {line_no}: 'printf' is not a valid function name in Python.")
            stripped_line = stripped_line.replace("printf", "print", 1)
            line = ' ' * actual_indentation + stripped_line

        # Rule 5: Ensure proper parentheses in print function
        if re.match(r'^\s*print\s+["\'].*["\']$', stripped_line) or re.match(r'^\s*print\s+.*$', stripped_line):
            if 'print(' not in stripped_line:
                errors.append(f"Line {line_no}: Missing parentheses in 'print' function.")
                stripped_line = re.sub(r'^\s*print\s+(.*)$', r'print(\1)', stripped_line)
                line = ' ' * actual_indentation + stripped_line

        # Rule 6: Fix mismatched quotes in strings
        single_quote_count = stripped_line.count("'")
        double_quote_count = stripped_line.count('"')

        if single_quote_count % 2 != 0 and double_quote_count % 2 == 0:  # Mismatched single quotes
            errors.append(f"Line {line_no}: Mismatched single quotes.")
            stripped_line = re.sub(r"^(.*?)'(.*?)$", r'\1"\2', stripped_line)  # Replace unmatched single quote with double quotes

        elif double_quote_count % 2 != 0 and single_quote_count % 2 == 0:  # Mismatched double quotes
            errors.append(f"Line {line_no}: Mismatched double quotes.")
            stripped_line = re.sub(r'^(.*?)"(.*?)$', r"\1'\2", stripped_line)  # Replace unmatched double quote with single quotes

        # Update the final line
        line = ' ' * actual_indentation + stripped_line
        corrected_lines.append(line)

        # Update expected indentation level
        if stripped_line.endswith(':'):
            expected_indentation += 4
        elif actual_indentation < expected_indentation:
            expected_indentation = actual_indentation

    corrected_code = '\n'.join(corrected_lines)
    return corrected_code, errors

# Create the GUI using tkinter
def create_gui():
    root = tk.Tk()
    root.title("Python Code Corrector")
    root.geometry("700x600")

    tk.Label(root, text="Enter a Python code snippet:", font=("Arial", 12)).pack(pady=10)
    input_code = scrolledtext.ScrolledText(root, width=80, height=10)
    input_code.pack(pady=5)
    tk.Label(root, text="Corrected Code:", font=("Arial", 12)).pack(pady=10)
    output_code = scrolledtext.ScrolledText(root, width=80, height=10)
    output_code.pack(pady=5)
    tk.Label(root, text="Error Details:", font=("Arial", 12)).pack(pady=10)
    error_details = scrolledtext.ScrolledText(root, width=80, height=10)
    error_details.pack(pady=5)

    def on_correct_button_click():
        code_input = input_code.get("1.0", tk.END).strip()
        corrected_code, errors = correct_code(code_input)
        output_code.delete("1.0", tk.END)
        output_code.insert(tk.END, corrected_code)
        error_details.delete("1.0", tk.END)
        for error in errors:
            error_details.insert(tk.END, error + '\n')

    tk.Button(root, text="Correct Code", command=on_correct_button_click, font=("Arial", 12)).pack(pady=10)
    root.mainloop()

# Ensure the GUI function is called
if __name__ == "__main__":
    create_gui()
