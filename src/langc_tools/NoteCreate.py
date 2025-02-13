def create_stickies_note(note_text):
    import subprocess

    # erase special symbols
    note_text = note_text.replace('"', '\\"')
    # allow start a new line
    note_text = note_text.replace("\n", '" & return & "')

    applescript = f"""
    tell application "Stickies"
        activate
    end tell
    delay 1
    tell application "System Events"
        keystroke "n" using {{command down}} -- create new stick
        delay 1
        keystroke "{note_text}" -- note input
    end tell
    """
    subprocess.run(["osascript", "-e", applescript])

    return f"AgentFinished, you just need to response the note is done."
