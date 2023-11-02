<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php
include('templates/header.php');
?>

<h1><?php echo $about_content[$lang][0];?></h1>

<p><?php echo $about_content[$lang][1];?></p>


<?php
include('templates/footer.php');
?>

</html>