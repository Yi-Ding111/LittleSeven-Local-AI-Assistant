def get_local_time(input: str = None) -> str:
    from datetime import datetime
    current_time = datetime.now().strftime("%H:%M:%S")
    # print(f"LocalTime tool called, returning: {current_time}")
    return f"Current local time is: {current_time}"