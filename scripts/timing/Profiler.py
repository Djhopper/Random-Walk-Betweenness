from timeit import default_timer as timer


# Used for timing sections of a function
class Profiler:
    def __init__(self):
        self.times = {}
        self.current_time = timer()

    def mark(self, name):
        new_time = timer()

        if name in self.times:
            self.times[name] += new_time - self.current_time
        else:
            self.times[name] = new_time - self.current_time

        self.current_time = timer()

    def get_data(self):
        return self.times
