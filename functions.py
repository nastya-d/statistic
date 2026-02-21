import pandas as pd

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

def print_all_table(f1, f2, f3, f4, f5, f6):
    df = pd.DataFrame({
        '№': (i for i in range(1,8)),
        'Интервал': f1,
        'Середина': f2,
        'Штрих-столбец': ('' for i in range(7)),
        'Частота': f3,
        'Отн. частота': f4,
        'Эмпр. ф. р.': f5,
        'Плотность': f6,
    })
    df.to_excel("output/table.xlsx", index=False)

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

if __name__ == '__main__':
    int_r = [(1, 2.8), (2.8, 4.6), (4.6, 6.4), (6.4, 9)]
    st_r = [1, 2, 3, 4, 4, 7, 7, 7, 9, 9]

    frequencies(int_r, st_r)