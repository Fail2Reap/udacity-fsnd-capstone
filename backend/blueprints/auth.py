from urllib.parse import urlencode

from flask import (
    Blueprint,
    url_for,
    redirect,
    session,
    current_app
)

auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.get('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('home_routes.home', _external=True),
        'client_id': current_app.config['AUTH_CLIENT_ID']
    }
    return redirect(
        f"https://{current_app.config['AUTH_DOMAIN']}/v2/logout?"
        f"{urlencode(params)}"
    )
