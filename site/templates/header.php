<head>
    <meta charset="UTF-8">
    <title><?php echo $title[$lang];?></title>
    <meta name="description" contents="Website for Revolutionary Gospel">
    <meta name="keywords" content="russian, literature, bible" />
    <meta name="robots" content="noindex" />
    <link rel="stylesheet" href="css/style.css" type="text/css">
    <link rel="stylesheet" href="css/normalize.css" type="text/css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.3.min.js" integrity="sha256-pvPw+upLPUjgMXY0G+8O0xUf+/Im1MZjXxxgOcBQBXU=" crossorigin="anonymous"></script>
    <script>
        function set_language(){
            var language=jQuery('#lang').val();
            window.location.href='?lang='+language;
        }
    </script>
</head>
<body>
    <header>
        <nav id="nav-header">
            <a href="index.php"><img id="nav-logo" src="./img/favicon-32x32.png"></a>
            <ul id="nav-menu">
                <li class="nav-item"><a href="index.php"><?php echo $nav_menu[$lang][0];?></a></li>
                <li class="nav-item"><a href="about.php"><?php echo $nav_menu[$lang][1];?></a></li>
                <li class="nav-item"><a href="bible.php"><?php echo $nav_menu[$lang][2];?></a></li>
                <li class="nav-item"><a href="texts.php"><?php echo $nav_menu[$lang][3];?></a></li>
                <li class="nav-item">
                    <select onchange="set_language()" name="set_lang" id="lang">
                        <option value="en" <?php echo $en_select?>>ENG</option>
                        <option value= "ru" <?php echo $ru_select?>>РУС</option>
                    </select>
                </li>
            </ul>
        </nav>
    </header>
    <div id="page-contents">