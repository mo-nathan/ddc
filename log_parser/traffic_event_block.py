class TrafficEventBlock(object):
    def __init__(self, count, start_time, end_time=None):
        if end_time is None:
            end_time = start_time
        if start_time and end_time < start_time:
            raise ValueError
        self.count = count
        self.start_time = start_time
        self.end_time = end_time

    def add_if_in_range(self, new_time, seconds):
        if new_time < self.end_time:
            return False
        if new_time - self.start_time > seconds:
            return False
        self.end_time = new_time
        self.count += 1
        return True
