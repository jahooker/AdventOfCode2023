#!python
''' Day 3
'''
import re
from functools import reduce

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


def get_number_spans(engine_schematic):
    for i, row in enumerate(engine_schematic):
        matches = re.finditer(r'(\d+)', row)
        for match in matches:
            yield int(match.group(0)), i, match.span()


def get_symbol_spans(engine_schematic):    
    for i, row in enumerate(engine_schematic):
        matches = re.finditer(r'([^\d.])', row)
        for match in matches:
            yield (match.group(0), i, match.span())


def spans_are_adjacent(this_span, that_span):
    i, (j0, j1) = this_span
    k, (l0, l1) = that_span
    if abs(i - k) > 1:
        return False
    if j0 < l0:
        return l0 <= j1
    else:
        return j0 <= l1


def neighbours(this, those):
    this_string, i, (j0, j1) = this
    outbox = set()
    for that in those:
        that_string, k, (l0, l1) = that
        if spans_are_adjacent((i, (j0, j1)),
                              (k, (l0, l1))) \
        and that not in outbox:
            yield that
            outbox.update(that)


def get_part_numbers(engine_schematic):
    ''' In the engine schematic,
        a number adjacent to a symbol (even diagonally) is a "part number".
        Periods '.' do not count as a symbol.
    '''
    engine_schematic = [line.strip() for line in engine_schematic]
    rows    = len(engine_schematic)
    columns = len(engine_schematic[0])
    # Rows must be all the same width
    assert all(len(row) == columns for row in engine_schematic)

    number_spans = [*get_number_spans(engine_schematic)]
    symbol_spans = [*get_symbol_spans(engine_schematic)]

    for number_span in number_spans:
        if tuple(neighbours(number_span, symbol_spans)):
            number, i, span = number_span
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


def get_gear_ratios(engine_schematic):
    ''' A gear is any '*' that is adjacent to exactly two part numbers.
        Its gear ratio is the product of those two numbers.
    '''
    engine_schematic = [line.strip() for line in engine_schematic]

    number_spans = [*get_number_spans(engine_schematic)]
    symbol_spans = [*get_symbol_spans(engine_schematic)]

    for symbol_span in symbol_spans:
        if symbol_span[0] == '*':
            nb = list(neighbours(symbol_span, number_spans))
            if len(nb) == 2:
                yield reduce(lambda x, y: x * y,
                             (x[0] for x in nb), 1)


def test2():
    engine_schematic = test_input.split('\n')
    gear_ratios = list(get_gear_ratios(engine_schematic))
    assert sorted(gear_ratios) == sorted((16345, 451490))
    assert sum(gear_ratios) == 467835


def part2():
    with open('day-3-input.txt') as file:
        lines = [line.strip() for line in file]
        gear_ratios = [*get_gear_ratios(lines)]
    return sum(gear_ratios)


if __name__ == '__main__':
    print(test_input)
    test1()
    print(f'Part 1: {part1()}')
    test2()
    print(f'Part 2: {part2()}')

