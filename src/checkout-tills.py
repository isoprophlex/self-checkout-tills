def minimum_time_at_tills(customers, n_tills):
    if not customers:
        return 0
    tills = [0] * n_tills
    for time in customers:
        min_time_index = tills.index(min(tills))
        tills[min_time_index] += time
    return max(tills)


def main():
    print(minimum_time_at_tills([5, 3, 4], 1))
    print(minimum_time_at_tills([10, 2, 3, 3], 2))
    print(minimum_time_at_tills([2, 3, 10], 2))


main()
