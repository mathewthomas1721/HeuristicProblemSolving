<!DOCTYPE html>
<html>

<link rel="stylesheet" type="text/css" href="incremental.css">
<h1>The Enterpren<i>Heurist</i> Game</h1>

<p>
<div class = "cashdisp" id = "cash" align = "right"></div>


<p>
<div class = "sectionAd" id = "adPane">
<div id = "advcount" align = "left" style = "font-weight: bold;">...</div>
<p>
<img src="nim.png" alt="Nim" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(1)">Add Constraints - Nim</button>
<span id = "tta1" class="tooltiptext">Testing</span>
</div>

<p>
<img src="ssp.jpg" alt="SSP" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(2)">Add Constraints - Stoplight</button>
<span id = "tta2" class="tooltiptext">Testing</span>
</div>

<p>
<img src="noTip.png" alt="noTip" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(3)">Add Constraints - NoTip</button>
<span id = "tta3" class="tooltiptext">Testing</span>
</div>

<p>
<img src="voronoi.png" alt="Voronoi" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(4)">Add Constraints - Voronoi</button>
<span id = "tta4" class="tooltiptext">Testing</span>
</div>

<p>
<img src="evasion.jpg" alt="Evasion" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(5)">Add Constraints - Evasion</button>
<span id = "tta5" class="tooltiptext">Testing</span>
</div>

<p>
<img src="dancing.jpg" alt="Dancing" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(6)">Add Constraints - Dancing</button>
<span id = "tta6" class="tooltiptext">Testing</span>
</div>

<p>
<img src="compatibility.jpg" alt="Compatibility" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(7)" style = "font-size: 0.65em;">Add Constraints - Compatibility</button>
<span id = "tta7" class="tooltiptext">Testing</span>
</div>

<p>
<img src="auction.jpg" alt="Auctions" style="width:40px;height:40px;display: block; margin-left: 50px;">
<div class="tooltip">
<button onclick="incremental.game.ApplyPenalty(8)">Add Constraints - Auction</button>
<span id = "tta8" class="tooltiptext">Testing</span>
</div>

</div>

<p>

<div class = "section" id = "sec1">
<img src="nim.png" alt="Nim" style="width:150px;height:100px;">
<br><br>
<div id = "prop1">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(1)" class = "buttonsize">Develop Algorithm 1</button>
<span id = "tt1" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(1)" class = "buttonsize">Improve Algorithm 1</button>
<span id = "ttu1" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC1"> Prop Cost </div><br><br><br>
<div id = "UC1"> Upgrade Cost </div>
</div>
</div>


<div class = "section" id = "sec2">
<img src="ssp.jpg" alt="SSP" style="width:150px;height:100px;">
<br><br>
<div id = "prop2">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(2)" class = "buttonsize">Develop Algorithm 2</button>
<span id = "tt2" class="tooltiptext" class = "buttonsize">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(2)" class = "buttonsize">Improve Algorithm 2</button>
<span id = "ttu2" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC2"> Prop Cost </div><br><br><br>
<div id = "UC2"> Upgrade Cost </div>
</div>
</div>

<div class = "section" id = "sec3">
<img src="noTip.png" alt="noTip" style="width:150px;height:100px;">
<br><br>
<div id = "prop3">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(3)" class = "buttonsize">Develop Algorithm 3</button>
<span id = "tt3" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(3)" class = "buttonsize">Improve Algorithm 3</button>
<span id = "ttu3" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC3"> Prop Cost </div><br><br><br>
<div id = "UC3"> Upgrade Cost </div>
</div>
</div>


<div class = "section" id = "sec4">
<img src="voronoi.png" alt="Voronoi" style="width:150px;height:100px;">
<br><br>
<div id = "prop4">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(4)" class = "buttonsize">Develop Algorithm 4</button>
<span id = "tt4" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(4)" class = "buttonsize">Improve Algorithm 4</button>
<span id = "ttu4" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC4"> Prop Cost </div><br><br><br>
<div id = "UC4"> Upgrade Cost </div>
</div>
</div>


<div class = "section" id = "sec5">
<img src="evasion.jpg" alt="Evasion" style="width:150px;height:100px;">
<br><br>
<div id = "prop5">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(5)" class = "buttonsize">Develop Algorithm 5</button>
<span id = "tt5" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(5)" class = "buttonsize">Improve Algorithm 5</button>
<span id = "ttu5" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC5"> Prop Cost </div><br><br><br>
<div id = "UC5"> Upgrade Cost </div>
</div>
</div>

