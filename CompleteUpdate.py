import timeit
import os
import time
import utils

formats = utils.get_formats()
run = []
run.append("pauper")
run.append("modern")
run.append("legacy")
run.append("pioneer")
run.append("standard")
run.append("vintage")

new_decks = {}
new_decks["pauper"] = 0
new_decks["modern"] = 0
new_decks["legacy"] = 0
new_decks["pioneer"] = 0
new_decks["standard"] = 0
new_decks["vintage"] = 0
new_decks["total"] = 0

get_tournaments = ""
# get_tournaments = input("Check New Tournaments?\n0 = No\n1 = Yes\n")
begin = timeit.default_timer()

# for mtg in formats:
# 	if mtg not in run or get_tournaments == '0':
# 		continue
# 	print(f"Updating {mtg.title()} Tournaments")
# 	start = timeit.default_timer()

# 	url = f"https://www.mtggoldfish.com/tournaments/{mtg}#paper"
# 	soup = utils.get_content(url)

# 	check = 0
# 	count = 0
# 	name = ""
# 	link = ""
# 	date = ""
# 	tournaments = utils.get_txt(mtg, "Tournaments")
# 	new_tournaments = []

# 	for tag in soup.find_all(True):
# 		if tag.name == "a":
# 			check = 1
# 			name = utils.sanitize_name(tag.text)
# 			attr = tag.attrs
# 		elif tag.name == "nobr" and check == 1:
# 			link = f"http://www.mtggoldfish.com{attr['href']}"
# 			soup_date = utils.get_content(link.strip())
# 			date = utils.get_date_tr(soup_date)
# 			tr = [link.strip(), name, date]
# 			if name.strip()[-3] == '(' and name.strip()[-1] == ')':
# 				continue
# 			if tr not in tournaments:
# 				new_tournaments.append(tr)
# 				count += 1
# 		else:
# 			check = 0
# 			name = ""
# 			link = ""
# 			date = ""

# 	with open(f"{mtg}\\Tournaments.txt", "a", encoding="utf-8") as file:
# 		for line in new_tournaments:
# 			file.write(str(line) + "\n")
# 	print(f"{count} New {mtg.title()} Tournaments")
# 	stop = timeit.default_timer()
# 	print('Time: ', stop - start)

for mtg in formats:
	if mtg not in run:
		continue
	start = timeit.default_timer()
	tournaments = utils.get_txt(mtg, "Tournaments")
	decks = utils.get_txt(mtg, "Decks")
	files = utils.list_files(f"{mtg}\\Decklists")

	size_decks = len(decks)
	for item in tournaments:
		today = time.localtime()
		today = time.strftime('%Y-%m-%d', today)
		today = time.strptime(today, '%Y-%m-%d')
		today_sec = time.mktime(today)
		date = time.strptime(item[2], "%Y-%m-%d")
		date_sec = time.mktime(date)
		dif_days = int((today_sec - date_sec) / (60 * 60 * 24))
		if dif_days > 10:
			continue
		# time.sleep(0.5)
		print(f"{item[1]}")
		soup = utils.get_content(item[0])
		utils.write_decks(soup, mtg, item)
		# next_page = soup.find("li", class_="next page-item")
		next_page = soup.find('a', class_='page-link', rel='next')
		pg = 1
		while next_page:
			pg += 1
			print(f"\tFetching Page {pg}")
			next_page = utils.tournament_check_pages(next_page, mtg, item)

	decks = utils.get_txt(mtg, "decks")

	new_decks[mtg] += len(decks)-size_decks
	new_decks["total"] += new_decks[mtg]

	print(f"{new_decks[mtg]} New Decks")
	stop = timeit.default_timer()
	print('Time: ', stop - start, '\n')

for mtg in formats:
	print(f"{mtg.title()} - {new_decks[mtg]} New Decks")

print(f"\n{new_decks['total']} Total New Decks\n")

for mtg in formats:
	if mtg not in run:
		continue
	print(f"Creating data for - {mtg.title()}")
	decks = utils.get_txt(mtg, "Decks")

	for deck in decks:
		deck_code = deck[2][-7:]
		if not os.path.exists(f"{mtg}\\Decklists\\{deck_code}.txt"):
			soup_deck = utils.get_content(deck[2])

			deck_input = soup_deck.find('input', {'name': 'deck_input[deck]'})
			if deck_input is not None:
				decklist = deck_input.get('value')
				with open(f"{mtg}\\Decklists\\{deck_code}.txt", "w", encoding="utf-8") as f_list:
					f_list.write(decklist.strip())

end = timeit.default_timer()
print('Time: ', end - begin)