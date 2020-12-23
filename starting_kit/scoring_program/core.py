from typing import List

import random
import os


class GameCoreException(Exception):
    pass


class FieldCell:
    def __init__(self, Type, importance=0, countLeft=0, tikDecrement=5):
        self.Type = Type
        self.tikDecrement = tikDecrement
        self.importance = importance
        self.countLeft = countLeft

    def ToString(self):
        if self.Type == 'product':
            return [
                ('c ' + str(self.countLeft)).center(7),
                self.Type.center(7),
                ('i ' + str(self.importance)).center(7)
            ]

        elif self.Type == 'empty':
            return [
                " ".center(7),
                'e'.center(7),
                " ".center(7)
            ]

        else:
            return [
                " ".center(7),
                self.Type.center(7),
                " ".center(7)
            ]


class Game:
    def __init__(self, heigth=5, width=10, randomSeed=-1, productCnt=-1, wallCnt=-1):
        self.backet = list()
        self.products = list()
        self.steps=list() #шаги, совершенные игроком

        if randomSeed > 0:
            random.seed(randomSeed)

        if productCnt==-1:
            productCnt=int(heigth*width*0.01*random.randint(6,10)) # 6-10% ячеек - продукты
        if productCnt==0:
            productCnt=1

        if wallCnt==-1:
            wallCnt=int(heigth*width*0.01*random.randint(2,6)) # 2-6% ячеек - стены

        self.currTik = 0
        self.fieldHeigth = heigth
        self.fieldWidth = width
        self.field = [[FieldCell('empty') for _ in range(width)] for _ in range(heigth)]

        w = random.randint(0, self.fieldWidth - 1)
        h = random.randint(0, self.fieldHeigth - 1)

        self.playerH = h
        self.playerW = w
        self.field[h][w] = FieldCell('AGENT')

        for p in range(productCnt):
            self.AddRandomCell('product',productCnt)

        for index, imp in enumerate(self.Split100(productCnt)):
            self.products[index].importance = imp

        for w in range(wallCnt):
            self.AddRandomCell('wall')

    def GetCurrentState(self):
        """ Возвращает текущее состояние поля , score, game_over """
        return self.field, self.CurrScore(), len([x for x in self.products if x.countLeft > 0]) == 0


    def Split100(self, parts):
        if parts==1:
            return [100]
        randDigth = []
        for p in range(parts):
            randDigth.append(random.randint(1, 1000))

        s = sum(randDigth)
        result = []
        for r in randDigth[:-2]:
            forAdd = int(r / s * 100)
            if forAdd < 1:
                forAdd = 1

            result.append(forAdd)

        forAdd = int((100 - sum(result)) / 2)
        if forAdd < 1:
            forAdd = 1

        result.append(forAdd)
        result.append(100 - sum(result))

        return result

    def AddRandomCell(self, Type,cntTotal=-1):
        while True:
            w = random.randint(0, self.fieldWidth - 1)
            h = random.randint(0, self.fieldHeigth - 1)

            if self.field[h][w].Type == 'empty':
                if Type == 'product':
                    maxCountLeft= int((cntTotal-cntTotal%10+ round(cntTotal%10 *0.1)*10)/2)
                    if maxCountLeft<2:
                        maxCountLeft=2
                    newProduct = FieldCell(
                        'product',
                        random.randint(1, cntTotal), #importance
                        random.randint(1, maxCountLeft), #countLeft
                        random.randint(2, 10) #tikDecrement
                    )

                    self.products.append(newProduct)
                    self.field[h][w] = newProduct

                elif Type == 'wall':
                    self.field[h][w] = FieldCell('wall')

                break

    def Move(self, direction):
        tryH = self.playerH
        tryW = self.playerW

        if direction == 'up':
            tryH = tryH - 1
        elif direction == 'down':
            tryH = tryH + 1
        elif direction == 'left':
            tryW = tryW - 1
        elif direction == 'right':
            tryW = tryW + 1
        elif direction == 'stay':
            pass
        else:
            raise GameCoreException(f"Неизвестное направление: <{direction}>")
        self.steps.append(direction)    
        if not self.GetCurrentState()[2]:
            is_moved = tryH != self.playerH or tryW != self.playerW
            is_moved = is_moved and not (tryH > self.fieldHeigth - 1 or tryH < 0 or tryW < 0 or tryW > self.fieldWidth - 1)
            is_moved = is_moved and not self.field[tryH][tryW].Type == 'wall'

            if is_moved and self.field[tryH][tryW].Type == 'empty':
                agent = self.field[self.playerH][self.playerW]
                self.field[self.playerH][self.playerW] = FieldCell('empty')
                self.playerH = tryH
                self.playerW = tryW
                self.field[self.playerH][self.playerW] = agent

            elif is_moved and self.field[tryH][tryW].Type == 'product':
                agent = self.field[self.playerH][self.playerW]
                product = self.field[tryH][tryW]
                product.countLeft = 0
                self.field[self.playerH][self.playerW] = FieldCell('empty')
                self.playerH = tryH
                self.playerW = tryW
                self.field[self.playerH][self.playerW] = agent
                self.backet.append({'imp': product.importance, 'tik': self.currTik})

            self.Tik()
        return self.GetCurrentState()

    def Tik(self):
        for p in self.products:
            if self.currTik != 0 and self.currTik % p.tikDecrement == 0 and p.countLeft > 0:
                p.countLeft -= 1

            if p.countLeft == 0:
                p.Type = 'empty'

        self.currTik += 1

    def CurrScore(self):
        """ Возвращает текущий score """
        score = 0
        if self.currTik > 0:
            score = sum([x['imp'] for x in self.backet]) / self.currTik

        return score * 1000

    def Show(self):
        """ Выводит в консоль текущее состояние поля и score """
        os.system('cls' if os.name == 'nt' else 'clear')
        for h in range(self.fieldHeigth):
            arr = []
            for w in range(self.fieldWidth):
                arr.append(self.field[h][w].ToString())

            for i in range(len(arr[0])):
                row = ''
                for el in arr:
                    row = row + ' ' + el[i]
                print(row)

        print(self.backet)
        print('score: {:.3f}'.format(self.CurrScore()))


    def _game_emulation(self, steps: List[str]) -> None:
        """ Эмуляция игры по последовательности шагов """

        iter = 0
        n = len(steps)
        while len([x for x in self.products if x.countLeft > 0]) > 0:
            direction = "stay"

            # Когда шаги закончились, а плюшки нет - агент стоит на месте
            if iter < n:
                direction = steps[iter]
                iter += 1

            # Выполнение действия
            self.Move(direction)

    def run_game_emulation(self, steps: List[str]) -> float:
        """ Запуск эмуляции игры и возврат рейтинга решения """

        self._game_emulation(steps)
        return self.CurrScore()
