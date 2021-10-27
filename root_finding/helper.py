import cmath
import random

def is_legal_start(char):
    ascii = ord(char)
    return ((ascii > 64 and ascii < 91) or (ascii > 96 and ascii < 123) or ascii == 95)

def is_legal_char(char):
    if is_legal_start(char):
        return True
    ascii = ord(char)
    return (ascii > 47 and ascii < 58)

def laguer(a, x, eps, polish):
    m = len(a) - 1
    zero = complex(0, 0)
    epss = 1e-14
    maxit = 100
    dxold = cmath.polar(x)[0]
    for iter in range(0, maxit):
        b = a[m]
        err = cmath.polar(b)[0]
        d = zero
        f = zero
        abx = cmath.polar(x)[0]
        for j in range(m - 1, -1, -1):
            f = x * f + d
            d = x * d + b
            b = x * b + a[j]
            err = cmath.polar(b)[0] + abx * err
        err *= epss
        if (cmath.polar(b)[0] <= err):
            return x
        g = d / b
        g2 = g * g
        h = g2 - 2 * f / b
        sq = cmath.sqrt((m - 1) * (m * h - g2))
        gp = g + sq
        gm = g - sq
        if cmath.polar(gp)[0] < cmath.polar(gm)[0]:
            gp = gm
        dx = m / gp
        x1 = x - dx
        if (x == x1):
            return x
        x = x1
        cdx = cmath.polar(dx)[0]
        if iter > 6 and cdx >= dxold:
            return x
        dxold = cdx
        if not polish:
            if cmath.polar(dx)[0] <= eps * cmath.polar(x)[0]:
                return x
    return "too many iterations"

def zroots(a, polish):
    # Make a copy of coefficients list, for deflation.
    ad = list(a)
    m = len(a) - 1
    eps = 1e-14
    roots = list()
    for j in range(m):
        new_m = m - j
        x = laguer(ad, complex(0, 0), eps, False)
        roots.append(x)
        b = ad[new_m]
        for jj in range(new_m - 1, -1, -1):
            c = ad[jj]
            ad[jj] = b
            b = x * b + c
        ad.pop()
    if polish:
        for j in range(m):
            root = laguer(a, roots[j], eps, True)
            if abs(root.imag) <= 2 * abs(root.real) * eps:
                root = complex(root.real, 0)
            roots[j] = root
    return sorted(roots, key = lambda x: x.real)

def parse_roots(str_in, json):
    if str_in[0] == '[':
        a = list(map(lambda x: float(x), str_in[1:-1].split(",")))
        roots = zroots(a, True)
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
        heading = "Results"
        your_poly = "your polynomial: " + str_in
        validity = "validity check of roots (All three numbers should be small.)"
        checks = [ \
            "based on product of roots: " + str(product), \
            "based on sum of roots: " + str(sum), \
            "based on sum of values of polynomial: " + str(func_mag), \
                ]
        root_str = "roots (including imaginary parts, if complex):"
        if json:
            return {heading: [your_poly, {validity: checks}, {root_str: roots}]}
        else:
            html = "<p align=center>" + heading + "</p>"
            html += "<ul><li>" + your_poly + "</li>"
            html += "<li>" + validity + "</li><ul>"
            for check in checks:
                html += "<li>" + check + "</li>"
            html += "</ul><li>" + root_str + "</li><ul>"
            for root in roots:
                html += "<li>" + root + "</li>"
            return html + "</ul></ul>"

general = [ \
    "After '...herokuapp.com' above you should type '/json/' and then your polynomial.  Input your polynomial according to one of the two formats below: 'array' or 'string'.", \
    "If you want the response in html rather than in json, omit '/json' from the address.", \
    "Spaces are allowed - but discouraged - in whichever format you use, because a '%20' will replace each space after you hit 'return', thereby making the address uglier.", \
    "The resulting page will show some 'validity checks', along with the roots themselves." \
]
array = [ \
    "This is a comma-separated list of coefficients, enclosed by square brackets.  List the coefficients in order of increasing exponent, ie starting with the 'constant' term.", \
    "Example: 1+5x-4x**3 would be represented by the following 'array': [1,5,0,-4].", \
]
string = [ \
    "Each of the polynomial's coefficients may be represented as an integer or decimal but not as fraction, because '/' has special meaning in a URL.",\
    "Your variable must be a string which starts with a letter (upper- or lowercase) or underscore. If your variable has multiple characters, they may only be letters, underscores, or digits.",\
    "Represent the product of a coefficient and a variable in the usual sequence: coefficient before variable, and represent the multiplication operation either by * or in an implied manner (ie with nothing separating the coefficient and the variable).",\
    "Represent 'x squared' either as 'x**2' (preferably) or 'x^2' (OK) but not as 'x*x'. Do likewise for larger powers.", \
    "You need not represent the absolute value of a coefficient if it equals 1.  For instance you may type 'x' instead of '1x' or '1*x', or '-x' instead of '-1x' or '-1*x'.",\
    "You need not type the polynomial's terms in any particular order (such as largest power first or last).",\
    "You need not include any terms in the polynomial for which the coefficient is zero. For instance you may write '4x**2-9' instead of '4x**2+0x-9'.",\
]
