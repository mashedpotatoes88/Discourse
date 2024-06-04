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
import json
from datetime import datetime
import discoursedbconn as dbconn

# SPECIFY PATH FOR NLTK DOWNLOADER
os.environ['APPDATA'] = r"C:\Users\YOUR_USER\AppData\Roaming"

# POPULATE LIST WITH ENGLISH STOPWORDS 
stop_words = set(stopwords.words("english"))

# <div class="container container-question"> STORED IN A TEMPLATE
html_template_question = f"""
    <!--QUESTION CONTAINER -->
        <div class="container container-question" data-questionid="%s">
            <!-- COURSE AND USERNAME -->
            <div class="question-header">
                <div class="question-header-details">
                    <div class="question-details">
                        <p class="question-detail">@%s</p>
                        <div class="tag tag-community"><p class="question-detail">%s</p></div>
                    </div>
                    <div class="time-posted">
                        <p class="question-detail">%s</p>
                    </div>
                </div>
                
                <!-- OPTIONS MENU -->
                <div class="options-menu">                            
                    <div class="sidebuttons">
                        <div class="addtoradardiv" data-questionid="%s">
                            <p class="addtoradartext">%s</p>
                            <div class="icon"><i class="fa-solid fa-satellite-dish"></i></div>
                        </div>
                    </div>
                    <div class="savequestion" data-questionId="%s">
                        <i class="fa-regular fa-bookmark"></i>  <!--Contains Save, Report, Similar Questions-->
                    </div>
                    <div class="copylink" data-questionId="%s">
                        <i class="fa-solid fa-link"></i>  <!--Contains Save, Report, Similar Questions-->
                        <div class="copied">
                                <p>Link Copied!</p>
                        </div>
                    </div>

                </div>
            </div>
            <a href="http://localhost/Discourse/html/test.html?questionId=%s" class="question-anchortag" data-questionId=%s>
                <!-- QUESTION AND RADAR BUTTON -->
                <div class="question-body">
                    <div class="content">
                        <div class="questionbox">%s</div>
                    </div>
                </div>
                <!-- QUESION NUMBERS -->
                <div class="question-numbers">
                    <p class="question-detail">%s comments</p>
                    <p class="question-detail">%s likes</p>
                </div>
            </a>
        </div>"""

# GET TIME AGO POSTED
def get_time_ago_posted(time_difference):
     # Convert the difference to a human-readable format
    seconds = time_difference.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7
    
    if seconds < 60:
        if int(seconds) == 1:
            return f"{int(seconds)} second ago"
        else:
            return f"{int(seconds)} seconds ago"
    elif minutes < 60:
        if int(minutes) == 1:
            return f"{int(minutes)} minute ago"
        else:
            return f"{int(minutes)} minutes ago"
    elif hours < 24:
        if int(hours) == 1:
            return f"{int(hours)} hour ago"
        else:
            return f"{int(hours)} hours ago"
    elif days < 7:
        if int(days) == 1:
            return f"{int(days)} day ago"
        else:
            return f"{int(days)} days ago"
    else:
        if int(weeks) == 1:
            return f"{int(weeks)} week ago"
        else:
            return f"{int(weeks)} weeks ago"

# function to CHECK FOR TYPOS

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
    sql_select = "SELECT users.username, community.tagname, questions.timestamp, questions.questionId, \
            questions.radarCount, questions.string, questions.answersCount, questions.totalLikesCount \
            FROM questions JOIN users ON questions.userId = users.userId JOIN community ON \
            users.communityId = community.communityId WHERE "
   
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
    time_ago_posted = get_time_ago_posted(time_difference) 
    

    # PUT TOGETHER THE HTML DIVS
    all_html_divs = []
    for i in range(len(results)):
        one_html_div = (html_template_question % (results[i][3], results[i][0], results[i][1], time_ago_posted, \
                                                results[i][3], results[i][4], results[i][3],\
                                                results[i][3], results[i][3],results[i][3],\
                                                results[i][5], results[i][6], results[i][7]))
        all_html_divs.append(one_html_div)   

    # SEND HTML TO JAVASCRIPT
    response = {'html_content': all_html_divs}
    json_response = json.dumps(response)
    print(json_response)


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