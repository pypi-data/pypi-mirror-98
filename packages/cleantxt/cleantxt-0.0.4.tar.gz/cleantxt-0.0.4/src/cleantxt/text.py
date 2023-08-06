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


def remove_accents(line):
    """Removes common accent characters.

    """

    line = re.sub(u"[àáâãäå]", 'a', line)
    line = re.sub(u"[èéêë]", 'e', line)
    line = re.sub(u"[ìíîï]", 'i', line)
    line = re.sub(u"[òóôõö]", 'o', line)
    line = re.sub(u"[ùúûü]", 'u', line)
    line = re.sub(u"[ýÿ]", 'y', line)
    line = re.sub(u"[ß]", 'ss', line)
    line = re.sub(u"[ñ]", 'n', line)
    line = re.sub(u"[ç]", 'c', line)
    return line


def remove_non_alphanum(text):
    return " ".join(re.compile(r'\W+', re.UNICODE).split(text))


def clean_text(text, witespace=True, punctuation=True, duplicated=True, alphnum=True, accent=True, others=[('ə', 'a')]):

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

    if alphnum:
        text = remove_non_alphanum(text)

    if others is not None:
        for rule in others:
            text = text.replace(rule[0], rule[1])

    return text
