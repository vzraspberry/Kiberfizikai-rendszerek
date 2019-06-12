<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Thermostat data mod</title>
</head>

<body>
	
	<form id="form1" name="form1" method="post" action="/feedback2.php" target="_self">
        <input type="submit" name="Submit" value="Ok" /></form>
	
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

$sql = "UPDATE thermostat SET value=$_POST[val] WHERE id=1";

if ($mysqli->query($sql) === TRUE) {
    echo "Hőmérséklet módositva";
} else {
    echo "Módositás sikertelen: " . $conn->error;
}

$mysqli>close();

?>

</body>
</html>
