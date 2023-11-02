<?php
$en_select='';
$ru_select='';		
$lang='';
if((isset($_GET['lang']) && $_GET['lang']=='en') || !isset($_GET['lang'])){
	$en_select='selected';	
	$lang='en';
}else{
	$ru_select='selected';
	$lang='ru';
}
?>