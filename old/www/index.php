<?php
require_once('config.php');
?>

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"></meta>
<title>DF Firewall Login</title>
</head>
<body>

<?php

//Get user ip-address

$ip_addr = $_SERVER['REMOTE_ADDR'];
$checklogin_cmd = $exec." INFO STATUS IP ".$ip_addr;
exec($checklogin_cmd, $out, $code);
echo("<!--ip addr:$ip_addr \nchecklogin_cmd:$checklogin_cmd \n- result: $out[0] \n- code: $code -->" );
if(True){
    echo("Time to go home...");
}
else{
if($ip_addr == '158.38.185.104'){
#	include('warning.php');
	header("Location: http://csaadf.uninett.no/");
}
if($code == 0 && $out[0] == "ACTIVE"){
    echo("<!-- USERSTATS -->");
    include('userstats.php');
}
elseif(isset($_POST['user'])){
    echo("<!-- LOGIN -->");
   include('login.php');
}
else{
    echo("<!-- FORM -->");
    include('loginform.php');
}
}
?>

</body>
</html>

