import re
import string
import numpy as np
import math
from porter import Porter


# Функция на замену спец символов
def clearWord(word):
    return re.sub('[' + string.punctuation + ']', '', word)


def stop_symbols(sentence):
    stop = ['-', 'еще', 'него', 'сказать', 'а', 'ж', 'нее', 'со', 'без', 'же', 'ней', 'совсем', 'более', 'жизнь',
            'нельзя', 'так', 'больше', 'за', 'нет', 'такой', 'будет', 'зачем', 'ни', 'там', 'будто', 'здесь', 'нибудь',
            'тебя', 'бы', 'и', 'никогда', 'тем', 'был', 'из', 'ним', 'теперь', 'была', 'из-за', 'них', 'то', 'были',
            'или', 'ничего', 'тогда', 'было', 'им', 'но', 'того', 'быть', 'иногда', 'ну', 'тоже', 'в', 'их', 'о',
            'только', 'вам', 'к', 'об', 'том', 'вас', 'кажется', 'один', 'тот', 'вдруг', 'как', 'он', 'три', 'ведь',
            'какая', 'она', 'тут', 'во', 'какой', 'они', 'ты', 'вот', 'когда', 'опять', 'у', 'впрочем', 'конечно', 'от',
            'уж', 'все', 'которого', 'перед', 'уже', 'всегда', 'которые', 'по', 'хорошо', 'всего', 'кто', 'под', 'хоть',
            'всех', 'куда', 'после', 'чего', 'всю', 'ли', 'потом', 'человек', 'вы', 'лучше', 'потому', 'чем', 'г',
            'между', 'почти', 'через', 'где', 'меня', 'при', 'что', 'говорил', 'мне', 'про', 'чтоб', 'да', 'много',
            'раз', 'чтобы', 'даже', 'может', 'разве', 'чуть', 'два', 'можно', 'с', 'эти', 'для', 'мой', 'сам', 'этого',
            'до', 'моя', 'свое', 'этой', 'другой', 'мы', 'свою', 'этом', 'его', 'на', 'себе', 'этот', 'ее', 'над',
            'себя', 'эту', 'ей', 'надо', 'сегодня', 'я', 'ему', 'наконец', 'сейчас', 'если', 'нас', 'сказал', 'есть',
            'не', 'сказала']

    sentence = clearWord(sentence).lower().split()
    clear_sentence = ''
    for word in sentence:
        if word not in stop:
            clear_sentence += word + ' '
    return clear_sentence.strip()


docs = [
    'Британская полиция знает о местонахождении основателя WikiLeaks',
    'В суде США начинается процесс против россиянина, рассылавшего спам',
    'Церемонию вручения Нобелевской премии мира бойкотируют 19 стран',
    'В Великобритании арестован основатель сайта Wikileaks Джулиан Ассандж',
    'Украина игнорирует церемонию вручения Нобелевской премии',
    'Шведский суд отказался рассматривать апелляцию основателя Wikileaks',
    'НАТО и США разработали планы обороны стран Балтии против России',
    'Полиция Великобритании нашла основателя WikiLeaks, но, не арестовал',
    'В Стокгольме и Осло сегодня состоится вручение Нобелевских премий'
]

docs_copy = docs.copy()

for i in range(len(docs)):
    docs[i] = stop_symbols(docs[i])

[print(elem) for elem in docs]
print()


def my_stemmer(sentence):
    porter = Porter()
    ready = ''
    sentence = sentence.split()
    for word in sentence:
        word = porter.stem(word)
        ready += word + ' '
    return ready.strip()


for i in range(len(docs)):
    docs[i] = my_stemmer(docs[i])

[print(elem) for elem in docs]
print()


def search_common_words(lst):
    result = []
    slov = {}
    for i in range(len(lst)):
        words = lst[i].split()
        for word in words:
            if word not in slov:
                slov[word] = 1
            else:
                slov[word] += 1
    keys = list(slov.keys())
    values = list(slov.values())
    for i in range(len(values)):
        if values[i] > 1 and keys[i] not in result:
            result.append(keys[i])
    return result


similar_words = sorted(search_common_words(docs))

print(similar_words)
print()


# Составление матрицы
def drawing_up_the_matrix(words, sentences):
    matrix = []
    for i in range(len(words)):
        matrix.append([])
        for text in sentences:
            text = text.split()
            matrix[i].append(text.count(words[i]))
    return matrix


matrix = drawing_up_the_matrix(similar_words, docs)
[print(elem) for elem in matrix]

U, S, Vt = np.linalg.svd(matrix)
print()

print('Здесь первые 2 строчки Vt матрица')
print(-1 * Vt[0:2, :])
print()
coord = -1 * Vt[0:2, :]
new_coord = []

for i in range(len(docs)):
    new_coord.append((round(coord[0][i], 4), round(coord[1][i], 4)))
print(new_coord)
print()


# Поиск ближайшего предложения
def find_near(coord, other_coords):
    # x, y = [], []
    values = []
    for i in range(len(other_coords)):
        values.append((round(abs(coord[0] - other_coords[i][0]), 4), round(abs(coord[1] - other_coords[i][1]), 4)))
    return other_coords.index(other_coords[values.index(min(values))]) + 1


print(docs_copy[find_near(new_coord[0], new_coord[1:])])
