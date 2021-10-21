import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from back.config import Config
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)

instructions = [\
"Each of the polynomial's coefficients may be represented as an integer or decimal, but not a fraction (because '/' has special meaning in a URL).",\
"Your variable must be a string which starts with a letter (upper- or lowercase) or underscore and which contains only letters, underscores, or digits.",\
"Represent the product of a number and a variable in the usual way: number ('coefficient') before variable, with the multiplication operation represented either by a '*' or in an implied manner (ie with nothing separating the coefficient and the variable).",\
"You need not represent the absolute value of a coefficient if it equals 1.  For instance you may type 'x' instead of '1x' or '1*x', or '-x' instead of '-1x' or '-1*x'.",\
"You need not type the polynomial's terms in any particular order (such as largest power first or last).",\
"You need not include any terms in the polynomial for which the coefficient is zero.  For instance you may write '4x^2-9' instead of '4x^2+0x-9'.",\
]


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
    return {"instructions": instructions}

@app.route('/<incoming_string>')
def index(incoming_string):
    return {"incoming_string": incoming_string}
