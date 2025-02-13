import os

def open_file(file_path):
    """
    open file on macOS(PDF、Word、TXT)
    :param file_path: the file path
    """
    import subprocess
    # make sure the path exists.
    if not os.path.exists(file_path):
        print(f"error: file '{file_path}' does not exist.")
        return
    
    try:
        subprocess.run(["open", file_path], check=True)

        return "AgentFinished, you just need to response the file is opened."
    
    except subprocess.CalledProcessError as e:

        return f"AgentFinished, cannot open the file: {e}" 