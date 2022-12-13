import re
from http import HTTPStatus

from flask import request, jsonify

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id

MAX_SHORT_URL_LEN = 16


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса',
                              HTTPStatus.BAD_REQUEST)
    elif 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!',
                              HTTPStatus.BAD_REQUEST)

    custom_id = data.get('custom_id')
    url = data.get('url')
    pattern = re.compile("^[a-zA-Z0-9]*$")

    if not custom_id:
        custom_id = get_unique_short_id()
    if custom_id and len(custom_id) > MAX_SHORT_URL_LEN:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой '
                              'ссылки', HTTPStatus.BAD_REQUEST)
    elif not pattern.match(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой '
                              'ссылки', HTTPStatus.BAD_REQUEST)

    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.',
                              HTTPStatus.BAD_REQUEST)

    urlmap = URLMap(
        original=url,
        short=custom_id,
    )
    db.session.add(urlmap)
    db.session.commit()
    urlmap.short = request.host_url + urlmap.short
    return jsonify(urlmap.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    data = {
        'url': urlmap.original
    }
    return jsonify(data), HTTPStatus.OK
