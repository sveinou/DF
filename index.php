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

    //we should probably check that input before sendingit with sudo... 

    print($cmd);
    exec($cmd, $out, $code);
    
    switch($code){
        case 0:
            $msg = "Welcome to the internet."
        case 1:
            $msg = "Login failed";
            break;
        case 2:
            $msg = "That combination of MAC and IP seems like horselasagne... ";
            break;
        case 2:
            $msg = "Something went wrong with the input you sent us.";
        default:
            $msg = "LOL.\n I DUNNO WHAT HAPPEND.";
    
    }
    ?>
    <h1><?=$msg?></h1>
    <p>
    <em><?=$out[0]?></em><br>
    EXIT CODE: <?=$code?>
    </p>
    <?
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

