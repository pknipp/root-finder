def is_legal_start(char):
    ascii = ord(char)
    return ((ascii > 64 and ascii < 91) or (ascii > 96 and ascii < 123) or ascii == 95)

def is_legal_char(char):
    if is_legal_start(char):
        return True
    ascii = ord(char)
    return (ascii > 47 and ascii < 58)

instructions = [ \
    "After '...herokuapp.com' above you should type a slash ('/') followed by the polynomial which you'd like to factor, following the format specified below.", \
    { \
        "polynomial format" :  \
            [ \
                "Each of the polynomial's coefficients may be represented as an integer or decimal but not as a fraction, because '/' has special meaning in a URL.",\
                "Your variable must be a string which starts with a letter (upper- or lowercase) or underscore and which - if multi-character - otherwise contains only letters, underscores, or digits.",\
                "Represent the product of a coefficient and a variable in the usual sequence: coefficient before variable.",    \
                "Represent the multiplication operation either by a '*' or in an implied manner (ie with nothing separating the coefficient and the variable).",\
                "Represent 'x squared' either as 'x**2' (preferably) or 'x^2' (OK) but not as 'x*x'. Do likewise for higher powers.", \
                "You need not represent the absolute value of a coefficient if it equals 1.  For instance you may type 'x' instead of '1x' or '1*x', or '-x' instead of '-1x' or '-1*x'.",\
                "You need not type the polynomial's terms in any particular order (such as largest power first or last).",\
                "You need not include any terms in the polynomial for which the coefficient is zero.  For instance you may write '4x**2-9' instead of '4x**2+0x-9'.",\
                "Spaces in your formula are optional, but be forewarned that their use will make the address less easy to read after you hit 'RETURN', because each space will be replaced by '%20'.", \
            ]   \
    }   \
]
