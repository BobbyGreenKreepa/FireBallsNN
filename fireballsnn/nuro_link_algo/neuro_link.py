from navec import Navec
from razdel import sentenize, tokenize
from slovnet import Morph

# окончания прилагательных и сокращенных прилагательных
adj_propn = {
    "вой": "вым",
    "ной": "ным",
    "кой": "ким",
    "ый": "ым",
    "ий": "им",
    "ая": "ой",
    "яя": "ей",
    "ое": "ым",
    "ее": "им",
    "-й": "-м",
    "-я": "-й",
    "-е": "-м",
}

# все окончания обрабатываемых частей речи
nominative_to_instrumental = {
    "ADJ": adj_propn,
    "PROPN": adj_propn,
    "NOUN": {
        "ья": "ьёй",
        "да": "дой",
        "она": "оном",
        "ок": "ком",
        "ие": "ием",
        "ись": "исью",
        "ия": "ией",
        "уд": "удом",
    },
}


def solveStr(name: str):
    text = name

    # разбить на токены
    chunk = []
    for sent in sentenize(name):
        tokens = [_.text for _ in tokenize(sent.text)]
        chunk.append(tokens)

    # морфологический анализ
    markup = next(morph_ds.map([list(map(str.lower, chunk[0]))]))

    first_piece = []
    last_piece = markup.tokens.copy()

    # разделение на две смысловые части
    for token in last_piece.copy():
        first_piece.append(last_piece.pop(0))
        if token.pos == "NOUN":
            break

    # склонение из именительного падежа в творительный (прилагательных, существительных и сокращений)
    for i, token in enumerate(first_piece):
        if token.pos in [
            "ADJ",
            "NOUN",
            "PROPN",
        ]:
            suffixes = nominative_to_instrumental[token.pos].keys()

            # перебор по суффиксам (можно еще сделать по хеш-таблице, но тут маленький словать, поэтому можно не выпендриваться)
            for suffix in suffixes:
                # получаем длину для слайсинга (длина отрицательная для слайсинга)
                suffix_len = -len(suffix)

                # получаем суффикс, для сравнивания
                token_suffix = token.text[suffix_len:]
                if token_suffix == suffix:
                    # склоненный токен
                    result = (
                            token.text[:suffix_len]
                            + nominative_to_instrumental[token.pos][suffix]
                    )

                    # если капсом
                    if chunk[0][i].isupper():
                        text = text.replace(token.text.upper(), result.upper())
                    # если sentense case
                    elif chunk[0][i][:1].isupper():
                        text = text.replace(
                            token.text.capitalize(), result.capitalize()
                        )
                    # если маленькими
                    elif chunk[0][i].islower():
                        text = text.replace(token.text.lower(), result.lower())
                    break

            # # если нулевое окончание (для слова "СУД", например)
            # if token.pos == "NOUN":
            #     result = token.text + "ом"
            #     text = text.replace(
            #         token.text.upper() if text.isupper() else token.text,
            #         result.upper() if text.isupper() else result,
            #     )
        # если сокращенное числительное
        elif token.pos == "NUM" and token.text.endswith("-й"):
            text = text.replace(
                "-Й" if chunk[0][i].isupper() else "-й",
                "-М" if chunk[0][i].isupper() else "-м",
            )
    return text


# данные для анализатора
navec_ds = Navec.load("nuro_link_algo/navec_news_v1_1B_250K_300d_100q.tar")
morph_ds = Morph.load("nuro_link_algo/slovnet_morph_news_v1.tar", batch_size=4)
morph_ds.navec(navec_ds)
