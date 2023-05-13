def split_time(time: str):
    if ':' in time:
        return [time.split(':')[0], time.split(':')[1]]
    if '.' in time:
        return [time.split('.')[0], time.split('.')[1]]