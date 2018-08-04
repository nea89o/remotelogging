from datetime import datetime

import rethinkdb as r
from flask import Blueprint, jsonify, g, abort, request

from remotelogging.server.util import requires_token
from .config import config

bp = Blueprint(__name__, __name__)


@bp.route('/verify/')
@requires_token
def verify():
    return jsonify({**list(r.table('tokens').filter({'id': g.token}).run(g.rdb_conn))[0], 'logged_in': True})


def get_name_for_token(token):
    return list(r.table('tokens').filter({'id': token}).run(g.rdb_conn))[0]['name']


@bp.route('/logs/<string:template>/', methods=['POST'])
@requires_token
def post_log(template):
    template = list(r.table('templates').filter({'id': template}).run(g.rdb_conn))
    if not template:
        abort(400)
    template = template[0]
    data = {}
    for var in template['vars']:
        val = request.form.get(var)
        if not val:
            abort(400)
        data[var] = val
    x = r.table('logs').insert(dict(
        template=template['id'],
        reporter=get_name_for_token(g.token),
        data=data,
        time=datetime.now(config.r_timezone)
    )).run(g.rdb_conn)
    return jsonify({'success': True})
