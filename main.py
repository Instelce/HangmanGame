from random import choice
import json

from draw import hangman_animation
from get_word import api_used, get_random_word, get_random_word_def
from words import words_list


class Game():
    def __init__(self, menu_choice, game_mode, word_choice, life):
        """
            Constructor

            args:
                menu_choice (str): choice of user in the menu
                game_mode (str): Get the game mode
                word_choice (str)
                life (int)        
        """
        self.menu_choice = menu_choice
        self.game_mode = game_mode
        self.word_choice = word_choice
        self.word_cheat_list = words_list
        self.life = life

        self.wrong_letter = []
        self.player_word = []
        self.is_win = False
        self.good_letter = 0
        self.hangman_frames = 0
        self.game_index = 0

        self.accents = {
            'a': ['a', 'à', 'â', 'ä'],
            'e': ['e', 'é', 'è', 'ê', 'ë'],
            'i': ['i', 'ì', 'î', 'ï'],
            'o': ['o', 'ò', 'ô', 'ö'],
            'u': ['u', 'ù', 'û', 'ü'],
        }

    def create_player_word(self):
        # Set the letter of player word to underscore
        if self.menu_choice == '3':
            for letter in range(self.random_lenght_word):
                self.player_word.append('_')
        else:
            for letter in self.word_choice:
                self.player_word.append('_')

    def update_data(self):
        file_data = 'data.json'

        with open(file_data, "r") as file:
            data = json.load(file)

        # Set game index
        if len(data) == 0:
            self.game_index = 0
        else:
            # Get the last game index
            self.game_index = data[f'game_{str(len(data) - 1)}'][0]['index'] + 1

        data[f'game_{self.game_index}'] = []
        data[f'game_{self.game_index}'].append({
            'game_mode': self.game_mode,
            'index': self.game_index,
            'word_choice': self.word_choice,
            'wrong_letter': self.wrong_letter,
            'remaining_life': self.life,
            'is_win': self.is_win,
        })

        with open(file_data, 'w') as outfile:
            json.dump(data, outfile)

    def display_data(self):
        separator()
        if self.hangman_frames == 0:
            pass
        else:
            for frame in hangman_animation[self.hangman_frames]:
                print(frame)
        print(f"\n❤ Life : {self.life}")
        print(f"✔ {self.good_letter} good letter : {' '.join(self.player_word)}")
        print(f"❌ Wrong letter : {', '.join(self.wrong_letter)}")
        separator()

    def run(self):
        self.word_cheat_list = words_list

        if self.menu_choice == '3':
            self.word_is_choice = False
            self.random_lenght_word = len(choice(self.word_cheat_list))

            word_cheat_list_temp = []

            # Retrieves all words with a length equal to random_lenght_word
            for word in self.word_cheat_list:
                if not len(word) != self.random_lenght_word:
                    word_cheat_list_temp.append(word)
            self.word_cheat_list = word_cheat_list_temp

        else:
            self.word_is_choice = True

        self.create_player_word()

        for i in range(50):
            print()

        separator()

        if self.menu_choice == '3':
            print(f"The mystery word as {self.random_lenght_word} letters. \n")
        else:
            print(f"The mystery word as {len(self.word_choice)} letters. \n")

        while self.life > 0:
            self.good_letter = 0

            player_letter = input(base(self.menu_choice, "Give a letter"))

            if self.menu_choice == '3' and not self.word_is_choice:
                word_cheat_list_temp = []
                for word in self.word_cheat_list:
                    if not player_letter in word:
                        word_cheat_list_temp.append(word)
                self.word_cheat_list = word_cheat_list_temp

                if len(self.word_cheat_list) <= 3:
                    word_choice_no_split = choice(self.word_cheat_list)
                    self.word_choice.clear()

                    for letter in word_choice_no_split:
                        self.word_choice.append(letter)

                    self.word_is_choice = True

            if self.word_is_choice:
                for index, letter in enumerate(self.word_choice):
                    # Check if the player letter is in the random word
                    if self.word_choice[index] == player_letter:
                        self.player_word[index] = player_letter

                    # Check accents
                    if player_letter in self.accents:
                        for accent in self.accents[player_letter]:
                            if accent == letter:
                                self.player_word[index] = accent

                    # Check if the player word it the same as the random word
                    if self.player_word[index] == letter:
                        self.good_letter += 1

            # Check if the player letter is not in the choice word
            if not player_letter in self.word_choice and not player_letter in self.wrong_letter:
                self.hangman_frames += 1
                self.life -= 1
                self.wrong_letter.append(player_letter)

            self.display_data()

            # Check win
            if self.good_letter == len(self.word_choice):
                self.is_win = True
                print(
                    f"Victory, you have found the word {''.join(self.word_choice)}.")

                if self.menu_choice == '1' and api_used:
                    print(
                        f"\nDefinition de {''.join(self.word_choice)}:\n{get_random_word_def(''.join(self.word_choice))}")
                separator()
                break

            # Check death
            if self.life <= 0:
                print(
                    f"Oh no, you lost, the word was {''.join(self.word_choice)}.")

                if self.menu_choice == '1' and api_used:
                    print(
                        f"\nDefinition de {''.join(self.word_choice)}:\n{get_random_word_def(''.join(self.word_choice))}")
                separator()
                break

        self.update_data()
        self.game_index += 1


