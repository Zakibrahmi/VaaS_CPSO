import numpy as np

def log_transform(values, desired_sum=None):
    log_values = [np.log1p(value) for value in values]  # np.log1p is used to handle log(0) case
    if desired_sum is not None:
        log_sum = sum(log_values)
        adjusted_values = [value / log_sum * desired_sum for value in log_values]
    else:
        adjusted_values = log_values
    return adjusted_values

values = [3.6365155159836138, 0.7600834638388854, 0.023977474695476668, 92.31878054871922]
desired_sum = None  # Set to None to keep the natural sum
scaled_values = log_transform(values, desired_sum)

print(f"Scaled values: {scaled_values}")
print(f"Sum of scaled values: {sum(scaled_values)}")