def colored_text(text, color_code, bold=True):
    """
    Generate colored and bold text
    """
    bold_code = "1;" if bold else ""
    return f"\033[{bold_code}{color_code}m{text}\033[0m"