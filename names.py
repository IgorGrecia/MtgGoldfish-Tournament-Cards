from os.path import basename
import os
import sys

if os.path.isfile("All\\new.txt"):
    os.remove("All\\new.txt")

files = os.listdir()
if len(files)==4:
	print("No Decks")
	sys.exit()

f2 = open("All\\new.txt", "w",encoding='utf8')

for i in files:
	if ".txt" in i:
		f1 = open(i, "r",encoding='utf8')
		for line in f1:
			f2.write(line)
		f1.close()
f2.close()

f2 = open("All\\new.txt", "r",encoding='utf8')
reader = f2.read()
f2.close()
reader = reader.replace("0", "#")
reader = reader.replace("1", "#")
reader = reader.replace("2", "#")
reader = reader.replace("3", "#")
reader = reader.replace("4", "#")
reader = reader.replace("5", "#")
reader = reader.replace("6", "#")
reader = reader.replace("7", "#")
reader = reader.replace("8", "#")
reader = reader.replace("9", "#")
reader = reader.replace("## ", "")
reader = reader.replace("# ", "")
reader = reader.replace("Snow-Covered Island\n", "\n")
reader = reader.replace("Snow-Covered Mountain\n", "\n")
reader = reader.replace("Snow-Covered Swamp\n", "\n")
reader = reader.replace("Snow-Covered Plains\n", "\n")
reader = reader.replace("Snow-Covered Forest\n", "\n")
reader = reader.replace("\nIsland\n", "\n\n")
reader = reader.replace("\nMountain\n", "\n\n")
reader = reader.replace("\nSwamp\n", "\n\n")
reader = reader.replace("\nPlains\n", "\n\n")
reader = reader.replace("\nForest\n", "\n\n")
f2 = open("All\\new.txt", "w",encoding='utf8')
f2.write(reader)
f2.close()
f2 = open("All\\new.txt", "r",encoding='utf8')
data=f2.readlines()
f2.close()
data.sort()
f2 = open("All\\new.txt", "w",encoding='utf8')
for i in range(len(data)-1):
	if data[i]!="\n" and data[i]!=data[i+1]:
		f2.write(data[i])
f2.write(data[len(data)-1])
f2.close()
f2 = open("All\\new.txt", "r",encoding='utf8')
data=f2.readlines()
f2.close()
comp = open("All\\Full.txt", "a",encoding='utf8')
comp.write("\n")
for i in range(len(data)):
	comp.write(data[i])
comp.close()
comp = open("All\\Full.txt", "r",encoding='utf8')
data=comp.readlines()
comp.close()
comp = open("All\\Full.txt", "w",encoding='utf8')
data.sort()
for i in range(len(data)-1):
	if data[i]!="\n" and data[i]!=data[i+1]:
		comp.write(data[i])
comp.write(data[len(data)-1])
comp.close()

os.startfile('All\\New.txt')
os.startfile('All\\Full.txt')