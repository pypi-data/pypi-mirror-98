from random import randint

words = ['дебил', 'идиот', 'маразматик', 'педик', 'кретин', 'сука', 'тупица', 'дуболом', 'конченный', 'с дуба рухнул']


def WhoIAm(name='кто-то'):
    print(f'{name} молодчинка, а Денис Варлаков 11Г {words[randint(0, len(words) - 1)]}')