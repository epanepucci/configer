# Configuration Manager

A web application for managing, versioning, and snapshotting configuration files for various instruments.

## Features

- Store configuration files in JSON format
- Download configurations as JSON files
- Update configurations through a web interface
- Version control for configurations
- Create named snapshots of configurations
- Support for multiple instruments

## Technology Stack

- **Frontend**: Vue 3 with Composition API, PrimeVue components
- **Backend**: Python FastAPI
- **Database**: Redis with RedisJSON for JSON data storage
- **Containerization**: Docker and Docker Compose

## Project Structure

The project follows a modern architecture with a clear separation between frontend and backend:

- `frontend/`: Vue 3 application
- `backend/`: Python FastAPI application
- `docker-compose.yml`: Docker Compose configuration for local development

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.10+ (for local backend development)

### Running with Docker Compose

1. Clone the repository
2. Start the services:

```bash
docker-compose up
```

This will start three services:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Redis: on port 6379

### Local Development

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Redis Data Model

The application uses Redis with RedisJSON to store configuration data, version history, and snapshots:

- `instrument:{instrument_id}:config` - Current active configuration
- `instrument:{instrument_id}:versions` - List of version IDs
- `instrument:{instrument_id}:snapshots` - List of snapshot names
- `instrument:{instrument_id}:version:{version_id}` - Individual version data
- `instrument:{instrument_id}:snapshot:{snapshot_name}` - Named snapshot
- `instruments:list` - Metadata about instruments

## API Endpoints

### Instruments

- `GET /api/instruments` - Get all instruments
- `GET /api/instruments/{instrument_id}` - Get a specific instrument
- `POST /api/instruments` - Create a new instrument

### Configurations

- `GET /api/configs/{instrument_id}` - Get current configuration
- `PUT /api/configs/{instrument_id}` - Update configuration
- `GET /api/configs/{instrument_id}/versions` - Get all version IDs
- `GET /api/configs/{instrument_id}/versions/{version_id}` - Get specific version data

### Snapshots

- `POST /api/snapshots/{instrument_id}` - Create a named snapshot
- `GET /api/snapshots/{instrument_id}` - Get all snapshot names
- `GET /api/snapshots/{instrument_id}/{snapshot_name}` - Get specific snapshot data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
