import html
import regex as re
from bs4 import BeautifulSoup

emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u200d"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\u3030"
    "\ufe0f"
    "]+",
    flags=re.UNICODE,
)

email_pattern = re.compile(
    """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
)

ascii_emoji_pattern = re.compile(":\\)|;\\)|:D|;D|:\\(|;\\(|:/|;/|xd|xD")

weekday_pattern = re.compile("monday|tuesday|wednesday|thursday|friday|saturday|sunday")

# Explanation:
# - this will match: http://google.com, www.google.com/a/b/c, www.google.com etc.
# - it will also match: google.com/a, google.com/a/b/c etc.
# - but it will NOT match: google.com
# since we want to avoid false positives like: Please help me.I have a ...
# where me.I could be matched as a link
url_pattern_base = "[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b[-a-zA-Z0-9()@:%_\\+.~#?&\\/\\/=]"  # noqa
url_pattern = re.compile(
    f"(?:(?:https?:\\/\\/|www\\.){url_pattern_base}*|{url_pattern_base}+)"
)


def normalize_special(text: str) -> str:
    text = str(text)
    text = text.replace("#", "")
    text = text.replace("&", "and")
    text = text.replace("’", "'")
    return text


def unescape_html(text: str) -> str:
    text = str(text)
    text = html.unescape(text)
    return text


def remove_html(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def unify_en_weekday(text: str) -> str:
    return weekday_pattern.sub("monday", str(text))


def remove_emoji(text: str) -> str:
    text = str(text)
    text = remove_unicode_emoji(text)
    text = remove_ascii_emoji(text)
    return text


def remove_unicode_emoji(text: str) -> str:
    return emoji_pattern.sub("", str(text))


def remove_ascii_emoji(text: str) -> str:
    return ascii_emoji_pattern.sub("", str(text))


def unify_url(text: str, replacement: str = "URL") -> str:
    return url_pattern.sub(replacement, str(text))


def unify_email(text: str, replacement: str = "EMAIL") -> str:
    return email_pattern.sub(replacement, str(text))


def simplify_punctuation(text: str) -> str:
    text = str(text)
    text = re.sub(r"([!?,;])\1+", r"\1", text)
    text = re.sub(r"\.{2,}", r"...", text)
    text = re.sub(r" ([,\.\?!])", r"\1", text)
    text = re.sub(r"^(\s|\.|,|\?|;|:|!)*(.*)$", r"\2", text)
    return text


def normalize_whitespace(text: str) -> str:
    text = str(text)
    text = re.sub(r"//t", r"\t", text)
    text = re.sub(r"( )\1+", r"\1", text)
    text = re.sub(r"(\n)\1+", r"\1", text)
    text = re.sub(r"(\r)\1+", r"\1", text)
    text = re.sub(r"(\t)\1+", r"\1", text)
    return text.strip(" ")


def unify_numbers(text: str) -> str:
    text = re.sub(r"\d", r"1", str(text))
    return text


def strip_en_welcome(text: str) -> str:
    welcomes = [
        "good morning",
        "good afternoon",
        "good evening",
        "morning",
        "evening",
        "welcome",
        "dear",
        "hi",
        "hey",
        "hello",
    ]

    seps = [",", "!", ".", ""]

    text = str(text)
    for sep in seps:
        for welcome in welcomes:
            prefix = welcome + sep
            if text.startswith(prefix):
                text = text[len(prefix) :].strip()

    return text
