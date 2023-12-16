class Dot:
    """
    x: Координата по оси x
    y: Координата по оси y
    """
    def __init__(self, x, y):
        if x not in range(1, 7) or y not in range(1, 7):
            raise ValueError('Please enter correct coordinates between 1 and 6')

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
        if not isinstance(start_dot, Dot):
            raise ValueError('Initialize a "Dot" class object for start_dot parameter.')

        self.length = length
        self.start = start_dot
        self.orient = orient
        self.lives = self.length

        if length != 1:
            if orient == 'h':
                self.my_dots = [self.start] + [Dot(self.start.x, self.start.y + i) for i in range(1, length)]
            else:
                self.my_dots = [self.start] + [Dot(self.start.x + i, self.start.y) for i in range(1, length)]
        else:
            self.my_dots = [self.start]

    def dots(self):
        return self.my_dots


class Board:
    """
    board: Двумерный список, в котором хранятся состояния каждой из клеток.
    ships: Список кораблей доски.
    hid: Параметр hid типа bool — информация о том, нужно ли скрывать корабли на доске (для вывода доски врага) или нет (для своей доски).
    alive_ships: Количество живых кораблей на доске.
    """
    def __init__(self):
        self.board = [[] * 6] * 6
        self.ships = []
        self.hid = False
        self.alive_ships = 0

    def add_ship(self):
        try:
            start = Dot(*map(int, input('Enter coordinates for the bow of the ship [e.g. 1 2]: ').split()))
        except ValueError:
            pass
