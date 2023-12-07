// makes language changer selection a URL parameter on change
function setLanguage(language){
    console.log("Lang is "+language);
    setCookie("lang", language, 99);
    location.reload();
    //window.location.href='?lang='+language;
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    console.log("decodedCookie = ");
    console.log(decodedCookie);
    let ca = decodedCookie.split(';');
    console.log("ca = ");
    console.log(ca);
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function checkCookie() {
    let lang = getCookie("lang");
    console.log("lang is " + lang);
    if ((lang != "en") && (lang != "ru")) {
        console.log("cookie is not 'en' or 'ru'");
    } else {
        $(".overlay").hide();
    }
}

$( document ).ready(function() {
    checkCookie();
});