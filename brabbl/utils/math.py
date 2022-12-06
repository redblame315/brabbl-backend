def iterative_mean(mean, count, value):
    return mean + 1 / (count + 1) * (value - mean)
