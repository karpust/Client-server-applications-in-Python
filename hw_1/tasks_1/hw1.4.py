"""Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить обратное
преобразование (используя методы encode и decode)."""

words = ['разработка', 'администрирование',
         'protocol', 'standard']


def en_de_code(list_of_words: list) -> None:
    """функция преобразовывает слова из строкового
    представления в байтовое и обратно
    """
    for word in list_of_words:
        print(f'\n--------------------- Слово «{word}» ---------------------')
        byte_word = word.encode('utf-8')
        print(f'В байтовом представлении: {byte_word}')
        string_word = bytes.decode(byte_word, encoding='utf-8')
        print(f'В строковом представлении: {string_word}')


en_de_code(words)
