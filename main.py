from text import input_document_spacy as inp
import pymysql
import config

db = pymysql.connect(host=config.sql_db_host,
                         user=config.sql_username,
                         password=config.sql_pw,
                         db=config.sql_db_name,
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
inp.reset_db(db)
#inp.read_data("./text/corpora/~test")