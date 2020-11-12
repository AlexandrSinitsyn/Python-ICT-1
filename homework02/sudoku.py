import pathlib
import typing as tp

from math import sqrt

import random

max_number = 9

count_in_block = int(sqrt(max_number))

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    global max_number
    global count_in_block

    max_number = 0
    while puzzle[max_number] != '\n':
        max_number += 1

    count_in_block = int(sqrt(max_number))

    digits = [c for c in puzzle if c in ([str(i) for i in range(1, max_number + 1)] + ["."])]
    grid = group(digits, max_number)
    return grid


tab_count = 5


def display(grid):
    tab = ""
    for i in range(tab_count):
        tab += "\t"

    for row in range(len(grid)):
        print(tab, end="")
        for e in range(len(grid[row])):
            print(grid[row][e], end=" ")

            if (e + 1) % count_in_block == 0 and (e + 1) != len(grid[row]):
                print("|", end=" ")
        print()

        if (row + 1) % count_in_block == 0 and (row + 1) != len(grid):
            print(tab, end="")
            for i in range(count_in_block):
                for j in range(count_in_block * 2):
                    print("-", end="")
                if i != count_in_block - 1:
                    print("+", end="")
                else:
                    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    res = [values[i:i + n] for i in range(0, len(values), n)]
    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [i[pos[1]] for i in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    w = pos[0] // count_in_block
    h = pos[1] // count_in_block

    return [grid[i][j] for i in range(w * count_in_block, w * count_in_block + count_in_block)
            for j in range(h * count_in_block, h * count_in_block + count_in_block)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for indexI, keyI in enumerate(grid):
        for indexJ, keyJ in enumerate(keyI):
            if keyJ == '.':
                return indexI, indexJ

    return -1, -1


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """ Вернуть множество всех возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    possible_values = set([str(i) for i in range(1, max_number + 1)])

    values = set([i for i in (get_col(grid, pos) + get_row(grid, pos) + get_block(grid, pos)) if i.isdigit()])

    return values ^ possible_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """

    def check(matrix):
        pos = find_empty_positions(matrix)
        if pos == (-1, -1):
            return matrix, True
        else:
            for e in find_possible_values(matrix, pos):
                matrix[pos[0]][pos[1]] = e

                if check(matrix)[1]:
                    return matrix, True

                matrix[pos[0]][pos[1]] = "."
            return None, False

    return check(grid)[0]


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    col_indices = [i for i in range(count_in_block)]
    row_indices = [i * count_in_block for i in range(count_in_block)]
    positions = [(i, j) for i in col_indices for j in row_indices]

    passed = []
    for i in positions:
        passed.append(len(set(get_block(solution, i))) == max_number)
        passed.append(len(set(get_row(solution, i))) == max_number)
        passed.append(len(set(get_col(solution, i))) == max_number)
    return all(passed)


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    matrix = [['.' for _ in range(max_number)] for _ in range(max_number)]
    matrix = solve(matrix)

    count = 0
    while count < max_number * max_number - N:
        i = random.randint(0, max_number - 1)
        j = random.randint(0, max_number - 1)

        if matrix[i][j] != '.':
            matrix[i][j] = '.'
            count += 1

    return matrix


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
