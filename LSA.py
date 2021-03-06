import re
import string
import numpy as np
from porter import Porter


class LSA:
    def __init__(self, question, questions):
        self.docs = questions
        self.docs.insert(0, question)

    # Функция на замену спец символов
    def clearWord(self, word):
        return re.sub('[' + string.punctuation + ']', '', word)

    def stop_symbols(self, sentence):
        stop = ['-', 'еще', 'него', 'сказать', 'а', 'ж', 'нее', 'со', 'без', 'же', 'ней', 'совсем',
                'более', 'жизнь',
                'нельзя', 'так', 'больше', 'за', 'нет', 'такой', 'будет', 'зачем', 'ни', 'там',
                'будто', 'здесь', 'нибудь',
                'тебя', 'бы', 'и', 'никогда', 'тем', 'был', 'из', 'ним', 'теперь', 'была', 'из-за',
                'них', 'то', 'были',
                'или', 'ничего', 'тогда', 'было', 'им', 'но', 'того', 'быть', 'иногда', 'ну',
                'тоже', 'в', 'их', 'о',
                'только', 'вам', 'к', 'об', 'том', 'вас', 'кажется', 'один', 'тот', 'вдруг', 'как',
                'он', 'три', 'ведь',
                'какая', 'она', 'тут', 'во', 'какой', 'они', 'ты', 'вот', 'когда', 'опять', 'у',
                'впрочем', 'конечно', 'от',
                'уж', 'все', 'которого', 'перед', 'уже', 'всегда', 'которые', 'по', 'хорошо',
                'всего', 'кто', 'под', 'хоть',
                'всех', 'куда', 'после', 'чего', 'всю', 'ли', 'потом', 'человек', 'вы', 'лучше',
                'потому', 'чем', 'г',
                'между', 'почти', 'через', 'где', 'меня', 'при', 'что', 'говорил', 'мне', 'про',
                'чтоб', 'да', 'много',
                'раз', 'чтобы', 'даже', 'может', 'разве', 'чуть', 'два', 'можно', 'с', 'эти', 'для',
                'мой', 'сам', 'этого',
                'до', 'моя', 'свое', 'этой', 'другой', 'мы', 'свою', 'этом', 'его', 'на', 'себе',
                'этот', 'ее', 'над',
                'себя', 'эту', 'ей', 'надо', 'сегодня', 'я', 'ему', 'наконец', 'сейчас', 'если',
                'нас', 'сказал', 'есть',
                'не', 'сказала']

        sentence = self.clearWord(sentence).lower().split()
        clear_sentence = ''
        for word in sentence:
            if word not in stop:
                clear_sentence += word + ' '
        return clear_sentence.strip()

    def my_stemmer(self, sentence):
        porter = Porter()
        ready = ''
        sentence = sentence.split()
        for word in sentence:
            word = porter.stem(word)
            ready += word + ' '
        return ready.strip()

    def search_common_words(self, lst):
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

    # Составление матрицы
    def drawing_up_the_matrix(self, words, sentences):
        matrix = []
        for i in range(len(words)):
            matrix.append([])
            for text in sentences:
                text = text.split()
                matrix[i].append(text.count(words[i]))
        return matrix

    # Поиск ближайшего предложения
    def find_near(self, coord, other_coords):
        ready = []
        for i in range(len(other_coords)):
            ready.append((i, (round(abs(coord[0] - other_coords[i][0]), 4),
                              round(abs(coord[1] - other_coords[i][1]), 4))))

        ready = sorted(ready, key=lambda x: x[1])

        return ready

    def main(self):
        self.docs_copy = self.docs.copy()

        for i in range(len(self.docs)):
            self.docs[i] = self.stop_symbols(self.docs[i])
        for i in range(len(self.docs)):
            self.docs[i] = self.my_stemmer(self.docs[i])

        similar_words = sorted(self.search_common_words(self.docs))
        matrix = self.drawing_up_the_matrix(similar_words, self.docs)
        U, S, Vt = np.linalg.svd(matrix)

        coord = -1 * Vt[0:2, :]
        new_coord = []

        for i in range(len(self.docs)):
            new_coord.append((round(coord[0][i], 4), round(coord[1][i], 4)))

        total = []
        ready = self.find_near(new_coord[0], new_coord[1:])

        for i in range(len(ready)):
            total.append(self.docs_copy[ready[i][0] + 1])

        return total


if __name__ == '__main__':
    print(LSA('Британская полиция знает о местонахождении основателя WikiLeaks',
              ['В суде США начинается процесс против россиянина, рассылавшего спам',
               'Церемонию вручения Нобелевской премии мира бойкотируют 19 стран',
               'В Великобритании арестован основатель сайта Wikileaks Джулиан Ассандж',
               'Украина игнорирует церемонию вручения Нобелевской премии',
               'Шведский суд отказался рассматривать апелляцию основателя Wikileaks',
               'НАТО и США разработали планы обороны стран Балтии против России',
               'Полиция Великобритании нашла основателя WikiLeaks, но, не арестовал',
               'В Стокгольме и Осло сегодня состоится вручение Нобелевских премий']).main())
