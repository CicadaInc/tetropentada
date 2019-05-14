### _Tetropentada - задавайте вопросы, делитесь ответами и бороздите просторы интернета!_
****
#### _Создатели:_
* [kuzdman](https://github.com/kuzdman) (Дмитрий Кузнецов)
* [Glander13](https://github.com/Glander13) (Иван Чебыкин)
* [SophIren](https://github.com/SophIren) (Марк Шкут)
****
_Tetropentada_ - это проект, посвященный теме серверов.
Цель данного проекта - создать форум, на котором могу задавать вопросы по любой теме 
и получать на них ответы.

На данный момент, у нас реализован сайт, позволяющий получать новую информацию посредством вопроса-ответа, т.е. один человек задает вопрос, другой отвечает на него.
С помощью поиска, реализованного на сайте, вы сможете, получить ответ искомый вопрос, если он существует или создать новый вопрос.
С помощью сортировки вы можете найти вопросы по интересующей вас области. А также с помощью умной сортировки (LSA) отсортировать вопросы по вашему поиску.

Также вы можете:
* Зарегистрироваться и войти в систему
* Получить информацию о пользователе задавшего или ответившего на вопрос
* Редактировать свой профиль
****
Проект состоит из нескольких частей. Например, таких как:
* Статистический контент (Папка Static)
* Шаблоны (Папка templates)
* LSA (LSA.py и porter.py)
* База данных (tetropentada.db)
* и др.

Более подробную информацию по структуре проекта можно найти в этой _[презентации](https://github.com/CicadaInc/tetropentada/blob/release/Tetropentada.pptx)_
****
Использованные технологии:
* Python 3
* IDE Pycharm
****
Использованные фреймворки:
* datetime - библиотека, позволяющая узнать время действий пользователя
* email - библиотека, позволяющая работать с электронной почтой
* flask - веб-фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2.
* re, string, numpy - фреймоврки, необходимые для полноценной работы LSA.py и porter.py
