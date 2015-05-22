$(document).ready(function() {

    $("div[id^=my-][id$=-cred] h2,h3").click(function() {
        $(this).siblings("div").toggle("fast");
    });
    
    $("div[id^=my-][id$=-cred] div").hide();
});