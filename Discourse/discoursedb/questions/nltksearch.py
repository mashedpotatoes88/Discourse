#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

# IMPORTS
import os
import cgi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import metaphone as mph
from metaphone import doublemetaphone as dmph
import difflib
import urllib.parse
from datetime import datetime
import discoursedbconn as dbconn

# SPECIFY PATH FOR NLTK DOWNLOADER
os.environ['APPDATA'] = r"C:\Users\YOUR_USER\AppData\Roaming"

# POPULATE LIST WITH ENGLISH STOPWORDS 
stop_words = set(stopwords.words("english"))

# function to CORRECT TYPO
def correct_word(typo_word):

    # CONVERT WORD TO PHONETIC FORM
    word_phonetic = dmph(typo_word)[0]
    
    # LOOK THROUGH KEYWORDS TABLE FOR EXACT MATCHES 
    sql_select = "SELECT keyword FROM keywords WHERE phoneticForm LIKE "
    dbconn.mycursor.execute(sql_select, word_phonetic)
    exact_matches = dbconn.mycursor.fetchall()

    if exact_matches == None or len(exact_matches) == 0:
        # FETCH ALL KEYWORDS AND ORDER THEM BY POPULARITY
        sql_select = "SELECT phoneticForm FROM keywords ORDER BY keywordHits"
        dbconn.mycursor.execute(sql_select)
        all_keywords = dbconn.mycursor.fetchall()
        
        # LOOK THROUGH ALL KEYWORDS AND RETURN THE FIRST 5 CLOSE MATCHES
        close_matches = difflib.get_close_matches(typo_word, all_keywords, 5, 0.5)    

# function to EXTRACT KEYWORDS FROM SEARCH 
def extract_keywords(search_query):
    # CONVERT QUERY STRING INTO LIST
    tokenized_query = word_tokenize(search_query)

    # REMOVE STOPWORDS FROM LIST AND REMAIN WITH KEYWORDS
    keywords_list = [word for word in tokenized_query if word.lower() not in stop_words]
    return keywords_list

# function to FETCH RESULTS
def fetch_questions(list_of_keywords):
    sql_select = f"SELECT users.username,\
                        community.tagname,\
                        questions.timestamp,\
                        questions.questionId,\
                        questions.radarCount,\
                        questions.string,\
                        questions.answersCount,\
                        questions.totalLikesCount\
                        FROM questions \
                        JOIN users ON questions.userId = users.userId \
                        JOIN community ON users.communityId = community.communityId \
                        WHERE "
            
    for word in list_of_keywords:
        sql_select += f"string LIKE '%{word}%' OR "
    
    sql_select = sql_select[:-3]
    sql_select += "ORDER BY questions.radarCount DESC" 


    # EXECUTE STATEMENT
    dbconn.mycursor.execute(sql_select)
    
    # STORE RESULTS IN VARIABLE
    results = dbconn.mycursor.fetchall()

    # USE TIMESTAMP TO GET "1 hour ago"
    time_difference = datetime.now() - datetime.strptime(str(results[0][2]), r"%Y-%m-%d %H:%M:%S")
    time_ago_posted = dbconn.get_time_ago_posted(time_difference) 

    # APPEND DATA TO EACH DIV AND RETURN ALL DIVS
    print(dbconn.return_all_html_divs(dbconn.html_template_question, results, time_ago_posted))

# STORE FORM DATA IN VARIABLE 
query_url = os.environ.get('QUERY_STRING', '')
params = urllib.parse.parse_qs(query_url)
query = params.get('query', [''])[0]  

# EXTRACT KEYWORDS
keywords_list = extract_keywords(query)

# FETCH MATCHING QUESTIONS
fetch_questions(keywords_list)

# EXTRACT KEYWORDS THAT MATCH THE PHONETIC FORM

# ORDER KEYWORDS ACCORDING TO POPULARITY

# FETCH QUESTIONS THAT CONTAIN ALL KEYWORDS THEN ALL-1 THEN 
# ALL-2 ...... THEN 1 KEYWORD (ORDER BY POPULARITY)
dbconn.mycursor.close()
dbconn.conn.close()