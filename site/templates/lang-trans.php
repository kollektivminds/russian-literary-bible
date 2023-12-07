<?php
$en_select='';
$ru_select='';		
//$lang='';

if(isset($_COOKIE['lang'])){
	$lang = $_COOKIE['lang'];
} else if ($_COOKIE['lang']=='ru'){
	$ru_select='selected';	
	$lang='ru';
} else {
	$en_select='selected';
	$lang='en';
}
?>