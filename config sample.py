sql_username = ""
sql_pw = ""
sql_db_name = ""
sql_db_host = ""
read_until = 7

to_read_dir = "./text/corpora/"
done_read_dir = "./text/processed_corpora/"
degree_association = 2

gmail_username = "test@gmail.com"
gmail_password = ""

pos = ['ADJ', 'ADP', 'ADV', 'AUX', 'CCONJ', 'DET', 'INTJ', 'NOUN', 'NUM', 'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X']


computers = [""]
computer_name = ""

tiers = {
	"tier_1": [""],   # full power
	"tier_2": [""],	  # full power but should not focus on processing
	"tier_3": [""],   # x86 no spacy
	"internet": [""], # internet access
	"router" : [""],  # computer running base celery
}