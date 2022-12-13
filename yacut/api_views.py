import re

from flask import request, jsonify

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    elif 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!', 400)

    custom_id = data.get('custom_id')
    url = data.get('url')
    pattern = re.compile("^[a-zA-Z0-9]*$")

    if 'custom_id' not in data or data['custom_id'] == None:
        custom_id = get_unique_short_id()

    if custom_id and len(custom_id) > 16:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой '
                              'ссылки', 400)
    elif not pattern.match(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой '
                              'ссылки', 400)

    if URLMap.query.filter_by(short=custom_id).first():
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.', 400)

    urlmap = URLMap(
        original=url,
        short=custom_id,
    )
    db.session.add(urlmap)
    db.session.commit()
    urlmap.short = request.host_url + urlmap.short
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if not urlmap:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    data = {
        'url': urlmap.original
    }
    return jsonify(data), 200
