import random

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
alphas = ["a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "l", "m", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

def generate_id(total_len=8, numeric_postfix_len=3):
    alpha_len = total_len - numeric_postfix_len

    random_alpha_idxes = random.sample(range(0, len(alphas)), alpha_len)
    random_numbers_idxes = random.sample(range(0,len(numbers)), numeric_postfix_len)

    return ''.join([alphas[x] for x in random_alpha_idxes]) + ''.join([numbers[x] for x in random_numbers_idxes])