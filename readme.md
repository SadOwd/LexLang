## Running the Project with Docker

This project provides a multi-service Docker setup for running the main Python (FastAPI) backend, a React frontend, and a React Native mobile example. The configuration is managed via Docker Compose and project-specific Dockerfiles.

### Project-Specific Docker Requirements

- **Python Backend**
  - Uses `python:3.11-slim` as the base image.
  - Installs dependencies from `requirements.txt` and/or `pyproject.toml`.
  - Runs the FastAPI app via Uvicorn on port **8000**.
  - Expects a `.env` file for environment variables (optional, see below).
  - Healthcheck is configured for `http://localhost:8000/health`.

- **React Frontend**
  - Uses `node:22.13.1-slim` (Node.js v22.13.1).
  - Installs dependencies from `package.json`.
  - Builds the app (if a build script is present).
  - Serves the static build using `npx serve`.

- **React Native Mobile Example**
  - Uses `node:22.13.1-slim` (Node.js v22.13.1).
  - Installs dependencies from `package.json`.
  - Runs with `npm start` (no port exposed by default).

### Environment Variables

- The backend service can use a `.env` file at the project root. If present, uncomment the `env_file` line in the `docker-compose.yml` under `python-app`.
- Frontend and mobile services can also use `.env` files in their respective directories; uncomment the `env_file` lines if needed.

### Build and Run Instructions

1. **Clone the repository and ensure Docker and Docker Compose are installed.**
2. *(Optional)* Create a `.env` file at the project root for backend configuration, based on `.env.example`.
3. *(Optional)* Create `.env` files in `./examples/frontend/react/` and `./examples/mobile/react_native/` if your frontend/mobile apps require environment variables.
4. **Build and start all services:**

   ```sh
   docker compose up --build
   ```

   This will build and start:
   - `python-app` (FastAPI backend)
   - `js-react` (React frontend)
   - `js-react_native` (React Native mobile example)

### Ports Exposed

- **python-app**: [http://localhost:8000](http://localhost:8000) (FastAPI backend)
- **js-react**: No port exposed by default (serves static files internally). To expose the React dev server, uncomment the `ports` section in `docker-compose.yml`.
- **js-react_native**: No port exposed by default. To expose the Metro bundler (e.g., for development), uncomment the `ports` section in `docker-compose.yml`.

### Special Configuration Notes

- All services are connected via the `app-network` Docker network.
- The React frontend depends on the backend (`depends_on: python-app`).
- If you add external services (e.g., a database), update the `docker-compose.yml` accordingly.
- The backend's healthcheck is set up for `/health` endpoint.

---

*For more details on API usage, data formats, and advanced deployment, see the `docs/` directory and related markdown files.*
