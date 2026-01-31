import ast
import pycodestyle
from google.colab import files

class CodeReviewer:
    def __init__(self):
        self.feedback = []

    def analyze_python_code(self, code):
        #Analyze Python code for errors and style violations.
        try:
            # Parse the Python code into an Abstract Syntax Tree
            tree = ast.parse(code)
        except SyntaxError as e:
            self.feedback.append(f"Syntax Error: {e}")
            return

        # Check for indentation errors and undefined variables
        self._check_indentation(tree)
        self._check_undefined_vars(tree)

        # Check code style using pycodestyle
        self._check_code_style(code)

        # Check code comments
        self._check_comments(code)

    def _check_indentation(self, tree):
        #Checks if functions and loops have proper indentation.
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.body and not isinstance(node.body[0], ast.Expr):
                    self.feedback.append(
                        f"Function '{node.name}' should have a docstring or 'pass' statement."
                    )
            elif isinstance(node, (ast.For, ast.While, ast.If, ast.With)):
                if not isinstance(node.body[0], ast.Expr):
                    self.feedback.append(
                        f"Indentation Error: Missing 'pass' statement for '{ast.dump(node)}'."
                    )

    def _check_undefined_vars(self, tree):
        #Detects variables that are used but not defined.
        undefined_vars = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                undefined_vars.discard(node.id)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                undefined_vars.add(node.id)

        for var in undefined_vars:
            self.feedback.append(f"Variable '{var}' is used but not defined.")

    def _check_code_style(self, code):
        """Checks for PEP 8 violations using pycodestyle."""
        style_guide = pycodestyle.StyleGuide(quiet=True)

        # Save code to a temporary file for analysis
        with open("temp_code.py", "w") as temp_file:
            temp_file.write(code)

        result = style_guide.check_files(["temp_code.py"])

        if result.total_errors > 0:
            self.feedback.append(f"Code style issues found: {result.total_errors} violations.")

    def _check_comments(self, code):
        """Checks for properly formatted comments."""
        lines = code.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("#"):
                if len(line.strip()) == 1 or (len(line.strip()) > 1 and line.strip()[1] != " "):
                    self.feedback.append(
                        f"Improve comment style in line {i + 1}: '{line.strip()}'"
                    )

    def get_feedback(self):
        """Returns the feedback collected during the review."""
        return self.feedback


# Upload Python file in Google Colab
print("📂 Please upload a Python (.py) file for code review.")
uploaded = files.upload()
file_name = list(uploaded.keys())[0]  # Get the uploaded file name

# Read and analyze the uploaded Python file
with open(file_name, "r") as file:
    code = file.read()

# Run the code reviewer
code_reviewer = CodeReviewer()
code_reviewer.analyze_python_code(code)

# Display feedback
feedback = code_reviewer.get_feedback()

print("\n📋 Code Review Feedback:")
if feedback:
    for msg in feedback:
        print(f"- {msg}")
else:
    print("✅ No coding errors found. Code looks good!")

