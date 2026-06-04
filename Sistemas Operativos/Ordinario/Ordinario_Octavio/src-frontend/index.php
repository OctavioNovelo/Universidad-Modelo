<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Octavio's App - Lord of the Rings</title>
    <style>
        body {
            font-family: 'Georgia', serif;
            background-color: #1a120b; /* Deep earth brown */
            color: #d5cea3; /* Aged parchment */
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-image: radial-gradient(circle, #2c1e12 0%, #1a120b 100%);
        }
        .container {
            background-color: #3c2a21;
            padding: 2.5rem;
            border-radius: 4px;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 550px;
            border: 2px solid #634832;
            position: relative;
        }
        /* Fancy border effect */
        .container::before {
            content: "";
            position: absolute;
            top: 5px; left: 5px; right: 5px; bottom: 5px;
            border: 1px solid #634832;
            pointer-events: none;
        }
        h1 {
            color: #e5ba73; /* Golden tone */
            text-align: center;
            margin-bottom: 2rem;
            font-variant: small-caps;
            letter-spacing: 3px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            border-bottom: 1px solid #634832;
            padding-bottom: 1rem;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            background: rgba(44, 30, 18, 0.6);
            margin-bottom: 1rem;
            padding: 1.2rem;
            border-radius: 2px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 3px solid #e5ba73;
            transition: all 0.3s ease;
        }
        li:hover {
            background: rgba(99, 72, 50, 0.4);
            transform: translateY(-2px);
            border-left-color: #ffe8d6;
        }
        .name {
            font-weight: bold;
            font-size: 1.2rem;
            color: #ffe8d6;
        }
        .race {
            font-size: 0.95rem;
            color: #e5ba73;
            font-style: italic;
            text-transform: lowercase;
            font-variant: small-caps;
        }
        .error {
            color: #ff6b6b;
            text-align: center;
            background: rgba(255,0,0,0.1);
            padding: 1rem;
        }
        .empty {
            color: #999;
            text-align: center;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Characters of Middle-earth</h1>
        <?php
        $backend_url = 'http://backend/'; 

        $json = @file_get_contents($backend_url);

        if ($json === FALSE) {
            echo '<p class="error">The fellowship is broken. Cannot reach the backend.</p>';
        } else {
            $response = json_decode($json, true);

            if (isset($response['status']) && $response['status'] === 'success') {
                if (!empty($response['data'])) {
                    echo '<ul>';
                    foreach ($response['data'] as $item) {
                        echo '<li>';
                        echo '<span class="name">' . htmlspecialchars($item['name']) . '</span>';
                        echo '<span class="race">' . htmlspecialchars($item['race']) . '</span>';
                        echo '</li>';
                    }
                    echo '</ul>';
                } else {
                    echo '<p class="empty">Middle-earth seems empty today.</p>';
                }
            } else {
                echo '<p class="error">Error: ' . htmlspecialchars($response['error'] ?? 'Dark magic interference') . '</p>';
            }
        }
        ?>
    </div>
</body>
</html>
