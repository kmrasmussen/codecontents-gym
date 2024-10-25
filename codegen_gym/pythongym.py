import os
import tempfile
import subprocess
import sys

def execute_code_with_input(code_string, input_string):
    # Create temporary files for code and input
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as code_file, \
         tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as input_file:
        
        # Write code and input to temporary files
        code_file.write(code_string)
        input_file.write(input_string)
        
        # Close the files to ensure all data is written
        code_file.close()
        input_file.close()
        
        try:
            # Execute the code using subprocess with input and output redirection
            with open(input_file.name, 'r') as input_file, \
                 tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as output_file:
                
                result = subprocess.run(
                    [sys.executable, code_file.name],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5  # 5 second timeout to prevent infinite loops
                )
                
                # Read the output
                output_file.seek(0)
                stdout = output_file.read()
            
            # Capture stderr
            stderr = result.stderr
            
            return stdout, stderr, result.returncode
        
        except subprocess.TimeoutExpired:
            return "", "Execution timed out after 5 seconds", 1
        except Exception as e:
            return "", f"An error occurred: {str(e)}", 1
        
        finally:
            # Clean up temporary files
            os.unlink(code_file.name)
            os.unlink(input_file.name)
            if 'output_file' in locals():
                os.unlink(output_file.name)

# Example usage
if __name__ == "__main__":
    code_string = """
import sys

# Read input
n, k = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# Print received input
print(f"n = {n}, k = {k}")
print(f"a = {a}")
print(f"b = {b}")

# Perform some operation (example)
result = sum(a) + sum(b)
print(f"Result: {result}")
"""

    input_string = """5 3
1 2 3 4 5
6 7 8 9 10
"""

    stdout, stderr, return_code = execute_code_with_input(code_string, input_string)

    print("Stdout:")
    print(stdout)
    print("\nStderr:")
    print(stderr)
    print(f"\nReturn code: {return_code}")