import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect, generate_csrf
from root_finding.config import Config
import json
import cmath
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
    html = "<h3><p align=center>Instructions:</p></h3>"
    html += "<div>General:</div><ul>"
    for line in helper.general:
        html += "<li>" + line + "</li>"
    html += "</ul>"
    html += "<div>Formats:</div><ol><li>array</li><ul>"
    for line in helper.array:
        html += "<li>" + line + "</li>"
    html += "</ul>"
    html += "<li>string: UNDER CONSTRUCTION</li><ul>"
    for line in helper.string:
        html += "<li>" + line + "</li>"
    html += "</ul></ol>"
    return html

    # return {"instructions": [ \
        # {"general": helper.general}, \
        # {"formats": [{"array": helper.array}, {"string": "UNDER CONSTRUCTION"}]} \
    # ]}

@app.route('/<str_in>')
def index(str_in):
    str_in = "".join(str_in.split(" ")) # Remove spaces in order to prevent '%20'.
    if str_in[0] == '[':
        a = list(map(lambda x: float(x), str_in[1:-1].split(",")))
        roots = helper.zroots(a, True)
        n = 16
        product = 1
        sum = 0
        func_mag = 0
        for root in roots:
            product *= cmath.polar(root)[0]
            sum += root.real
            func = 0
            pow = 1
            for coef in a:
                func += coef * pow
                pow *= root
            func_mag += cmath.polar(func)[0]
        product *= (a[len(a) - 1] / a[0])
        product -= 1
        sum *= -(a[len(a) - 1] / a[len(a) - 2])
        sum -= 1
        roots = list(map(lambda x: str(round(x.real, n)) + (((' + ' if x.imag > 0 else ' - ') + str(abs(x.imag)) + 'j') if x.imag else ''), roots))
        html = "<h3><p align=center>Results:</p></h3><ul>"
        html += "<li>your polynomial: " + str_in + "</li>"
        html += "<li>validity check of roots (All three numbers should be small.): </li><ul>"
        html += "<li>based on product of roots: " + str(product) + " </li>"
        html += "<li>based on sum of roots: " + str(sum) + " </li>"
        html += "<li>based on sum of values of polynomial: " + str(func_mag) + " </li></ul>"
        html += "<li>roots (including imaginary parts - if complex):<ul>"
        for root in roots:
            html += "<li>" + root + "</li>"
        html += "</ul>"
        return html
    str_in = "^".join(str_in.split("**")) # Temporarily replace ** with ^, to allow removal of single *.
    str_in = "^".join(str_in.split("^+")) # '+' is unnecessary in exponent.
    str_in = "".join(str_in.split("*")) # Make multiplication implicit rather than explicit.
    str_in = "**".join(str_in.split("^")) # Replace '^' by '**', to prevent instances of '%5E'.
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
    strs = str_in.split(var)
    end = strs.pop()
    # if not len(strs):
        # return {"message": "This polynomial has only the 'constant' term, so there are no roots."}
    front = strs.pop(0)
    coefs = {} # This dict'll have two properties: exponent and coefficient
    # make a helper function which checks an element of strs for more than 0 or 1 +/- sign
    # if such an excess is detected, split it, and reinsert it assuming exponent of leading term is zero
    # for str in strs:
        # pass
    return {"variable string": var, "strs": strs}
    # return {"incoming_string": incoming_string}
