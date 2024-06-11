// DEFINING FUNCTIONS
let userId 
let username 
let communityid 
let radarCount 
let notificationsCount 
let lastOnline 
let communityname
let questioncontent
let currentpage = 'Explore - Learn from peers!'

// EXECUTING A SEARCH
function extract_from_url(type) {
    const urlParams = new URLSearchParams(window.location.search);
    const value = urlParams.get(type);
    return value;
};
function fetchSearchResults() {
    query = extract_from_url('query');  
    fetch(`../discoursedb/questions/nltksearch.py?query=${encodeURIComponent(query)}`)
        .then(response => {
            return response.json();
        })
        .then(data => {
            const container = document.getElementsByClassName('container-feed')[0]; 
            container.innerHTML = ''; 
            data.html_content.forEach(html => {
                container.innerHTML += html; 
            });
            if (data.html_content) {
              savePageState(query);
            };
        });
    console.log("Fetch Complete!");
};

// FETCH AND DISPLAY 
function viewuser() {
    const userId = extract_from_url('userId');
    fetch('../discoursedb/questions/viewuser.py', {
        method: 'POST',
        header: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            userId : userId
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        parent = document.querySelector('.container-feed');
        parent.innerHTML = data.html_content;
    })
};
function viewcommunity() {
    const userId = extract_from_url('userId');
    fetch('../discoursedb/questions/viewuser.py', {
        method: 'POST',
        header: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            userId : userId
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        parent = document.querySelector('.container-feed');
        parent.innerHTML = data.html_content;
    })
};
function fetch_user_content(_name_of_tab, _userId) {
    highlight_profile_tab(_name_of_tab);
    console.log("Fetching results for ", _name_of_tab, " and ", _userId);
    fetch("../discoursedb/questions/profiletabs.py", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            userid : _userId,
            name_of_tab : _name_of_tab
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        parent = document.querySelector('.user-content');
        parent.innerHTML = '';
        if (data.html_content) {
            data.html_content.forEach(html => {
                parent.innerHTML += html;
            });
        }
        else {
            parent.textContent = 'No Records Found!';
        }
    });
};
function fetch_community_content(_name_of_tab, _userId) {
    highlight_profile_tab(_name_of_tab);
    console.log("Fetching results for ", _name_of_tab, " and ", _userId);
    fetch("../discoursedb/questions/profiletabs.py", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            userid : _userId,
            name_of_tab : _name_of_tab
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        parent = document.querySelector('.user-content');
        parent.innerHTML = '';
        if (data.html_content) {
            data.html_content.forEach(html => {
                parent.innerHTML += html;
            });
        }
        else {
            parent.textContent = 'No Records Found!';
        }
    });
};
function displayquestion(_innerhtml) {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get('questionId');
    if (questionId) {
        console.log("Showing Question!")
        showquestion(questionId, _innerhtml);
    }
    else {
        console.log("Not Showing Question!")
    };
    function showquestion(_questionId, _innerhtml) {
        const container = document.querySelector('.container-feed');
        container.innerHTML = _innerhtml;
    
        const parent = document.querySelector('.container-question');    
        fetch("../discoursedb/questions/showquestion.py", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
                },
            body: JSON.stringify({_questionId})
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            answersDiv = document.createElement('div');
            answersDiv.classList.add('answers-container');
            
            data.html_content.forEach(answer => {
                answersDiv.innerHTML += answer;
            });
            parent.appendChild(answersDiv);
            answersDiv.style.height = "100%";
            savePageState('');
        })
        .catch(error => console.error("Error Fetching Answers: ", error))
    };
};
function fetchRadarQuestions(userid) {     
    fetch(`../discoursedb/questions/test.py`, {
        method: "POST",
        header: {
            "Content-Type" : "application/json"
        },
        body: {
            userid : userid
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        const container = document.getElementsByClassName('container-feed')[0]; 
        container.innerHTML = ''; 
        if (data.html_content) {
            data.html_content.forEach(html => {
                container.innerHTML += html;
            });
            savePageState('');
        }
        else{
            container.innerHTML = 'No questions in Radar yet!';
        }
    });
    console.log("Fetch Complete!");
};
function highlight_profile_tab(name_of_tab) {
    console.log(name_of_tab);
    const profile_tabs = document.querySelectorAll('.tab');
    console.log(profile_tabs);
    profile_tabs.forEach(tab => {
        if (tab.classList.contains('highlighted-profile-tab')) {
            tab.classList.remove('highlighted-profile-tab');
            console.log("Profile Tab Unhighlighted! ", tab);
        }
        if (tab.textContent === name_of_tab) {
            tab.classList.add('highlighted-profile-tab');
            console.log("Profile tab highlighted! ", tab);
        }
        else{
            console.log(`${name_of_tab} is not equal to ${tab}`);
        }
    });
};

// MANAGING PAGE STATES
function savePageState(searchQuery) {
    // Store Page State
    const pageState = {
        htmlContent: document.documentElement.innerHTML,
        searchquery: searchQuery
    };
    // Add the Page to Browser History 
    newUrl = window.location.href;
    history.replaceState({pageState}, '', newUrl);
    console.log("Page State Saved!", pageState.searchquery);
};
function restorePageState(event) {
    const {state} = event;
    if (state && state.pageState) {
        searchquery = state.pageState.searchquery
        document.documentElement.innerHTML = state.pageState.htmlContent;
        document.getElementById('query').value = searchquery;
        console.log("Page restored!", searchquery);

        // update page title
        update_page_title(searchquery);
    }
    else{
        console.log("Page not restored!");
    }
};
function update_url(value, type) {
    if (value === '' ) {
        const newUrl = `${window.location.origin}${window.location.pathname}`;
        history.pushState('', '', newUrl);
        console.log("Url Updated: ", newUrl);
    }
    else {
        const newUrl = `${window.location.origin}${window.location.pathname}?${type}=${value}`;
        history.pushState('', '', newUrl);
        console.log("Url Updated: ", newUrl);
    };
};
function update_page_title(searchquery) {
    DOMtitle = document.querySelector('title');
    currentpage = `${searchquery} - Search Query`;
    DOMtitle.textContent = currentpage;
}

// FUNCTIONS FOR USER DETAILS 
function updateProfile() {
    removeForm("loginbtn");
    const container = document.querySelector('.profile');

    const anchor = document.createElement('a');
    anchor.classList.add = 'profile-top';
    anchor.href = "#";
    anchor.textContent = '@' + username;
    console.log("Anchor Tag Created!")
    
    const div = document.createElement('div');
    div.classList.add('user-username');
    div.appendChild(anchor);
    
    container.appendChild(div);
    console.log("Div Created!")
};

// FUNCTIONS FOR SESSION STORAGE
function saveSearchToSessionStorage(userDetails) {
    sessionStorage.setItem('searchQuery', query);
    sessionStorage.setItem('searchResults', JSON.stringify(results));
};

// Login Form
function removeForm(csselement) {
    document.querySelector('.' + csselement).remove();
};
function validateLoginForm(_username, _password) {
    console.log('Validating Login Details');
    fetch("../python/resources/getuserdata.py", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
            },
        body: JSON.stringify({
            username: _username,
            password: _password
        })
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        if (data.hasOwnProperty('log')) {
            console.log("Login Unsuccessful!");
            let p = document.createElement('p');
            p.textContent = data.log;
            p.style.color = 'red';
            // clear fields
            const formfields = document.querySelectorAll('#login-form-field input');
            formfields.forEach(formfield => {
                formfield.value = '';
            })
            // display error message
            let elementBefore = formfields[1].parentNode;
            elementBefore.insertAdjacentElement('afterend', p);
        }
        else {
            console.log("Login Successful!");
            updateProfile();
            removeForm('tray-login-form');
        }
    })
    .catch(error => console.error("Error Validating Login Details: ", error));
};

