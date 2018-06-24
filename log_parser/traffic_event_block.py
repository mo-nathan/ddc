class TrafficEventBlock(object):
    def __init__(self, count, start_time, end_time):
        if start_time and end_time < start_time:
            raise ValueError
        self.count = count
        self.start_time = start_time
        self.end_time = end_time
