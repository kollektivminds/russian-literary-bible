        </div>
        <script>
            // keeps search string between pages (e.g. "lang=ru")
            var searchString = new URL(window.location).search;
            if (searchString.includes("lang=")) {
                document.querySelectorAll("[href]").forEach(link => {
                        if (link.href.startsWith("/") || link.href.startsWith(".") || (link.href.startsWith("http") && link.href.includes(window.location.hostname)) && (link.href.endsWith(".php"))) {
                                var current = link.href;
                                link.href = current + searchString;
                                console.log(link.href);
                        }
                });
            }
            
        </script>
        <footer>
            <nav id="nav-footer">
            <ul id="nav-menu">
                <li class="nav-item"><a href="index.php"><?php echo $nav_menu[$lang][0];?></a></li>
                <li class="nav-item"><a href="about.php"><?php echo $nav_menu[$lang][1];?></a></li>
                <li class="nav-item"><a href="bible.php"><?php echo $nav_menu[$lang][2];?></a></li>
                <li class="nav-item"><a href="texts.php"><?php echo $nav_menu[$lang][3];?></a></li>
            </ul>
            </nav>
            <p id="copyright">&copy; Aaron M. Thompson <?php echo date("Y"); ?></p>
        </footer> 
    </body>