from json import load


def get_token_list(name):
    TOKEN_LISTS = [
        '1inch',
        'coingecko',
        'uniswap',
    ]

    if name not in TOKEN_LISTS:
        raise Exception('Unknown tokenlists name')

    with open(f'lists/{name}.json') as f:
        return load(f)
