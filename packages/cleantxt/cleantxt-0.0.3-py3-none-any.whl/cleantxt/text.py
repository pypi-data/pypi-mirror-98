import re
import string
from collections import Counter


def is_arabic(word):
    re = False
    for ch in word:
        if ('\u0600' <= ch <= '\u06FF' or
            '\u0750' <= ch <= '\u077F' or
            '\u08A0' <= ch <= '\u08FF' or
            '\uFB50' <= ch <= '\uFDFF' or
            '\uFE70' <= ch <= '\uFEFF' or
            '\U00010E60' <= ch <= '\U00010E7F' or
                '\U0001EE00' <= ch <= '\U0001EEFF'):
            re = True
            break
    return re


def remove_duplicated_letter(line):

    result = []
    for w in line.split(' '):
        try:
            count = Counter(w).most_common()[0][1]
            if count > 2:
                result.append(re.sub(r'(\w)\1+', r'\1', w))
            else:
                result.append(w)
        except:
            result.append(w)

    return ' '.join(result)


def remove_white_spaces(line):
    return " ".join(line.split())


def remove_accents(raw_text):
    """Removes common accent characters.

    """

    raw_text = re.sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = re.sub(u"[èéêë]", 'e', raw_text)
    raw_text = re.sub(u"[ìíîï]", 'i', raw_text)
    raw_text = re.sub(u"[òóôõö]", 'o', raw_text)
    raw_text = re.sub(u"[ùúûü]", 'u', raw_text)
    raw_text = re.sub(u"[ýÿ]", 'y', raw_text)
    raw_text = re.sub(u"[ß]", 'ss', raw_text)
    raw_text = re.sub(u"[ñ]", 'n', raw_text)
    return raw_text


def clean_text(text, witespace=True, punctuation=True, duplicated=True, alt=True, accent=True, others=None):

    arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    english_punctuations = string.punctuation
    arabic = False

    for x in text.split(' '):
        if is_arabic(x):
            arabic = True
            break

    if punctuation:

        if arabic:
            punctuations_list = arabic_punctuations + english_punctuations
        else:
            punctuations_list = english_punctuations

        translator = str.maketrans('', '', punctuations_list)
        text = text.translate(translator)

    if arabic:
        arabic_diacritics = re.compile("""
                                    ّ    | # Tashdid
                                    َ    | # Fatha
                                    ً    | # Tanwin Fath
                                    ُ    | # Damma
                                    ٌ    | # Tanwin Damm
                                    ِ    | # Kasra
                                    ٍ    | # Tanwin Kasr
                                    ْ    | # Sukun
                                    ـ     # Tatwil/Kashida

                                """, re.VERBOSE)

        text = re.sub(arabic_diacritics, '', text)

    if witespace:
        text = remove_white_spaces(text)
    if duplicated:
        text = remove_duplicated_letter(text)

    if accent:
        text = remove_accents(text)

    if alt:
        text = text.replace('@', '')

    if others is not None:
        other = re.compile(others, re.VERBOSE)
        text = re.sub(other, '', text)

    return text
