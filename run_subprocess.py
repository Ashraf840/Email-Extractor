import subprocess

# Command to run (replace it with your own command)
# command = "python -c 'print(\"Hello, subprocess!\")'"
# command = ["python", "-c", 'print("Hello, subprocess!")']
command = ["ls -la"]

# Run the command
result = subprocess.run(
    command, 
    shell=True, 
    # stdout=subprocess.PIPE, 
    # stderr=subprocess.PIPE, 
    text=True,
    capture_output=True,
    )

# Print the result
print("Exit Code:", result.returncode)
print("Standard Output:", result.stdout)
print("Standard Error:", result.stderr)