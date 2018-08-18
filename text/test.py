import os
from collections import defaultdict
import string

# UNUSED
def batch_increment(conn, default_dict):
    print("building query...")
    items = []
    for word, count in default_dict.items():
        items.append([count, word])
        if not was_added(word):
            conn.execute("INSERT INTO wordbank (word, count) VALUES (?, ?)", [word, 0])
    print("sending query...")
    conn.batch_execute("UPDATE wordbank SET count=count+? WHERE word=?", items)
    print("excecuted query.")

def get_pages_list(start=""):
    pages = []
    base_path = "./wikiextractor-master/text/"+start
    for subdir in os.listdir(base_path):
        if start == "":
            for page in os.listdir(base_path + subdir):
                pages.append(base_path + subdir + "/" + page)
        else:
            pages.append(base_path + subdir)
    return pages

def append_page_info(page, defdict):
    with open(page, encoding="UTF-8") as file:
        for line in file.readlines():
            for item in line.split(" "):
                item = clean_string(item)
                item = item.lower()
                if exclude(item):
                    continue
                defdict[item] += 1
    return defdict

def clean_string(s):
    return ''.join(e for e in s if e.isalnum())

def has_num(s):
    for i in "0123456789":
        if i in s:
            return True
        
def exclude(s):
    return (s=="doc") or (s[:3]=="url") or (s[:5]=="title" and len(s) > 6) or (has_num(s)) or (s=="")

result = defaultdict(int)
counter = 0

for page in get_pages_list(start=""):
    print("starting page", page)
    result = append_page_info(page, result)
    counter += 1
    print(page, "done", counter)

with open("output.txt", "w", encoding="UTF-8") as file:
    file.write(str(result))
    
print("DONE")

