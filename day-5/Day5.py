#!python3
''' Day 5
'''
import re

# The almanac lists:
# - What kind of seeds to plant 
# - What kind of soil to use with each kind of seed
# - What kind of fertilizer to use with each kind of soil
# - What kind of water to use with each kind of fertilizer 
# - And so on
# Each kind of seed, soil, fertilizer, and so on is identified by a number. 
# Numbers are reused by each category
# --- that is, soil 123 and fertilizer 123 aren't necessarily related.

test_input = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4\
'''

def make_seed2location(information: dict, seed_number: int) -> int:
    sections = information['sections']
    seed2soil            = mapping_from_triples(sections['seed', 'soil'])
    soil2fertilizer      = mapping_from_triples(sections['soil', 'fertilizer'])
    fertilizer2water     = mapping_from_triples(sections['fertilizer', 'water'])
    water2light          = mapping_from_triples(sections['water', 'light'])
    light2temperature    = mapping_from_triples(sections['light', 'temperature'])
    temperature2humidity = mapping_from_triples(sections['temperature', 'humidity'])
    humidity2location    = mapping_from_triples(sections['humidity', 'location'])
    return humidity2location(
            temperature2humidity(
             light2temperature(
              water2light(
               fertilizer2water(
                soil2fertilizer(
                 seed2soil(seed_number)))))))


def parse_almanac(almanac: str):
    information = {'seeds': [], 'sections': {}}
    lines = [line.strip() for line in almanac.split('\n')]
    # The almanac starts by listing which seeds need to be planted
    seedline = lines.pop(0)
    match = re.match(r'seeds: +(\d+(?: +\d+)*)', seedline)
    assert match is not None
    information['seeds'] = [int(s) for s in match.group(1).split(' ') if s]
    # The rest of the almanac describes a collection of mappings 
    # between two categories of numbers.
    # The "seed-to-soil map" section describes how to convert a seed number (the source) to a soil number (the destination). 
    # This says which soil to use with which seeds, 
    # which water to use with which fertilizer, and so on.
    for line in lines:

        # Section title? 
        title_match = re.match('(.*)-to-(.*) map:', line)
        if title_match is not None:
            src, dest = title_match.groups()
            information['sections'][src, dest] = []

        # Range description?
        range_match = re.match(r'(\d+) +(\d+) +(\d+)', line)
        if range_match is not None:
            # Each mapping is described in terms of a range of numbers. 
            # Each line contains three numbers:
            # - The destination range start 
            # - The source range start
            # - The range length
            dest0, src0, length = map(int, range_match.groups())
            information['sections'][src, dest].append((dest0, src0, length))

        if not line:
            src, dest = '', ''

    return information


def mapping_from_triples(triples):

    def mapping(i: int) -> int:
        for a, b, c in triples:
            sr = list(range(b, b + c))  # Source      range
            dr = list(range(a, a + c))  # Destination range
            if i in sr:
                return dr[sr.index(i)]
        return i

    return mapping


def test1():
    information = parse_almanac(test_input)
    seeds = information['seeds']
    assert sorted(seeds) == sorted((79, 14, 55, 13))

    sections = information['sections']

    assert sections['seed', 'soil'] == [
        (50, 98,  2),  # The first line indicates 
                       # a source range starting at 98
                       # and a destination range starting at 50,
                       # Both ranges are of length 2.
        (52, 50, 48),  # The second line indicates 
                       # a source range starting at 50
                       # and a destination range starting at 52.
                       # Both ranges are of length 48.
    ]

    m = mapping_from_triples
    seed2soil            = m(sections['seed', 'soil'])
    soil2fertilizer      = m(sections['soil', 'fertilizer'])
    fertilizer2water     = m(sections['fertilizer', 'water'])
    water2light          = m(sections['water', 'light'])
    light2temperature    = m(sections['light', 'temperature'])
    temperature2humidity = m(sections['temperature', 'humidity'])
    humidity2location    = m(sections['humidity', 'location'])

    # Seed numbers correspond to soil numbers as follows:
    seed_numbers = range(100)
    soil_numbers = list(map(seed2soil, seed_numbers))
    assert soil_numbers == [*range(50), *range(52, 100), *range(50, 52)]

    # Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    assert seed2soil(79) == 81
    assert soil2fertilizer(81) == 81
    assert fertilizer2water(81) == 81
    assert water2light(81) == 74
    assert light2temperature(74) == 78
    assert temperature2humidity(78) == 78
    assert humidity2location(78) == 82
    # Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    # Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    # Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

    seed2location = lambda i: make_seed2location(information, i)
    location_numbers = [seed2location(i) for i in information['seeds']]
    assert min(location_numbers) == 35




def part1():
    ''' What is the lowest location number 
        that corresponds to one of the initial seed numbers?
    '''
    with open('day-5/input.txt') as file:
        almanac = ''.join(file)
    information = parse_almanac(almanac)
    print(information)
    return
    seed2location = lambda i: make_seed2location(information, i)
    location_numbers = [seed2location(i) for i in information['seeds']]
    assert min(location_numbers) == 35


if __name__ == '__main__':
    test1()
    print(f'Part 1 {part1()}')


