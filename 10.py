import random
import time
import matplotlib.pyplot as plt
from statistics import mean


# Task 1: QuickSort comparison

def deterministic_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  # middle element as pivot
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return deterministic_quick_sort(left) + middle + deterministic_quick_sort(right)


def randomized_quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return randomized_quick_sort(left) + middle + randomized_quick_sort(right)


def benchmark_sorting_algorithms(sizes, trials=5):
    results = []
    for size in sizes:
        det_times = []
        rnd_times = []
        for _ in range(trials):
            array = [random.randint(-10**6, 10**6) for _ in range(size)]
            start = time.perf_counter()
            deterministic_quick_sort(array.copy())
            det_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            randomized_quick_sort(array.copy())
            rnd_times.append(time.perf_counter() - start)

        results.append({
            "size": size,
            "deterministic_avg": mean(det_times),
            "randomized_avg": mean(rnd_times)
        })
    return results


# Task 2: Greedy scheduling

class Teacher:
    def __init__(self, first_name, last_name, age, email, can_teach_subjects):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()


def create_schedule(subjects, teachers):
    uncovered_subjects = set(subjects)
    schedule = []

    while uncovered_subjects:
        best_teacher = None
        best_coverage = set()

        for teacher in teachers:
            available = teacher.can_teach_subjects & uncovered_subjects
            if not available:
                continue
            if (not best_teacher or
                len(available) > len(best_coverage) or
                (len(available) == len(best_coverage) and teacher.age < best_teacher.age)):
                best_teacher = teacher
                best_coverage = available

        if not best_teacher:
            return None

        best_teacher.assigned_subjects = best_coverage
        uncovered_subjects -= best_coverage
        schedule.append(best_teacher)

    return schedule


# Running both tasks
sizes = [10_000, 50_000, 100_000, 500_000]
sort_results = benchmark_sorting_algorithms(sizes)

# Plotting results
sizes = [r['size'] for r in sort_results]
det_times = [r['deterministic_avg'] for r in sort_results]
rnd_times = [r['randomized_avg'] for r in sort_results]

plt.plot(sizes, det_times, label='Deterministic QuickSort')
plt.plot(sizes, rnd_times, label='Randomized QuickSort')
plt.xlabel('Array Size')
plt.ylabel('Average Time (seconds)')
plt.title('QuickSort Algorithm Performance Comparison')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd
df = pd.DataFrame(sort_results)
print(df.to_string(index=False))
