import time
import timeit
import os
import re
import ast
import urllib.request
from bs4 import BeautifulSoup
from collections import Counter

basics = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest', "Wastes", 'Snow-Covered Plains', 'Snow-Covered Island', 'Snow-Covered Swamp', 'Snow-Covered Mountain', 'Snow-Covered Forest', "Snow-Covered Wastes"]
baseurl = "https://www.mtggoldfish.com"

def find_duplicates(lst):
	seen = set()
	duplicates = set()
	for item in lst:
		if item in seen:
			duplicates.add(item)
		else:
			seen.add(item)
	return list(duplicates)

def write_card_list(folder, filename, cardlist, mtg):
	with open(f"{mtg}\\{folder}\\{filename}.txt", "w", encoding='utf-8') as file:
		for key, value in sorted(cardlist.items(), key=lambda item: item[1]):
			if key not in basics:
				file.write(f"{key}: {value}\n")

def league_or_challenge(filename, mtg):
	if f"{mtg} league 2024-" in filename.lower():
		return "league"
	if f"{mtg} challenge " in filename.lower():
		return "challenge"
	else:
		return ""

def get_formats():
	formats = ["pauper", "modern", "legacy", "pioneer", "standard", "vintage"]
	valid_formats = [mtg for mtg in formats if os.path.exists(mtg) and os.path.isdir(mtg)]
	return valid_formats

def get_mtg():
	mtg = input("Choose your format\n1 = Pauper\n2 = Modern\n3 = Legacy\n4 = Pioneer\n5 = Standard\n6 = Vintage\n")

	if mtg not in ['legacy', 'modern', 'pauper', 'pioneer', '1', '2', '3', '4']:
		print("Wrong input\n")
		exit()

	if mtg == '1':
		mtg = 'pauper'
	if mtg == '2':
		mtg = 'modern'
	if mtg == '3':
		mtg = 'legacy'
	if mtg == '4':
		mtg = 'pioneer'
	if mtg == '5':
		mtg = 'standard'
	if mtg == '6':
		mtg = 'vintage'

	return mtg

def list_files(folder):
	return os.listdir(f"{folder}")

def get_card(line):
	match = re.match(r'(\d+)\s+(.*)', line)
	if match:
		return int(match.group(1)), match.group(2)
	return None, line

def sanitize_name(name):
	# Define a regular expression pattern for invalid characters
	invalid_chars = r'[\',<>:"/\\|?*°ºª\tŁ]'
	# Replace invalid characters with an underscore
	sanitized = re.sub(invalid_chars, '_', name)
	sanitized = sanitized.replace("\'", "_")
	return sanitized.strip()

def sanitize_name_testing(name):
	# Define a regular expression pattern for invalid characters
	invalid_chars = []
	invalid_chars.append("\'")
	invalid_chars.append('<')
	invalid_chars.append('>')
	invalid_chars.append(':')
	invalid_chars.append("\"")
	invalid_chars.append('/')
	invalid_chars.append('\\')
	invalid_chars.append('|')
	invalid_chars.append('?')
	invalid_chars.append('*')
	invalid_chars.append('°')
	invalid_chars.append('º')
	invalid_chars.append('ª')
	invalid_chars.append('\t')
	invalid_chars.append('Ł')
	# Replace invalid characters with an underscore
	for letter in invalid_chars:
		name = name.replace(letter, "_")
	return sanitized.strip()

def get_txt(mtg, file, mult=0):
	arr = []
	with open(f"{mtg}\\{file}.txt", "r", encoding="utf-8") as f:
		for line in f:
			if mult == 0:
				array = ast.literal_eval(line)
				arr.append(array)
			else:
				arr.append(line.replace("\n", ""))
	return arr

def get_date(deck):
	deck_info = deck.find('p', class_='deck-container-information')
	if deck_info is None:
		return None

	lines = deck_info.get_text(separator="\n").split("\n")
	deck_date = None
	for line in lines:
		if "Deck Date:" in line:
			deck_date = line.split("Deck Date:")[1].strip()
			break

	return deck_date

def get_date_tr(tournament):
	for tag in tournament.find_all('p'):
		for line in tag:
			if "Date: " in line:
				tournament_date = line.split("Date:")[1].strip()
				break
	return tournament_date

def get_content(url):
	# time.sleep(2)
	req = urllib.request.Request(
		url,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
		}
	)

	with urllib.request.urlopen(req) as response:
		html_content = response.read()

	html_content = html_content.decode('utf-8')
	soup = BeautifulSoup(html_content, 'html.parser')
	return soup

def tournament_check_pages(url, mtg, tournament):
	if url:
		next_page_link = url['href']
		full_next_page_link = f"https://www.mtggoldfish.com{next_page_link}"
		soup = get_content(full_next_page_link.strip())
		write_decks(soup, mtg, tournament)
		# url = soup.find("li", class_="next page-item")
		url = soup.find('a', class_='page-link', rel='next')
	return url

