<!DOCTYPE html>
<html>
<head>
    <?php $base = "../../" ?>
    <base href="../../">
    <script src="js/jquery-2.2.4.min.js"></script>
    <script src="js/facebox.js"></script>
    <link rel="stylesheet" type="text/css" href="css/facebox.css"/>
    <link rel="stylesheet" type="text/css" href="css/main.css"/>
    <link rel="stylesheet" type="text/css" href="css/bootstrap.css"/>
    <script type="text/javascript">
        jQuery(document).ready(function($) {
            $('a[rel*=facebox]').facebox()
        })
    </script>
</head>
<body>
<div class="container">
    <?php include "header.php"; ?>
<nav>
  <ul>
      <li><a href="">Home</a></li>
<!--    <li><a href="memory">Memory Game</a></li>-->
<!--    <li><a href="games/empty">Empty Template</a></li>-->
  </ul>
    <?php include $base."leftMenuGame.php"; ?>
</nav>
<article>
<div id="intro", class="jumbotron">
  <p>
  The year is 2018. Flesh-eating Baby Snakes have devoured all non-heurists, society has collapsed, and the economy runs entirely on KitKat bars. With his seemingly endless stash of candy, Lord Shasha rules the business world. The only way to improve your station is to sell him algorithms that solve his problems. Get to work and become the greatest omniheurist in the land. Earn as many KitKats as you can, but watch out, Lord Shasha has been known to change his problems to make them more challenging.
  <p>
  The object of the EntreprenHeurist Game is to earn as many KitKits as possible in a set amount of time. You can enter a time limit (in seconds) below. By default, the game will run forever. The game can be played either as a classic single player incremental game, or as a two player, adversarial game.
  <p>
  In single player mode, you play as the entreprenheurist and aim to earn as many KitKats as possible by developing and improving algorithms for various games. As a programmer requires sugary fuel to work, it costs some of your KitKats to develop algorithms. Once developed, they will provide you a steady stream of income. Any improvements on your algorithm will cost more than the one before it. Use the mouse to choose your algorithms and upgrades.
  <p>
  In two player mode, the first player plays as the entreprenheurist and uses the mouse to develop and improve algorithms with the goal of earning as many KitKats as possible. The second player acts as Lord Shasha and adds new constraints to make an efficient algorithm harder to develop, and therefore more costly. The goal of the adversary is to apply these penalties in order to minimize the amount of KitKats the the entreprenheurist can earn. The adversary earns a penalty each time the entreprenheurist develops an algorithm and also when the player has been inactive for 20 seconds. The adversary applies these penalties using the number keys or mouse clicks.
  <br><br><a href="https://cims.nyu.edu/~mmc691/drecco2016/games/TEG3/incremental.html" target="_blank">START GAME</a>
</div>
<!--h2><a href="images/loading.gif" rel="facebox">text</a-->
</article>
    <?php include "footer.php"; ?>
</div>

</body>

</html>
