import numpy as np

def log_transform(values, desired_sum=None):
    log_values = [np.log1p(value) for value in values]  # np.log1p is used to handle log(0) case
    if desired_sum is not None:
        log_sum = sum(log_values)
        adjusted_values = [value / log_sum * desired_sum for value in log_values]
    else:
        adjusted_values = log_values
    return adjusted_values


x = [((185, (0,)), (211, (1,))), ((208, (0,)), (156, (1,))), ((110, (0,)), (109, (1,))), ((146, (0, 1)),)]
for s in x:
    print(s)
    for value, index in s:
        print(value, index)