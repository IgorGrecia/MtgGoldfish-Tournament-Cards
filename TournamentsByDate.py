import timeit
import os
import time
import utils
from datetime import datetime, timedelta

formats = utils.get_formats()
run = []
run.append("pauper")
run.append("modern")
run.append("legacy")
run.append("pioneer")
run.append("standard")
run.append("vintage")

get_tournaments = ""
# get_tournaments = input("Check NewMomycarterx Tournaments?\n0 = No\n1 = Yes\n")
begin = timeit.default_timer()

today = datetime.today()

# days = int(input("How long ago?\n"))
days = 10

time_select = today - timedelta(days=days)

start_day = time_select.day
start_month = time_select.month
start_year = time_select.year
end_day = today.day
end_month = today.month
end_year = today.year

new_tournaments = {}
new_tournaments["pauper"] = 0
new_tournaments["modern"] = 0
new_tournaments["legacy"] = 0
new_tournaments["pioneer"] = 0
new_tournaments["standard"] = 0
new_tournaments["vintage"] = 0
new_tournaments["total"] = 0

for mtg in formats:
	if mtg not in run or get_tournaments == '0':
		continue
	print(f"Updating {mtg.title()} Tournaments")
	start = timeit.default_timer()
	pg = 1
	count = 0
	
	while True:
		start = timeit.default_timer()
		url = f"https://www.mtggoldfish.com/tournament_searches/create?commit=Search&page={pg}&tournament_search%5Bdate_range%5D={start_month}%2F{start_day}%2F{start_year}+-+{end_month}%2F{end_day}%2F{end_year}&tournament_search%5Bformat%5D={mtg}&tournament_search%5Bname%5D="
		soup = utils.get_content(url)
		if "No tournaments found." in soup.body.get_text():
			break
		print(f"\tFetching Page {pg}")
		new_tournaments[mtg] += utils.write_tournaments(soup, mtg)
		pg += 1
		stop = timeit.default_timer()
		print('Time: ', stop - start)

	print(f"{new_tournaments[mtg]} Total New {mtg.title()} Tournaments\n")
	new_tournaments["total"] += new_tournaments[mtg]

for mtg in formats:
	print(f"{mtg.title()} - {new_tournaments[mtg]} New Tournaments")

print(f"{new_tournaments['total']} Total New Tournaments\n")

end = timeit.default_timer()
print('Time: ', end - begin)