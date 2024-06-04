// DEFINING FUNCTIONS
let userId 
let username 
let communityid 
let radarCount 
let notificationsCount 
let lastOnline 
let communityname
let questioncontent

function test(num) {
    console.log("Test", num); 
}

// EXECUTING A SEARCH
function extract_query(url) {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('query');
    return query;
};
function fetchSearchResults() {
    query = extract_query();  
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
function displayquestion(_innerhtml) {
    const urlParams = new URLSearchParams(window.location.search);
    const questionId = urlParams.get('questionId');
    if (questionId) {
        showquestion(questionId, _innerhtml);
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
        })
        .catch(error => console.error("Error Fetching Answers: ", error))
    };
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
    console.log("Page State Saved: ", history.state.pageState);
};
function restorePageState(event) {
    console.log(history.state.pageState);
    const {state} = event;
    if (state && state.pageState) {
        document.documentElement.innerHTML = state.pageState.htmlContent;
        document.getElementById('query').innerHTML = state.pageState.searchquery;
        console.log("Page restored!");
    }
    else{
        console.log("Page not restored!");
    }
};
function update_url(query) {
    if (query === '' ) {
        const newUrl = `${window.location.origin}${window.location.pathname}`;
        history.pushState('', '', newUrl);
        console.log("Url Updated: ", newUrl);
    }
    else {
        const newUrl = `${window.location.origin}${window.location.pathname}?query=${query}`;
        history.pushState('', '', newUrl);
        console.log("Url Updated: ", newUrl);
    }
};

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
function setUserDetails() {
    const container = document.querySelector('.user-community');
    container.innerHTML = 'UON/' + communityname;
    console.log("User's Community Set: " + communityname);
};
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
    fetch("../python/resources/validateuser.py", {
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
        console.log("...Database Updated!")
    })
    .catch(error => console.error("Error updating radar counts in Database: ", error))

};






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

// MY COMMUNITIES
document.querySelector('.option-mycommunities').addEventListener('click', function() {
    const dropdown = document.querySelector('.dropdown-community');
    console.log("My Communities Clicked!")
    if (dropdown.style.display === 'none' || dropdown.style.display === '') {
        dropdown.style.display = 'block';       
    } else {
        dropdown.style.display = 'none';
    }
});

// QUERY SUBMITTED IN SEARCHBAR
document.addEventListener('submit', function(event) {
    if (event.target.matches('#form-search')) {
        event.preventDefault();
        console.log("matches #form-search");
        document.getElementById('form-search').addEventListener('submit', function(formSubmitted) {
            // Prevent default action
            formSubmitted.preventDefault();
        
            // Store search query
            const query = document.getElementById('query').value;
        
            // Log to Console
            console.log("Search Query submitted: " + query);
        
            // Update Url
            update_url(query);
        
            // Call function to fetch using the new query in URL
            fetchSearchResults(); // save current page state > enter new page > display search results
        });
    }
    else{
        console.log("No Search Query Submitted");
    };
})

// USER CLICKS ON PROFILE

// USER CLICKS ON ADD TO RADAR
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


// USER CLICKS ON COPY LINK
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

// USER HOVERS OVER QUESTION
document.addEventListener('mouseover', function(event){
    const hoveredElement = event.target.closest('.question-anchortag');
    if (hoveredElement) {
        const questionId = hoveredElement.getAttribute('data-questionId');
        const userId = hoveredElement.getAttribute('data-userId');

    }


});

// USER CLICKS ON QUESTION
document.addEventListener('click', function(event){
    const clickedElement = event.target.closest('.question-anchortag');
    const question = event.target.closest('.container-question')
    if (clickedElement) {
        event.preventDefault();
        const questionId = question.getAttribute('data-questionId');
        questioncontent = question.outerHTML;
        console.log("Question Clicked: " + questionId);
        displayquestion(questioncontent);
    };
});

// PAGE REFRESHED
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentDetails();
    setUserDetails();
    update_url('');
    savePageState();
});

// USER GOES BACKWARD IN HISTORY
window.addEventListener('popstate', restorePageState);

// USER CLICKS ON DROPDOWN UNDER MY COMMUNITIES

