<?php

$filepath = '@CENTREON_ETC@/centreon.conf.php';
//$filepath = '/etc/centreon/centreon.conf.php';

if (file_exists($filepath)) {
	include($filepath);
	$connect = mysql_connect($conf_centreon['hostCentreon'], $conf_centreon['user'], $conf_centreon['password']) or die('Impossible de se connecter � la base de donnees'.mysql_error());
	mysql_select_db($conf_centreon['db']) or die('Impossible de trouver la base de donnees '.mysql_error());
	
	$sql1 = mysql_query('SELECT id,done,plage FROM mod_discovery_rangeip;');
	echo '<p style="text-align:center"> ';
	$oneScanDone = 0;
	while($rangeToScan = mysql_fetch_array($sql1,MYSQL_ASSOC)){
		if (($rangeToScan["done"]==2) && ($rangeToScan["id"]==0)){
			echo 'Scan done<br><br>';
			echo '<input type=button value=" Show results " onClick="self.location=\'./main.php?p=61202\'">';
			echo '<p style="display:none">end</p>';
			return;
		}
		else{		
			/* Si done = 2 alors le scan est termin� */
			if (($rangeToScan["done"]==2) && ($rangeToScan["id"]!=0)){
					echo 'Range : '.$rangeToScan["plage"].' | <b style="color:green">Scan done</b><br>';
					$oneScanDone = 1;
			}
			/* Sinon si done = 3 alors il y a une erreur pendant le scan */
			else if (($rangeToScan["id"]!=0) && ($rangeToScan["done"]==3)){ 
					echo 'Range : '.$rangeToScan["plage"].' | <b style="color:red">ERROR : Connection lost with the poller agent...</b><br>';
			}
			/* Sinon le scan est en cours */
			else if (($rangeToScan["id"]!=0) && ($rangeToScan["done"]!=0)){ 
					echo 'Range : '.$rangeToScan["plage"].' | <b style="color:orange">Scanning in progress...</b><br>';
			}
		}
	}
	if ($oneScanDone == 1){
		echo '<br><br><input type=button value=" Show current results " onClick="self.location=\'./main.php?p=61202\'">';
	}
	echo '</p>';
}
?>