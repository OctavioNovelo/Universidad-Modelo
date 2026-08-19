<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frontend App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f7f6;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fff;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            background: #e9ecef;
            margin-bottom: 0.5rem;
            padding: 0.75rem;
            border-radius: 4px;
            color: #495057;
            font-weight: 500;
            transition: transform 0.2s;
        }
        li:hover {
            transform: translateX(5px);
            background: #dee2e6;
        }
        .error {
            color: #d9534f;
            text-align: center;
        }
        .empty {
            color: #777;
            text-align: center;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User List</h1>
        <?php
        // El nombre del servicio backend en docker-compose es 'patito'
        $backend_url = 'http://patito/';

        $json = @file_get_contents($backend_url);

        if ($json === FALSE) {
            echo '<p class="error">Error connecting to backend service.</p>';
        } else {
            $response = json_decode($json, true);

            if (isset($response['status']) && $response['status'] === 'success') {
                if (!empty($response['data'])) {
                    echo '<ul>';
                    foreach ($response['data'] as $item) {
                        echo '<li>' . htmlspecialchars($item['name']) . '</li>';
                    }
                    echo '</ul>';
                } else {
                    echo '<p class="empty">No users found.</p>';
                }
            } else {
                echo '<p class="error">Error: ' . htmlspecialchars($response['error'] ?? 'Unknown error') . '</p>';
            }
        }
        ?>
    </div>
</body>
</html>
