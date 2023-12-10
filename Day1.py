#!python3
''' Advent of Code 2023 --- Day 1
'''


def calibration_values_part1(lines):
    ''' The newly-improved calibration document consists of lines of text;
        each line originally contained a specific calibration value 
        that the Elves now need to recover. 
        On each line, the calibration value can be found 
        by combining the first digit and the last digit (in that order) 
        to form a single two-digit number.
    '''
    digits = [str(i) for i in range(10)]
    for line in lines:
        digit1_indices = map(line.find,  digits)
        digit2_indices = map(line.rfind, digits)
        digit1_indices  = (i for i in digit1_indices if i != -1)
        digit2_indices  = (i for i in digit2_indices if i != -1)
        digit1 = line[min(digit1_indices)]
        digit2 = line[max(digit2_indices)]
        yield int(digit1 + digit2)


def test1():
    test_input = '1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet'
    values = list(calibration_values_part1(test_input))
    for x, y in zip(values, (12, 38, 15, 77)):
        assert x == y
    assert sum(values) == 142


def part1():
    with open('day-1-input.txt') as file:
        print(sum(calibration_values_part1(file)))


def calibration_values_part2(lines):
    ''' Some of the digits are actually spelled out with letters:
        one, two, three, four, five, six, seven, eight, and nine 
        also count as valid "digits".
    '''

    english = ['one', 'two', 'three', 'four', 'five', 
               'six', 'seven', 'eight', 'nine']
    eng2dec = lambda s: english.index(s) + 1
    digits = [str(i) for i in range(10)] + english

    for line in lines:
        digit1_indices = {digit: line. find(digit) for digit in digits}
        digit2_indices = {digit: line.rfind(digit) for digit in digits}
        digit1_indices = {digit: i for digit, i in digit1_indices.items() 
                          if i != -1}
        digit2_indices = {digit: i for digit, i in digit2_indices.items() 
                          if i != -1}
        digit1, _ = min(digit1_indices.items(), key=lambda pair: pair[1])
        digit2, _ = max(digit2_indices.items(), key=lambda pair: pair[1])
        if digit1 in english: digit1 = str(eng2dec(digit1))
        if digit2 in english: digit2 = str(eng2dec(digit2))
        yield int(digit1 + digit2)


def test2():
    test_input = 'two1nine', 'eightwothree', 'abcone2threexyz', \
                 'xtwone3four', '4nineeightseven2', 'zoneight234', \
                 '7pqrstsixteen'
    values = list(calibration_values_part2(test_input))
    for x, y in zip(values, (29, 83, 13, 24, 42, 14, 76)):
        assert x == y, (x, y)
    assert sum(values) == 281


def part2():
    with open('day-1-input.txt') as file:
        print(sum(calibration_values_part2(file)))


if __name__ == '__main__':
    test1()
    part1()
    test2()
    part2()


