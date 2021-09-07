sliding_value_sum = 0
sliding_value_queue = []


def smooth(value_list, window_size, ignoreZeros):
    global sliding_value_sum
    sliding_value_sum = 0
    global sliding_value_queue
    sliding_value_queue = []
    smoothed_value_list = []
    for val in value_list:
        if ignoreZeros and val == 0:
            continue
        smoothed_value_list.append(sliding_window_average(val, window_size))
    return smoothed_value_list


def sliding_window_average(current_value, windowSize):
    global sliding_value_sum
    sliding_value_sum += current_value
    sliding_value_queue.append(current_value)
    if len(sliding_value_queue) > windowSize:
        sliding_value_sum -= sliding_value_queue.pop(0)
        return sliding_value_sum/windowSize
    return current_value
