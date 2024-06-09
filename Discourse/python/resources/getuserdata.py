#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import os
import sys
import json
import discoursedbconn as dbconn
from datetime import datetime

# READ JSON FROM STDIN
content_length = int(os.environ.get('CONTENT_LENGTH', 0))
json_data = sys.stdin.read(content_length)
data = json.loads(json_data)

# GETTING FORM INPUTS AND STORING IN VARIABLES
username_entry = data.get("username")
password_entry = data.get("password")


# CHECK IF USERNAME AND PASSWORD MATCH IN THE DB
sql_select = f"SELECT users.userId, 
                    users.communityId, 
                    users.username, 
                    users.savedQuestionsCount,
                    users.radarCount,
                    users.notificationsCount, 
                    community.communityName
                    users.lastOnline,
                    users.yearJoined
                    FROM users JOIN community ON 
                    users.communityId = community.communityId WHERE username = '{username_entry}' \
                    AND password = '{password_entry}'"

dbconn.mycursor.execute(sql_select)
results = list(dbconn.mycursor.fetchall())

def stringify_data(results):
    for result in results:
        result = list(result)
        for i in range(len(result)):
            if type(result[i]) == int:
                result[i] = str(result[i])
            else:
                continue

if results != None or len(results) != 0:
    stringify_data(results)

results = results[0]

# FETCH RADAR QUESTIONS
def fetch_radar_questions(userid):
    sql_select = f"SELECT users.username,
                        community.tagname,
                        questions.timestamp,
                        questions.questionId,
                        questions.radarCount,
                        questions.string,
                        questions.answersCount,
                        questions.totalLikesCount
                        usersradar.timestamp
                        FROM usersradar 
                        JOIN users ON questions.userId = users.userId 
                        JOIN community ON users.communityId = community.communityId 
                        WHERE userId = {userid} 
                        ORDER BY usersradar.timestamp DESC"
    
    # EXECUTE STATEMENT
    dbconn.mycursor.execute(sql_select)
    
    # STORE RESULTS IN VARIABLE
    results = dbconn.mycursor.fetchall()

    # USE TIMESTAMP TO GET "1 hour ago"
    time_difference = datetime.now() - datetime.strptime(str(results[0][2]), r"%Y-%m-%d %H:%M:%S")
    time_ago_posted = dbconn.get_time_ago_posted(time_difference) 
    
    # APPEND DATA TO EACH DIV AND RETURN ALL DIVS
    print(dbconn.return_all_html_divs(dbconn.html_template_question, results, time_ago_posted))

# FETCH SAVED QUESTIONS
def fetch_saved_questions():
    sql_select = "SELECT * FROM table" 
# FETCH LIKED ANSWERS
def fetch_like_answers():
    sql_select = "SELECT * FROM table"
# FETCH CONTRIBUTIONS 
def fetch_comments_and_answers():
    sql_select = "SELECT * FROM table"
# FETCH MY QUESTIONS
def fetch_my_questions():
    sql_select = "SELECT * FROM table"


# SEND THESE NUMBERS TO JAVASCRIPT
response = {'userId': results[0],
            'communityId': results[1],
            'username': results[2],
            'savedQuestionsCount': results[3],
            'radarCount': results[4],
            'notificationsCount': results[5],
            'communityName': results[6],
            'lastOnline': results[7],
            'yearJoined': results[8],
            }
json_response = json.dumps(response).strip()
print(json_response)