def base(menu_choice='', info=''):
    return f'{info} [{menu_choice}]>> '


def split_word(word):
    word_split = []
    for letter in word:
        word_split.append(letter)
    return word_split


def separator(character="=", lenght=50):
    print()
    for letter in range(lenght):
        print(character, end='')
    print('\n')


def get_stats():
    with open('data.json', 'r') as file:
        data = json.load(file)

    separator()
    print("Your statistic\n"
          f"{len(data)} game played")
    separator()

    # Fetch data
    for row in data:
        for game in data[row]:
            if game['is_win']:
                print(f"Game n°{game['index'] + 1}, is win")
            else:
                print(f"Game n°{game['index'] + 1}, is lose")
            print(f"Game mode : {game['game_mode']}")
            print(f"Choice word : {''.join(game['word_choice'])}")
            print(f"Wrong letter : {', '.join(game['wrong_letter'])}")
            print(f"Remaining life : {game['remaining_life']}")
            separator()


def clear_stats():
    with open('data.json', 'w') as file:
        json.dump({}, file)
    separator()
    print("Stats data have been suppressed.")
    separator()


print("Welcome to hangman game\n")

# Game loop
while True:
    # Reset life
    life = 10

    # Set the menu
    print("Hangman Game Menu\n"
          "[1] Versus the computer\n"
          "[2] Player versus player\n"
          "[3] Cheat computer\n"
          "[S] Your stat\n"
          "[C] Clear stat\n"
          "[E] Exit the game")
    menu_choice = input(base('', "Choose a choice"))

    # Player versus computer
    if menu_choice == '1':
        game_mode = 'Player versus computer'

        if api_used:
            random_word = split_word(get_random_word())
        else:
            random_word = split_word(choice(words_list))

        player_vs_computer = Game(
            menu_choice, game_mode, random_word, life)
        player_vs_computer.run()
    # Player versus player
    elif menu_choice == '2':
        game_mode = 'Player versus player'

        player_choice_word = split_word(input(
            base(menu_choice, "\nChoose a word for your friend")))

        player_vs_player = Game(
            menu_choice, game_mode, player_choice_word, life)
        player_vs_player.run()
    # Player versus cheat computer
    elif menu_choice == '3':
        game_mode = 'Player versus cheat computer'

        player_vs_cheat_computer = Game(
            menu_choice, game_mode, words_list, life)
        player_vs_cheat_computer.run()
    # Display stats
    elif menu_choice == 'S':
        get_stats()
    # Clear stats
    elif menu_choice == 'C':
        clear_stats()
    # Exit
    elif menu_choice == 'E':
        break
