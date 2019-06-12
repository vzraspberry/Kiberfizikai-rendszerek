<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Thermostat feedback and adjustment</title>
</head>

<body>

 <?php
$servername = "localhost";
$username = "phpmyadmin";
$password = "raspberry";

$database = "phpmyadmin";

$mysqli = new mysqli($servername, $username, $password, $database);

if($mysqli->connect_errno){
	die("Mysql hiba csatlakozáskor: ".$mysqli->connect_errno.": ".$mysqli->connect_error);
}
else{
	$mysqli->set_charset("utf8");
	if($mysqli->errno){
		die("Mysql hiba a karakterkészlet beállításakor: ".$mysqli->errno.": ".$mysqli->error);
	}
}

//Aktuális thermosztát beállítás

$sql9="SELECT thermostat.* FROM thermostat WHERE thermostat.id=(SELECT MAX(id) FROM thermostat)";
$result9 = $mysqli->query($sql9);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array9 = $result9->fetch_all(MYSQLI_ASSOC);
$value = "";
if(isset($result_array9[0])){
	$value = $result_array9[0]["value"];
}
?>

<table width="500">
  <tbody>
    <tr>
      <td width="200"align="right" valign="middle">Thermostat aktuális beállitás:</td>
      <td width="100"align="center" valign="middle"><B><?php echo $value." 'C"; ?></B></td>
      <td width="200"align="left" valign="middle"><form id="form1" name="form1" method="post" action="/thermin.php" target="_self">
      	<label for="textfield">Új érték:</label><br>
      	<input type="text" maxlength="4" name="val" id="textfield" ><br>
        <input type="submit" name="Submit" value="Módositás" /></form>
      </td>
    </tr>
  </tbody>
</table>
</body>
</html>
