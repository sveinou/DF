
<?php
//Checking and cleaning input
    $username = escapeshellcmd($_POST['user']);     //this should remove any shell-hacks
    $username = str_replace(" ","\\ ", $username);
    $password = escapeshellcmd($_POST['pass']);          
#    $password = str_replace(" ","\\ ",$password);   //adding support for whitespaces in passwords
   
    // sudo _FW_ login username password 1.2.3.4
    $cmdL = $exec."LOGIN ".$ip_addr." ".$username." ".$password;
    
    exec($cmdL, $outL, $codeL);
    echo("<!-- \nCommand: $cmdL \nOutput: $outL[0] \nReturncode: $codeL -->");
    switch($codeL){
        case 0:
            $msg = "Welcome to the internet.";
            if($redirect_url != "NO-REDIRECT"){
                header("Location: ".$redirect_url);
//                echo "<a href=\"http://lan.tithlde.org\"> INFO!</a>";
            }
//            echo '<meta http-equiv="Refresh" content="1;URL=http:////lan.tihlde.org">';
        break;
        case 1:
            $msg = "Login failed";
            break;
        case 2:
            $msg = "That combination of MAC and IP seems like horselasagne... ";
            break;
        case 3:
            $msg = "Something went wrong with the input you sent us.";
            break;
        default:
            $msg = "LOL.\n I DUNNO WHAT HAPPEND.";
	        break;
}
?>
<h1><?=$msg?></h1>
<p>
<em><?=$outL[0]?></em><br>
EXIT CODE: <?=$codeL?>
</p>

</body>
</html>

