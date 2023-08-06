import colored
from colored import stylize


def b62enc(num):
    encoding = ""
    while num:
        num, rem = divmod(num, 62)
        encoding = alphabet[rem] + encoding
    return encoding


def paint(txt, fgr, fgg, fgb, bgr, bgg, bgb):
    fgcolor = f"#{hex(fgr)[2:].rjust(2, '0')}{hex(fgg)[2:].rjust(2, '0')}{hex(fgb)[2:].rjust(2, '0')}"
    # bgcolor = f"#{hex(bgr)[2:].rjust(2, '0')}{hex(bgg)[2:].rjust(2, '0')}{hex(bgb)[2:].rjust(2, '0')}"
    return stylize(txt, colored.fg(fgcolor) + colored.attr("bold"))  # + colored.bg(bgcolor))


alphabet = tuple("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
rev_alphabet = dict((c, v) for v, c in enumerate(alphabet))


def b62dec(string):
    num = 0
    for char in string:
        num = num * 62 + rev_alphabet[char]
    return num


def lim(x):
    return min(255, max(0, x))


def colorize128bit(n, id, ampl=0.7, change=0.3):
    byts = n.to_bytes(16, "big")
    bs = list(reversed(byts))
    margin = 255 * (1 - ampl)
    fgr = margin + sum(bs[:4]) % int(255 * ampl)
    fgg = margin + sum(bs[4:8]) % int(255 * ampl)
    fgb = margin + sum(bs[8:12]) % int(255 * ampl)
    out = ""
    for i, c in enumerate(id):
        quot, dr = divmod(b62dec(c), 4)
        quot, dg = divmod(quot, 4)
        db = quot % 4
        r = max(margin, lim(fgr + 255 * change * (dr - 2) / 2))
        g = max(margin, lim(fgg + 255 * change * (dg - 2) / 2))
        b = max(margin, lim(fgb + 255 * change * (db - 2) / 2))
        out += f"{paint(c, int(r), int(g), int(b), 0, 0, 0)}"
    return out
