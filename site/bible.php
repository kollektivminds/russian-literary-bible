<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include "templates/header.php";
?>

<script>

    window.onload = function () {

        bookArray = [];
        //console.log(bookArray);
        //console.log("window.ready");
                
        $.getJSON("data/booksDict.json", function(data) {
            json = data;
            console.log(json);
            bookArray = []
            $.each( data, function( key,val ) {
                //console.log(key);
                //console.log(data[key]["ru_name"]);
                bookArray.push(data[key]["<?php echo $lang?>_name"]);
            });
            console.log(bookArray);
            txt = "<option value='#' selected='selected'></option>";
            for (i = 0; i < bookArray.length; i++) {
                txt += "<option value='"+(i+1)+"'>"+bookArray[i]+"</option>";
            }
            document.getElementById("bookSelect").innerHTML = txt;
        });
    };
    
    $(document).ready(function () {
        $(document).on("change", "select[id='bookSelect']", function() {
            window.bookNum = $(this).val();
            console.log("bookNum: "+window.bookNum);
            chapLen = Object.keys(json[window.bookNum-1].chap_verse).length
            console.log(chapLen)
            txt = "<option value='#' selected='selected'></option>";
            for (i = 0; i < chapLen; i++) {
                txt += "<option value='"+(i+1)+"'>"+(i+1)+"</option>";
            }
            document.getElementById("chapterSelect").innerHTML = txt;
        });
    });
    $(document).ready(function () {
        $(document).on("change", "select[id='chapterSelect']", function() {
            window.chapNum = $(this).val();
            console.log("chapNum: "+window.chapNum);
            chapVers = json[window.bookNum-1].chap_verse[chapNum]
            console.log(chapVers)
            txt = "<option value='#' selected='selected'></option>";
            for (i = 0; i < chapVers; i++) {
                txt += "<option value='"+(i+1)+"'>"+(i+1)+"</option>";
            }
            document.getElementById("verseSelect").innerHTML = txt;
        });
    });
    $(document).ready(function() {
        $(document).on("change", "select[id='verseSelect']", function() {
            window.versNum = $(this).val();
            console.log("versNum: "+window.versNum);
        });
    });
</script>



<h1><?php echo $bible_content[$lang][0];?></h1>

<p><?php echo $bible_content[$lang][1];?></p>

<form>
    <input type="search" />
    <input type="submit" />
</form>

<hr>



<p><?php echo $bible_content[$lang][2];?></p>
    
<form name="biblePartSelector" id="bibleSelect" action="">
<?php echo $bible_content[$lang][3];?>: 
    <select name="book" id="bookSelect" onchange="">
        <option value="" selected="selected"><?php echo $bible_content[$lang][3];?></option>
    </select>    
<?php echo $bible_content[$lang][5];?>:
    <select name="chapter" id="chapterSelect" onchange="">
        <option value="" selected="selected"><?php echo $bible_content[$lang][4];?></option>
    </select>
<?php echo $bible_content[$lang][6];?>: 
    <select name="verse" id="verseSelect" onchange="">
        <option value="" selected="selected"><?php echo $bible_content[$lang][4];?></option>
    </select>
</form> 
<hr>
<div id="results">
    <p><?php echo $bible_content[$lang][7];?>:</p>
    <div id="results-text">
    <?php

    $contents = " ";

    // Initialize the XML parser
    $parser=xml_parser_create();

    // Function to use at the start of an element
    function start($parser,$element_name,$element_attrs) {
        echo "$element_name:$element_attrs<br>";
        switch($element_name) {
            case "v":
            echo "-- Note --<br>";
            break;
        }
    }

    // Function to use at the end of an element
    function stop($parser,$element_name) {
    echo "<br><hr>";
    }

    // Function to use when finding character data
    function char($parser,$data) {
    echo $data;
    }

    // Specify element handler
    xml_set_element_handler($parser,"start","stop");

    // Specify data handler
    xml_set_character_data_handler($parser,"char");

    // Open XML file
    $fp=fopen("data/bible.xml","r");

    // Read data
    while ($data=fread($fp,4096)) {
    xml_parse($parser,$data,feof($fp)) or
    die (sprintf("XML Error: %s at line %d",
    xml_error_string(xml_get_error_code($parser)),
    xml_get_current_line_number($parser)));
    }

    // Free the XML parser
    xml_parser_free($parser);
    ?> 
    </div>
</div>

<?php
include "templates/footer.php";
?>

</html>