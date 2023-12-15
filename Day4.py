#!python3
''' Day 4: Scratchcards
'''
import re

test_input = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\
'''


def parse_cards(lines: str):
    ''' Each card has two lists of numbers, separated by a vertical bar:
        a list of winning numbers
        and a list of your numbers. 
    '''
    lines = [line.strip() for line in lines.split('\n')]
    subpattern = r'\d+(?: +\d+)*'
    pattern = re.compile(rf'Card +(\d+): +({subpattern}) \|'
                                      f' +({subpattern})')
    for line in lines:
        match = pattern.match(line)
        assert match is not None, line
        card_number, winning_numbers, your_numbers = match.groups()
        winning_numbers = [int(s) for s in winning_numbers.split(' ') if s]
        your_numbers    = [int(s) for s in your_numbers   .split(' ') if s]
        yield card_number, winning_numbers, your_numbers


def points(matches: int) -> int:
    ''' How many points is a card with `matches` matches worth?
        1 match makes a card worth 1 point.
        Each additional match doubles the point value of the card.
    '''
    return 2 ** (matches - 1) if matches >= 1 else 0


def get_matches(lines: str):
    ''' Which of your numbers are winning numbers?
    '''
    for i, xs, ys in parse_cards(lines):
        yield [y for y in ys if y in xs]


def part1():
    ''' How many points are the cards worth in total?
    '''
    with open('day-4-input.txt') as file:
        lines = ''.join(line for line in file if line)
    matcheses = get_matches(lines)
    return sum(points(len(matches)) for matches in matcheses)


def test1():
    answers = [
        ((48, 83, 17, 86),  # You have 4 winning numbers on card 1,
         8),                # so it is worth 8 points.
        ((32, 61),          # You have 2 winning numbers on card 2 (32, 61),
         2),                # so it is worth 2 points.
        (( 1, 21),          # You have 2 winning numbers on card 3 (1, 21), 
         2),                # so it is worth 2 points.
        ((84,),             # You have 1 winning number  on card 4 (84), 
         1),                # so it is worth 1 point.
        ((),                # You have no winning numbers on card 5,
         0),                # so it is worth 0 points.
        ((),                # You have no winning numbers on card 6,
         0),                # so it is worth 0 points.
    ]
    matcheses = list(get_matches(test_input))
    for matches, (your_winning_numbers, your_points) \
    in zip(matcheses, answers):
        m = len(matches)
        assert sorted(matches) == sorted(your_winning_numbers)
        assert points(m) == your_points
    # The pile of scratchcards is worth 13 points.
    assert sum(points(len(matches)) for matches in matcheses) == 13


if __name__ == '__main__':
    parse_cards(test_input)
    test1()
    print(f'Part 1: {part1()}')


