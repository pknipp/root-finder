import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from back.config import Config
from datetime import datetime
from . import helper

app = Flask(__name__)
app.config.from_object(Config)

# Application Security
CORS(app)

@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') else False,
        samesite='Strict' if os.environ.get('FLASK_ENV') else None,
        httponly=True)
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    print("path", path)
    if path == 'favicon.ico':
        return app.send_static_file('favicon.ico')
    return app.send_static_file('index.html')


@app.route('/')
def hello():
    return {"instructions": helper.instructions}

@app.route('/<str_in>')
def index(str_in):
    str_in = "".join(str_in.split(" "))
    str_in = "**".join(str_in.split("^"))
    str_in = "**".join(str_in.split("**+"))
    str_in = "".join(str_in.split("*"))
    if "**-" in str_in:
        return {"error": "A polynomial does not contain negative powers."}
    var = None
    found_var = False
    for char in str_in:
        if not found_var:
            if helper.is_legal_start(char):
                found_var = True
                var = char
        else:
            if helper.is_legal_char(char):
                var += char
            else:
                break
    if var is None:
        return {"error": "No legal variable name was found."}
    return {"variable string": var}
    # return {"incoming_string": incoming_string}
