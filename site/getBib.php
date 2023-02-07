<?php

$q=$_GET["q"];

$bibleXML = new DOMDocument();
$bibleXML->load("./data/bible.xml")/*  or die("Error: Cannot create object") */;
$bible = $bibleXML->documentElement;

foreach ($bible->getElementsByTagName('b') as $bibbook) {
    $bibbook->getAttribute('name');
}
?>