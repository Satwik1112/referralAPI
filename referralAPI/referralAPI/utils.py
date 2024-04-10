def _generate_ID_():
    from string import digits, ascii_letters
    from random import choice
    return "".join([choice(digits + ascii_letters) for _ in range(5)])


def _getToken_():
    from string import digits, ascii_letters
    from random import choice
    return "".join([choice(digits + ascii_letters) for _ in range(15)])
