- valid in url: letters (UPPER and lower), 0-9, -.*)(
- reserved characters: percent sign, dollar sign, ampersand, plus sign, comma, forward slash, colon, semi-colon, equal sign, question mark and “@” symbol.
- valid in Chrome url: +
- encoded hex versions of various chars (hex indicated by leading %):
    " "(20), - slash route takes no params, returning only instructions for how to use the API
- route w/params takes a string representing an equation to be factorized.
- parse the string, as follows:
    - Replace each instance of " " with "".
    - Replace each instance of "**" with "^".
    - Replace each instance of "^+" with "^".
    - Replace each instance of "*" with "".
    - Any instance of "^-" generates an early return, with error message.
    - Trace thru the string until encountering an underscore or a letter (upper- or lower-case), which itself should be identified as the first character of the string.  Continue to trace until finding a character which is not an acceptable character (letter, underscore, or number).  This defines the end of the string and hence the string itself.  (This equates to the js rule - excluding $ - or the python rule.)
    - Now string_tot = str/var/str/var/str/etc
    - If the stuff preceding the first string contains a non-leading "+" or "-":
        split this on that sign (and put that sign on 2nd element), in which case
        string_tot = const_str/var/^0/str/var/str/var/str/etc
         preceding first string can be either "" (1), "-" (-1), or any (complex?)number.  NOTE THAT THE FIRST STRING MAY CONTAIN THE CONSTANT TERM, which is indicated if it contains a non-leading "+" or "-"
    - now string_tot = #/var/str/var/str/etc
    - parse the str after each var, which should begin with "^" & be immediately followed by the digit 0-9, which should itself be immediately followed by any digit 0-9, until reaching a non-digit character.
    - now total string is of the form #/var/^/int/str/var/^/int/str/var/etc
    - if the leading char of str is "/" followed by a positive number followed by "+" or "-", interpret this as the inverse of the coefficient for the preceding term.  (Do not allow more than one "/"?).
    - Now total string is of the form #/var/^/int/str/var/^/int/str/etc
    - if the leading char of string is "+" or "-" followed by either "" (= 1) or a positive number, interpret this as something which should multiply the coefficient of the following term.
    - Now total string is of the form #/var/^/int/#/var/^/int/str/etc, ie completely parsed into a form which can be used to load a COEFS array.
    - HOW TO FIND THE VAR^0 TERM IN THE POLYNOMIAL? (replace this by var^0)
    - Return an error message if parsing is unsuccessful.
- import cmath, to allow complex arithmetic
- Use Laguerre's method for finding roots (found on p. 263 of Numerical Recipes), as follows:
    COEFS2 = [...COEFS]
    roots = [(0, 0), (0, 0), ...]
    loop over COEFS:
        use COEFS2, starting from particular element of roots, to iterate to a particular root (root0), without polishing
        use root0 to overwrite particular root in roots list
        overwrite COEFS2 by deflating COEFS2 with (z - root0)
    loop over COEFS (again):
        same as above, but (1) use COEFS instead of COEFS2, (2) do polish, and (3) don't deflate
- Present results in 2 - 3 ways:
    - roots sorted in order of increasing order of abs value of real part (which means that complex roots will appear in adjacent cc pairs)
    - (completely) factored form, ie in terms of binomials, some of which may contain complex numbers
    - IF original polynomial had real coefficients and if there are some CC pairs, "maximally" factorize the polynomial, ie including some irreduciable quadratic factors.
