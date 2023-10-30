<?php
    $CONFIG_DBNAME = "";
    $CONFIG_USER = "";
    $CONFIG_PASSWORD = "";
    $CONFIG_URL_ID = 1;
    try {
        $conn = new PDO("mysql:host=localhost;dbname=" . $CONFIG_DBNAME, $CONFIG_USER, $CONFIG_PASSWORD);
    }
    catch (PDOException $e) {
        echo "Connection failed: " . $e->getMessage();
        die();
    }
    if ($_SERVER["REQUEST_METHOD"] === "POST") {
        $data = json_decode(file_get_contents('php://input'), true);
        if (array_key_exists("token", $data) and array_key_exists("new_url", $data)){
            $sql = "SELECT `token` FROM `tokens` WHERE `token` = :token";
            $stmt = $conn->prepare($sql);
            $stmt->bindValue(":token", $data["token"]);
            $stmt->execute();
            if($stmt->rowCount() > 0){
                $sql = "UPDATE `map` SET `url` = :url WHERE `id` = :urlid";
                $stmt = $conn->prepare($sql);
                $stmt->bindValue(":url", $data["new_url"]);
                $stmt->bindValue(":urlid", $CONFIG_URL_ID);
                $stmt->execute();
                echo "OK";
            }
        }
        
    }else{
        $sql = "SELECT `url` FROM `map` WHERE `id` = :urlid";
        $stmt = $conn->prepare($sql);
        $stmt->bindValue(":urlid", $CONFIG_URL_ID);
        $stmt->execute();
        if($stmt->rowCount() > 0){
            while($row = $stmt->fetch()){
                header("Location: ". $row["url"]);
            }
        }
    }

    

?>