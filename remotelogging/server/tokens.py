import rethinkdb as r
from flask import Blueprint, render_template, request, g, redirect, abort, url_for

from .util import requires_auth, generate_token

bp = Blueprint(__name__, __name__)


@bp.route('/')
@requires_auth
def tokens():
    return render_template('tokens.html', tokens=r.table("tokens").run(g.rdb_conn))


@bp.route('/new/', methods=['GET'])
@requires_auth
def add_token():
    return render_template('add_token.html', error=request.args.get('error', None))


@bp.route('/new/', methods=['POST'])
@requires_auth
def do_add_token():
    name = request.form.get('name', None)
    if name is None or len(name) < 5:
        return redirect(url_for('.add_token', error="Missing or too short name (at least 5 chars)"))
    r.table('tokens').insert(
        {'name': name, 'last_used': r.epoch_time(0).to_iso8601(), 'id': generate_token()}).run(g.rdb_conn)
    return redirect('tokens')


@bp.route('/delete/', methods=['GET'])
@requires_auth
def confirm_delete_token():
    token = request.args.get('token', None)
    if token is None:
        abort(400)
    return render_template(
        'confirm-delete-token.html',
        token=list(r.table('tokens').filter({'id': token}).run(g.rdb_conn))[0])


@bp.route('/delete/', methods=['POST'])
@requires_auth
def delete_token():
    token = request.form.get('token', None)
    if token is None:
        abort(400)
    r.table('tokens').filter({'id': token}).delete().run(g.rdb_conn)
    return redirect(url_for('.tokens'))
