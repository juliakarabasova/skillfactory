CHAR_DICT = {'x': 1, 'o': 2, ' ': 0}


def new_game():
    """
    A tic-tac-toe game from start to victory/draw
    """
    print('\nWelcome to tic-tac-toe! You surely know the rules. '
          'Player 1 always plays as "x" and Player 2 as "o". X`s start first.')

    field = [[' ', 0, 1, 2],
             [0, ' ', ' ', ' '],
             [1, ' ', ' ', ' '],
             [2, ' ', ' ', ' ']]

    show_field(field)
    win = False
    cur_player = 1
    actions = {1: 'x', 2: 'o'}

    while not win and win is not None:
        moves = input(
            f'Player {cur_player}, enter your move as coordinates separated with space [↓ →] (e.g. 0 1):   '
        ).strip().split()

        if len(moves) != 2 or not any(move.isdigit() for move in moves):
            print('Please enter only 2 digits separated with space.')
            continue
        else:
            move_x, move_y = map(int, moves)

        if move_x not in range(3) or move_y not in range(3):
            print('Your coordinates should be numbers between 0 and 2!')
        elif field[move_x+1][move_y+1] in actions.values():
            print('That space is already taken! Choose another one.')
        else:
            field[move_x+1][move_y+1] = actions[cur_player]
            cur_player = 2 if cur_player == 1 else 1
            show_field(field)
            win = check_win(field)

    if win is None:
        print('Oh! That`s a tie! Well played players!')
    else:
        winner = 2 if cur_player == 1 else 1
        print(f'Game over! Congratulations to *player {winner}* for victory!')


def show_field(field):
    """
    Print current field state to the console
    """
    for row in ['', *field]:        # Empty strings to add space around field as every print ends with \n
        print(*row, sep=' | ')


def check_win(field):
    """
    Check if current values on the field are victorious
    """
    filtered_field = [[CHAR_DICT[elem] for elem in row if elem in CHAR_DICT] for row in field[1:]]

    if any([any(set(row) in [{1}, {2}] for row in filtered_field),
            any(set([row[i] for row in filtered_field]) in [{1}, {2}] for i in range(3)),
            set([filtered_field[i][i] for i in range(3)]) in [{1}, {2}],
            set([filtered_field[i][2-i] for i in range(3)]) in [{1}, {2}]]):
        return True
    elif all(set(row) in [{1, 2}, {2, 1}] for row in filtered_field):
        return None
    else:
        return False


if __name__ == '__main__':
    start_anew = 'y'
    while start_anew.lower() != 'n':
        new_game()
        start_anew = input('Do you want to start a new game? (y/n):   ').strip().lower()
        while start_anew not in ['y', 'n']:
            start_anew = input('I only accept "y" or "n". Do you want to start a new game? (y/n):   ').strip().lower()
