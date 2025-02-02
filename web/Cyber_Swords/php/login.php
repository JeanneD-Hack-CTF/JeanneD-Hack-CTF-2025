<?php
require 'vendor/autoload.php';
use \Firebase\JWT\JWT;

$key = "ship-in-the-harbor-is-safe-but-that-is-not-what-a-ship-is-for";

setcookie("token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6bnVsbH0.nfmQYDKfZ7CA-mxkyQeCnzcmD_oEar0Cf5EtxOOMG0c", time() + 3600, "/");

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if ($username == 'jeanne154a@aahegizo!!)$£rt' && $password == 'Pa$Sw0RdD1@!') {
        $payload = array(
            "user_id" => 1,
            "username" => $username,
            "gender" => "female",
            "role" => "user"
        );

        $jwt = JWT::encode($payload, $key, 'HS256');
        setcookie("token", $jwt, time() + 3600, "/");

        header("Location: user_profile.php");
        exit();
    } else {
        ?>
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Login</title>
            <link rel="stylesheet" href="css/style.css">
        </head>
        <body>
                <header>
                <div class="header-container">
                    <h1>189aXA - Cybernetics swords</h1>
                    <nav>
                        <a href="index.html">Accueil</a>
                        <a href="articles.html">Articles</a>
                        <a href="propos.html">A propos</a>
                        <a href="login.php">Connexion</a>
                    </nav>
                </div>
            </header>
            <div class="container">
                <img src="img/logo.png" alt="Logo">
                <h1>Login</h1>
                <form method="POST">
                    <label for="username">Username:</label><br>
                    <input type="text" name="username" placeholder="Nom d'utilisateur" required>
                    <label for="password">Password:</label><br>
                    <input type="password" name="password" placeholder="Mot de passe" required>
                    <input type="submit" value="Se connecter">
                    <!-- Permet de se connecter pour avoir le cookie - JWT "token" -->
                </form>
            </div>
            <?php
                if ($username == "jeanne" && $password == 'Pa$Sw0RdD1@') {
                    echo "<script>alert(\"Ah ah, la vie n'est pas si simple parfois.\")</script>";
                } else {
                    echo "<script>alert(\"Nom d'utilisateur ou mot de passe incorrect.\")</script>"; 
                }
            ?>
        </body>
        </html>
        <?php 
    }
} else {
    ?>
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <header>
                <div class="header-container">
                    <h1>189aXA - Cybernetics swords</h1>
                    <nav>
                        <a href="index.html">Accueil</a>
                        <a href="articles.html">Articles</a>
                        <a href="propos.html">A propos</a>
                        <a href="login.php">Connexion</a>
                    </nav>
                </div>
            </header>
        <!-- Error in red -->
        <p style="color: red;">
            <?php
            if (isset($_GET['error'])) {
                $error = $_GET['error'];
                echo "Vous avez été redirigé vers cette page car :";
                if ($error == "no_username") {
                    echo "Nom d'utilisateur manquant dans le token";
                } elseif ($error == "no_role") {
                    echo "Rôle manquant dans le token";
                } elseif ($error == "not_logged_in") {
                    echo "Vous devez vous connecter pour accéder à cette page.";
                }
            }
            ?>
        <div class="container">
            <img src="img/logo.png" alt="Logo">
            <h1>Login</h1>
            <form method="POST">
                <label for="username">Username:</label><br>
                <input type="text" name="username" placeholder="Nom d'utilisateur" required>
                <label for="password">Password:</label><br>
                <input type="password" name="password" placeholder="Mot de passe" required>
                <input type="submit" value="Se connecter">
                <!-- Permet de se connecter pour avoir le cookie - JWT "token" -->
            </form>
        </div>
    </body>
    </html>
    <?php
}
?>
