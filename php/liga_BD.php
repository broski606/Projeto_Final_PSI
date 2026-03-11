<?php
    //Variáveis para a connexão à BD
    $host = "localhost";
    $user = "root";
    $pass = "";
    $dbname = "Columbofilia_Armazem";
    $port = "3306";

    $con = null;
    try {
        $con = new PDO(
            "mysql:host=$host;port=$port;dbname=$dbname;charset=utf8mb4",
            $user,
            $pass,
            [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false
            ]
        );
    } catch (PDOException $e) {
        echo "Erro: Conexão com a BD falhou. Erro: " . htmlspecialchars($e->getMessage());
        exit;
    }
?>