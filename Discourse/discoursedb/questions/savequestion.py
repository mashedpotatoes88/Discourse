#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type:text/html")
print()

import discoursedbconn as dbconn

# STOR FORM INPUTS IN VARIABLES
formuserid = "1"
formquestionid = "58"

##FUNCTION TO EDIT THE COUNT IN THE TABLE 'questions'
def editSavedCount(questionid):
    # SQL STATEMENTS
    sql_fetch = "SELECT savedCount FROM questions WHERE questionId = '%s'"
    sql_update = "UPDATE questions SET savedCount = '%s' WHERE questionId = '%s'"

    # FETCH savedCount AND INCREMENT
    dbconn.mycursor.execute(sql_fetch % questionid)
    result= dbconn.mycursor.fetchone()
    print(result)
    current_saved_count = result[0]
    current_saved_count += 1
    print(current_saved_count)

    # UPDATE savedCount IN THE questions TABLE
    variables_list = (current_saved_count, questionid)
    dbconn.mycursor.execute(sql_update % variables_list)
    dbconn.conn.commit()

## FUNCTION TO LOG THE SAVE QUESTION INTO THE TABLE 'savedquestions'
def logSavedQuestion(user_id, question_id):
    time_of_save = "some_time"

    # SQL STATEMENT AND VARIABLES
    sql_insert = "INSERT INTO savedquestions (questionId, userId) \
                VALUES ('%s', %s)"
    variables_tuple = (question_id, user_id)

    # EXECUTE STATEMENT
    print(sql_insert % variables_tuple)
    dbconn.mycursor.execute(sql_insert % variables_tuple)
    dbconn.conn.commit()

# CALLING FUNCTIONS
editSavedCount(formquestionid)
logSavedQuestion(formuserid, formquestionid)

# CLOSING CURSOR AND CONNECTION
dbconn.mycursor.close()
dbconn.conn.close()