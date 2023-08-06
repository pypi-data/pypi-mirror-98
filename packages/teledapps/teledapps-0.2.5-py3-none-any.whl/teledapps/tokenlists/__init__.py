from json import load
import os


def get_token_list(name):
    TOKEN_LISTS = [
        '1inch',
        'coingecko',
        'uniswap',
    ]

    if name not in TOKEN_LISTS:
        raise Exception('Unknown tokenlists name')

    path = f'{os.path.dirname(os.path.realpath(__file__))}/lists/{name}.json'

    with open(path) as f:
        return load(f)
