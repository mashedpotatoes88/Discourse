#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type:text/html")
print()

import json
import discoursedbconn as dbconn

##FUNCTION TO EDIT THE COUNT IN THE TABLE 'questions'
def edit_questionSavedCount(questionId, inc_or_dec):
    sql_select = f"SELECT savedCount FROM questions \
                WHERE questionId = {questionId}"
    # EXECUTE SELECT
    dbconn.mycursor.execute(sql_select)
    result = dbconn.mycursor.fetchall()[0]
    count = result[0]

    # UPDATE COUNT
    if inc_or_dec == "inc":
        count += 1 
    elif inc_or_dec == "dec":
        count -= 1

    sql_update = f"UPDATE questions SET savedCount = '{count}'\
                WHERE questionId = {questionId}"
    # EXECUTE UPDATE
    dbconn.mycursor.execute(sql_update)
    dbconn.conn.commit()

## FUNCTION TO LOG THE SAVE QUESTION INTO THE TABLE 'savedquestions'
def logSavedQuestion(user_id, question_id, inc_or_dec):
    # SQL STATEMENT AND VARIABLES
    sql_insert = "INSERT INTO savedquestions (questionId, userId) \
                VALUES ('%s', %s)"
    sql_delete = "DELETE FROM savedquestions WHERE questionId = '%s'\
                AND userId = '%s'"
    variables_tuple = (question_id, user_id)

    # EXECUTE STATEMENT
    if inc_or_dec == "inc":
        dbconn.mycursor.execute(sql_insert % variables_tuple)
    elif inc_or_dec == "dec":
        dbconn.mycursor.execute(sql_delete % variables_tuple)

    dbconn.conn.commit()


def edit_userSavedCount(userId, inc_or_dec):
    sql_select = f"SELECT savedQuestionsCount FROM users \
                WHERE userId = {userId}"
    # EXECUTE SELECT
    dbconn.mycursor.execute(sql_select)
    result = dbconn.mycursor.fetchall()[0]
    count = result[0]

    # UPDATE COUNT
    if inc_or_dec == "inc":
        count += 1 
    elif inc_or_dec == "dec":
        count -= 1

    sql_update = f"UPDATE users SET savedQuestionsCount = '{count}'\
                WHERE userId = {userId}"
    # EXECUTE UPDATE
    dbconn.mycursor.execute(sql_update)
    dbconn.conn.commit()

# GETTING DATA FROM JSON INPUT
data = dbconn.read_json_input()
userId = data.get("userId")
questionId = data.get("questionId")
inc_or_dec = data.get("inc_or_dec")

# userId = 5
# questionId = "69"
# inc_or_dec = "inc"

# CALLING FUNCTIONS
edit_questionSavedCount(questionId, inc_or_dec)
edit_userSavedCount(userId, inc_or_dec)
logSavedQuestion(userId, questionId, inc_or_dec)

response = {"log": "savequestion.py: Database Updated!"}
json_response = json.dumps(response)
print(json_response)

# CLOSING CURSOR AND CONNECTION
dbconn.mycursor.close()
dbconn.conn.close()