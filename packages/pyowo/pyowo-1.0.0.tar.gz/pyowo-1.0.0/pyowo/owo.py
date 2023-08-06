from re import compile, sub


replacements = [
    (compile(r"(?:r|l)"), "w"),
    (compile(r"(?:R|L)"), "W"),
    (compile(r"n([aeiou])"), "ny\\1"),
    (compile(r"N([aeiou])"), "Ny\\1"),
    (compile(r"N([AEIOU])"), "NY\\1"),
    (compile(r"ove"), "uv"),
]

def owo(text: str):
    for r in replacements:
        text = sub(r[0], r[1], text)
    return text
