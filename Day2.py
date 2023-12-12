#!python3
import re
from functools import reduce

def parse(lines):
    ''' The game involves a small bag and some red, green, and blue cubes.
        Each game,
        the Elf will hide some number of cubes of each color in the bag. 
        Each game, the Elf will load the bag with cubes.
        Your goal is to figure out information about the number of cubes.

        Each game consists of a few rounds 
        in which the Elf will remove a random set of cubes from the bag,
        show them to you,
        and return them to the bag. 

        You play several games and record the cube counts
        (your puzzle input). 
        Each game is listed with its ID number (like the 11 in Game 11: ...)
        followed by a semicolon-separated list
        of subsets of cubes that were revealed from the bag 
        (like 3 red, 5 green, 4 blue).
    '''

    # Patterns
    game_pattern = re.compile(r'Game (\d+): (.*)')
    spec_pattern = re.compile(r'(\d+) (red|green|blue)')

    for line in map(str.strip, lines):
        match = game_pattern.fullmatch(line)
        assert match is not None, line
        game_number, rounds = match.groups()
        rounds = rounds.split('; ')
        game = []
        for round_ in rounds:
            rgb = {color: 0 for color in ('red', 'green', 'blue')}
            specs = round_.split(', ')
            for spec in specs:
                match = spec_pattern.fullmatch(spec)
                assert match is not None
                count, color = match.groups()
                rgb[color] = int(count)
            game.append(rgb)

        yield game


def possible_game_ids(lines):
    ''' Which games would have been possible
        if the bag contained 12 red, 13 green, and 14 blue cubes?
    '''

    def game_is_possible(game: list[dict]):
        return all(    rgb['red']   <= 12 \
                   and rgb['green'] <= 13 \
                   and rgb['blue']  <= 14 for rgb in game)

    possible_games = [game_id for game_id, game 
                      in enumerate(parse(lines), start=1) 
                      if game_is_possible(game)]
    return possible_games


def test1():
    ''' Which games would have been possible 
        if the bag had been loaded 
        with only 12 red cubes, 13 green cubes, and 14 blue cubes?
        And what is the sum of the IDs of those games?
    '''

    test_input = \
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green', \
        'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue', \
        'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red', \
        'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red', \
        'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'
    # Here, games 1, 2, and 5 would have been possible.
    # However, game 3 would have been impossible 
    # because at one point the Elf showed you 20 red cubes at once. 
    # Similarly, game 4 would also have been impossible 
    # because the Elf showed you 15 blue cubes at once. 
    result = tuple(possible_game_ids(test_input))
    assert result == (1, 2, 5)
    # The sum of the IDs of the games that would have been possible is 8.
    assert sum(result) == 8


def part1():
    with open('day-2-input.txt') as file:
        result = tuple(possible_game_ids(file))
    print(result)
    print(sum(result))

def minimal_cube_set(game):
    ''' What is the fewest number of cubes of each color 
        that could have been in the bag to make each game possible?
    '''
    colors = ('red', 'green', 'blue')
    cubes = {color: 0 for color in colors}
    for rgb in game:
        for color in colors:
            if rgb[color] > cubes[color]:
                cubes[color] = rgb[color]
    return cubes

def power(cube_set):
    ''' The power of a set of cubes
        is the product of its red, green, and blue cube counts. 
    '''
    colors = ('red', 'green', 'blue')
    return reduce(lambda x, y: x * y,
                  (cube_set[color] for color in colors),
                  1)

def test2():

    test_input = (
        'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
        'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
        'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
        'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
        'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green')

    test_output = (
        # - Game 1 needed at least 4 red, 2 green, and 6 blue cubes. 
        {'red':  4, 'green':  2, 'blue':  6},
        # - Game 2 needed at least 1 red, 3 green, and 4 blue cubes.
        {'red':  1, 'green':  3, 'blue':  4},
        # - Game 3 needed at least 20 red, 13 green, and 6 blue cubes.
        {'red': 20, 'green': 13, 'blue':  6},
        # - Game 4 needed at least 14 red, 3 green, and 15 blue cubes.
        {'red': 14, 'green':  3, 'blue': 15},
        # - Game 5 needed at least 6 red, 3 green, and 2 blue cubes.
        {'red':  6, 'green':  3, 'blue':  2})
    test_powers = 48, 12, 1560, 630, 36
        # The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. 
        # Adding up these five powers produces the sum 2286.

    games = list(parse(test_input))
    for game, answer, test_power in zip(games, test_output, test_powers):
        mcs = minimal_cube_set(game) 
        assert mcs == answer
        assert power(mcs) == test_power
    assert sum(power(minimal_cube_set(game))
               for game in parse(test_input)) == 2286

def part2():
    with open('day-2-input.txt') as file:
        games = tuple(parse(file))
    print(sum(power(minimal_cube_set(game)) for game in games))


if __name__ == '__main__':
    test1()
    part1()
    test2()
    part2()

