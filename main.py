from main_meanings import read_data
from functions import *
from math import log10
import matplotlib.pyplot as plt

import os
from sys import argv
SHOW_GRAPHS = (len(argv) > 1 and argv[1] == 'show-graphs')
os.makedirs('output', exist_ok=True)

# первичная обработка выборки
statistical_row = sorted(read_data()) # статистический ряд

a = [(i, statistical_row.count(i)) for i in statistical_row]
b= list(dict.fromkeys(a))
variation_row = [x[0] for x in b] # вариационный ряд

frequencies_row_all = [x[1] for x in b] # частоты вариационного ряда

n = sum(frequencies_row_all) # объём выборки
relative_frequencies_all = [i/n for i in frequencies_row_all] # относительные частоты вариационного ряда

x_min = min(variation_row) # минимальное значение
x_max = max(variation_row) # максимальное значение
R = x_max - x_min # размах выборки
h = round((R / (1 + (3.322 * log10(n)))), 2) # шаг
interval_row = borders(h, x_min, x_max) # интервальный ряд
middle_row = [round((i[0]+i[1])/2, 3) for i in interval_row] # середины интервалов
frequencies_row = frequencies(interval_row, statistical_row) # частоты интервалов
relative_frequencies = [i/n for i in frequencies_row] # относительные частоты интервалов
empirical_distribution_function = emp_distr_f(relative_frequencies) # эмпирическая функция распределения
frequency_density = [round(i/h, 2) for i in relative_frequencies] # плотность частоты

# вывод таблицы 1
print('Статистический интервальный ряд распределения и основные характеристики')
print(f'Объём выборки: {n}')
print(f'Минимальное значение: {x_min}; Максимальное значение: {x_max}')
print(f'Размах выборки: {R};        Шаг: {h}')
print_all_table(interval_row, middle_row, frequencies_row, relative_frequencies, empirical_distribution_function, frequency_density)

# графики
# полигон частот
plt.plot(middle_row, frequencies_row)
plt.xlabel('частичные интервалы')
plt.ylabel('частоты')
plt.title('Полигон частот')
plt.savefig('output/Полигон частот.png')
if SHOW_GRAPHS: plt.show()
plt.clf()

# полигон относительных частот
plt.plot(middle_row, relative_frequencies)
plt.xlabel('частичные интервалы')
plt.ylabel('относительные частоты')
plt.title('Полигон относительных частот')
plt.savefig('output/Полигон относительных частот.png')
if SHOW_GRAPHS: plt.show()
plt.clf()

# гистограмма относительных частот
plt.bar(middle_row, frequency_density, width=0.3, edgecolor = 'black')
plt.title('Гистограмма относительных частот')
plt.xlabel('частичные интервалы')
plt.ylabel('плотность частоты')
plt.savefig('output/Гистограмма относительных частот.png')
if SHOW_GRAPHS: plt.show()
plt.clf()

# эмпирическая функция распределения
plt.plot(middle_row, empirical_distribution_function)
plt.xlabel('частичные интервалы')
plt.ylabel('эмпирическая функция распределения')
plt.title('Эмпирическая функция распределения')
plt.savefig('output/Эмпирическая функция распределения.png')
if SHOW_GRAPHS: plt.show()
plt.clf()

# точечные оценки числовых характеристик
M = math_o(middle_row, relative_frequencies) # выборочное среднее
D = disp(middle_row, relative_frequencies) # выборочная дисперсия
SKO = round(D**0.5, 4) # выборочное СКО
corrected_D = round((n/(n-1))*D, 4) # исправленная выборочная дисперсия
corrected_SKO = round(corrected_D**0.5, 4) # исправленное выборочное СКО
median = median(middle_row) # медиана
moda = moda(middle_row, frequencies_row) # мода

print('\nТочечные оценки числовых характеристик')
print(f'Выборочное среднее: {M}')
print(f'Выборочная дисперсия: {D}')
print(f'Выборочное СКО: {SKO}')
print(f'Исправленная выборочная дисперсия: {corrected_D}')
print(f'Исправленное выборочное СКО: {corrected_SKO}')
print(f'Выборочная медиана: {median}')
print(f'Выборочная мода: {moda}')