// Update Database
function update_question_radarCount(inc_or_dec, ins_or_del, questionId, radarCount, userid) {
    fetch('../discoursedb/questions/addtoradar.py', {
        method: 'POST',
        headers: {
            "Content-Type" : "application/json" 
        },
        body: JSON.stringify({
            inc_or_dec: inc_or_dec,
            ins_or_del: ins_or_del,
            questionId: questionId,
            radarCount: radarCount,
            userid: userid
        })
    })
    .then(response =>{
        response.json()
    })            
    .then(data => {
        console.log(data.html_content);
    })
    .catch(error => console.error("Error updating radar counts in Database: ", error))
};
function update_question_savedCount(userId, questionId, inc_or_dec) {
    fetch("../discoursedb/questions/savequestion.py", {
        method: "POST",
        header: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            userId : userId,
            questionId : questionId,
            inc_or_dec : inc_or_dec
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data.log);
    })
    .catch(error => console.error("Error updating saved counts: ", error))
};


//------------------------------------------------- EVENT LISTENERS -----------------------------------------//

// log in
document.addEventListener("click", function(event){
    if (event.target.closest('.btn-login')) {
        event.preventDefault();
        console.log("Login Clicked!");
        const container = document.querySelector("body")
        fetch("../python/resources/loginform.py")
        .then(response => {
            return response.json()
        })
        .then(data => {
            container.innerHTML += data.html_content[0]
            console.log("Login Form Displayed!")
        })
        .catch(error => console.error("Error Displaying Form: ", error))   
    }
});

