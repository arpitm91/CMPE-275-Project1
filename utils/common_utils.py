import random


def get_random_numbers(upper_limit, random_count):
    random_numbers = []
    while len(random_numbers) < random_count:
        number = random.randint(0, upper_limit-1)
        if number not in random_numbers:
            random_numbers.append(number)
    return random_numbers