def write_decks(soup, mtg, tournament):
	decks = get_txt(mtg, "Decks")
	files = list_files(f"{mtg}\\Decklists")
	date = get_date_tr(soup)

	codes = []
	for deck in decks:
		codes.append(deck[2][-7:])

	links_followed_by_manacost = soup.select('a + span.manacost')
	for span in links_followed_by_manacost:
		a_tag = span.find_previous_sibling('a')
		deck_code = f"{a_tag['href'][6:]}"
		deck = f"{baseurl}{a_tag['href']}"

		for file in files:
			if deck_code in file:
				if deck_code not in codes:
					soup_deck = get_content(deck)
					deck_name = sanitize_name(a_tag.text.strip())
					deck_link = f"{baseurl}{a_tag['href']}"
					tournament_name = tournament[1]
					player = sanitize_name(soup_deck.find('span', class_='author').text[3:])
					tournament_code = tournament[0][-5:]

					deck_data = [deck_name, date, deck_link, tournament_name, player, tournament_code]

					with open(f"{mtg}\\Decks.txt", "a", encoding="utf-8") as file:
						file.write(str(deck_data) + "\n")

					print(deck_data)
				break
		else:
			soup_deck = get_content(deck)
			deck_name = sanitize_name(a_tag.text.strip())

			print(f"{tournament[1]} - {deck_name} - {deck_code}")
			
			deck_link = f"{baseurl}{a_tag['href']}"
			tournament_name = tournament[1]
			player = sanitize_name(soup_deck.find('span', class_='author').text[3:])
			tournament_code = tournament[0][-5:]


			deck_input = soup_deck.find('input', {'name': 'deck_input[deck]'})
			if deck_input is not None:
				decklist = deck_input.get('value')
				with open(f"{mtg}\\Decklists\\{deck_code}.txt", "w", encoding="utf-8") as f_list:
					f_list.write(decklist.strip())

				deck_data = [deck_name, date, deck_link, tournament_name, player, tournament_code]

				if deck_data not in decks:
					with open(f"{mtg}\\Decks.txt", "a", encoding="utf-8") as file:
						file.write(str(deck_data) + "\n")

def parse_archetype(file, folder, mtg):
	maindeck = Counter()
	sideboard = Counter()
	is_sideboard = False

	with open(f"{mtg}\\{folder}\\{file}", "r", encoding='utf8') as file:
		for line in file:
			line = line.strip()
			if line.lower() == "sideboard":
				is_sideboard = True
				continue
			if line:
				parts = line.split(" ", 1)
				if len(parts) == 2:
					quantity = int(parts[0])  # Parse the quantity
					card_name = parts[1].replace("Snow-Covered ", "")
					if is_sideboard:
						sideboard[card_name] += quantity
					else:
						maindeck[card_name] += quantity

	return maindeck, sideboard

def jaccard_similarity(counter1, counter2):
	intersection = sum((counter1 & counter2).values())  # Min of counts
	union = sum((counter1 | counter2).values())		 # Max of counts
	return intersection / union if union > 0 else 0

def compare_lists(deck, archetype, mtg):
	maindeck1, sideboard1 = parse_archetype(deck, "decklists", mtg)
	maindeck2, sideboard2 = parse_archetype(archetype, "archetypes", mtg)

	maindeck_similarity = jaccard_similarity(maindeck1, maindeck2)
	sideboard_similarity = jaccard_similarity(sideboard1, sideboard2)

	maindeck_weight = sum((maindeck1 | maindeck2).values())
	sideboard_weight = sum((sideboard1 | sideboard2).values())
	total_weight = maindeck_weight + sideboard_weight

	overall_similarity = (
		(maindeck_similarity * maindeck_weight + sideboard_similarity * sideboard_weight)
		/ total_weight
		if total_weight > 0
		else 0
	)
	return maindeck_similarity, overall_similarity

# def tournament_by_date(url, mtg, pg):
# 	if url:
# 		next_page_link = url.find("a")["href"]
# 		full_next_page_link = f"https://www.mtggoldfish.com{next_page_link}"
# 		soup = get_content(full_next_page_link.strip())
# 		write_tournaments(soup, mtg)
# 		url = soup.find("li", class_="next page-item")
# 	return url

def write_tournaments(soup, mtg):
	tournaments = get_txt(mtg, "Tournaments")

	tournament_data = []
	new_tournaments = []
	for row in soup.find_all("tr"):
		# Find tournament links within the row
		link_tag = row.find("a", href=True)
		date_tag = row.find("td")  # Find the date column (adjust class if necessary)
		if link_tag and "/tournament/" in link_tag["href"] and '(1)' not in link_tag.text:
			name = link_tag.text.strip()  # Tournament name
			link = f"https://www.mtggoldfish.com{link_tag['href']}"  # Full link
			date = date_tag.text.strip() if date_tag else "No date available"  # Extract the date
			tournament_data.append([link.strip(), name, date])

	# Print the tournament names and links
	count = 0
	for link, name, date in tournament_data:
		check = 0
		for item in tournaments:
			if link[-5:] in item[0][-5:]:
				# print("Found")
				check = 1
		if check == 0:
			print(f"{name} - {link} - {date}")
			new_tournaments.append([link, name, date])
			count += 1
			# print(f"Tournament Name: {name}")
			# print(f"Link: {link}")
			# print(f"Date: {date}")

	# for name, link, date in tournaments:
	# 	print(f"Tournament Name: {name}")
	# 	print(f"Link: {link}")
	# 	print(f"Date: {date}")


	with open(f"{mtg}\\Tournaments.txt", "a", encoding="utf-8") as file:
		for line in new_tournaments:
			file.write(str(line) + "\n")
	print(f"{count} New {mtg.title()} Tournaments")
	return count