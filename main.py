from random import choice
import keyboard
import json


def base(menu_choice=''):
	return f'[{menu_choice}]>> '


def separator():
	print("\n===========================================\n")


def game(menu_choice, random_word, life, game_index):
	wrong_letter = []
	player_word = []
	is_win = False
	
	# Set the letter of player word to underscore
	for letter in random_word:
		player_word.append('_')

	separator()
	print(f"The word has {len(random_word)} letters.")
	separator()

 
	while life > 0:
		# Player versus computer
		if menu_choice == '1':
			game_mode = 'Player versus computer'
			player_letter = input(base(menu_choice))

			good_letter = 0
			for index, letter in enumerate(random_word):

				# Check if the player letter is in the random word 
				if random_word[index] == player_letter:
					player_word[index] = player_letter

				# Check if the player word it the same as the random word
				if player_word[index] == letter:
					good_letter += 1

			if not(player_letter) in random_word:
				life -= 1
				wrong_letter.append(player_letter)

			# Check win
			if good_letter == len(random_word):
				is_win = True
				separator()
				print('Victory, you have found the word')
				separator()
				break

			separator()
			print(random_word)
			print(f"❤ Life : {life}")
			print(f"✔ {good_letter} good letter : {' '.join(player_word)}")
			print(f"❌ Wrong letter : {', '.join(wrong_letter)}")
			separator()

	if life <= 0:
		print(f"Oh no, you lost, the word was {''.join(random_word)}.")
		separator()

	# Stock data into json file
	with open('data.json', "r") as file:
		data = json.load(file)

	# Set game index
	if len(data) == 0:
		game_index = 0
	else:
		# Get the last game index 😤
		game_index = data[f'game_{str(len(data)-1)}'][0]['index'] + 1

	data[f'game_{game_index}'] = []
	data[f'game_{game_index}'].append({
			'game_mode': game_mode,
			'index': game_index,
			'random_word': random_word,
			'wrong_letter': wrong_letter,
			'remaining_life': life,
			'is_win': is_win,
		})

	with open('data.json', 'w') as outfile:
		json.dump(data, outfile)


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
				print(f"Game n°{game['index']+1}, is win")
			else:
				print(f"Game n°{game['index']+1}, is lose")
			print(f"Game mode : {game['game_mode']}")
			print(f"Random word : {''.join(game['random_word'])}")
			print(f"Wrong letter : {', '.join(game['wrong_letter'])}")
			print(f"Remaining life : {game['remaining_life']}")
			separator()


def clear_stats():
	with open('data.json', 'w') as file:
		json.dump({}, file)
	separator()
	print("Stats data have been suppressed.")
	separator()


word_list = ['mot', 'sucre', 'farine', 'pomme', 'poulet']
game_index = 0


# Game loop
while True:
	life = 11

	random_word = choice(word_list)
	random_word_split = []
	for letter in random_word:
		random_word_split.append(letter)

	# Set the menu
	print("Welcome to hangman game\n"
		"[1] Versus the computer\n"
		"[2] Player versus player\n"
		"[S] Your stat\n"
		"[C] Clear stat\n"
		"[E] Exit the game")
	menu_choice = input(base())

	if menu_choice == 'E':
		break
	elif menu_choice == 'S':
		get_stats()
	elif menu_choice == 'C':
		clear_stats()
	elif menu_choice == '1' or menu_choice == '2':
		game(menu_choice, random_word_split, life, game_index)
		game_index +=1
