<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include "templates/header.php";
?>

<?php 
/* foreach ($libTitles as $file_name) {
    $rawTitle = rtrim($file_name, ".xml");
    $cleanTitle = ucfirst($rawTitle);
    echo "<div id='$cleanTitle' class='text-div'>$cleanTitle text div</div>";
} */
?>


<hr>

<div id="displayTextParent">

<?php 
include "templates/displayText.php";
?>

</div>

<?php
include "templates/footer.php";
?>

</html>
