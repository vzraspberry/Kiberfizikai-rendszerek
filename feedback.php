<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Data feedback</title>
</head>

<body>
<!---------------------------------->
<!--Oldal frissitése félpercenként-->
<!---------------------------------->

    <script>
        window.setInterval('refresh()', 10000);   // A FÜGGVÉNY HÍVÁSA MINDEN 10000 EZREDMÁSODPERCBEN AZAZ 10. MÁSODPERCBEN.
        // AZ OLDAL FRISSÍTÉSE, ÚJRATÖLTÉSE
        function refresh() {
            window.location.reload();
        }
    </script>

<!------------------------->   
<!--Adatbázis műveletek-->
<!------------------------->

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

//Hőmérséklet, páratartalom, légnyomás lekérdezés

$sql="SELECT datas.* FROM datas WHERE datas.id=(SELECT MAX(id) FROM datas)";
$result = $mysqli->query($sql);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array = $result->fetch_all(MYSQLI_ASSOC);
$tmp = "";
$hum = "";
$press = "";
$date = "";
$time = "";
if(isset($result_array[0])){
	$tmp = $result_array[0]["temp"];
	$hum = $result_array[0]["hum"];
	$press = $result_array[0]["press"];
	$date = $result_array[0]["date"];
	$time = $result_array[0]["time"];
}

//Bejárati ajtó állpota

$sql2="SELECT Door.* FROM Door WHERE Door.id=(SELECT MAX(id) FROM Door)";
$result2 = $mysqli->query($sql2);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array2 = $result2->fetch_all(MYSQLI_ASSOC);
$opn = "";
$cls = "";
if(isset($result_array2[0])){
	$opn = $result_array2[0]["open"];
	$cls = $result_array2[0]["close"];
}

//Nappali ablak bukó állpota

$sql3="SELECT win1t.* FROM win1t WHERE win1t.id=(SELECT MAX(id) FROM win1t)";
$result3 = $mysqli->query($sql3);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array3 = $result3->fetch_all(MYSQLI_ASSOC);
$opn3 = "";
$cls3 = "";
if(isset($result_array3[0])){
	$opn3 = $result_array3[0]["open"];
	$cls3 = $result_array3[0]["close"];
}

//Nappali ablak nyíló állpota

$sql4="SELECT win1o.* FROM win1o WHERE win1o.id=(SELECT MAX(id) FROM win1o)";
$result4 = $mysqli->query($sql4);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array4 = $result4->fetch_all(MYSQLI_ASSOC);
$opn4 = "";
$cls4 = "";
if(isset($result_array4[0])){
	$opn4 = $result_array4[0]["open"];
	$cls4 = $result_array4[0]["close"];
}

//Hálószoba ablak bukó állpota

$sql5="SELECT win2t.* FROM win2t WHERE win2t.id=(SELECT MAX(id) FROM win2t)";
$result5 = $mysqli->query($sql5);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array5 = $result5->fetch_all(MYSQLI_ASSOC);
$opn5 = "";
$cls5 = "";
if(isset($result_array5[0])){
	$opn5 = $result_array5[0]["open"];
	$cls5 = $result_array5[0]["close"];
}

//Hálószoba ablak nyíló állpota

$sql6="SELECT win2o.* FROM win2o WHERE win2o.id=(SELECT MAX(id) FROM win2o)";
$result6 = $mysqli->query($sql6);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array6 = $result6->fetch_all(MYSQLI_ASSOC);
$opn6 = "";
$cls6 = "";
if(isset($result_array6[0])){
	$opn6 = $result_array6[0]["open"];
	$cls6 = $result_array6[0]["close"];
}

//Legutolsó tűzjelzés

$sql7="SELECT fire.* FROM fire WHERE fire.id=(SELECT MAX(id) FROM fire)";
$result7 = $mysqli->query($sql7);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array7 = $result7->fetch_all(MYSQLI_ASSOC);
$firedat = "";
$firetime = "";
if(isset($result_array7[0])){
	$firedat = $result_array7[0]["date"];

  $firetime = $result_array7[0]["time"];
}

//Legutolsó áramszünet

