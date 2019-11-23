from nlp_tools import tokenizer


def canonicalize_text(s):
    words, _ = tokenizer.basic_tokenizer(s)
    return ' '.join(words)


