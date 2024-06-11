#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import discoursedbconn as dbconn
from datetime import datetime
import json

# DEFINE FETCH RADAR QUESTIONS
def fetch_radar_questions(userid):
    sql_select = f"""SELECT users.username,\
                        community.tagname,\
                        questions.timestamp,\
                        questions.questionId,\
                        questions.radarCount,\
                        questions.string,\
                        questions.answersCount,\
                        questions.totalLikesCount,\
                        usersradar.timestamp\
                        FROM usersradar \
                        JOIN questions ON usersradar.questionId = questions.questionId\
                        JOIN users ON questions.userId = users.userId \
                        JOIN community ON users.communityId = community.communityId \
                        WHERE usersradar.userId = {userid} \
                        ORDER BY usersradar.timestamp DESC"""
    
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

# # READ JSON INPUT AND STORE IN DICT
# data = dbconn.read_json_input()

# # READ DICT TO GET USER ID
# userid = data.get('userid')

userid = 5

# CALL FETCH RADAR QUESTIONS
fetch_radar_questions(userid)