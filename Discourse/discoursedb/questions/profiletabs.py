#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import json
import discoursedbconn as dbconn
from datetime import datetime

# DEFINE FETCH MY QUESTIONS
def fetch_my_questions(userid):
    sql_select = f"SELECT users.username,\
                        community.tagname,\
                        questions.timestamp,\
                        questions.questionId,\
                        questions.radarCount,\
                        questions.string,\
                        questions.answersCount,\
                        questions.totalLikesCount,\
                        questions.userId,\
                        users.communityId\
                        FROM questions \
                        JOIN users ON questions.userId = users.userId \
                        JOIN community ON users.communityId = community.communityId \
                        WHERE questions.userid = '{userid}'\
                        ORDER BY questions.timestamp DESC"
    
    # EXECUTE STATEMENT
    dbconn.mycursor.execute(sql_select)
    
    # STORE RESULTS IN VARIABLE
    results = dbconn.mycursor.fetchall()

    # USE TIMESTAMP TO GET "1 hour ago"
    time_difference = datetime.now() - datetime.strptime(str(results[0][2]), r"%Y-%m-%d %H:%M:%S")
    time_ago_posted = dbconn.get_time_ago_posted(time_difference) 

    # APPEND DATA TO EACH DIV AND RETURN ALL DIVS
    print(dbconn.return_all_html_divs(dbconn.html_template_question, results, time_ago_posted))

def fetch_saved_questions(userid):
    sql_select = f"SELECT users.username,\
                        community.tagname,\
                        questions.timestamp,\
                        questions.questionId,\
                        questions.radarCount,\
                        questions.string,\
                        questions.answersCount,\
                        questions.totalLikesCount,\
                        questions.userId,\
                        users.communityId\
                        FROM savedquestions \
                        JOIN users ON savedquestions.userId = users.userId \
                        JOIN community ON users.communityId = community.communityId\
                        JOIN questions ON savedquestions.questionId = questions.questionId\
                        WHERE questions.userid = '{userid}'\
                        ORDER BY questions.timestamp DESC"
    
    # EXECUTE STATEMENT
    dbconn.mycursor.execute(sql_select)
    
    # STORE RESULTS IN VARIABLE
    results = dbconn.mycursor.fetchall()

    if len(results) != 0:
        # USE TIMESTAMP TO GET "1 hour ago"
        time_difference = datetime.now() - datetime.strptime(str(results[0][2]), r"%Y-%m-%d %H:%M:%S")
        time_ago_posted = dbconn.get_time_ago_posted(time_difference) 

        # APPEND DATA TO EACH DIV AND RETURN ALL DIVS
        print(dbconn.return_all_html_divs(dbconn.html_template_question, results, time_ago_posted))
    else:
        response = {"log" : "No records found!"}
        json_response = json.dumps(response)
        print(json_response)

# READ JSON INPUT AND STORE IN DICT
data = dbconn.read_json_input()

# READ DICT TO GET USER ID
name_of_tab = data.get('name_of_tab')
userid = data.get('userid')

# name_of_tab = "Questions"
# userid = "5"

# CALL FUNCTION
if name_of_tab == "Questions":
    fetch_my_questions(userid)
elif name_of_tab == "Saved Questions":
    fetch_saved_questions(userid)
