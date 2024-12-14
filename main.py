import math
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, f, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Шаг 1: Загрузка датасета из CSV файла
# Предположим, что в файле data.csv есть столбцы 'X' и 'Y'
# Если столбцы называются иначе, замените их названия в коде
data = pd.read_csv('data.csv')  # Замените 'data.csv' на путь к вашему файлу

# Удаляем пробелы в именах столбцов
data.columns = data.columns.str.strip()

# Проверяем наличие столбца 'Y'
if 'Y' not in data.columns:
    raise ValueError("Столбец 'Y' не найден в DataFrame. Доступные столбцы: " + ", ".join(data.columns))

n = len(data)
sum_of_squares = 0

# Шаг 2: Вычисление математического ожидания и разностей
expected_value = data['Y'].mean()
data['y_i-y'] = data['Y'] - expected_value
# Вычисление квадрата разности
data['(Разница)^2'] = data['y_i-y'] ** 2
sum_of_squares = data['(Разница)^2'].sum()

# Шаг 3: Вычисление несмещённой дисперсии и стандартного отклонения
unbiased_variance = data['Y'].var(ddof=1)
std_dev = np.sqrt(unbiased_variance)

# Шаг 4: Вычисление статистики Ирвина
data['Абсолютная разница'] = data['Y'].diff().abs()
data['Статистика Ирвина'] = data['Абсолютная разница'] / std_dev

# Шаг 5: Определение критического значения для заданного p
p = 0.95
S_crit = 1.3

data['Статистика Ирвина'] = data['Статистика Ирвина'].fillna(0)
data['Выброс'] = data['Статистика Ирвина'].apply(lambda x: 'Да' if x > S_crit else 'Нет')

data.rename(columns={
    'X': 'X',
    'Y': 'Значение Y',
}, inplace=True)

# Вывод результатов
print("1) Математическое ожидание (среднее значение):", expected_value)
print("4) Сумма квадратов отклонений", sum_of_squares)
print("5) Выборочная дисперсия", sum_of_squares/(n-1))
print("6) Выборочное стандартное отклонение", math.sqrt(sum_of_squares / (n - 1)))
print("Критическое значение статистики Ирвина для p =", p, ":", S_crit)
print("\nДанные с вычислениями:")
print(data)

# Аппроксимация (линейная регрессия)
x_vals = data['X'].values
y_vals = data['Значение Y'].values
a, b = np.polyfit(x_vals, y_vals, 1)

x_line = np.linspace(min(x_vals), max(x_vals), 100)
y_line = a*x_line + b

outliers = data['Выброс'] == 'Да'

# Построение графика
plt.figure(figsize=(10, 6))
plt.title("График с выделением выбросов, средним и линейной аппроксимацией")

# Исходные точки
plt.scatter(data['X'], data['Значение Y'], label='Данные', c='blue')

# Отдельно отобразим выбросы (если есть)
if outliers.any():
    plt.scatter(data.loc[outliers, 'X'], data.loc[outliers, 'Значение Y'],
                color='red', label='Выбросы')


# Линия аппроксимации
plt.plot(x_line, y_line, color='orange', label=f'Аппроксимация: y={a:.2f}x+{b:.2f}')

plt.xlabel('X')
plt.ylabel('Значение Y')
plt.grid(True)
plt.legend()
plt.show()
