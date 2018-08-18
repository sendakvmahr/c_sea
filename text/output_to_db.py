import sqlite3
import regex
CUTOFF = 1000

items = []

def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

print("READING")
with open("output.txt", "r", encoding="UTF-8") as file:
    s = file.read()[28:-2]
    temp = ""
    for i in range(len(s)):
        char = s[i]
        if char == " ":
            continue
        elif char == ",":
            word, num = temp.replace("'", "").split(":")
            num = int(num)
            if num >= CUTOFF and is_english(word):
                items.append([word, num])
            temp = ""
        else:
            temp += char
print("READ")          
items.sort()
print("SORTED")

conn = sqlite3.connect("wordbank.db")
cur = conn.cursor()
print("SENDING")
cur.executemany("INSERT INTO wordbank (word, count) VALUES (?, ?)", items)
conn.commit()
conn.close()
print("DONE")
