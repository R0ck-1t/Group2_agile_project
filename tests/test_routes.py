from flask import Flask
import json

from routes.flaskroutes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/login'

    response = client.get(url)
    assert response.status_code == 200