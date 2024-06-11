#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import json
import discoursedbconn as dbconn

def stringify_data(results):
        for result in results:
            result = list(result)
            for i in range(len(result)):
                if type(result[i]) == int:
                    result[i] = str(result[i])
                else:
                    continue

def sql_statement(string):
     savedQuestionsIds = "SELECT questionId FROM savedquestions WHERE userId = '%s'"
     radarQuestionsIds = "SELECT questionId FROM usersradar WHERE userId = '%s'"
     likedAnswersIds = "SELECT answerId FROM answerlikes WHERE userId = '%s'"
     likedCommentsIds = "SELECT commentId FROM commentlikes WHERE userId = '%s'"
     votedAnswersIds = "SELECT answerId FROM answervotes WHERE userId = '%s'"

     if string == "savedQuestionsIds":
        return savedQuestionsIds 
     elif string == "radarQuestionsIds":
        return radarQuestionsIds 
     elif string == "likedAnswersIds":
        return likedAnswersIds 
     elif string == "likedCommentsIds":
        return likedCommentsIds 
     elif string == "votedAnswersIds":
        return votedAnswersIds 

def execute_sql_statement(string, userid):
    sql_select = sql_statement(string)

    dbconn.mycursor.execute(sql_select % userid)
    results = dbconn.mycursor.fetchall()

    list_of_ids = []
    for result in results:
        list_of_ids.append(result[0])
    
    return list_of_ids

def fetch_user_details(username_entry, password_entry) :
    sql_select = f"SELECT users.userId,\
                    users.communityId,\
                    users.username,\
                    users.savedQuestionsCount,\
                    users.radarCount,\
                    users.notificationsCount,\
                    community.communityName,\
                    users.lastOnline,\
                    users.yearJoined\
                    FROM users JOIN community ON\
                    users.communityId = community.communityId WHERE username = '{username_entry}'\
                    AND password = '{password_entry}'"

    dbconn.mycursor.execute(sql_select)
    results = list(dbconn.mycursor.fetchall())

    if len(results) != 0:
        stringify_data(results)

    return results

# Read json from stdin
data = dbconn.read_json_input()
username_entry = data.get("username")
password_entry = data.get("password")

# username_entry = "eric"
# password_entry = "oj"

results = fetch_user_details(username_entry, password_entry)

if len(results) != 0:
    results = results[0]
    userid = results[0]
    savedQuestionsIds = execute_sql_statement("savedQuestionsIds", userid)
    radarQuestionsIds = execute_sql_statement("radarQuestionsIds", userid)
    likedAnswersIds = execute_sql_statement("likedAnswersIds", userid)
    likedCommentsIds = execute_sql_statement("likedCommentsIds", userid)
    votedAnswersIds = execute_sql_statement("votedAnswersIds", userid)

    # Send values to javascript
    response = {'userId': results[0],
                'communityId': results[1],
                'username': results[2],
                'savedQuestionsCount': results[3],
                'radarCount': results[4],
                'notificationsCount': results[5],
                'communityName': results[6],
                'lastOnline': str(results[7]),
                'yearJoined': results[8],
                'savedQuestionsIds': savedQuestionsIds,
                'radarQuestionsIds': radarQuestionsIds,
                'likedAnswersIds': likedAnswersIds,
                'likedCommentsIds': likedCommentsIds,
                'votedAnswersIds': votedAnswersIds
                }
    json_response = json.dumps(response).strip()
    print(json_response)
else:
    response = {"log": "Incorrect username or password!"}
    json_response = json.dumps(response).strip()
    print(json_response)

