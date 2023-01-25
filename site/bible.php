<!DOCTYPE html>

<?php
$pageTitle = "RG Bible"
?>

<?php
include "templates/header.php";
include "pages/about.html";


$xml=simplexml_load_file("../texts/bible/bible.xml") or die("Error: Cannot create object");
echo $xml->t[0]->b[0]->c[0]->v[0];

#print_r($xml);

include "templates/footer.php";
?>