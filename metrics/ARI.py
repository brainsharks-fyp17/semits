import re
from string import digits

sinhala_start = 0xd80
cons_start = 0xd9a
cons_end = 0xdc6
sinhala_end = 0xdf5


def remove_digits(sent):
    trans = str.maketrans('', '', digits)
    return sent.translate(trans)


def is_sinhala_letter(letter):
    unicode_val = ord(letter)
    if sinhala_start <= unicode_val <= sinhala_end:
        return True


def is_sinhala_word(word):
    letter_count = 0
    for letter in word:
        if is_sinhala_letter(letter):
            letter_count += 1
            if letter_count >= 1:
                return True
    return False


def ari_stats(sentence):
    n_sentences = 1
    n_words = 0
    n_chars = 0
    words = sentence.split()
    for word in words:
        if is_sinhala_word(word):
            n_words += 1
            n_chars += len(word)
    return n_chars, n_words, n_sentences


def ari_score(sentence):
    a = 4.71
    b = 0.5
    c = -21.43
    sentence = re.sub("[\(\[{]+[^\(\)\[\]{}]*[\)\]}]+", "", sentence)
    sentence = remove_digits(sentence)
    n_chars, n_words, n_sentences = ari_stats(sentence)
    if n_words == 0:
        return 0
    ari = a * (n_chars / n_words) + b * (n_words / n_sentences) + c
    # ari = round(ari, 3)
    return ari


if __name__ == '__main__':
    sent1 = "ඈ පිළිබඳව ලියන්නේ නම් මා එය ලිවිය යුත්තේ දැනට ලියා ඇති හොඳම මවු ගුණ ගී අතලොස්ස හා යම් මට්ටමකටවත් සමීප " \
            "වීමට සමත් විය හැකි ලෙසටය "
    sent2 = "එකල ඇසූ ගුවන් විදුලි ගීයක් නැවත රසවින්දෙමි"
    print(ari_score(sent1))
    print(ari_score(sent2))