<div class = "section" id ="sec6">
<img src="dancing.jpg" alt="Dancing" style="width:150px;height:100px;">
<br><br>
<div id = "prop6">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(6)" class = "buttonsize">Develop Algorithm 6</button>
<span id = "tt6" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(6)" class = "buttonsize">Improve Algorithm 6</button>
<span id = "ttu6" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC6"> Prop Cost </div><br><br><br>
<div  id = "UC6"> Upgrade Cost </div>
</div>
</div>

<div class = "section" id = "sec7">
<img src="compatibility.jpg" alt="Compatibility" style="width:150px;height:100px;">
<br><br>
<div id = "prop7">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(7)" class = "buttonsize">Develop Algorithm 7</button>
<span id = "tt7" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(7)" class = "buttonsize">Improve Algorithm 7</button>
<span id = "ttu7" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC7"> Prop Cost </div><br><br><br>
<div id = "UC7"> Upgrade Cost </div>
</div>
</div>

<div class = "section" id = "sec8">
<img src="auction.jpg" alt="Auction" style="width:150px;height:100px;">
<br><br>
<div id = "prop8">...</div>
<br><br>
<div class = "buttonalign">
<div class="tooltip">
<button onclick="incremental.game.BuyProp(8)" class = "buttonsize">Develop Algorithm 8</button>
<span id = "tt8" class="tooltiptext">Testing</span>
</div>
<br><br>
<div class="tooltip">
<button onclick="incremental.game.UpgradeProp(8)" class = "buttonsize">Improve Algorithm 8</button>
<span id = "ttu8" class="tooltiptext">Testing</span>
</div>
</div>
<div class = "buttontextdesc">
<div id = "PC8"> Prop Cost </div><br><br><br>
<div id = "UC8"> Upgrade Cost </div>
</div>
</div>

<div class = "resultsDiv" id = "resDiv">
  Testing
</div>

<div class="testdiv" id="startButtons">
  <button onclick="incremental.game.StartOnePlayer()" class = "buttonsize">Single Player Game</button>
  <button onclick="incremental.game.StartTwoPlayer()" class = "buttonsize">Two Player Game</button><br><br>
  <form id="timeSet">
  Time: <input type="number" name="time" value="0"> <br><br>Enter Game Duration<br> Enter zero for an infinite game<br>
</form>
</div>
<div class = "storydiv" id="story" >
  <p>
  The year is 2018. Flesh-eating Baby Snakes have devoured all non-heurists, society has collapsed, and the economy runs entirely on KitKat bars. With his seemingly endless stash of candy, Lord Shasha rules the business world. The only way to improve your station is to sell him algorithms that solve his problems. Get to work and become the greatest omniheurist in the land. Earn as many KitKats as you can, but watch out, Lord Shasha has been known to change his problems to make them more challenging.
  <p>
  The object of the EntreprenHeurist Game is to earn as many KitKits as possible in a set amount of time. You can enter a time limit (in seconds) below. By default, the game will run forever. The game can be played either as a classic single player incremental game, or as a two player, adversarial game.
  <p>
  In single player mode, you play as the entreprenheurist and aim to earn as many KitKats as possible by developing and improving algorithms for various games. As a programmer requires sugary fuel to work, it costs some of your KitKats to develop algorithms. Once developed, they will provide you a steady stream of income. Any improvements on your algorithm will cost more than the one before it. Use the mouse to choose your algorithms and upgrades.
  <p>
  In two player mode, the first player plays as the entreprenheurist and uses the mouse to develop and improve algorithms with the goal of earning as many KitKats as possible. The second player acts as Lord Shasha and adds new constraints to make an efficient algorithm harder to develop, and therefore more costly. The goal of the adversary is to apply these penalties in order to minimize the amount of KitKats the the entreprenheurist can earn. The adversary earns a penalty each time the entreprenheurist develops an algorithm and also when the player has been inactive for 20 seconds. The adversary applies these penalties using the number keys or mouse clicks.
</div>
<div class = "instructiontext" id = "ins">
  Key Mappings For Adversary :<br>
  1 : Add Constraints - Nim <br>
  2 : Add Constraints - Stoplight <br>
  3 : Add Constraints - NoTip <br>
  4 : Add Constraints - Voronoi <br>
  5 : Add Constraints - Evasion <br>
  6 : Add Constraints - Dancing <br>
  7 : Add Constraints - Compatibility <br>
  8 : Add Constraints - Auction <br>
</div>

<script src="__javascript__/incremental.js"></script>
</html>
