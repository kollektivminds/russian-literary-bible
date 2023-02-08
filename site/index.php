<!DOCTYPE html>

<?php
include('templates/translations.php');
include('templates/lang-trans.php');
?>

<?php 
include "templates/header.php";
?>
<p id="homeheader">
    <em><?php echo $index_content[$lang][0];?></em>
</p>

<p><?php echo $index_content[$lang][1];?></p>

<?php
include "templates/footer.php";
?>

</html>