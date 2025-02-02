<?php

function base64UrlDecode($input) {
    $remainder = strlen($input) % 4;
    if ($remainder) {
        $addlen = 4 - $remainder;
        $input .= str_repeat('=', $addlen);
    }
    return base64_decode(strtr($input, '-_', '+/'));
}

if (isset($_COOKIE['token'])) {
    $jwt = $_COOKIE['token'];
    $tokenParts = explode('.', $jwt);
    $payload = base64UrlDecode($tokenParts[1]);
    $decodedPayload = json_decode($payload, true);

    $username = htmlspecialchars($decodedPayload['username']);
    $role = htmlspecialchars($decodedPayload['role']);
    $gender = htmlspecialchars($decodedPayload['gender']);
    $logo = htmlspecialchars($decodedPayload['logo_svg']);

    // Si $username est null ou vide, on redirige l'utilisateur vers la page de connexion
    if (empty($username)) {
        # Redirect to login page
        header("Location: login.php?error=no_username");
        exit();
    }
    // Si $role est null ou vide, on redirige l'utilisateur vers la page de connexion
    if (empty($role)) {
        # Redirect to login page
        header("Location: login.php?error=no_role");
        exit();
    }

    ?>
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Profil Utilisateur</title>
            <link rel="stylesheet" href="css/style.css">
        </head>
        <body>
            <div class="container">
            <!-- "logo_svg" for logo in PAYLOAD-DATA JWT token -->
                <?php
                    // If logo is not empty, display the logo
                    if (!empty($logo)) {
                        echo file_get_contents($logo);
                        // echo "<img src=\"$logo\" alt=\"Logo\">";
                    } else {
                        if ($gender == "male") {
                            echo file_get_contents("img/male.svg");
                            // echo "<img src=\"img/male.png\" alt=\"Profile Image\">";
                        } else {
                            echo file_get_contents("img/female.svg");
                            // echo "<img src=\"img/female.png\" alt=\"Profile Image\">";
                        }
                    }
                ?>
                <h1>Bienvenue, <?php echo $username; ?>!</h1>
                <p>Droit de l'utilisateur : <?php echo $role; ?></p>
                <?php
                if ($role == "admin") {
                    # Read and write /tmp/flag.txt
                    // $flag = file_get_contents("/tmp/flag.txt");
                    // echo "<p>Flag : $flag</p>";
                    # Panel for admin
                    echo "<a href=\"@dm1n.php\">Panel Admin</a>";
                }
                ?>
            </div>
        </body>
        </html>
    <?php
} else {
    header("Location: login.php?error=not_logged_in");
    exit();
}

?>
