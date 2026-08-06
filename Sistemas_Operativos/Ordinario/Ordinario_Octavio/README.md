# Ordinario Octavio Project

This project is a variation of the original `phpapp`, featuring a **Lord of the Rings** theme.

## Architecture

- **Database (MariaDB)**: Stores characters from Middle-earth.
- **Backend (PHP/Apache)**: A RESTful API that fetches character data (name and race) from the database.
- **Frontend (PHP/Apache)**: A web interface that consumes the Backend API and displays the characters with an epic fantasy aesthetic.

## How to Run

1. Make sure you have Docker and Docker Compose installed.
2. Navigate to this directory in your terminal.
3. Run the following command:
   ```bash
   docker-compose up --build
   ```

## Services

- **Frontend**: Available at [http://localhost:9081](http://localhost:9081)
- **Backend API**: Available at [http://localhost:9080](http://localhost:9080)
- **Database**: Port `3307` on localhost (user: `octavio_user`, pass: `octavio_pass`, db: `octavio_db`)

## Changes from original `phpapp`

- Database name changed to `octavio_db`.
- Theme changed to **The Lord of the Rings**.
- Port numbers changed to `9080` (Backend) and `9081` (Frontend) to avoid conflicts.
- Container names updated to `octavio_*`.
- Data structure changed to include `race` instead of a generic name.
- Custom CSS for a parchment/fantasy look.
