<?php
$en_select='';
$ru_select='';		
$lang='';
if(($_GET['lang']=='ru')){
	$ru_select='selected';	
	$lang='ru';
}else{
	$en_select='selected';
	$lang='en';
}
//echo "lang is $lang";
?>