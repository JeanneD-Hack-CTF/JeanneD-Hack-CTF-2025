<?php
    include 'php/db.php';
    include 'php/api.php';

    header("Content-Type: application/json");

    if (!isset($_GET["serial"])) {
        send_response(500, "Missing serial parameter");
        die();
    }

    $serial = $_GET["serial"];
    $conn = getDBConnection();

    $query = $conn->prepare("SELECT winner FROM tickets WHERE serial LIKE ?");
    $query->bind_param("s", $serial);

    if (!$query->execute()) {
        send_response(500, "Something went wrong :/");
        die();
    }

    $query->bind_result($winner);
    $response = $query->fetch();

    $query->close();
    $conn->close();

    if (!$response) {
        send_response(200, "Le ticket de numéro de série donné n'a pas été trouvé.");
    } else if (!$winner) {
        send_response(200, "Malheureusement le ticket est perdant :( Retente ta chance !");
    } else {
        send_response(200, "Félicitations ! Le ticket est gagnant :) Utilises ce numéro de série afin de valider le challenge.");
    }
?>
