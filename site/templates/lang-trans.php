<?php
$en_select='';
$ru_select='';		
//$lang='';
if(isset($_GET['lang']) && ($_GET['lang']=='ru')){
	$ru_select='selected';	
	$lang='ru';
}else{
	$en_select='selected';
	$lang='en';
}
?>