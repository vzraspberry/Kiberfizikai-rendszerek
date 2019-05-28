<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Untitled Document</title>
</head>

<body>
<table width="300" align="center">
  <tbody>
    <tr>
      <td align="center" valign="middle"><label for="textfield">Új hőmérséklet érték:</label>
      <input name="value" type="number" /></td>
    </tr>
    <tr>
      <td align="center" valign="middle"><input name="submit" type="submit" id="submit" formmethod="POST" value="Bevitel">
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

$sql = "UPDATE thermostat SET value=\"$_POST[value]\" WHERE id=1";

if ($conn->query($sql) === TRUE) {
    echo "Hőmérséklet módositva";
} else {
    echo "Módositás sikertelen: " . $conn->error;
}

$conn->close();

?>

</td>
    </tr>
  </tbody>
</table>
</body>
</html>