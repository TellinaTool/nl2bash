_SPACE = "<SPACE>"

_NUMBER = "_NUMBER"
_SIZE = "_SIZE"
_TIMESPAN = "_TIMESPAN"
_DATETIME = "_DATETIME"
_PATH = "_PATH"
_FILE = "_FILE"
_DIRECTORY = "_DIRECTORY"
_PERMISSION = "_PERMISSION"
_REGEX = "_REGEX"

_PATTERNS = ['Regex', 'File', 'Directory', 'Path']
_QUANTITIES = ['Number', '+Number', '-Number',
               'Size', '+Size', '-Size',
               'Timespan', '+Timespan', '-Timespan',
               'DateTime', '+DateTime', '-DateTime',
               'Permission', '+Permission', '-Permission']
_ENTITIES = _PATTERNS + _QUANTITIES

category_conversion = {
    _FILE: 'File',
    _DIRECTORY: 'Directory',
    _PATH: 'Path',
    _PERMISSION: 'Permission',
    _DATETIME: 'DateTime',
    _TIMESPAN: 'Timespan',
    _REGEX: 'Regex',
    _SIZE: 'Size',
    _NUMBER: 'Number',
}

_SPECIAL_SYMBOL_RE = r'[^ ]*[\.\*|\\|\/|\~|\@|\%|\#|\?|\+|\$|\{|\}]+[^ ]*'
_FILE_EXTENSION_RE = r'(aiff|cda|mid|mp3|mp4|mpa|ogg|wav|wma|wpl|7z|arj|deb|pkg|' \
        r'rar|rpm|gz|bin|dmg|iso|vcd|vcr|dvd|csv|dat|db|log|mdb|sav|sql|' \
        r'xml|apk|bat|bin|cgi|pl|com|html|css|js|exe|gadget|jar|py|wsf|fnt|' \
        r'fon|otf|ttf|ai|bmp|gif|ico|jpg|jpeg|png|psd|svg|tif|java|php|txt|c|' \
        r'cpp|cc|o|htm|asp|cer|jsp|json|rss|xhtml|odp|ppt|pptx|class|h|sh|swift|' \
        r'vb|ods|xlr|xlsx|xls|ini|msi|sys|tmp|drv|dmp|dll|bak|3gp|flv|h264|avi|' \
        r'mkv|mov|m4v|rm|mpg|mpeg|swf|wmv|doc|docx|tex|pdf|rtf|wps|wpd|xz|cvs)'

_PATH_RE = r'([^ ]*\/)+[^ ]*'

_DIGIT_RE = r'\d*\.?\d+'

_NUMERICAL_PERMISSION_RE = r'[0-7]{3,4}'
_PATTERN_PERMISSION_RE = r'([u|g|o]+[+|-|=][r|w|x|s|u|t]+)+'

# Credit: time expressions adapted from
# https://github.com/nltk/nltk_contrib/blob/master/nltk_contrib/timex.py
_MONTH_RE = r'(january|jan|jan\.|february|feb|feb\.|march|mar|mar\.|april|apr|apr\.|' \
            r'may|june|jun|jun\.|july|jul|jul\.|august|aug|aug\.|september|sep|sep\.|' \
            r'october|oct|oct\.|november|nov|nov\.|december|dec|dec\.)'
_REL_DAY_RE = r'(today|yesterday|tomorrow|the day before yesterday|' \
              r'the day after tomorrow)'

digitize_month = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12"
}

_SIZE_UNIT = r'(kilobyte|kilobyt|kilo byte|megabyte|megabyt|mega byte|gigabyte|' \
             r'gigabyt|terabyte|terabyt|byte|byt|kb|mb|gb|tb|b|k|m|g|t)'

_DURATION_UNIT = r'(second|sec|minute|minut|min|hour|hr|day|week|' \
             r'month|mon|year|yr|s|m|h|d|w|y)'

# Regular expressions used to tokenize an English sentence.
_WORD_SPLIT = "^\s+|\s*,\s*|\s+$|^[\(|\[|\{|\<]|[\)|\]|\}|\>]$"
_WORD_SPLIT_RESPECT_QUOTES = '(?:[^\s,"]|"(?:\\.|[^"])*")+'

ENGLISH_STOPWORDS = {
    # "a",
    # "an",
    "the",
    # "be",
    # "is",
    # "been",
    # "being",
    # "was",
    # "were",
    # "are",
    "has",
    "have",
    "had",
    "here",
    "there",
    "do",
    "how",
    "i",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "me",
    "my",
    "myself",
    "can",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "must",
    "should",
    "would",
    "you",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "your",
    "yours",
    "yourself",
    "yourselves",
     "he",
    "he'd",
    "he'll",
    "he's",
    "her",
    "here",
    "here's",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "she",
    "she'd",
    "she'll",
    "she's",
    # "it",
    "it's",
    # "its",
    "itself",
    "we",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "their",
    "theirs",
    # "them",
    "themselves",
    "then",
    "there",
    "there's",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "let",
    "let's",
    "this",
    # "that",
    # "these",
    # "those",
    # "what",
    "what's",
    # "which",
    # "whose",
    "how",
    "how's"
}

word2num = {'one':   1, 'eleven':     11,
            'two':   2, 'twelve':     12,
            'three': 3, 'thirteen':   13,
            'four':  4, 'fourteen':   14,
            'five':  5, 'fifteen':    15,
            'six':   6, 'sixteen':    16,
            'seven': 7, 'seventeen':  17,
            'eight': 8, 'eighteen':   18,
            'nine':  9, 'nineteen':   19,
            'ten':     10,
            'twenty':  20,
            'thirty':  30,
            'forty':   40,
            'fifty':   50,
            'sixty':   60,
            'seventy': 70,
            'eighty':  80,
            'ninety':  90,
            'twenty-four': 24
}

size_units = {
    'b',
    'k',
    'm',
    'g',
    't',
    'kb',
    'mb',
    'gb',
    'tb',
    'byt',
    'byte',
    'kilobyt',
    'kilobyte',
    'megabyt',
    'megabyte',
    'gigabyt',
    'gigabyte',
    'terabyt',
    'terabyte'
}

duration_units = {
    's',
    'm',
    'h',
    'd',
    'w',
    'm',
    'y',
    'sec',
    'second',
    'min',
    'minut',
    'minute',
    'hour',
    'day',
    'week',
    'month',
    'year'
}

def include_space(r):
    """
    A regular expression has to have a whitespace or other separator at both
    ends.
    """
    return r'(^|\s)' + r + r'(\s|$)'

def quotation_safe(r):
    """
    Match a regular expression with or without quotation marks.
    """
    return r'"?' + r + r'"?'

def polarity_safe(r):
    """
    Match a regular expression with or without "+/-" signs.
    """
    return r'[+|-]?' + r

def add_quotations(s):
    return '"' + s + '"'

def with_quotation(s):
    return s[0] in ['"', '\''] and s[-1] in ['"', '\'']

def is_float(s):
    return '.' in s

def is_stopword(w):
    return w in ENGLISH_STOPWORDS
