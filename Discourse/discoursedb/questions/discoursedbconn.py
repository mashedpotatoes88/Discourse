#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print()
import mysql.connector as mysqlconn

# CREATE CONNECTION
conn = mysqlconn.connect(host="localhost", user="root", password="")

# CREATE A CURSOR
mycursor = conn.cursor()

# USE THE DATABASE CALLED "discourse"
mycursor.execute("USE discourse")


# FUNCTION
def return_all_html_divs(html_template_question, results, time_ago_posted):
    import json
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
    return(json_response)

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

template_user_profile = f"""
<div class="profile-container">
    <div class="profile-header">
        <div class="username">@fiona</div>
        <div class="community">Comp Sci</div>
        <div class="year-joined">Joined 2022</div>
        <div class="tabs">
            <div class="tab">My Questions</div>
            <div class="tab">My Comments</div>
            <div class="tab">Liked Answers</div>
            <div class="tab">Saved Questions</div>
        </div>
    </div>
    <div class="profile-body">
        <div class="user-content">
            <!-- DISPLAY DYNAMICALLY -->
            <!-- DEFAULT IS "my questions" -->
        </div>
    </div>
</div>"""


def read_json_input():
    import json
    import sys
    import os

    # READ JSON FROM STDIN
    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    json_data = sys.stdin.read(content_length)
    data = json.loads(json_data)
    return data