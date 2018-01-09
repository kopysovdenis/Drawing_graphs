from numpy.ma import ceil


class param_stabs():
    def __init__(self):
        pass

    def make_intervals(self, start_intense, final_intense, interval, duration, step_length, files_count,
                       init_delay=0):
        try:
            intervals_per_step = int(ceil(float(step_length) / interval))
            step_count = int(duration / step_length)
            interval = int(round(float(step_length) / intervals_per_step * 60))
            start_intense_per_step = round(start_intense / (60.0 / step_length))
            final_intense_per_step = round(final_intense / (60.0 / step_length))
            step_intense = (final_intense_per_step - start_intense_per_step) / (step_count - 1 if step_count > 1 else 1)
            intenses = [int(round(start_intense_per_step + i * step_intense)) for i in range(0, step_count)]
            steps = [i * files_count for i in intenses]
            out = []
            for s in steps:
                taill = 0
                for i in range(0, intervals_per_step):
                    new_val = int(round(((float(s) / intervals_per_step) + taill) / 2.) * 2)
                    taill += float(s) / intervals_per_step - new_val
                    out.append(new_val)
            return [sum(out) / files_count] + [[interval if n > 0 else 0, o] for n, o in enumerate(out)]
        except Exception as e:
            return e