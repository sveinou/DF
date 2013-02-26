<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"></meta>
<title>DF Firewall Login</title>
</head>
<body>

<?php

//Get user ip-address
$ip_addr = $_SERVER['REMOTE_ADDR'];
$exec = "sudo python ./df_login.py ";

// 
if(isset($_POST['user'])){
    // kjører login scriptet

    $username = $_POST['user'];
    $password = $_POST['pass'];         
    $cmd = $exec." ".$username." ".$password." ".$ip_addr;

    print($cmd);
    exec($cmd, $out);
    print "<h1> Internet enabled </h1> ".$out;
}

else{ ?>

    <center>
    <h1>Login to enable internet <h1>
    <br><b>Logg inn</b><br><br>
    <form method="POST">
    Brukernavn:<br>
    <input type="text" name="user"><br>
    Passord:<br>
    <input type="password" name="pass"><br><input value="internetz?" type="submit"></form>
    </center>
    <?
}
?>
</body>
</html>

