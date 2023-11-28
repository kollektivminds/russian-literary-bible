<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include "templates/header.php";
?>

<script>
    const queryString = window.location.search;
    //console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    const bookSelected = urlParams.get('book');
    const chapSelected = urlParams.get('chapter');
    const versSelected = urlParams.get('verse');
    window.onload = function () {

        $.getJSON("data/booksDict.json", function(data) {
            json = data;
            //console.log(json);
            bookArray = []
            $.each( data, function( key,val ) {
                //console.log(key);
                //console.log(data[key]["ru_name"]);
                bookArray.push(data[key]["<?php echo $lang?>_name"]);
            });
            console.log(bookArray);
            
            if (!bookSelected) {
                //console.log("bookSelected is null");
                txt = "<option value='' selected></option>";
                for (i = 0; i < bookArray.length; i++) {
                    txt += "<option value='"+(i+1)+"'>"+bookArray[i]+"</option>";
                }
                document.getElementById("bookSelect").innerHTML = txt;
            } else {
                console.log("bookSelected is not null: "+bookSelected);
                txt = "<option value=''></option>";
                for (i = 0; i < bookArray.length; i++) {
                    if ((i+1) == bookSelected) {
                        txt += "<option value='"+(i+1)+"' selected>"+bookArray[i]+"</option>";
                    } else {
                        txt += "<option value='"+(i+1)+"'>"+bookArray[i]+"</option>";
                    }
                    //document.getElementById("bookSelect").innerHTML = txt;
                }
                document.getElementById("bookSelect").innerHTML = txt;
                if (!chapSelected) {
                    $("#bookSelect").trigger("change");
                } else {
                    console.log("chapSelected is not null: "+chapSelected);
                    chapLen = Object.keys(json[bookSelected].chap_verse).length;
                    txt = "<option value=''></option>";
                    for (i = 1; i < (chapLen+1); i++) {
                        if (i == chapSelected) {
                            txt += "<option value='"+i+"' selected>"+i+"</option>";
                        } else {
                            txt += "<option value='"+i+"'>"+i+"</option>";
                        }
                        //document.getElementById("bookSelect").innerHTML = txt;
                    }
                    document.getElementById("chapterSelect").innerHTML = txt;
                    if (!versSelected) {
                        $("#chapterSelect").trigger("change");
                    } else {
                        console.log("versSelected is not null: "+versSelected);
                        versLen = json[bookSelected].chap_verse[chapSelected];
                        txt = "<option value=''></option>";
                        for (i = 1; i < versLen+1; i++) {
                            if (i == versSelected) {
                                txt += "<option value='"+i+"' selected>"+i+"</option>";
                            } else {
                                txt += "<option value='"+i+"'>"+i+"</option>";
                            }
                            
                        
                    }
                    document.getElementById("verseSelect").innerHTML = txt;
                    }
                }
                
            }
        });
    };
    
    $(document).ready(function () {
        $(document).on("change", "select[id='bookSelect']", function() {
            $bookNum = $(this).val();
            chapLen = Object.keys(json[$bookNum].chap_verse).length;
            txt = "<option value='' selected='selected'></option>";
            for (i = 0; i < chapLen; i++) {
                txt += "<option value='"+(i+1)+"'>"+(i+1)+"</option>";
            }
            document.getElementById("chapterSelect").innerHTML = txt;
            document.getElementById("verseSelect").innerHTML = "<option value='' selected='selected'></option>";
        });
    });
    $(document).ready(function () {
        $(document).on("change", "select[id='chapterSelect']", function() {
            $chapNum = $(this).val();
            //console.log("chapNum: "+$chapNum);
            if (typeof $bookNum === 'undefined') {
                $bookNum = bookSelected;
                $chapNum = chapSelected;
            }
            $chapVers = json[$bookNum].chap_verse[$chapNum];
            //console.log($chapVers);
            txt = "<option value='' selected='selected'></option>";
            for (i = 0; i < $chapVers; i++) {
                txt += "<option value='"+(i+1)+"'>"+(i+1)+"</option>";
            }
            document.getElementById("verseSelect").innerHTML = txt;
        });
    });
    $(document).ready(function() {
        $(document).on("change", "select[id='verseSelect']", function() {
            window.versNum = $(this).val();
            //console.log("versNum: "+window.versNum);
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
    
<form name="biblePartSelector" id="bibleSelect" action="" method="get">
<?php echo $bible_content[$lang][3];?>: 
    <select name="book" id="bookSelect" onchange=""></select>    
<?php echo $bible_content[$lang][5];?>:
    <select name="chapter" id="chapterSelect" onchange=""></select>
<?php echo $bible_content[$lang][6];?>: 
    <select name="verse" id="verseSelect" onchange=""></select>
    <input type="submit" name="submit" value="submit">
</form> 
<hr>
<div id="results">
    <p><?php echo $bible_content[$lang][7];?>:</p>
    <div id="results-text">
    <?php
    $myXml=simplexml_load_file("./data/bible.xml");

    if(isset($_GET["book"])) {
        $book=$_GET["book"];
        $bookXpath = "b[@n=".strval($book)."]";
        $textXml = $myXml->xpath($bookXpath)[0];
        $bookName_ru = $textXml['name_ru'];
        $bookName_en = $textXml['name_en'];
    }

    if(isset($_GET["chapter"])) {
        $chap=$_GET["chapter"];
        $chapXpath = "c[@n=".strval($chap)."]";
    }

    if(isset($_GET["verse"])) {
        $vers=$_GET["verse"];
        $versXpath = "v[@n=".strval($vers)."]";
    }

    switch ($lang) {
        case 'ru':
            echo "<br>$bookName_ru<br>";
            break;
        
        case 'en':
            echo "<br>$bookName_en<br>";
            break;
    }

    // process textXml
    if(empty($_GET["book"])) {
        //$randBook = rand(1,77);
        $textXml = $myXml->xpath("b[@n='1']")[0]->children()[0];
        //print_r($textXml);
        for ($i=1; $i < $textXml->children()->count(); $i++) { 
            echo "1:$i ";
            echo $textXml->children()[($i-1)]."<br>";
        }
    } elseif (empty($_GET["chapter"]) && empty($_GET["verse"])) {
        for ($h=0; $h < $textXml->children()->count(); $h++) {
            $chapName = $textXml->children()[$h]['name'];
            echo "<br>Chapter $chapName<br><br>";
            for ($i=0; $i < $textXml->children()[$h]->children()->count(); $i++) { 
                echo $chapName.":".($i+1)." ";
                echo $textXml->children()[$h]->children()[$i]."<br>";
            }
        }
    } elseif (isset($_GET["chapter"]) && empty($_GET["verse"])) {
        //echo "print full chapter (".$_GET["chapter"].")<br>";
        $chapXml = $textXml->children()[(intval($_GET["chapter"])-1)];
        for ($i=0; $i < $chapXml->children()->count(); $i++) { 
            echo "<br>Verse ".($i+1).": ";
            echo $chapXml->children()[$i]."<br>";
        }
    } elseif (isset($_GET["chapter"]) && isset($_GET["verse"])) {
        echo "<br>".$_GET["chapter"].":".$_GET["verse"]." ";
        echo $textXml->children()[(intval($_GET["chapter"])-1)]->children()[(intval($_GET["verse"])-1)];
    } else {
        echo "something went wrong";
    }
    ?> 
    </div>
</div>

<?php
include "templates/footer.php";
?>

</html>