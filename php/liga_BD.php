<?php
    //Variáveis para a connexão à BD
    $host = "localhost";
    $user = "root";
    $pass = "";
    $dbname = "";
    $port = "3306";

    try {
        $con = new PDO("mysql:host=$host;port=$port;dbname=".$dbname, $user, $pass);
    } catch (PDOException $e) {
        echo "Erro: Conexão com a BD falhou. Erro gerado: : " . $e->getMessage();
    }
?>