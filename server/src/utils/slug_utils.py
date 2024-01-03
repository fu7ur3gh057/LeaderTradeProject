import os
from datetime import datetime
from django.template.defaultfilters import slugify as django_slugify

alphabet = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ы": "i",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def slugify(text: str):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify("".join(alphabet.get(w, w) for w in text.lower()))


def slug_path(base_path, filename):
    now = datetime.now()
    fname, dot, extension = filename.rpartition(".")
    slug = slugify(fname)
    return os.path.join(datetime.strftime(now, base_path), "%s.%s" % (slug, extension))
