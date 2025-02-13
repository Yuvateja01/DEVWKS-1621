import subprocess

def run_script(script_path):
    """
    Runs a Python script located at the given path.

    Args:
        script_path (str): The file path to the Python script to be executed.

    Prints:
        A message indicating the script is being run.
        A success message if the script runs successfully.
        An error message if there is an issue running the script.

    Raises:
        subprocess.CalledProcessError: If the script execution fails.
    """
    print(f"Running script: {script_path}")
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Successfully ran {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")

if __name__ == "__main__":
    scripts = [
        'data_collection/get_configs.py',
        'data_transformation/transformation.py',
        'data_import/webex_user_import.py',
        'webex_device_import.py'
    ]

    success_count = 0
    failure_count = 0

    for script in scripts:
        try:
            run_script(script)
            success_count += 1
        except Exception:
            failure_count += 1

    print(f"\nSummary:")
    print(f"Total scripts: {len(scripts)}")
    print(f"Successfully ran: {success_count}")
    print(f"Failed to run: {failure_count}")