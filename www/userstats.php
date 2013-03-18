
<?php


if(isset($_GET['logmeout'])){
    echo("<!-- log me out! -->");
    $drop_cmd = $exec." DROP ".$ip_addr;
    echo("<!-- drop cmd: $drop_cmd -->");
    exec($drop_cmd);
    header("Location: http://".$_SERVER['SERVER_NAME']."/");
}
$stats_cmd = $exec."INFO STATS IP ".$ip_addr;
exec($stats_cmd, $stats);

?>

<h1><?=$stats[0]?></h1>
<pre><?=$stats[1]?></pre>
<pre><?=$stats[2]?></pre>
<pre><?=$stats[3]?></pre>
</p>
<?=$stats[5]?> - <a href="<?=$_SERVER['PHP_SELF']?>?logmeout=True"> Logout </a>