$sql8="SELECT blackout.* FROM blackout WHERE blackout.id=(SELECT MAX(id) FROM blackout)";
$result8 = $mysqli->query($sql8);
if($mysqli->errno){
	die("Mysql hiba lekérdezéskor: ".$mysqli->errno.": ".$mysqli->error);
}
$result_array8 = $result8->fetch_all(MYSQLI_ASSOC);
$bodat = "";
$botime = "";
if(isset($result_array8[0])){
	$bodat = $result_array8[0]["date"];
  $botime = $result_array8[0]["time"];
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

<!------------------------>
<!--Adattábla felépitése-->
<!------------------------>

<table width="800">
        <tbody>
          <tr>
            <td width="238" height="144" align="center" valign="top"><table width="250" height="140">
              <tbody>
                <tr>
                  <td height="21" colspan="2"><strong>Komfort adatok:</strong></td>
                </tr>
                <tr>
                  <td width="120" height="21" align="left">Hőmérséklet:</td>
                  <td width="100" align="left"><strong><?php echo $tmp." 'C"; ?></strong></td>
                </tr>
                <tr>
                  <td width="120" height="21" align="left">Páratartalom:</td>
                  <td align="left"><strong><?php echo $hum." %"; ?></strong></td>
                </tr>
                <tr>
                  <td width="120" height="21" align="left">Légnyomás:</td>
                  <td align="left"><strong><?php echo $press." mBar"; ?></strong></td>
                </tr>
                <tr>
                  <td width="120" rowspan="2" align="left">Legutolsó mérés időpontja:</td>
                  <td height="20" align="left"><strong><?php echo $date; ?></strong></td>
                </tr>
                <tr>
                  <td height="20" align="left"><strong><?php echo $time; ?></strong></td>
                </tr>
              </tbody>
            </table>
            </td>
            <td width="550" align="center" valign="top"><table width="550">
              <tbody>
              </tbody>
              <tbody>
                <tr>
                  <td colspan="2" valign="middle" align="center"><strong>Ajtók/ablakok állapota</strong></td>
                  <td colspan="2" valign="middle" align="center"><strong>Események</strong></td>
                </tr>
                <tr>
                  <td width="170" align="left">Bejárat:</td>
                  <td width="120" valign="middle" align="left"><strong>
                    <?php if($opn==1){
                                                                      echo "Nyitva";
                                                                    }
                                                                    else{
                                                                      echo "Zárva";
                                                                    }
                  ?>                                                  
                  </strong></td>
                  <td width="120" rowspan="2" valign="top">Tűzjelzés:</td>
                  <td width="120"><strong><?php echo $firedat; ?></strong></td>
                </tr>
                <tr>
                  <td align="left">Nappali ablak bukó:</td>
                  <td width="120" valign="middle" align="left"><strong>
                    <?php if($opn3==1){
                                                                      echo "Nyitva";
                                                                    }
                                                                    else{
                                                                      echo "Zárva";
                                                                    }
                  ?> 
                  </strong></td>
                  <td width="120"><strong><?php echo $firetime; ?></strong></td>
                </tr>
                <tr>
                  <td align="left">Nappali ablak nyíló:</td>
                  <td width="120" valign="middle" align="left"><strong>
                    <?php if($opn4==1){
                                                                      echo "Nyitva";
                                                                    }
                                                                    else{
                                                                      echo "Zárva";
                                                                    }
                  ?>
                  </strong></td>
                  <td width="120">&nbsp;</td>
                  <td width="120">&nbsp;</td>
                </tr>
                <tr>
                  <td align="left">Háló ablak bukó:</td>
                  <td width="120" valign="middle" align="left"><strong>
                    <?php if($opn5==1){
                                                                      echo "Nyitva";
                                                                    }
                                                                    else{
                                                                      echo "Zárva";
                                                                    }
                  ?>
                  </strong></td>
                  <td width="120" rowspan="2" valign="top">Áramszünet:</td>
                  <td width="120"><strong><?php echo $bodat; ?></strong></td>
                </tr>
                <tr>
                  <td align="left">Háló ablak nyíló:</td>
                  <td width="120" valign="middle" align="left"><strong>
                    <?php if($opn6==1){
                                                                      echo "Nyitva";
                                                                    }
                                                                    else{
                                                                      echo "Zárva";
                                                                    }
                  ?>
                  </strong></td>
                  <td width="120"><strong><?php echo $botime; ?></strong></td>
                </tr>
              </tbody>
              <tbody>
              </tbody>
            </table></td>
          </tr>
        </tbody>
</table>
</body>
</html>