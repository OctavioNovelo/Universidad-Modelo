<?php
header('Content-Type: application/json');

// El host debe ser 'db' para coincidir con el nombre del servicio en docker-compose.yml
$host = 'db';
$db   = 'patito_db';
$user = 'patito_user';
$pass = 'patito_pass';

// Intentar la conexión
$conn = new mysqli($host, $user, $pass, $db);

$response = [];

if ($conn->connect_error) {
    http_response_code(500);
    echo json_encode(['error' => 'Connection failed: ' . $conn->connect_error]);
    exit;
}

$sql = "SELECT name FROM test";
$result = $conn->query($sql);

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
        'message' => '0 results or table does not exist',
        'data' => []
    ];
}

echo json_encode($response);
$conn->close();
?>