// submit login form
document.addEventListener("submit", function(event) {
    if (event.target.closest('.login-form')) {
        event.preventDefault();
        // variables
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        // logic
        console.log("Login Details Submitted!", username, password);
        validateLoginForm(username, password);
    }
});

// Query submitted in searchbar
document.addEventListener('submit', function(event) {
    const form = document.getElementById('form-search');

    if (event.target.matches('#form-search')) {
        // Prevent default action
        event.preventDefault();
    
        // Store search query
        const query = document.getElementById('query').value;
    
        // Log to Console
        console.log("Search Query submitted: " + query);
    
        // Update Url
        update_url(query, 'query');

        // Update page title
        update_page_title(query);
    
        // Call function to fetch using the new query in URL
        fetchSearchResults(); // save current page state > enter new page > display search results
    };
});

//-------------------------------------------- QUESTION ACTIONS ---------------------------------------------//

// ADD TO RADAR
document.addEventListener('click', function(event) {
    const clickedElement = event.target.closest('.addtoradardiv');
    if (clickedElement) {
        console.log("AddToRadar Clicked!");
        // Check current backgroundColor
        let container_style = window.getComputedStyle(clickedElement);
        let currentbgcolor = container_style.backgroundColor;

        // Initialise constants
        const addtoradartext = clickedElement.querySelector('.addtoradartext');
        const questionId = clickedElement.getAttribute('data-questionid');

        // Initialise Variables
        let count = parseInt(addtoradartext.textContent);
        let inc_or_dec;
        let ins_or_del;

        // Update Background Color and New Radar Count (Front End)
        if (currentbgcolor === 'rgb(128, 128, 128)') {
            console.log("Incrementing Radar Count");
            clickedElement.style.backgroundColor = '#4081B5';
            count++;
            inc_or_dec = 'inc';
            ins_or_del = 'ins';
        } else {
            clickedElement.style.backgroundColor = 'gray';
            if (count > 0){
                console.log("Decrementing Radar Count");
                count--;
                inc_or_dec = 'dec';
                ins_or_del = 'del';
            }
        };
        addtoradartext.textContent = count;

        // Call function that updates radar counts (Back End)
        update_question_radarCount(inc_or_dec, ins_or_del, questionId, count, userId);
    };
});

