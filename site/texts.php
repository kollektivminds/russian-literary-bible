<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include "templates/header.php";
?>

<?php

$libLoc = './texts/';

?>

<script>
    const libLoc = './texts'
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
                    //console.log(_chapN);
                    _chapDict[_chapName] = _chapN;
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

    /* $(document).ready(function() {
        $("").click(function(){
            $(this).parents("").hide();
        });
    });

    $("#textDisplay").append("<h3 id='"+_chapN+"' class='workChapName'>"+_chapName+"</h3>");
    $(this).find('paragraph').each(function () {
        $("#textDisplay").append("<p class='work'>"+$(this).text()+"</p>");
    }); */
    
    /*var _chapDiv = document.createElement('div');
    _chapDiv.setAttribute('class', 'chapText');
    _chapDiv.setAttribute('id', _chapN);
    _chapDiv.append("<h3 id='"+_chapN+"'>"+_chapName+"</h3>");
    //$("#textDisplay").append("<div id='"+_chapN+"' class='chapText' style='border:2px solid black;'><h3 id='"+_chapN+"' class='workChapName'>"+_chapName+"</h3>");
    $(this).find('paragraph').each(function () {
        _chapDiv.append("<p class='work'>"+$(this).text()+"</p>");
    });
    $("#textDisplay").html(_chapDiv);*/
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
