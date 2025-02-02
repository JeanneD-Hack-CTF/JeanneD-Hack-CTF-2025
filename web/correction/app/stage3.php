<?php

    session_start();

    header('Content-Type: application/json');
    $status = "success";
    $message = "Congratulation Agent, here is the flag : JDHACK{Pr0cess_1nitializ3d_0veR}";
    $code = 200;

    if (!isset($_SESSION["stage"]) || $_SESSION["stage"] !== "stage2") {
        $status = "failure";
        $message = "Stage 2 has't been loaded.";
        $code = 400; 
    } 

    if (!isset($_POST["level"]) || $_POST["level"] !== "Stage 3") {
        $status = "failure";
        $message = "Invalid level parameter.";
        $code = 400;
    }

    $_SESSION['stage'] = "stage3";
    http_response_code($code);
    echo json_encode(array(
        "status" => $status,
        "message" => $message,
    ));
    die();

?>