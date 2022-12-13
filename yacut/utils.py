from random import choice

from yacut.models import URLMap

SHORT_URL_LEN = 6
SHORT_URL_CHARS = ('abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123 '
                   '4567890')


def get_unique_short_id():
    while True:
        short_link = ''
        for _ in range(SHORT_URL_LEN):
            short_link += choice(SHORT_URL_CHARS)
        if not URLMap.query.filter_by(short=short_link).first():
            break
    return short_link
