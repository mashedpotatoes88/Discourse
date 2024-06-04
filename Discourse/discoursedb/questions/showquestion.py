#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type:text/html")
print()

from datetime import datetime
import os
import sys
import json
import discoursedbconn as dbconn

# <div class="container container-question"> STORED IN A TEMPLATE
html_template_answer = f"""
    <a href="" class="answer-anchortag">
        <div class="container container-answer">
            <div class="answer-votes">
                <i class="fa-solid fa-sort-up"></i>
                <div class="votes">%s</div>
                <i class="fa-solid fa-sort-down"></i>
            </div>
            <div class="answer-body">
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
                        <div class="copylink" data-questionId="%s">
                            <i class="fa-solid fa-link"></i>  <!--Contains Save, Report, Similar Questions-->
                        </div>
                    </div>
                </div>
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
            </div>
        </div>
    </a>"""

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

# function to FETCH ANSWERS
def fetch_answers(_questionid):
    sql_select = f"SELECT answers.voteCount, users.username, community.tagname, answers.timestamp,\
            answers.questionId,  answers.string, answers.commentsCount, answers.likesCount\
            FROM answers JOIN users ON answers.userId = users.userId JOIN community ON \
            users.communityId = community.communityId WHERE answers.questionId = {_questionid}\
            ORDER BY answers.likesCount DESC"

    # EXECUTE STATEMENT
    dbconn.mycursor.execute(sql_select)
    
    # STORE RESULTS IN VARIABLE
    results = dbconn.mycursor.fetchall()

    # USE TIMESTAMP TO GET "1 hour ago"
    time_difference = datetime.now() - datetime.strptime(str(results[0][3]), r"%Y-%m-%d %H:%M:%S")
    time_ago_posted = get_time_ago_posted(time_difference) 
    

    # PUT TOGETHER THE HTML DIVS
    all_html_divs = []
    for i in range(len(results)):
        one_html_div = (html_template_answer % (results[i][0],results[i][1], results[i][2], time_ago_posted, \
                                                results[i][4], results[i][5], results[i][6], results[i][7]))
        all_html_divs.append(one_html_div)   

    # SEND HTML TO JAVASCRIPT
    response = {'html_content': all_html_divs}
    json_response = json.dumps(response)
    print(json_response)

# READ JSON STRING FROM ENVIRONMENT VARIABLES
content_length = int(os.environ.get('CONTENT_LENGTH', 0))
json_data = sys.stdin.read(content_length)

# CONVERT FROM JSON AND STORE IN VARIABLES
data = json.loads(json_data)
questionId = data.get('_questionId')

# questionId = "72"



fetch_answers(questionId)