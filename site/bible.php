<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include "templates/header.php";
?>

<h1><?php echo $bible_content[$lang][0];?></h1>

<script>

    var bibLoc = 'data/bible.xml';

    // example: loadDoc("url", myFunction);
    function loadDoc(url, cFunction) {
        var xhttp;
        xhttp=new XMLHttpRequest();
        xhttp.onreadystatechange=function() {
            if (this.readyState==4 && this.status==200) {
                cFunction(this);
            }
        };
        xhttp.open("GET", url, true);
        xhttp.send();
    }

    // getBooks(xhttp) {}
    function getBooks(xhttp) {
        xmlDoc = xhttp.responseXML;
        txt = "<option value='#' selected='selected'><?php echo $bible_content[$lang][3];?></option>";
        x = xmlDoc.getElementsByTagName("b");
        for (i = 0; i < x.length; i++) {
            txt += "<option value='"+x[i].getAttribute("n")+"'>"+x[i].getAttribute("name")+"</option>";
        }
        document.getElementById("bookSelect").innerHTML = txt;
    }
    
    // getChaps() {}
    function getChaps(xhttp) {
        xmlDoc = xhttp.responseXML;
        txt = "<option value='#' selected='selected'><?php echo $bible_content[$lang][4];?></option>";
        x = xmlDoc.getElementsByTagName("b")[(window.bookNum-1)].getElementsByTagName("c");
        for (i = 0; i < x.length; i++) {
            txt += "<option value='"+x[i].getAttribute("name")+"'>"+x[i].getAttribute("name")+"</option>";
        }
        document.getElementById("chapterSelect").innerHTML = txt;
    }

    // getVers() {}
    function getVers(xhttp) {
        xmlDoc = xhttp.responseXML;
        txt = "<option value='#' selected='selected'><?php echo $bible_content[$lang][5];?></option>";
        x = xmlDoc.getElementsByTagName("b")[(window.bookNum-1)].getElementsByTagName("c")[(window.chapNum-1)].getElementsByTagName("v");
        for (i = 0; i < x.length; i++) {
            txt += "<option value='"+x[i].getAttribute("name")+"'>"+x[i].getAttribute("name")+"</option>";
        }
        document.getElementById("verseSelect").innerHTML = txt;
    }

    function showBible(str) {
        if (str=="") {
            document.getElementById("results").innerHTML="";
            return;
        }
        
    }
    
    window.onload = function() {

        // load books list
        loadDoc(bibLoc, getBooks);
        
    }

    $(document).ready(function () {
        $(document).on("change", "select[id='bookSelect']", function() {
            window.bookNum = $(this).val();
            console.log(window.bookNum);
            loadDoc(bibLoc, getChaps);
        })
    
    $(document).ready(function () {
        $(document).on("change", "select[id='chapterSelect']", function() {
            window.chapNum = $(this).val();
            console.log(window.chapNum);
            loadDoc(bibLoc, getVers);
        })
    })

    })

</script>

<p><?php echo $bible_content[$lang][1];?></p>

<form>
    <input type="search" />
    <input type="submit" />
</form>

<p><?php echo $bible_content[$lang][2];?></p>
    
<form name="biblePartSelector" id="bibleSelect" action="">
<?php echo $bible_content[$lang][3];?>: 
    <select name="book" id="bookSelect" onchange=""><?php echo $bible_content[$lang][4];?></select>
    <?php echo $bible_content[$lang][5];?>:
    <select name="chapter" id="chapterSelect">
        <option value="" selected="selected"><?php echo $bible_content[$lang][4];?></option>
    </select>
    <?php echo $bible_content[$lang][6];?>: 
    <select name="verse" id="verseSelect">
        <option value="" selected="selected"><?php echo $bible_content[$lang][4];?></option>
    </select>
</form> 
<hr>
<div id="results">
    <p><?php echo $bible_content[$lang][7];?>:</p>
</div>

<?php
include "templates/footer.php";
?>

</html>