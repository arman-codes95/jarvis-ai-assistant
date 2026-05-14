import os
import subprocess


# -----------------------------
# SAVE FILE
# -----------------------------
def save_code_file(filename, content):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"{filename} has been saved successfully."
    except Exception as e:
        return f"Error saving file: {str(e)}"


# -----------------------------
# RUN PYTHON FILE
# -----------------------------
def run_python_file(filename):
    try:
        result = subprocess.run(
            ["python", filename],
            capture_output=True,
            text=True
        )

        if result.stderr:
            return result.stderr

        return result.stdout if result.stdout else "Execution completed successfully."

    except Exception as e:
        return f"Python execution error: {str(e)}"


# -----------------------------
# COMPILE & RUN JAVA FILE
# -----------------------------
def run_java_file(filename):
    try:
        # Compile
        compile_process = subprocess.run(
            ["javac", filename],
            capture_output=True,
            text=True
        )

        if compile_process.stderr:
            return compile_process.stderr

        # Extract class name safely
        class_name = os.path.splitext(os.path.basename(filename))[0]

        # Run
        run_process = subprocess.run(
            ["java", class_name],
            capture_output=True,
            text=True
        )

        if run_process.stderr:
            return run_process.stderr

        return run_process.stdout if run_process.stdout else "Execution completed successfully."

    except Exception as e:
        return f"Java execution error: {str(e)}"


# -----------------------------
# OPEN TERMINAL
# -----------------------------
def open_terminal():
    try:
        subprocess.Popen("start cmd", shell=True)
        return "Opening terminal."
    except Exception as e:
        return f"Error opening terminal: {str(e)}"