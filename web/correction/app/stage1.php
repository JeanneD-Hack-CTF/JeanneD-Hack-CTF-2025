<?php

    error_reporting(E_ALL); // Report all types of errors
    ini_set('display_errors', 1); // Display errors in the browser

    session_start();

    header('Content-Type: application/json');
    $status = "success";
    $message = "Loading temporal constants...";
    $code = 200;

    if (!str_contains($_SERVER['HTTP_USER_AGENT'], "JDHACK")) {
        $status = "failure";
        $message = "Only JDHACK agents are authorized";
        $code = 400;
    }

    if (!isset($_POST["level"]) || $_POST["level"] !== "Stage 1") {
        $status = "failure " . $_POST["level"];
        $message = "Invalid level parameter.";
        $code = 400;
    }

    $_SESSION['stage'] = "stage1";
    http_response_code($code);
    echo json_encode(array(
        "status" => $status,
        "message" => $message,
    ));
    die();

?>