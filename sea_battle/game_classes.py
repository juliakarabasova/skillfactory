import random

from custom_exceptions import *


class Dot:
    """
    x: Координата по оси x
    y: Координата по оси y
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other_dot):
        return self.x == other_dot.x and self.y == other_dot.y


class Ship:
    """
    length: Длина.
    start_dot: Точка, где размещён нос корабля.
    orient: Направление корабля (вертикальное/горизонтальное).
    lives: Количество жизней (сколько точек корабля ещё не подбито).
    """
    def __init__(self, length, start_dot, orient):
        if length not in range(1, 4):
            raise ValueError('Ship length must be 1, 2 or 3.')
        if orient not in ['h', 'v']:
            raise ValueError('Orientation must be written as "h" or "v".')

        self.length = length
        self.start = start_dot
        self.orient = orient
        self.lives = self.length

        if length != 1:
            if orient == 'v':
                self.my_dots = [self.start] + [Dot(self.start.x, self.start.y + i) for i in range(1, length)]
            else:
                self.my_dots = [self.start] + [Dot(self.start.x + i, self.start.y) for i in range(1, length)]
        else:
            self.my_dots = [self.start]

    def dots(self):
        """
        Возвращает список всех точек корабля
        """
        return self.my_dots


class Board:
    """
    board: Двумерный список, в котором хранятся состояния каждой из клеток.
    ships: Список кораблей доски.
    hid: Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски).
    alive_ships: Количество живых кораблей на доске.
    """
    def __init__(self, hid=True):
        self.board = [[Dot(x, y) for x in range(6)] for y in range(6)]
        # self.board = [['o' for x in range(6)] for y in range(6)]
        self.taken_spots = []
        self.shots = []
        self.misses = []
        self.ships = []
        self.hid = hid
        self.alive_ships = 0        # list of ships?

    def add_ship(self, x: int, y: int, orient: str, length: int):
        """
        Ставит корабль на доску
        """
        if self.out(Dot(x, y)):
            raise BoardOutException('Dot coordinates must be within the board')

        ship_lengths = [ship.length for ship in self.ships]
        if (length == 3 and 3 in ship_lengths) \
                or (length == 2 and ship_lengths.count(2) == 2)\
                or (length == 1 and ship_lengths.count(1) == 4):
            raise MaxShipOfLength('Sorry you cant place another ship of that length!')

        new_ship = Ship(length, Dot(x - 1, y - 1), orient)
        if any(dot in self.taken_spots for dot in new_ship.dots()):
            raise TooCloseException('The ship cant be placed here.')

        self.ships.append(new_ship)
        self.alive_ships += 1
        self.contour(self.ships[-1])

    def contour(self, ship):
        """
        Обводит корабль по контуру
        """
        dots = []
        for dot in ship.dots():
            dots.extend(self.check_in([dot,
                                       Dot(dot.x-1, dot.y),
                                       Dot(dot.x-1, dot.y-1),
                                       Dot(dot.x, dot.y-1),
                                       Dot(dot.x+1, dot.y-1),
                                       Dot(dot.x+1, dot.y),
                                       Dot(dot.x+1, dot.y+1),
                                       Dot(dot.x, dot.y+1),
                                       Dot(dot.x-1, dot.y+1),
                                       Dot(dot.x-1, dot.y)]))
        self.taken_spots = list(set(self.taken_spots + dots))

    def __str__(self):
        """
        Переопределяет метод для вывода доски в консоль
        """
        ships_dots = []
        for ship in self.ships:
            ships_dots.extend(ship.dots())

        print('\n')
        print(*[' ', 1, 2, 3, 4, 5, 6], sep=' | ')
        for row in range(6):
            print(row + 1, end=' | ')
            for dot in self.board[row]:
                if dot in self.shots:
                    print('X', end=' | ')
                elif dot in ships_dots and not self.hid:
                    print('■', end=' | ')
                elif dot in self.misses:
                    print('T', end=' | ')
                else:
                    print('o', end=' | ')
            print('\n')
        return ''

    @staticmethod
    def out(dot: Dot):
        """
        Проверяет, выходит ли точка за пределы поля
        """
        if dot.x in range(6) and dot.y in range(6):
            return False
        return True

    def shot(self, x: int, y: int):
        """
        Делает выстрел по доске
        """
        dot = Dot(x, y)
        if self.out(dot):
            raise BoardOutException('Dot coordinates must be within the board')
        if dot in self.shots:
            raise AlreadyShotException('You cant shoot here.')

        if any(dot in ship.dots() for ship in self.ships):
            self.shots.append(dot)
            return True
        else:
            self.misses.append(dot)
            return False

    def check_in(self, dots):
        return [dot for dot in dots if not self.out(dot)]


class Player:
    """
    my_board: Собственная доска игрока
    enemy_board: Доска врага
    """
    def __init__(self):
        self.my_board = Board(hid=False)
        self.enemy_board = Board(hid=True)

    def ask(self):
        """
        «Спрашивает» игрока, в какую клетку он делает выстрел
        """
        return None, None, None, None

    def move(self):
        """
        Делает ход в игре

        Тут мы вызываем метод ask, делаем выстрел по вражеской доске, отлавливаем исключения,
        и если они есть, пытаемся повторить ход.
        Метод должен возвращать True, если этому игроку нужен повторный ход
        (например, если он выстрелом подбил корабль).
        """
        try:
            x, y = self.ask()
            result = self.enemy_board.shot(x, y)
        except Exception as e:
            print(e)
            self.move()
        else:
            return result


class AI(Player):
    def ask(self):
        x = random.randint(1, 7)
        y = random.randint(1, 7)
        return x, y


class User(Player):
    def ask(self):
        try:
            x, y = map(int, input('Where are you taking your shot? (e.g. 1 2): ').split())
        except ValueError:
            print('Coordinates must be numbers')
            self.ask()
        else:
            return x, y


class Game:
    def __init__(self):
        self.user = User()
        self.user_board = self.user.my_board

        self.ai = AI()
        self.ai_board = self.ai.my_board

    def random_board(self):
        """
        Генерирует случайную доску
        """
        for _ in range(500):
            x = random.randint(1, 7)
            y = random.randint(1, 7)
            orient = random.choice(['h', 'v'])
            if not self.ai_board.ships:
                length = 3
            elif len(self.ai_board.ships) in [1, 2]:
                length = 2
            elif len(self.ai_board.ships) in range(3, 8):
                length = 1
            else:
                break

            try:
                self.ai_board.add_ship(x, y, orient, length)
            except:
                continue
        else:
            self.random_board()

    def fill_user_board(self):
        """
        Метод запроса пользователя для добавления кораблей
        """
        while self.user_board.alive_ships != 7:
            print(self.user_board)
            try:
                x, y = map(int, input('Input coordinates of the bow of the ship (e.g. 1 2): ').split())
            except ValueError:
                print('Coordinates must be numbers')
                self.fill_user_board()
            else:
                orient = input('Which way is it sailing - horizontaly (h) or vertically (v)?: ')
                length = input('What`s the length of this ship?: ').strip()

                try:
                    self.user_board.add_ship(int(x), int(y), orient, int(length))
                except:
                    self.fill_user_board()

    @staticmethod
    def greet():
        """
        В консоли приветствует пользователя и рассказывает о формате ввода
        """
        print('='*50)
        print('''
        Welcome, dear user, to the SEA BATTLE game!
        You are going to play against AI randomly placing its ships and taking its shots.
        
        The board is 6x6. You`ll have to place:
                ► 1 ship of 3 cells long;
                ► 2 ships of 2 cells long;
                ► 4 ships of 1 cell.
                
        The game will ask you to enter first coordinates of the head of your ship in two numbers separated with space.
        Then, you are to enter which way your ship is facing and lastly the length of it.
        
        When you set all your ships up, the game will begin. You start first, then AI shoots.
        Whenever anyone hits a ship, they get another move.
        The game ends when one of you hits all ships of the enemy. Good luck, player!
        ''')
        print('=' * 50)

    def loop(self):
        """
        Метод с самим игровым циклом

        Последовательно вызываем метод move для игроков и делаем проверку,
        сколько живых кораблей осталось на досках, чтобы определить победу
        """
        # fill human board # TODO: check that person entered enough ships in FILL_USER_BOARD method
        print('Lets begin by setting up your ships:')
        self.fill_user_board()
        print('Please wait while AI is setting its board up...')
        self.random_board()
        print('All players are ready. Let the game begin!')

        while self.user_board.alive_ships or self.ai_board.alive_ships:
            print('User, your turn!')
            print(self.user.enemy_board)
            result = self.user.move()
            while result:
                print('Nice shot! You get another one.')
                print(self.user.enemy_board)
                result = self.user.move()

            print('Now it`s AIs move.')
            result_ai = self.ai.move()
            print(self.user.my_board)
            while result_ai:
                print('Oh crap! He hit it! AI`s going for another shot.')
                result_ai = self.ai.move()
                print(self.user.my_board)
        else:
            if not self.ai_board.alive_ships:
                print('Oh my god! You did it! Congratulations user, it`s your victory!!!!!!!!!!!!')
                print(self.ai.my_board)
            else:
                print('Well, the AI has a good eye today. Better luck next time, user!')
                print(self.user.my_board)

    def start(self):
        """
        Запуск начала игры
        """
        self.greet()
        self.loop()
