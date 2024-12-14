import random
from random import randint

import numpy as np
import pandas as pd

# Временной ряд

time_series  = [random.randint(1, 20) for _ in range(20)]
time_series = [10, 12, 15, 18, 20, 25, 28, 30, 35, 40, 42, 45, 48, 50, 55, 58, 60, 65, 68, 70]
sorted_data = sorted(time_series)
import math

# Шаг 1: Определяем данные
data =  [random.randint(1, 20) for _ in range(20)]  # Замените на ваши данные

# Шаг 2: Создаем вариационный ряд (сортируем данные)
sorted_data = sorted(time_series)

# Шаг 3: Находим медиану
n = len(sorted_data)
if n % 2 == 0:  # Если количество элементов четное
    median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
else:  # Если количество элементов нечетное
    median = sorted_data[n // 2]

print(f"Медиана: {median}")


binary_sequence = ["+" if x > median else "=" if x == median else "-" for x in time_series]

print(f"последовательность: {binary_sequence}")


current = binary_sequence[0]
series_count = 1
series_lengths = [1]


def group_series(signs):
    grouped = []
    current_series = signs[0]
    count = 1
    for i in range(1, len(signs)):
        if signs[i] == current_series:
            count += 1
        else:
            if current_series != '=':
                grouped.append((current_series, count))
            current_series = signs[i]
            count = 1
    if current_series != '=':
        grouped.append((current_series, count))
    return grouped

grouped_series = group_series(binary_sequence)
print(grouped_series)

U_n = len(grouped_series)

print(f"Количество серий: {U_n }")


max_series_length = max(series_lengths)

# Рассчитываем пороговое значение t(n)
tn = 3.3 * (math.log10(n) + 1)

# Проверяем неравенства

v_n = math.floor(series_count)
t_n = math.floor(max_series_length)
vn=1/2*(n+2-1.96*(n-1)**(0.5))



print(f"Пороговое значение t(n): {tn:.2f}")
print(f"Число серий v(n): {v_n}")
print(f"Максимальная длина серии t(n): {t_n}")

if t_n < tn or v_n > vn:
    print("Тренд есть.")
else:
    print("Тренд отсутствует.")
