from random import choice

from flask import abort, flash, redirect, render_template, request

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap


SHORT_URL_LEN = 6
SHORT_URL_CHARS = ('abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123 '
                   '4567890')


def get_unique_short_id():
    while True:
        short_link = ''
        for n in range(SHORT_URL_LEN):
            short_link += choice(SHORT_URL_CHARS)
        if not URLMap.query.filter_by(short=short_link).first():
            break
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    url = ''
    if form.validate_on_submit():
        short_link = form.custom_id.data
        if short_link:
            if URLMap.query.filter_by(short=short_link).first():
                flash(f'Имя {short_link} уже занято!"')
                return render_template('yacut/index.html', form=form)
        else:
            short_link = get_unique_short_id()

        urlmap = URLMap(
            original=form.original_link.data,
            short=short_link,
        )
        db.session.add(urlmap)
        db.session.commit()
        url = request.host_url + short_link
    return render_template('yacut/index.html', form=form, url=url)


@app.route('/<string:url>')
def redirect_view(url):
    url_obj = URLMap.query.filter_by(short=url).first()
    if not url_obj:
        abort(404)
    return redirect(url_obj.original)
