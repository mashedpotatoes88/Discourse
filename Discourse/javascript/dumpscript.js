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
};

function test(num) {
    console.log("Test", num); 
}
