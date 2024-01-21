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
$libTitles = array_diff(scandir($libLoc), array('.', '..'));
foreach ($libTitles as $file_name) {
    $rawTitle = rtrim($file_name, ".xml");
    $cleanTitle = ucfirst($rawTitle);
    echo "<div id='$cleanTitle' class='text-div'><a class='text-link' href='#'>$cleanTitle</a></div>";
};
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
