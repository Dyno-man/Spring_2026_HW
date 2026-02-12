def log_calc(num):
    if num == 1:
        return 0
    elif num == 2:
        return 1
    else:
        return 1 + log_calc(num//2)

print(log_calc(128))
