<?php
$tipo = isset($_GET['tipo']) ? $_GET['tipo'] : '';
$n = isset($_GET['n']) ? intval($_GET['n']) : 0;

// montar HTML inicial
$dados = "<!DOCTYPE html>";
$dados .= "<html>";
$dados .= "<head>";
$dados .= "<meta charset='utf-8'>";
$dados .= "<title>Fatura Encomenda</title>";
$dados .= "<style>body{font-family:Helvetica,Arial,sans-serif;}"
       ."table{width:100%;border-collapse:collapse;}"
       ."th,td{border:1px solid #000;padding:4px;text-align:left;}";
$dados .= "</style>";
$dados .= "</head>";
$dados .= "<body>";

include 'liga_BD.php';
// lembrete con é a cena que vem do liga_BD.php
if (!isset($con) || !$con) {
    die("Não foi possível estabelecer ligação à base de dados.");
}

// query da encomenda
if ($tipo === 'armazem') {
    $sql = "SELECT e.nEncomendaArmazem AS num, u.nome AS user, e.dataEncomenda, e.dataEntrega
            FROM EncomendaArmazem e
            JOIN Utilizador u ON e.idUtilizador = u.id
            WHERE e.nEncomendaArmazem = ?";
} else {
    $sql = "SELECT e.nEncomendaLoja AS num, u.nome AS user, l.nome AS loja, e.dataEncomenda, e.dataEntrega
            FROM EncomendaLoja e
            JOIN Utilizador u ON e.idUtilizador = u.id
            JOIN Loja l ON e.idLoja = l.id
            WHERE e.nEncomendaLoja = ?";
}
$stmt = $con->prepare($sql);
$order = null;
if ($stmt->execute([$n])) {
    $order = $stmt->fetch(PDO::FETCH_ASSOC);
}

if (!$order) {
    $dados .= "<h2>Encomenda não encontrada</h2>";
} else {
    $dados .= "<h1>Encomenda #" . htmlspecialchars($order['num']) . "</h1>";
    $dados .= "<p>Utilizador: " . htmlspecialchars($order['user']) . "</p>";
    if (isset($order['loja'])) {
        $dados .= "<p>Loja destino: " . htmlspecialchars($order['loja']) . "</p>";
    }
    $dados .= "<p>Data encomenda: " . htmlspecialchars($order['dataEncomenda']) . "</p>";
    $dados .= "<p>Data entrega: " . htmlspecialchars($order['dataEntrega']) . "</p>";

    // linhas da encomenda
    if ($tipo === 'armazem') {
        $detSql = "SELECT p.designacao, d.quantidade, d.precoUnitario
                   FROM DetalheEncomendaArmazem d
                   JOIN Produto p ON p.id = d.idProduto
                   WHERE d.nEncomendaArmazem = ?";
    } else {
        $detSql = "SELECT p.designacao, d.quantidade, d.precoUnitario
                   FROM DetalheEncomendaLoja d
                   JOIN Produto p ON p.id = d.idProduto
                   WHERE d.nEncomendaLoja = ?";
    }
    $detStmt = $con->prepare($detSql);
    $detStmt->execute([$n]);
    $items = $detStmt->fetchAll(PDO::FETCH_ASSOC);

    $dados .= "<table>";
    $dados .= "<tr><th>Artigo</th><th>Qt.</th><th>Preço unit.</th><th>Subtotal</th></tr>";
    $total = 0;
    foreach ($items as $it) {
        $sub = $it['quantidade'] * $it['precoUnitario'];
        $total += $sub;
        $dados .= "<tr>";
        $dados .= "<td>" . htmlspecialchars($it['designacao']) . "</td>";
        $dados .= "<td>" . $it['quantidade'] . "</td>";
        $dados .= "<td>" . number_format($it['precoUnitario'],2) . "</td>";
        $dados .= "<td>" . number_format($sub,2) . "</td>";
        $dados .= "</tr>";
    }
    $dados .= "<tr><td colspan='3'><strong>Total</strong></td><td><strong>" . number_format($total,2) . "</strong></td></tr>";
    $dados .= "</table>";
}

$dados .= "</body></html>";

// gerar PDF com Dompdf
use Dompdf\Dompdf;
require './dompdf/autoload.inc.php';
$dompdf = new Dompdf();
$dompdf->loadHtml($dados);
$dompdf->set_option('defaultFont','DejaVu Sans');
$dompdf->setPaper('A4','portrait');
$dompdf->render();
$filename = 'fatura_' . $tipo . '_' . $n . '.pdf';
$dompdf->stream($filename);
?>