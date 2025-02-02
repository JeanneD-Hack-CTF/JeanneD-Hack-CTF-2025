<?php

    session_start();
    header('Content-Type: application/json');

    if (!isset($_SESSION["stage"]) || $_SESSION["stage"] !== "stage1") {
        $status = "failure";
        $message = "Stage 1 has't been loaded.";
        $code = 400; 
    } 
    
    else if (!str_starts_with($_SERVER["CONTENT_TYPE"], "multipart/form-data")) {
        $status = "failure";
        $message = "Level has not been understood";
        $code = 400;
    }

    else if (!isset($_POST["level"]) || $_POST["level"] !== "Stage 2") {
        $status = "failure";
        $message = "Invalid level parameter.";
        $code = 400;
    }
    
    else {
        $status = "success";
        $message = "Initializing cosmic variables...";
        $code = 200;
        $_SESSION['stage'] = "stage2";
    }

    http_response_code($code);
    echo json_encode(array(
        "status" => $status,
        "message" => $message,
    ));
    die();

?>