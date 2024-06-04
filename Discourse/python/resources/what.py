#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import os
import sys
import json
import discoursedbconn as dbconn

try:
    # Read JSON data from stdin
    content_length = int(os.environ.get('CONTENT_LENGTH', 0))
    json_data = sys.stdin.read(content_length)
    data = json.loads(json_data)
    
    # Get form inputs
    username_entry = data.get("username")
    password_entry = data.get("password")

    # Simulate database response
    if username_entry == "eric" and password_entry == "pass":
        response_data = {
            "userId": 1,
            "username": username_entry,
            "communityId": 101,
            "radarCount": 5,
            "notificationsCount": 10,
            "lastOnline": "2023-05-26T12:00:00Z",
            "html_content": "User authenticated successfully"
        }
    else:
        response_data = {
            "error": "Invalid or password"
        }
    
    # Print JSON response
    print("Content-Type: application/json")
    print()
    print(json.dumps(response_data))

except Exception as e:
    print("Content-Type: application/json")
    print()
    print(json.dumps({"error": str(e)}))