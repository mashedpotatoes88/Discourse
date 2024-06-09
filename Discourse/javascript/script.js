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

function test(num) {
    console.log("Test", num); 
}

// EXECUTING A SEARCH
function extract_from_url() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('query');
    return query;
};
function fetchSearchResults() {
    query = extract_from_url();  
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
function displayuser(userid) {
    fetch()
}
function fetchRadarQuestions(userid) {     
    fetch(`../test.py`, {
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
        data.html_content.forEach(html => {
            container.innerHTML += html; 
        });
        if (data.html_content) {
            savePageState(query);
        };
    });
    console.log("Fetch Complete!");
};
function fetch_user_content(_name_of_tab, _userid) {
    console.log("Fetching results for ", _name_of_tab, " and ", _userid);
    fetch("../discoursedb/questions/profiletabs.py", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: JSON.stringify({
            userid : _userid,
            name_of_tab : _name_of_tab
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        parent = document.querySelector('.user-content');
        parent.innerHTML = '';
        data.html_content.forEach(html => {
            parent.innerHTML += html;
        });
    });
};
function update_url_question(questionId) {
    if (questionId === '' ) {
        const newUrl = `${window.location.origin}${window.location.pathname}`;
        history.pushState('', '', newUrl);
        console.log("Url Updated: ", newUrl);
    }
    else {
        const newUrl = `${window.location.origin}${window.location.pathname}?questionId=${questionId}`;
        history.pushState('', '', newUrl);
        console.log("Url Updated: ", newUrl);
    };
}

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
        console.log(window.location.origin, window.location.pathname);
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
function saveCurrentDetails() {
    let userDetails = [userId, username, communityid, radarCount, notificationsCount, communityname];
    console.log("User Details Saved: " + userDetails);
    localStorage.setItem('userDetails', JSON.stringify(userDetails));
};
function loadCurrentDetails() {
    let userDetailsJson = localStorage.getItem('userDetails')
    if (userDetailsJson) {
        let userDetails= JSON.parse(userDetailsJson);
        updateUserDetails(userDetails[0], userDetails[1], userDetails[2], userDetails[3], userDetails[4], userDetails[5]);
    };
};
function updateUserDetails(_userId, _username, _community, _radarCount, _notificationsCount, _communityname) {
    userId = _userId;
    username = _username;
    communityid = _community;
    radarCount = _radarCount;
    notificationsCount = _notificationsCount;
    communityname = _communityname;
};
        // using the details to update elements
function updateProfile() {
    removeForm("loginbtn");
    const container = document.querySelector('.profile');

    const anchor = document.createElement('a');
    anchor.href = "#";
    anchor.textContent = '@' + username;
    console.log("Anchor Tag Created!")
    
    const div = document.createElement('div');
    div.classList.add('user-username');
    div.appendChild(anchor);
    
    container.appendChild(div);
    console.log("Div Created!")
};

// FUNCTIONS FOR LOCAL STORAGE
function saveSearchToLocalStorage(query, results) {
    localStorage.setItem('searchQuery', query);
    localStorage.setItem('searchResults', JSON.stringify(results));
};
function displaySavedSearchResults(results) {
    const container = document.getElementsByClassName('container-feed')[0]; 
    container.innerHTML = ''; 
    results.forEach(html => {
        container.innerHTML += html;
    }) 
};

// FUNCTIONS TO DO WITH FORM
function removeForm(csselement) {
    document.querySelector('.' + csselement).remove();
};
function validateLoginForm(_username, _password) {
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
        // UPDATE GLOBAL VARIABLES userId, username, community, radarCount, notificationsCount and lastOnline
        data_array = data.html_content;
        updateUserDetails(data_array[0], data_array[1], data_array[2], data_array[3], data_array[4], data_array[5]);
        console.log("Login Successful!");
        // removeForm("tray-login-form");
        saveCurrentDetails();
    })
    .catch(error => console.error("Error Validating Login Details: ", error))
    return false;
};

// UPDATE DATABASE
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


//------------------------------------------------- EVENT LISTENERS -----------------------------------------//

    // LOG IN
document.querySelector(".btn-login").addEventListener("click", function(loginClicked){
    loginClicked.preventDefault();
    console.log("Login Clicked!");
    const container = document.querySelector("body")
    fetch("../python/resources/loginform.py")
    .then(response => {
        return response.json()
    })
    .then(data => {
        container.innerHTML += data.html_content[0]
        console.log("Login Form Displayed!")

        // WHEN USER SUBMITS LOGIN FORM
        document.querySelector(".login-form").addEventListener("submit", function(loginFormSubmitted) {
        loginFormSubmitted.preventDefault();
        console.log("Login Details Submitted!");
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        validateLoginForm(username, password);
        updateProfile();
        removeForm("tray-login-form");
    });
    })
    .catch(error => console.error("Error Displaying Form: ", error))   
});

    // QUERY SUBMITTED IN SEARCHBAR
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

    // USER CLICKS ON SAVE


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

    // USER CLICKS ON user
document.addEventListener('click', function(event) {
    if (event.target.matches('.user-profile')) {
        userId = document.querySelector('.user-profile').getAttribute('data-userId');
        update_url(userId, 'userId');
    }
});

    // USER CLICKS ON QUESTION
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

    // USER CLICKS ON MY RADAR
document.addEventListener('click', function(event) {
    if (event.target.closest('.option-radar')) {
        event.preventDefault();
        document.querySelector('.option-radar').addEventListener('click', function(myradarclicked) {
            // Prevent default action
            myradarclicked.preventDefault();

            const userid = userId;
        
            // Log to Console
            console.log("Fetching Radar Questions for " + userid);
        
            // Call function to fetch using the new query in URL
            fetchRadarQuestions(userid); // save current page state > enter new page > display search results
        });
    };
})

//-------------------------------------------------- PROFILE TABS -------------------------------------------//

document.addEventListener('click', function(event) {
    clickedElement = event.target.closest('.tab');
    if (clickedElement) {
        name_of_tab = clickedElement.textContent;
        console.log("You have clicked on: ", name_of_tab);

        // CALL FUNCTION TO FETCH AND DISPLAY IN "user-content"
        fetch_user_content(name_of_tab, userId);
    };
});

// ----------------------------------------------------- MAIN -----------------------------------------------//

    // PAGE REFRESHED
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentDetails();
    update_url('');
});

    // USER GOES BACKWARD IN HISTORY
window.addEventListener('popstate', restorePageState);


