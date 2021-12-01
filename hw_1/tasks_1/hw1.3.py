"""Определить, какие из слов «attribute», «класс», «функция»,
«type» невозможно записать в байтовом типе."""

words = ['attribute', 'класс', 'функция', 'type']


def may_in_bytes(list_of_words) -> None:
    """ф-ция определяет и выводит слова, которые
    нельзя представить в виде байтового литерала
    """
    if not isinstance(list_of_words, list):
        list_of_words = (list_of_words, )
    for word in list_of_words:
        try:
            eval(f"b'{word}'")
        except SyntaxError:
            print(f'Слово «{word}» - невозможно записать в байтовом типе')
        # else:
        #     print(f'Слово «{word}» в байтовом типе')


may_in_bytes(words)
may_in_bytes('attribute')



