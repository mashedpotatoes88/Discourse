#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import os
import sys
import json
import discoursedbconn as dbconn

log = ""
# UPDATE questions.radarCount
def update_questions_radarCount(questionId, newradarCount):
    sql_update = "UPDATE questions SET radarCount = '%s' WHERE questionid = '%s'"

    # POST NEW VALUE TO TABLE
    variables_tuple = (newradarCount, questionId)
    dbconn.mycursor.execute(sql_update % variables_tuple)
    dbconn.conn.commit()
    return f"questions.radarCount Updated: {newradarCount}\n"

# UPDATE users.radarCount
def update_user_radar_count(userid, inc_or_dec):
    # SQL STATEMENT
    sql_update = "UPDATE users SET radarCount = '%s' WHERE userId = '%s'"
    sql_select = "SELECT username, radarcount FROM users WHERE userid = '%s'"

    # SELECT 
    dbconn.mycursor.execute(sql_select % userid)
    result = dbconn.mycursor.fetchall()[0]
    oldradarcount = result[1]

    # INCREMENT or DECREMENT
    if inc_or_dec == "inc":
        newradarCount = oldradarcount + 1
    else:
        newradarCount = oldradarcount - 1

    # POST NEW VALUE TO TABLE
    variables_tuple = (newradarCount, userid)
    dbconn.mycursor.execute(sql_update % variables_tuple)
    dbconn.conn.commit()

    dbconn.mycursor.execute(sql_select % userid)
    result = dbconn.mycursor.fetchall()[0]
    return f"users.radarCount Updated: {result[0]}, {result[1]}\n"

# UPDATE communityradar.usersCount OR INSERT OR DELETE
def update_community_radar_count(inc_or_dec, questionid, newradarcount):
    # SQL STATEMENTS
    sql_update = "UPDATE communityradar SET usersCount = '%s' WHERE questionId = '%s'"
    sql_insert = "INSERT INTO communityradar (questionId, usersCount) VALUES ('%s', '1')"
    sql_delete = "DELETE FROM communityradar WHERE questionId = '%s'"

    if newradarcount == None or newradarcount == 0:
        # DELETE QUESTION FROM communityradar
        dbconn.mycursor.execute(sql_delete % questionid)
        dbconn.conn.commit()
        return "communityradar.usersCount 1 record deleted!\n"
    elif inc_or_dec == "inc" and newradarcount == 1:
        # INSERT NEW QUESTION 
        dbconn.mycursor.execute(sql_insert % questionid)
        dbconn.conn.commit()
        return "communityradar.usersCount 1 record inserted!\n"
    else:
        # POST DECREMENTED VALUE TO THE TABLE
        dbconn.mycursor.execute(sql_update % (newradarcount, questionid))
        dbconn.conn.commit()
        return f"communityradar.usersCount Updated: {newradarcount}\n"

# INSERT INTO OR DELETE FROM usersradar
def log_to_users_radar(ins_or_del, userid, questionid):
    sql_insert = "INSERT INTO usersradar (questionId, userId) VALUES ('%s', '%s')"
    sql_delete = "DELETE FROM usersradar WHERE questionId = '%s' AND userId = '%s'"
    variables_tuple = (questionid, userid)

    if ins_or_del == "ins":
        # ADDING TO RADAR
        dbconn.mycursor.execute(sql_insert % variables_tuple)
        dbconn.conn.commit()
        return "usersradar 1 record inserted!\n"
    else:
        # DELETING FROM RADAR
        dbconn.mycursor.execute(sql_delete % variables_tuple)
        dbconn.conn.commit()
        return "usersradar 1 record deleted!\n"

# READ JSON STRING FROM ENVIRONMENT VARIABLES
content_length = int(os.environ.get('CONTENT_LENGTH', 0))
json_data = sys.stdin.read(content_length)

# CONVERT FROM JSON AND STORE IN VARIABLES
data = json.loads(json_data)

userid = data.get('userid')
questionid = data.get('questionId')
newradarcount = data.get('radarCount')
inc_or_dec = data.get('inc_or_dec')
ins_or_del = data.get('ins_or_del')

# userid = "1"
# questionid = "72"
# newradarcount = "1"
# inc_or_dec = "inc"
# ins_or_del = "ins"

# CALLING FUNCTIONS
log += update_questions_radarCount(questionid, newradarcount)
log += update_user_radar_count(userid, inc_or_dec)
log += update_community_radar_count(inc_or_dec, questionid, newradarcount)
log += log_to_users_radar(ins_or_del, userid, questionid)

response = {"html_content": log}
json_response = json.dumps(response)
print(json_response)

# CLOSE CONNECTION
dbconn.mycursor.close()
dbconn.conn.close()