#!C:/Users/ADMIN/AppData/Local/Programs/Python/Python312/python
print("Content-Type: application/json")
print()

import json

def display(data):
    # SEND HTML TO JAVASCRIPT
    response = {'html_content': [data]}
    json_response = json.dumps(response)
    return(json_response)

def login_form():
    html_template = """
        <div class="tray-login-form">
            <div class="container-login-form">
                <div>
                    <i class="fa-solid fa-xmark"></i>
                </div>
                <h1>DISCOURSE</h1>
                <p>Log in to continue.</p>
                <form action="../python/resources/validateuser.py" method="post" class="login-form">
                    <div id="login-form-field">
                        <input type="text" name="username" id="username" class="form-control" placeholder="Username/Registration Number" required>
                    </div>
                    <div id="login-form-field">
                        <input type="text" name="password" id="password" class="form-control" placeholder="Password" required>
                    </div>
                    <p><a href="">Forgot password</a></p>
                    <button type="submit" class="btn submit-btn-login">Log In</button>
                </form>
                <p>Don't have an account? <a href="">Sign up.</a></p>
            </div>
        </div>"""
    return html_template

print(display(login_form()))