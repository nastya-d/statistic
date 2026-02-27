import pandas as pd
from scipy.stats import norm, chi2


def borders(h, x_min, x_max):
    row = []
    a, b, c = x_min, x_max, x_min
    for i in range(int((x_max-x_min)/h)):
        c += h
        row.append((round(a, 2), round(c, 2)))
        a = c
    row.append((round(c, 2), round(b, 2)))
    return row


def frequencies(int_row, stat_row):
    n_row = []
    c = 0
    for i in range(len(int_row)):
        for j in stat_row:
            if int_row[i][0] <= j and j <= int_row[i][1]:
                c += 1
        n_row.append(c)
        c = 0
    return n_row


def emp_distr_f(rel_fr):
    row = []
    c = 0
    for i in rel_fr:
        c += i
        row.append(round(c, 2))
    return row


def print_all_table_1(f1, f2, f3, f4, f5, f6):
    df = pd.DataFrame({
        '№': (i for i in range(1,8)),
        'Интервал': f1,
        'Середина': f2,
        'Частота': f3,
        'Отн. частота': f4,
        'Эмпр. ф. р.': f5,
        'Плотность': f6,
    })
    df.to_excel("output/table_1.xlsx", index=False)

    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    print(df.to_string(index=False, justify='center'))

def print_all_table_2(f1, f2, f3, f4, f5, f6, f7):
    df = pd.DataFrame({
        '№': (i for i in range(1,6)),
        'Интервал': f1,
        'Частота': f2,
        'Стандартизация': f3,
        'Функция Лапласа': f4,
        'Теорет. вероятн.': f5,
        'Теорет. частоты': f6,
        'Хи-квадрат': f7,
    })
    df.to_excel("output/table_2.xlsx", index=False)

    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    print(df.to_string(index=False, justify='center'))

def math_o(mid_r, rel_r):
    m = 0
    for i in range(len(mid_r)):
        m += mid_r[i] * rel_r[i]
    return round(m, 4)

def disp(mid_r, rel_r):
    d = 0
    for i in range(len(mid_r)):
        d += rel_r[i] * (mid_r[i] - math_o(mid_r, rel_r))**2
    return round(d, 4)

def median(mid_r):
    l = len(mid_r)
    if l % 2 == 0:
        return (mid_r[int(l/2) - 1] + mid_r[int(l/2 + 1) - 1]) / 2
    else:
        return mid_r[int(l/2)]

def moda(mid_r, fre_r):
    ind = fre_r.index(max(fre_r))
    return mid_r[ind]

def u_f(x: tuple[float, float], m, s) -> tuple[float, float]:
    u1 = (x[0] - m)/s
    u2 = (x[1] - m)/s
    return (round(u1, 4), round(u2, 4))


def fu_f(x: tuple[float, float]) -> tuple[float, float]:
    f1 = float(norm.cdf(x[0]))
    f2 = float(norm.cdf(x[1]))
    return (round(f1, 4), round(f2, 4))

def pearson_criterion(int_row, m, correct_sko, n, f_row, st_row, s):
    # проверка критериев
    standardization_row = [u_f(x, m, correct_sko) for x in int_row]  # стандартизация
    fu_row = [fu_f(x) for x in standardization_row]  # функция лапласа
    theoretical_probabilities_of_intervals = [x[1] - x[0] for x in fu_row]  # теоретические вероятности интервалов
    theoretical_frequencies_row = [n * x for x in theoretical_probabilities_of_intervals]  # теоретические частоты

    while any(f < 5 for f in theoretical_frequencies_row):
        for i in range(len(theoretical_frequencies_row))[::-1]:
            if theoretical_frequencies_row[i] < 5:
                if i == 0:
                    new_interval = (int_row[i][0], int_row[i + 1][1])
                    int_row[i] = new_interval
                    del int_row[i + 1]
                else:
                    new_interval = (int_row[i-1][0], int_row[i][1])
                    int_row[i-1] = new_interval
                    del int_row[i]
                break
        f_row = frequencies(int_row, st_row)
        standardization_row = [u_f(x, m, correct_sko) for x in int_row]  # стандартизация
        fu_row = [fu_f(x) for x in standardization_row]  # функция лапласа
        theoretical_probabilities_of_intervals = [x[1] - x[0] for x in fu_row]  # теоретические вероятности интервалов
        theoretical_frequencies_row = [n * x for x in theoretical_probabilities_of_intervals]  # теоретические частоты
    xixi = []
    for i in range(len(f_row)):
        xixi.append(((f_row[i] - theoretical_frequencies_row[i])**2 / theoretical_frequencies_row[i]))
    k = len(int_row) - 2 - 1 # число степеней свободы (число инт - число оцененных параметров - 1)
    krit_xixi = chi2.ppf(1 - s, k)

    print('\nПроверка критерия Пирсона')
    print('Проверка статистической гипотезы с помощью критерия Пирсона ')
    # print(len(int_row), len(f_row), len(standardization_row), len(fu_row), len(theoretical_probabilities_of_intervals), len(theoretical_frequencies_row), len(xixi))
    print_all_table_2(int_row, f_row, standardization_row, fu_row, theoretical_probabilities_of_intervals, theoretical_frequencies_row, xixi)
    print('Основная гипотеза H0: распределение является нормальным')
    print(f'Значение статистики критерия: {round(sum(xixi), 4)}')
    print(f'Уровень значимости: {s}')
    print(f'Число степеней свободы: {k}')
    print(f'Критическое значение (квантиль): {round(krit_xixi, 4)}')

    if sum(xixi) < krit_xixi:
        print('Гипотеза не отвергается')
    else:
        print('Гипотеза отвергается')


if __name__ == '__main__':
    int_r = [(1, 2.8), (2.8, 4.6), (4.6, 6.4), (6.4, 9)]
    st_r = [1, 2, 3, 4, 4, 7, 7, 7, 9, 9]

    frequencies(int_r, st_r)