#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import discoursedbconn as dbconn
import json

def fetch_community_profile(userId):
    sql_select = f"""SELECT community.communityId,\
                        community.communityName,\
                        community.membersCount\
                        community.membersOnlineCount\
                        community.radarQuestionsCount\
                        FROM community\
                        WHERE community.communityId = '{communityId}' """
    
    # EXECUTE SQL STATEMENT
    dbconn.mycursor.execute(sql_select)
    result = dbconn.mycursor.fetchall()[0]

    # INSERT DATA INTO TEMPLATE
    response = dbconn.template_community_profile % (result[0], result[1], result[2], result[3], result[4])
    return response

data = dbconn.read_json_input()
communityId = data.get("communityId")

# communityId = 1

# MAIN
content = fetch_community_profile(communityId)

# RETURN JSON
response = {"html_content" : content}
json_response = json.dumps(response)
print(json_response)

# Close
dbconn.mycursor.close()
dbconn.conn.close()