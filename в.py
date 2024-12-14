import numpy as np
from scipy.stats import f, ttest_ind


def detect_trend_with_var_test(data, alpha=0.05):


    data = np.asarray(data)
    n = len(data)
    if n < 4:

        return False, None

    # Делим данные на две примерно равные части
    first_half = data[:n // 2]
    second_half = data[n // 2:]

    # Оценим дисперсии
    var1 = np.var(first_half, ddof=1)
    var2 = np.var(second_half, ddof=1)


    if var1 > var2:
        F = var1 / var2
        dfn = len(first_half) - 1
        dfd = len(second_half) - 1
    else:
        F = var2 / var1
        dfn = len(second_half) - 1
        dfd = len(first_half) - 1


    # P(F > f) = 2 * min(P(F > F_obs), P(F < 1/F_obs))

    p_value_f = 2 * min(f.sf(F, dfn, dfd), f.cdf(F, dfn, dfd))


    equal_var = p_value_f > alpha


    t_stat, p_value_t = ttest_ind(first_half, second_half, equal_var=equal_var)

    # Двухсторонняя альтернатива
    trend = p_value_t < alpha

    return trend, p_value_t



if __name__ == "__main__":
    np.random.seed(42)

    data_no_trend = np.concatenate([np.random.normal(0, 1, 50),
                                    np.random.normal(0, 1, 50)])
    data=[10, 12, 15, 18, 20, 25, 28, 30, 35, 40, 42, 45, 48, 50, 55, 58, 60, 65, 68, 70]
    trend_detected, p = detect_trend_with_var_test(data, alpha=0.05)
    print("", "Тренд есть" if trend_detected else "Тренда нет")

    # Генерируем данные с трендом: вторая часть со сдвигом по среднему
    data_with_trend = np.concatenate([np.random.normal(0, 1, 50),
                                      np.random.normal(1, 1, 50)])
    trend_detected, p = detect_trend_with_var_test(data_with_trend, alpha=0.05)
    print("With trend data:", "Trend" if trend_detected else "No Trend", "p-value:", p)
