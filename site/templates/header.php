<head>
    <meta charset="UTF-8">
    <title><?php echo $title[$lang]; ?></title>
    <meta name="description" contents="Website for Revolutionary Gospel">
    <meta name="keywords" content="russian, literature, bible, dissertation, digital, humanities" />
    <meta name="robots" content="noindex" />
    <link rel="stylesheet" href="css/style.css" type="text/css">
    <link rel="stylesheet" href="css/normalize.css" type="text/css">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>
    <script src="js/main.js" type="text/javascript"></script>
</head>

<body>
    <header>
        <nav id="nav-header">
            <a href="index.php"><img id="nav-logo" src="./img/favicon-32x32.png"></a>
            <ul id="nav-menu">
                <li class="nav-item"><a href="/index.php"><?php echo $nav_menu[$lang][0]; ?></a></li>
                <li class="nav-item"><a href="/about.php"><?php echo $nav_menu[$lang][1]; ?></a></li>
                <li class="nav-item"><a href="/bible.php"><?php echo $nav_menu[$lang][2]; ?></a></li>
                <li class="nav-item"><a href="/texts.php"><?php echo $nav_menu[$lang][3]; ?></a></li>
                <li class="nav-item"><a href="/portfolio.php"><?php echo $nav_menu[$lang][4];?></a></li>
            </ul>
            <select onchange="setLanguage(this.value)" name="set_lang" id="lang">
                <option value="en">eng</option>
                <option value="ru">рус</option>
            </select>
        </nav>
    </header>
    <div id="page-contents">