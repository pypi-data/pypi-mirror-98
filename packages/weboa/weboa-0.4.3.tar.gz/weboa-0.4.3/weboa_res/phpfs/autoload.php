<?php
$abs = __DIR__;
$scan = scandir($abs);
unset($scan[0], $scan[1]);
foreach($scan as $file)
{
    if($file=="autoload.php")
        continue;

    if(!is_dir($abs."/".$file))
    {
        if(strpos($file, '.php') !== false)
        {
            $s = $abs."/".$file;
            try {
                include_once($s);
            }
            catch(Exception $e) { die("Lib error"); }
        }
    }
}

?>