#!python3
''' Advent of Code 2023 Day 2
'''
import re
from functools import reduce

Color = str
GameRound = dict[Color, int]
CubeSet   = GameRound
Game = list[GameRound]

colors = ('red', 'green', 'blue')


def parse(lines):
    ''' Each game, 
        some number of red, green, and blue cubes are put in a bag.
        Then, for some number of rounds
        you will be shown some set of cubes from the bag.

        `lines` is a record of the cube counts from some games.
        Each game is listed with an ID number (e.g. Game 1)
        followed by a semicolon-separated list
        of sets of cubes revealed from the bag
        (e.g. 3 red, 5 green, 4 blue).
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
            rgb = {color: 0 for color in colors}
            specs = round_.split(', ')
            for spec in specs:
                match = spec_pattern.fullmatch(spec)
                assert match is not None
                count, color = match.groups()
                rgb[color] = int(count)
            game.append(rgb)
        yield game


def game_is_possible(game: Game, bag: CubeSet) -> bool:
    ''' Could this game occur with the given bag?
    '''
    return all(all(round_[color] <= bag[color]
                   for color in colors)
                   for round_ in game)


def possible_game_ids(lines):
    ''' Which games would have been possible
        if the bag contained 12 red, 13 green, and 14 blue cubes?
    '''
    bag = {'red': 12, 'green': 13, 'blue': 14}
    possible_games = [game_id for game_id, game
                      in enumerate(parse(lines), start=1)
                      if game_is_possible(game, bag)]
    return possible_games


test_input = (
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green')


def test1():
    ''' Which games would have been possible
        if the bag had been loaded
        with only 12 red cubes, 13 green cubes, and 14 blue cubes?
        And what is the sum of the IDs of those games?
    '''
    which_games = tuple(possible_game_ids(test_input))
    # Only games 1, 2, 5 would have been possible.
    assert which_games == (1, 2, 5)
    # The IDs of these games sum to 8.
    assert sum(which_games) == 8


def part1() -> int:
    with open('day-2/input.txt') as file:
        which_games = tuple(possible_game_ids(file))
    return sum(which_games)


def minimal_cube_set(game: Game) -> CubeSet:
    ''' What is the fewest number of cubes of each color
        that could have been in the bag to make this game possible?
    '''
    cubes = {color: 0 for color in colors}
    for round_ in game:
        for color in colors:
            if (n := round_[color]) > cubes[color]:
                cubes[color] = n
    return cubes


def power(cubes: CubeSet) -> int:
    ''' The power of a set of cubes
        is the product of its red, green, and blue cube counts.
    '''
    assert set(cubes.keys()) == set(colors)
    return reduce(lambda x, y: x * y, cubes.values(), 1)


def test2():

    test_minimal_cube_sets = (
        # - Game 1 needs at least 4 red, 2 green, and 6 blue cubes.
        {'red':  4, 'green':  2, 'blue':  6},
        # - Game 2 needs at least 1 red, 3 green, and 4 blue cubes.
        {'red':  1, 'green':  3, 'blue':  4},
        # - Game 3 needs at least 20 red, 13 green, and 6 blue cubes.
        {'red': 20, 'green': 13, 'blue':  6},
        # - Game 4 needs at least 14 red, 3 green, and 15 blue cubes.
        {'red': 14, 'green':  3, 'blue': 15},
        # - Game 5 needs at least 6 red, 3 green, and 2 blue cubes.
        {'red':  6, 'green':  3, 'blue':  2})

    # The powers of the minimal cube sets
    test_powers = 48, 12, 1560, 630, 36

    games = list(parse(test_input))
    for game, test_minimal_cube_set, test_power in zip(games, 
                                        test_minimal_cube_sets, 
                                        test_powers):
        ours = minimal_cube_set(game)
        assert ours == test_minimal_cube_set
        assert power(ours) == test_power

    # The sum of the powers of the five games is 2286.
    assert sum(power(minimal_cube_set(game))
               for game in parse(test_input)) == 2286


def part2() -> int:
    with open('day-2/input.txt') as file:
        games = tuple(parse(file))
    return sum(power(minimal_cube_set(game)) for game in games)


if __name__ == '__main__':
    test1()
    print(f'Part 1: {part1()}')
    test2()
    print(f'Part 2: {part2()}')

