<?php
include "header_simulate.php";
include "dbsimulate.php";
?>

<?php
$data = json_decode(file_get_contents('php://input'), true);
// print_r($data);
$gewicht = $data["payload_fields"]["value"];
?>

<?php
$sql = "INSERT INTO `Waardes`(`ID`, `value`) VALUES (UUID(),'".$gewicht."')";
$result = $conn->query($sql);
?>
