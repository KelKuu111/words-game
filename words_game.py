import json
import os


# Путь к файлу сохранения
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Настройки, режим проверки словаря
dictionary = ['on']
# Счётчик сколько игрок пропустил слов [1 игрок, 2 игрок]
passing = [0, 0]


# Если файла не существует - создаем
def no_file():
    os.system('cls')
    temp = {'words': ['арбуз'], 'turn': 1}
    save(temp)
    main_game()


# Распределение хода игрока, начало игры, выход в меню
def main_game():
    while True:
        with open('words.json', 'r+', encoding='utf-8') as f:
            words = json.load(f)

            if words['turn'] == 1:
                result = player_1(words)
            elif words['turn'] == 2:
                result = player_2(words)

        if result == 'menu':
            break
        if result in [1, 2]:
            os.system('cls')
            print(f'~-~Игрок {result} проиграл!~-~')
            with open('words.json', 'r+', encoding='utf-8') as f:
                words = json.load(f)
            print(f' Всего введено слов: {len(words['words'])}')
            input('Enter для продолжения...')
            break
        
        save(result)


# Проверка последней буквы
def last_letter(all_words):
    last_word = all_words['words'][-1].lower()

    if last_word[-1] in 'ьъы':
        letter = last_word[-2]
    else:
        letter = last_word[-1]
    return [f'{last_word}, слово на букву: {letter}', letter]


# Сохранение
def save(all_words):
    with open('words.json', 'w+', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=4)
    

# Проверка и ввод слова
def checking_word(all_words, letter, player_num):
    
    while True:
        print(f'~----- Ход игрока: {player_num} ----~')
        print('--[ "exit" Чтобы выйти ]--')
        print('["pass" Если нет вариантов]')
        print(last_letter(all_words)[0])

        word = input().lower()

        if word == 'pass':
            passing[player_num - 1] += 1
            if 3 in passing:
                save(all_words)
                passing[0] = passing[1] = 0
                return player_num   # Возвращает номер проигравшего игрока
            else:
                break

        if word == '':
            os.system('cls')
            print('Введите слово!')
            continue

        if word.lower() == 'exit':
            save(all_words)
            return 'menu'

        if not exist(word):
            os.system('cls')
            print(f'"{word}" Не существует!')
            continue

        if word in all_words['words']:
            os.system('cls')
            print(f'"{word}" Уже было использовано!')
            continue

        if word[0] != letter:
            os.system('cls')
            print(f'"{word}" Не подходит!')
            continue

        if len(word) == 1:
            os.system('cls')
            print(f'"{word}" Состоит лишь из одной буквы!')
            continue

        break
    if word != 'pass':
        all_words['words'].append(word)
    all_words['turn'] = 2 if all_words['turn'] == 1 else 1
    os.system('cls')
    return all_words


# Ход игрока 1
def player_1(all_words):
    letter = last_letter(all_words)[1]
    return checking_word(all_words, letter, 1)


# Ход игрока 2
def player_2(all_words):
    letter = last_letter(all_words)[1]
    return checking_word(all_words, letter, 2)


# Проверка существует ли слово
def exist(word):
    return word in words_set if dictionary[0] == 'on' else True


# Старт программы
def start():
    os.system('cls')
    if os.path.exists('words.json'):
        main_game()
    else:
        no_file()


# Главное меню
def main_menu():
    while True:
        os.system('cls')
        print('[    ~-~{ Words Game }~-~      ]')
        print('[      1 - Продолжить          ]')
        print('[      2 - Новая игра          ]')
        print(f'    Проверка по словарю: {dictionary[0]}')
        print('[("off/on" - вкл/выкл проверку)]')
        print('[ ~-~{ "exit" Чтобы выйти }~-~ ]\n')

        choice = input().lower()

        if choice == '1':
            start()
        elif choice == '2':
            no_file()
        elif choice in ['on', 'off']:
            dictionary[0] = choice
        elif choice == 'exit':
            exit()


# Читаем словарь
with open('russian.txt', 'r', encoding='utf-8') as f:
    words_set = set(line.strip().lower() for line in f)

main_menu()
