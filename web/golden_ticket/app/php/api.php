<?php
    function send_response($status_code, $message) {
        $resp = array("status" => $status_code, "message" => $message);
        echo json_encode($resp);
    }
?>
