I'll create a single Dockerfile per service plus a docker-compose.yml to orchestrate both:

Now one small but important tweak — the frontend/app.py currently hardcodes http://localhost:8000 as the API URL, but inside Docker localhost refers to the container itself. It needs to read from the API_BASE env var that compose injects:

All three files are created. Here are the only commands you need:

Build & run with Docker Compose (recommended)
bash
# From the project root — builds both images and starts both containers

```bash
docker compose up --build

```
That's it. After it starts:

Streamlit UI → http://localhost:8501
FastAPI docs → http://localhost:8000/docs

If you prefer building the images individually
bash
# Build backend image
docker build -f Dockerfile.backend -t loglens-backend .
# Build frontend image
docker build -f Dockerfile.frontend -t loglens-frontend .
# Run backend (reads .env for GROQ_API_KEY)
docker run -p 8000:8000 --env-file .env loglens-backend
# Run frontend (pointing to the running backend container)
docker run -p 8501:8501 -e API_BASE=http://host.docker.internal:8000 loglens-frontend
Other useful commands
bash
docker compose down          # stop & remove containers
docker compose logs -f       # stream logs from both services
docker compose restart       # restart without rebuilding
Note: Your .env file (with GROQ_API_KEY) is read at runtime via env_file in compose — it's never baked into the image, which is the safe way to handle secrets.



┌─────────────────────┐        ┌──────────────────────┐        ┌─────────────────────┐
│   Your Laptop       │  push  │   GitHub Actions      │  SSH   │   EC2 Instance      │
│   (git push main)   │───────▶│   ubuntu-latest       │        │   (self-hosted)     │
└─────────────────────┘        │                       │        │                     │
                               │  Job 1: CI            │        │  Job 2: CD          │
                               │  ✔ checkout           │        │  ✔ docker pull ECR  │
                               │  ✔ docker build       │        │  ✔ write .env       │
                               │  ✔ push to ECR        │───────▶│  ✔ docker compose   │
                               │                       │        │    up -d            │
                               └──────────────────────┘        └─────────────────────┘


The key is runs-on: self-hosted in Job 2 — that tells GitHub to run that job on your EC2 machine (not on GitHub's cloud). GitHub reaches your EC2 via the runner agent you install there.

One-Time EC2 Setup (do this once)
Step 1 — Launch EC2
AMI: Ubuntu 22.04
Instance type: t3.medium or bigger (BERT model needs RAM)
Security group: open ports 8000 (backend) and 8501 (frontend)
Step 2 — Install Docker on EC2
bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker ubuntu
newgrp docker
Step 3 — Install the GitHub Actions Runner on EC2
Go to your GitHub repo → Settings → Actions → Runners → New self-hosted runner → choose Linux → copy the commands GitHub gives you, run them on EC2:

bash
# Example (GitHub generates the exact token for you)
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64.tar.gz -L https://github.com/actions/runner/releases/download/v2.x.x/...
tar xzf ./actions-runner-linux-x64.tar.gz
./config.sh --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN
# Run as a background service
sudo ./svc.sh install
sudo ./svc.sh start
After this, the runner appears as Online in GitHub → Settings → Runners.

What Happens on Every git push main
1. GitHub detects push
2. Job 1 runs on GitHub's cloud (ubuntu-latest):
   → Builds Dockerfile.backend  → pushes to ECR
   → Builds Dockerfile.frontend → pushes to ECR
3. Job 2 runs ON YOUR EC2 (self-hosted runner):
   → Pulls both images from ECR
   → Writes .env from GitHub Secrets
   → docker compose up -d --no-build
   → Both containers restart with the new images


Port Access Summary
Service	Port	Access
FastAPI backend	8000	http://<EC2-public-IP>:8000
Streamlit frontend	8501	http://<EC2-public-IP>:8501


