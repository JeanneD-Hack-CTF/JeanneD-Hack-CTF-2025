<?php
    include 'php/db.php';
    include 'php/api.php';

    header("Content-Type: application/json");

    if (!isset($_GET["tirage"]) || $_GET["tirage"] !== "true") {
        send_response(500, "Missing tirage parameter");
        die();
    }

    $conn = getDBConnection();
    $query = $conn->prepare("INSERT INTO tickets (serial) VALUES (?)");

    // Fonction pour générer une chaîne aléatoire
    function rstring($length = 16) {
        return bin2hex(random_bytes($length));
    }

    // Générer une chaîne aléatoire
    $random_string = rstring(16);
    // Calculer le hash SHA1 de la chaîne aléatoire
    $sha1 = sha1($random_string);

    // Ajoute le ticket à la BDD
    $query->bind_param("s", $sha1);
    $query->execute();
    $query->close();
    $conn->close();

    // Retourne le ticket à l'utilisateur
    send_response(200, $sha1);
?>
