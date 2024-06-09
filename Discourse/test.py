#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import discoursedbconn as dbconn
from datetime import datetime

# READ JSON INPUT AND STORE IN DICT
data = dbconn.read_json_input()

# READ DICT TO GET USER ID
userid = data.get('userid')

# DEFINE FETCH RADAR QUESTIONS
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

# CALL FETCH RADAR QUESTIONS
fetch_radar_questions(userid)

<!--QUESTION CONTAINER -->
<div class="container container-question">
    <!-- COURSE AND USERNAME -->
    <div class="question-header">
        <div class="question-header-details">
            <div class="question-details">
                <p class="question-detail">@ericmacharia82</p>
                <div class="tag tag-community"><p class="question-detail">Comp Sci</p></div>
            </div>
            <div class="time-posted">
                <p class="question-detail">1 hour ago</p>
            </div>
        </div>
        
        <!-- OPTIONS  -->
        <div class="options-menu">   
            <!-- add to radar -->
            <div class="addtoradardiv">
                <p class="addtoradartext">7</p>
                <div class="icon"><i class="fa-solid fa-satellite-dish"></i></div>
            </div>
            <!-- save question -->
            <div class="savequestion" data-questionId="72">
                <i class="fa-regular fa-bookmark"></i>  <!--Contains Save, Report, Similar Questions-->
            </div>
            <!-- copy link -->
            <div class="copylink" data-questionId="72">
                <i class="fa-solid fa-link"></i>  
                <div class="copied">
                    <p>Link Copied!</p>
                </div>
            </div>
        </div>                       
    </div>
    <div class="question-body">
        <div class="content">
            <div class="questionbox">In Machine Learning, Lorem ipsum dolor sit amet consectetur adipisicing elit. In id praesentium accusamus maxime minus quis blanditiis voluptatibus reiciendis, ad deleniti. what is a decision tree used for?</div>
        </div>
    </div>
    <div class="question-numbers">
        <p class="question-detail">21 comments</p>
        <p class="question-detail">43 likes</p>
    </div>
</div>