import cmath
import random

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

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
    str_in = "".join(str_in.split(" ")) # Remove spaces in order to prevent '%20' in address bar.
    a = None # Initialize this in outer scope.
    if str_in[0] == '[': # Polynomial is formatted as an array.
        str_in = str_in[1:] # removing leading open bracket
        if not str_in[-1] == ']':
            return {"error": "You forgot the closing square bracket."}
        coefs = str_in[:-1].split(",")
        n_coef = len(coefs)
        leading_coef = coefs[n_coef - 1]
        if is_number(leading_coef) and not float(leading_coef):
            coefs.pop() # Trim the array if the highest coefficient vanishes, to avoid divide-by-zero error.
            n_coef -= 1
        not_a_number = 0
        for coef in coefs:
            if not is_number(coef):
                not_a_number += 1
        if not_a_number:
            return {"error": str(not_a_number) + " of your coefficients is/are not a number."}
        if n_coef == 1:
            return {"error": "Your polynomial seems to be constant, which'll lead to either zero roots or an infinite number thereof."}
        a = list(map(lambda x: float(x), coefs)) # Convert list items from strings to numbers.
    else:                # Polynomial is formatted as a string.
        if str_in[0] == "+":
            str_in = str_in[1:] #leading "+" is unnecessary
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
                if is_legal_start(char):
                    found_var = True
                    var = char
            else:
                if is_legal_char(char):
                    var += char
                else:
                    break
        if var is None:
            return {"error": "No legal variable name was found."}
        strs = str_in.split(var)
        # Ensure that any linear term is written as, e.g., 2x**1
        for i in range(1, len(strs)):
            if not strs[i][0:2] == "**":
                strs[i] = "**1" + strs[i]
        # Ensure that any constant term is written as, e.g., 2x**0
        # Deal with leading term separately:
        leading = strs[0][1:]
        signs = ['+', '-']
        for sign in signs:
            if sign in leading:
                i = leading.index(sign)
                strs[0] = strs[0][0:i]
                strs.insert(1, "**0" + strs[0][i:])

        # Now deal with rest of terms in list, except for trailing one.
        i_str = 1
        while i_str < len(strs) - 1:
            string = strs[i_str]
            i = None
            ## Seek 1st sign, which MUST exist.
            for sign in signs:
                if sign in string:
                    i = string.index(sign)
            ## Seek 2nd sign, which MAY exist.
            for sign in signs:
                if sign in string[i + 1:]:
                    i = string.index(sign, i + 1)
                    strs[i_str] = string[0:i]
                    strs.insert(i_str + 1, "**0" + strs[i_str][i:])
            i_str += 1

        # Now deal w/trailing term
        trailing = strs[len(strs) - 1]
        if "+" in trailing or "-" in trailing:
            strs.append("**0")

        i_str = 0
        while i_str < len(strs):
            string = strs[i_str]
            coef = None
            sign_count = 0
            for i in range(1, len(string)):
                if string[i] == '+' or string[i] == '-':
                    sign_count += 1
            if sign_count > 1:
                return {"error": "There is something wrong with this string: " + string}
            elif sign_count == 1:
                for sign in ["+", "-"]:
                    if sign in string:
                        strings = string.split(sign)
                        strs[i_str] = strings[0]
                        strs.insert(i_str + 1, strings[1])

            if "+" in string[1:] or "-" in strs[0][1:]:
                strs[i_str] = "**0" + string
                strs.insert(i_str + 1, string.split())
        coefs = {} # This dict'll have two properties: exponent and coefficient
        leading = strs[0]
        for i_str in range(len(strs) - 2):
            coef = None
            if is_number(leading):
                coef = float(leading)
            else:
                return {"error": "There is a problem with one of your coefficients: " + leading}
            trailing = strs[i_str + 1]
            trailings = None
            is_negative = None
            if '-' in trailing:
                trailings = trailing.split("-")
                is_negative = True
            else:
                trailings = trailing.split("+")


        # Parse the first string separately.
        front = strs.pop(0)
        coef = None
        if is_number(front):
            coef = float(front)
        else:
            return {"error": "There is a problem with your leading coefficient: " + front}
        coef = 1
        if front[0] == "-":
            coef *= -1
            front = front[1:]
        n_char = len(front)
        i_char = 0
        if front[i_char] == ".":
            i_char += 1
        while i_char < n_char and is_number(front[0: i_char + 1]):
            coef
            i_char += 1
        coefs = {} # This dict'll have two properties: exponent and coefficient
        end = strs.pop() # Parse this last.

        # make a helper function which checks an element of strs for more than 0 or 1 +/- sign
        # if such an excess is detected, split it, and reinsert it assuming exponent of leading term is zero
    
        return {"error": "I've not yet finished coding this."}
        return {"variable string": var, "strs": strs}
        # return {"incoming_string": incoming_string}

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
    product *= a[len(a) - 1]
    if a[0]:
        product /= a[0]
        product -= 1
    sum *= -a[len(a) - 1]
    if a[len(a) - 2]:
        sum /= a[len(a) - 2]
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
