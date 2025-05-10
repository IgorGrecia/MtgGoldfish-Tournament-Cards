import os
import utils
import csv
import json
import timeit
import re

def fix_name(s):
	if ',' in s:
		return f"\"{s}\""
	return s

def matches_format(s, mtg):
	# Define patterns for League and Challenge
	pattern_league = [
		rf"{mtg} league 20\d{{2}}-\d{{2}}-\d{{2}}",  # Escaping curly braces for regex
	]

	pattern_challenge = [
		rf"{mtg} challenge \d+ 20\d{{2}}-\d{{2}}-\d{{2}}"
	]

	# Check for League match
	if any(re.fullmatch(pattern, s, flags=re.IGNORECASE) for pattern in pattern_league):
		return "League"
	
	# Check for Challenge match
	if any(re.fullmatch(pattern, s, flags=re.IGNORECASE) for pattern in pattern_challenge):
		return "Challenge"

	# Return blank if no match
	return "Other"

def get_types(types):

	type_list = types.split(" // ")[0]
	type_line = ""
	if "Artifact" in type_list:
		type_line += " Artifact"
	if "Creature" in type_list:
		type_line += " Creature"
	if "Enchantment" in type_list:
		type_line += " Enchantment"
	if "Land" in type_list:
		type_line += " Land"
	if "Instant" in type_list:
		type_line += " Instant"
	if "Sorcery" in type_list:
		type_line += " Sorcery"
	if "Planeswalker" in type_list:
		type_line += " Planeswalker"
	if "Battle" in type_list:
		type_line += " Battle"
	if "Kindred" in type_list:
		type_line += " Kindred"

	return type_line.strip()

new_decks = {}
new_decks["pauper"] = 0
new_decks["modern"] = 0
new_decks["legacy"] = 0
new_decks["pioneer"] = 0
new_decks["standard"] = 0
new_decks["vintage"] = 0
new_decks["total"] = 0

custom_order = 'WUBRG'
order_map = {char: index for index, char in enumerate(custom_order)}

filetypes = ".csv"
delimiter = ','

dfcs = {}
with open(f"LookerStudioData\\CardData{filetypes}", mode="r", newline="", encoding="utf-8") as file:
	csv_reader = csv.reader(file, delimiter=delimiter)
	for row in csv_reader:
		dfcs[row[0]] = [row[1], row[2], row[3]]

dfcs["Lorien Revealed"] = ["Sorcery", 5, "U"]
dfcs["Troll of Khazad-dum"] = ["Creature", 6, "B"]
dfcs["Palantir of Orthanc"] = ["Artifact", 3, "C"]
dfcs["Jotun Grunt"] = ["Creature", 2, "W"]
dfcs["Bartolome del Presidio"] = ["Creature", 2, "WB"]
dfcs["Lim-Dul's Vault"] = ["Instant", 2, "UB"]
dfcs["Negan, the Cold-Blooded"] = ["Creature", 5, "WBR"]

# csv_starter = []
csv_text = []
new_deck_codes = []
csv_tournaments = []
csv_tournaments.append(["Tournament_Code", "Tournament_Name", "Format", "LorC", "Tournament_Link", "Date"])
csv_decks = []
csv_decks.append(["Code", "Deck_Name", "Player", "Deck_Link", "Tournament_Code"])

# with open(f"LookerStudioData\\DecksDataNew{filetypes}", mode="w", newline="", encoding="utf-8") as file:
	# csv_starter.append(["Count", "CardName", "MBorSB", "Code"])
	# writer = csv.writer(file, delimiter=delimiter, lineterminator="\n")
	# writer.writerows(csv_starter)

with open('Oracle_Cards.json', 'r', encoding='utf-8') as file:
	oracle = json.load(file)  # Load JSON data

formats = utils.get_formats()