// SAVE
document.addEventListener('click', function(event) {
    if (event.target.closest('.savequestion')) {
        console.log("Save Question Clicked!");
        event.preventDefault();
        //variables
        const questionId = event.target.closest('.container-question').getAttribute('data-questionid');
        const savequestionbtn = event.target.closest('.savequestion');
        const bookmarkSwitch = savequestionbtn.getAttribute('data-bookmark-switch');
        let inc_or_dec = '';
        //logic
        if (bookmarkSwitch === "off") {
            savequestionbtn.dataset.bookmarkSwitch = 'on';
            console.log(savequestionbtn.dataset.bookmarkSwitch);
            savequestionbtn.innerHTML = `<i class="fa-solid fa-bookmark"></i>`;
            inc_or_dec = 'inc';
            console.log("Bookmark changed to dark!");
        }
        else {
            savequestionbtn.dataset.bookmarkSwitch = 'off';
            console.log(savequestionbtn.dataset.bookmarkSwitch);
            savequestionbtn.innerHTML = `<i class="fa-regular fa-bookmark"></i>`;
            inc_or_dec = 'dec';
            console.log("Bookmark changed to clear!");
        }
        update_question_savedCount(userId, questionId, inc_or_dec);
    };
});

// COPY LINK
function showcopied() {
    const div = document.querySelector('.copied');
    div.classList.add('show');
    console.log(div.classList);
    setTimeout(() => {
        div.classList.remove('show');
        console.log("Copied removed!");
    }, 3000);
};
document.addEventListener('click', function(event){
    const clickedElement = event.target.closest('.copylink')
    if (clickedElement) {
        const questionId = clickedElement.getAttribute('data-questionId');
        console.log(questionId);
        // Create link 
        const link = `${window.location.origin}${window.location.pathname}?questionId=${questionId}`;
        // Copy to clipboard
        navigator.clipboard.writeText(link)
        .then(function() {
            console.log('Link copied to clipboard!');
            showcopied();
        })
    };
});

// ------------------------------------------- ANCHORTAG LINKS ---------------------------------------------//

// click on specific user
document.addEventListener('click', function(event) {
    if (event.target.closest('.user-profile')) {
        event.preventDefault();
        const userId = event.target.closest('.user-profile').getAttribute('data-userid');
        console.log('User Clicked!', userId);
        savePageState('');
        update_url(userId, 'userId');
        viewuser();
        fetch_user_content('Questions', userId);
    };
});

// click on specific community
document.addEventListener('click', function(event) {
    if (event.target.closest('.user-community')) {
        event.preventDefault();
        const communityid = event.target.closest('.user-community').getAttribute('data-community-id');
        console.log('User Clicked!', communityid);
        savePageState('');
        update_url(communityid, 'communityid');
        viewcommunity();
        fetch_community_content('Timeline', communityid);
    };
});

// specific question
document.addEventListener('click', function(event){
    if (event.target.closest('.question-anchortag')) {
        event.preventDefault();
        // variables
        const question = event.target.closest('.container-question')
        const questionId = question.getAttribute('data-questionId');
        questioncontent = question.outerHTML;
        // logic
        console.log("Question Clicked: " + questionId);
        savePageState('');
        update_url(questionId, 'questionId');
        displayquestion(questioncontent);
    };
});

// my radar
document.addEventListener('click', function(event) {
    if (event.target.closest('.option-radar')) {
        event.preventDefault();
        //variables
        const userid = userId;
        //logic
        console.log("Fetching Radar Questions for " + userid);
    
        // save current page state > enter new page > display search results
        fetchRadarQuestions(userid); 
    };
})

//--------------------------------------------- PROFILE TABS ------------------------------------------------//

document.addEventListener('click', function(event) {
    clickedElement = event.target.closest('.tab');
    if (clickedElement) {
        name_of_tab = clickedElement.textContent;
        console.log("You have clicked on: ", name_of_tab);
        // variables
        const userId = document.querySelector('.username').getAttribute('data-userid');

        // CALL FUNCTION TO FETCH AND DISPLAY IN "user-content"
        fetch_user_content(name_of_tab, userId);
    };
});

// --------------------------------------------- MAIN -------------------------------------------------------//

    // PAGE REFRESHED
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentDetails();
});

    // USER GOES BACKWARD IN HISTORY
window.addEventListener('popstate', restorePageState);


