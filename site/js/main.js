// makes language changer selection a URL parameter on change
function set_language(){
    var language=jQuery('#lang').val();
    console.log("Lang is "+language);
    window.location.href='?lang='+language;
}