start_all = timeit.default_timer()
for mtg in formats:
	start = timeit.default_timer()
	if not (os.path.exists(mtg) and os.path.isdir(mtg)):
		continue
	print(f"Excelifying {mtg.title()} Tournaments")
	
	deck_codes = []
	with open(f"LookerStudioData\\DeckCodes.txt", "r", encoding='utf8') as file:
		for line in file:
			deck_codes.append(line.replace("\n", ""))

	tournament_dict = {}
	tournaments = utils.get_txt(mtg, "Tournaments")

	for item in tournaments:
		tournament_code = item[0][-5:]
		tournament_name = item[1]
		tournament_date = item[2]
		tournament_dict[tournament_code] = [tournament_date, tournament_name]
		leagorchall = matches_format(tournament_name, mtg)

		csv_tournaments.append([tournament_code, fix_name(tournament_name), mtg, leagorchall, item[0], tournament_date])

	decks = utils.get_txt(mtg, "Decks")
	counter = 0

	for item in decks:
		deck_name = item[0]
		deck_code = item[2][-7:]
		deck_link = item[2]
		deck_tournament = item[3]
		deck_user = item[4]
		deck_tournament_code = item[5]
		deck_date = tournament_dict[deck_tournament_code][0]
		
		# csv_decks.append([deck_code, deck_name, deck_type, deck_user, deck_link])
		csv_decks.append([deck_code, fix_name(deck_name), fix_name(deck_user), deck_link, deck_tournament_code])

		if deck_code in deck_codes:
			continue
		else:
			new_deck_codes.append(deck_code)
			counter+=1
			new_decks[mtg] += 1
			# if counter > 200:
				# continue
			if counter % 500 == 0:
				print(f"Deck #{counter} - {item[2][-7:]}")

		with open(f"{mtg}\\Decklists\\{deck_code}.txt", "r", encoding='utf8') as file:
			mainorside = 'Main'
			for line in file:
				if line[0] != '0':
					line = line.replace("\n", "")
					if line.lower() == 'sideboard':
						mainorside = 'Side'
					else:
						count, card_name = line.split(" ", 1)
						card_name = card_name.replace("&&", "//")
						
						colors = ""
						type_line = ''
						manavalue = 0

						if card_name in dfcs:
							type_line = dfcs[card_name][0]
							manavalue = dfcs[card_name][1]
							colors = dfcs[card_name][2]
						else:
							for card in oracle:
								if card['name'] == card_name and 'Token' not in card['type_line'] and card['layout'] != 'art_series':
									manavalue = int(card['cmc'])

									type_line = get_types(card['type_line'])

									for color in card['colors']:
										colors += color
									break  # Stop searching after finding the first match
							else:
								for card in oracle:
									if card_name in card['name'] and 'Token' not in card['type_line'] and card['layout'] != 'art_series':

										if "colors" in card:
											for color in card['colors']:
												colors += color
										if "type_line" in card:
											type_line = get_types(card['type_line'])
										if "cmc" in card:
											manavalue = int(card['cmc'])

										if "card_faces" in card:
											if "colors" in card['card_faces'][0]:
												for color in card['card_faces'][0]['colors']:
													colors += color
											if "type_line" in card['card_faces'][0]:
												type_line = get_types(card['card_faces'][0]['type_line'])
											if "cmc" in card['card_faces'][0]:
												manavalue = int(card['card_faces'][0]['cmc'])
										break  # Stop searching after finding the first match

							if colors == '':
								colors = 'C'

							colors = ''.join(sorted(colors, key=lambda x: order_map.get(x, float('inf'))))
							dfcs[card_name] = [type_line, manavalue, colors]

						csv_text.append([count, fix_name(card_name), mainorside, deck_code])
	
	stop = timeit.default_timer()
	print('Time: ', stop - start)
	print(f"{mtg} - {new_decks[mtg]} New Decks Registered\n")
	new_decks["total"] += new_decks[mtg]

with open(f"LookerStudioData\\DecksData{filetypes}", mode="a", newline="\n", encoding="utf-8") as file:
	writer = csv.writer(file, delimiter=delimiter, lineterminator="\n")
	writer.writerows(csv_text)

# with open(f"LookerStudioData\\DecksDataNew{filetypes}", mode="a", newline="", encoding="utf-8") as file:
	# writer = csv.writer(file, delimiter=delimiter, lineterminator="\n")
	# writer.writerows(csv_text)

with open(f"LookerStudioData\\ListData{filetypes}", mode="w", newline="", encoding="utf-8") as file:
	writer = csv.writer(file, delimiter=delimiter, lineterminator="\n")
	writer.writerows(csv_decks)

with open(f"LookerStudioData\\TournamentsData{filetypes}", mode="w", newline="", encoding="utf-8") as file:
	writer = csv.writer(file, delimiter=delimiter, lineterminator="\n")
	writer.writerows(csv_tournaments)

with open(f"LookerStudioData\\DeckCodes.txt", "a", encoding='utf8') as file:
	for line in new_deck_codes:
		file.write(str(line) + "\n")

with open(f"LookerStudioData\\CardData{filetypes}", mode="w", newline="", encoding="utf-8") as file:
	writer = csv.writer(file, delimiter=delimiter, lineterminator="\n")
	card_data = []
	for key, value in dfcs.items():
		card_data.append([fix_name(key), value[0], value[1], value[2]])
	writer.writerows(card_data)

for mtg in formats:
	print(f"{mtg.title()} - {new_decks[mtg]} New Decks")

print(f"\n{new_decks['total']} Total New Decks\n")

stop_all = timeit.default_timer()
print('Time: ', stop_all - start_all)