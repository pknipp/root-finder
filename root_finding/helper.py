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

# a = [2, -3, 1, 3, 5]
# x = 0
# x = laguer(a, x, 1e-6, False)
# print("x = ", x)
# sum = 0
# pow = 1
# for coef in a:
    # sum += coef * pow
    # pow *= x
# print("At this point the function equals ", sum)

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

general = [ \
    "After '...herokuapp.com' above you should type a slash ('/') followed by your polynomial.", \
    "Input your polynomial according to one of the two formats below: 'array' or 'string'.", \
    "In whichever format you use, spaces are allowed - but discouraged.", \
    "A '%20' will replace each space after you hit 'return', making the address uglier.", \
    "The resulting page will show the some 'validity checks', along with the roots themselves." \
]
array = [ \
    "This is a comma-separated list of coefficients, enclosed by square brackets.", \
    "List these in order of increasing exponent, ie starting with the 'constant' term.", \
    "E.g., 1+5x-4x**3 could be represented by the following 'array': [1,5,0,-4].", \
]
string = [ \
    "Each of the polynomial's coefficients may be represented as an integer or decimal but not as fraction, because '/' has special meaning in a URL.",\
    "Your variable must be a string which starts with a letter (upper- or lowercase) or underscore.", \
    "If your variable has multiple characters, they may only be letters, underscores, or digits.",\
    "Represent the product of a coefficient and a variable in the usual sequence: coefficient before variable", \
    "Represent the multiplication operation either by a '*' or in an implied manner (ie with nothing separating the coefficient and the variable).",\
    "Represent 'x squared' either as 'x**2' (preferably) or 'x^2' (OK) but not as 'x*x'. Do likewise for larger powers.", \
    "You need not represent the absolute value of a coefficient if it equals 1.", \
    "For instance you may type 'x' instead of '1x' or '1*x', or '-x' instead of '-1x' or '-1*x'.",\
    "You need not type the polynomial's terms in any particular order (such as largest power first or last).",\
    "You need not include any terms in the polynomial for which the coefficient is zero.", \
    "For instance you may write '4x**2-9' instead of '4x**2+0x-9'.",\
]
