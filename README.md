# tensorflow_dsc12


Я участвовал в соревновании DSC12 на площадке Codalab. Надо было написать нейросеть, которая сама научится проходить в игру.

### Немного об игре:
Игра представляет собой матрицу(карту), на которой расположены продукты и стены.

### Цель игры: за минимальное количество шагов собрать максимальное количество продуктов.
Здесь представляю свою реализацию, которая набрала 470 баллов и взяла 17 место из 46.

# По заданию нужно было реализовать функцию agent, в tensorflow_dsc12/starting_kit/sample_code_submission/agent.py
Там реализована сама функция + функции для создания и обучения нейросети.
Сама модель находится как в папке sample_code_submission(этого требует соревнование), так и в папке starting_kit.
Для запуска тестирования или обучения необходимо запустить файл start.py:
Для обучения:
```
for i in range(0, 500):
    print(i)
    g = Game(random.randint(2,25), random.randint(2,25), i)
    predict(g)
```
Для тестирования:
```
g = Game(25, 1, 4)
agent(g)
```
Game - класс(карта), для создания объекта нужно передать размеры и seed.
Для обучения модели ее нужно положить рядом с файлом start.py, если ее там не будет модель будет создана автоматически.
