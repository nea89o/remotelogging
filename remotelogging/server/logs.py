import rethinkdb as r
from flask import Blueprint, render_template, request, g

from remotelogging.server.util import requires_auth

bp = Blueprint(__name__, __name__)


def fill_text(template, data):
    t = list(r.table('templates').filter(dict(id=template)).run(g.rdb_conn))
    if len(t) == 0:
        return f"{template} % {repr(data)}"
    return t[0]['text'].format(**data)


@bp.route('/')
@requires_auth
def view_logs():
    try:
        offset = int(request.args.get('page', '0'))
    except ValueError:
        offset = 0
    return render_template('logs.html', fill_text=fill_text, offset=offset,
                           entries=r.table('logs').order_by('time').skip(50 * offset).limit(50).run(g.rdb_conn))
