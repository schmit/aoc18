"""
Useful helper functions for Advent of Cobe 2018
"""



def read_input(day, transform=lambda x: x):
    with open(f'inputs/day{day}.txt', 'r') as f:
        for line in f:
            yield transform(line)

