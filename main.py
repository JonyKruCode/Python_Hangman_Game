import re # модуль для работы с регулярными выражениями
import random # модуль для генерации случайного числа
from distutils.command.clean import clean

# количество попыток
attempt_counter = 0
# список названных букв
voiced_letters = []
# загаданное слово в виде списка символов
hidden_word_array = []
# маска загаданного слова, вначале состоит из звездочек
# и по мере угадывания звездочки заменяются на буквы
mask_hidden_word_array = []

# функция рисует виселицу в консоли
def draw_hangman(how_many_attempt):
    match how_many_attempt:
            case 6:
                picture_of_symbols = """
_________
| /     |
|/      |
|       |
|       O
|      V|V
|       П
|
|__________                            
                            """
                print(picture_of_symbols)
            case 5:
                picture_of_symbols = """
_________
| /     |
|/      |
|       |
|
|
|
|
|__________
                        """
                print(picture_of_symbols)
            case 4:
                picture_of_symbols = """
_________
| /
|/
|
|
|
|
|
|__________
                        """
                print(picture_of_symbols)
            case 3:
                picture_of_symbols = """
| /
|/
|
|
|
|
|
|__________
                        """
                print(picture_of_symbols)
            case 2:
                picture_of_symbols = """
|
|
|
|
|
|
|
|__________
                        """
                print(picture_of_symbols)
            case 1:
                picture_of_symbols = """
|__________
                        """
                print(picture_of_symbols)

# обработка выбора Играть или Выйти (return: True/False) плюс валидация ввода
def play_or_quit():
    answer = input("Поиграем в виселицу? (1 - поиграем, 2 - нет \n")

    # валидация ввода (да/нет)
    while not re.match(r"^(1|2)$", answer):
        answer = input("введи только 1 или 2 \n")

    if answer == "1":
        print("""
Отлично! я загадаю слово,
а ты должен называть буквы и отгадать его,
можешь ошибиться 5 раз,
а на шестой я тебя повешу)))
                """)
        # обнуляем счетчик
        global attempt_counter
        attempt_counter = 0
        draw_hangman(6)  # покажем полный рисунок мельницы
        return True
    elif answer == "2":
        print("Жаль, мне так хотелось тебя вздернуть)))")
        draw_hangman(6) # покажем полный рисунок мельницы
        print("еще увидимся)))")
        return False

# функция загадывания слова (return: загаданное слово)
def make_a_word():
    # открываем файл на чтение
    with open("word.txt") as file_word:
        # считываем все строки в список
        words = file_word.readlines()
        # удаляем символы переноса строки
        words = [word.strip() for word in words]
        # возвращаем произвольный элемент списка
        return words[random.randint(0, len(words) - 1)]

# проверить введенную букву на валидность (return: True/False)
def check_the_letter_for_validity(letter):
    return bool(re.match(r"^[а-яё]$", letter))

# проверяем называлась ли буква (return: True/False)
def check_letter_was_called(letter):
    i = 0
    while i < len(voiced_letters):
        if voiced_letters[i] == letter:
            return True
        i += 1
    return False

# сохраняем букву в список названых букв, если буква не называлась,
# то сохраняем (return: True (сохранилась) /False (не сохранилась)
def save_letter(letter):
    if check_letter_was_called(letter):
        return False
    else:
        voiced_letters.append(letter)
        return True

# проверяем правильная ли буква, если правильная то записываем ее в маску (return: True(правильная и записали)/False)
def checking_the_entered_letter_in_word(single_char):
    letter_exists = False
    for i, char in enumerate(hidden_word_array):
        if char == single_char:
            # записываем правильную букву в маску
            write_the_letter_in_the_mask(i, single_char)
            letter_exists = True
    return letter_exists

# записываем правильную букву в маску нашего слова
# ничего не возвращаем, только записываем букву в маску
def write_the_letter_in_the_mask(position_letter, letter):
        global mask_hidden_word_array
        mask_hidden_word_array[position_letter] = letter

# считываем введенный юзером символ и вызовем метод проверки его корректности
# (return: введенный юзером символ (если он буква)
def read_the_entered_letter():
    print(f"у тебя осталось {6 - attempt_counter} попыток \n", )

    # если какие-то буквы уже назывались, то покажем их
    if voiced_letters:
        print(f'ты называл следующие буквы: \n {" ".join(voiced_letters)}')

    letter = input("введи букву \n")
    # проверка ввода на валидность (кириллица, одиночная)
    while not check_the_letter_for_validity(letter):
        letter = input("введи одну прописную букву на кириллице \n")
    return letter

# проверка победы
def check_win():
    i = 0
    win = True
    while i < len(mask_hidden_word_array):
        if mask_hidden_word_array[i] == '*':
            win = False
        i += 1
    return win

# проверка проигрыша
def check_game_over():
    global attempt_counter
    if attempt_counter == 6:
        return True
    return False

def main():
    while play_or_quit():
        # очищаем список названых букв и загаданное слово
        global voiced_letters
        voiced_letters.clear()
        global hidden_word_array
        hidden_word_array.clear()

        # преобразуем загаданное слово в список символов
        hidden_word_array = list(make_a_word())

        # создаем маску загаданного слова
        global mask_hidden_word_array
        mask_hidden_word_array = hidden_word_array.copy()
        # и заменяем все буквы на *
        i = 0
        while i < len(mask_hidden_word_array):
            mask_hidden_word_array[i] = '*'
            i += 1

        print("перед тобой загаданное слово")
        # выводим буквы с пробелами между ними
        print(" ".join(mask_hidden_word_array))

        # основной цикл работы программы
        global attempt_counter
        while attempt_counter < 6:
            while not save_letter(read_the_entered_letter()):
                print("Ты уже вводил эту букву")

            # берем последнюю названную юзером букву
            last_letter = voiced_letters[-1]

            # и проверяем есть ли она в слове
            if checking_the_entered_letter_in_word(last_letter):
                print("ты молодец - угадал")
            else:
                print("ты ошибся - нет такой буквы")

                attempt_counter += 1 # уменьшаем счетчик попыток в случае ошибки
                if check_game_over(): # проверяем на проигрыш
                    print("Ты проиграл и будешь повешен!")

                draw_hangman(attempt_counter)

            print(" ".join(mask_hidden_word_array))

            # проверка на выигрыш
            if check_win():
                print("Поздравляю, ты выиграл!")
                break

main()