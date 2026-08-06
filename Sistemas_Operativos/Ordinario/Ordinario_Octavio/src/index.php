<?php
header('Content-Type: application/json');

$host = 'db'; // Coincide con el nombre del servicio en docker-compose.yml
$db   = 'octavio_db';
$user = 'octavio_user';
$pass = 'octavio_pass';

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(['error' => 'Connection failed: ' . $conn->connect_error]);
    exit;
}

// Cambiado de 'role' a 'race' para coincidir con la nueva tabla del Señor de los Anillos
$sql = "SELECT name, race FROM characters";
$result = $conn->query($sql);

$response = [];
if ($result && $result->num_rows > 0) {
    $data = [];
    while($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    $response = [
        'status' => 'success',
        'data' => $data
    ];
} else {
    $response = [
        'status' => 'success',
        'message' => 'No characters found in Middle-earth',
        'data' => []
    ];
}

echo json_encode($response);
$conn->close();
?>
