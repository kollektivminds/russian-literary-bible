<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include "templates/header.php";
?>


<script>
    var textLoc = 'texts/mother.xml';

    $.ajax({
        type: "GET",
        url: textLoc,
        dataType: "xml",
        success: function(xml) {
            //remainder of the code
            $(xml).find('part').each(function() {
                _partName = $(this).attr("name");
                const _chapList = [];
                var _chapDict = {};
                $(this).find('chapter').each(function() {
                    var _chapName = $(this).attr("name");
                    var _chapN = $(this).attr("n");
                    console.log(_chapN);
                    _chapDict[_chapName] = _chapN;
                    $("#textDisplay").append("<h3 id='"+_chapN+"' class='workChapName'>"+_chapName+"</h3>");
                    $(this).find('paragraph').each(function () {
                        $("#textDisplay").append("<p class='work'>"+$(this).text()+"</p>");
                    });
                });
                $("#navDisplay").append("<p>Part "+_partName+": ");
                $.each(_chapDict, function( k , v ) {
                    $("#navDisplay").append("<a href='#"+v+"'>"+k+"</a> ");
                });
            });
        },
        //other code
        error: function() {
            alert("The XML File could not be processed correctly.");
            }
    });

    /*

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
        document.getElementById("textDisplay").innerHTML = txt;
    }

    function showBible(str) {
        if (str=="") {
            document.getElementById("results").innerHTML="";
            return;
        }
        
    }

    window.onload = function() {

        // load books list
        loadDoc(textLoc, getBooks);
        
    }

    $(document).ready(function () {
        $(document).on("change", "select[id='bookSelect']", function() {
            window.bookNum = $(this).val();
            console.log(window.bookNum);
        })

    $(document).ready(function () {
        $(document).on("change", "select[id='chapterSelect']", function() {
            window.chapNum = $(this).val();
            console.log(window.chapNum);
        })
    })

    })*/
</script>

<div id="navDisplay">

</div>
<hr>
<div id="textDisplay" style="overflow-x:hidden;overflow-y:auto;height:600px;">

</div>

<?php
include "templates/footer.php";
?>

</html>
