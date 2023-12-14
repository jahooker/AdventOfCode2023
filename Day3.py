#!python
''' Day 3
'''
import re

test_input = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..\
'''

def get_part_numbers(engine_schematic):
    ''' In the engine schematic,
        a number adjacent to a symbol (even diagonally) is a "part number".
        Periods '.' do not count as a symbol.
    '''
    rows    = len(engine_schematic)
    columns = len(engine_schematic[0])
    # Rows must be all the same width
    assert all(len(row) == columns for row in engine_schematic)

    number_spans = []
    for i, row in enumerate(engine_schematic):
        matches = re.finditer(r'(\d+)', row)
        for match in matches:
            number_spans.append((int(match.group(0)), i, match.span()))
    
    symbol_spans = []
    for i, row in enumerate(engine_schematic):
        matches = re.finditer(r'([^\d.])', row)
        for match in matches:
            symbol_spans.append((match.group(0), i, match.span()))

    # TODO Since we have our spans sorted by row number,
    # we can stop searching early if we find no adjacent symbols
    # in the rows immediately above or below
    # (or the current row, of course).

    def neighbors(i, j):
        for di in (-1, 0, +1):
            for dj in (-1, 0, +1):
                yield i + di, j + dj

    def is_adjacent_to_symbol(i, span, symbol_spans):
        j0, j1 = span
        for j in range(j0, j1):
            for symbol, k, (l0, l1) in symbol_spans:
                for l in range(l0, l1):
                    for ii, jj in neighbors(i, j):
                        if (ii, jj) == (k, l):
                            return True
        return False


    for number, i, span in number_spans:
        if is_adjacent_to_symbol(i, span, symbol_spans):
            yield number


def test1():
    engine_schematic = test_input.split('\n')
    part_numbers = [*get_part_numbers(engine_schematic)]
    assert sorted(part_numbers) \
        == sorted([467, 35, 633, 617, 592, 755, 664, 598])
    assert sum(part_numbers) == 4361

def part1():
    with open('day-3-input.txt') as file:
        lines = [line.strip() for line in file]
        part_numbers = [*get_part_numbers(lines)]
    return sum(part_numbers)

if __name__ == '__main__':
    test1()
    print(part1())

