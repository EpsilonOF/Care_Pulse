# DoctoGreed Hackathon – AI Infrastructure for Cardiology

Welcome to this AI chatbot project dedicated to cardiology, designed to assist with patient pre-evaluation, the generation of structured medical reports, and post-consultation follow-up.

The overall architecture is orchestrated via Docker Compose, and includes:

- A backend in FastAPI (Python) using Tortoise ORM for the PostgreSQL database.
- A frontend in Streamlit enabling interaction with the patient (questionnaire, post-consultation) and with the doctor (follow-up interface, PDF generation, etc.).
- A PostgreSQL database to store patient, diagnosis, and physician information.

## Table of Contents

1. Context: AI use case in cardiology
2. Main features
3. Project structure
4. Prerequisites
5. How to launch the project?
6. Contribution & License

## Context: AI use case in cardiology

This project addresses a concrete need in the medical field:

- Shortage of cardiologists and uneven distribution of expertise.
- Non-optimized patient triage, without prior medical evaluation.
- Time wasted in consultation (basic questions).
- Lack of structured post-consultation follow-up.

Objective: An AI assistant that prepares and optimizes consultations:

   - Pre-evaluates the patient before the appointment.
   - Generates a structured report of symptoms/medical history.
   - Helps the cardiologist prioritize the most urgent cases.
   - Ensures intelligent post-consultation follow-up (reminders, alerts, etc.).

## Main features

1. Patient triage: Analysis of responses and prioritization of urgent cases.
2. Preliminary consultation: Gathering important information (symptoms, history, current treatments).
3. Post-consultation follow-up: Reminders to take medication, check progress, alerts if worsening.
4. Report generation: PDF export, display on the doctor's side, possibly notifications for the patient.

## Project structure

```
decapix-doctogreed-hackathon/
├── README.md                <-- You are here (overall presentation)
├── docker-compose.yaml      <-- Docker Compose configuration
├── .dockerignore            <-- Files ignored by Docker
├── backend/
│   ├── backend.md           <-- Backend-specific documentation
│   ├── Dockerfile           <-- Backend Dockerfile
│   ├── requirements.txt     <-- Backend Python dependencies
│   └── app/
│       ├── __init__.py
│       ├── db_models.py
│       ├── ds.py
│       ├── enter_model.py
│       ├── main.py
│       └── routes.py
└── frontend/
    ├── frontend.md          <-- Frontend-specific documentation
    ├── Dockerfile           <-- Frontend Dockerfile
    ├── requirements.txt     <-- Frontend Python dependencies
    └── pages/
    ├── doctor.py
    └── patient.py
```

## Prerequisites

- Docker (version 20+ recommended)
- Docker Compose (version 3.8+)
- (Optional) Basic knowledge of FastAPI, Streamlit, and PostgreSQL to customize the application.

## How to launch the project?

1. Clone the repository:
```bash
git clone https://github.com/votre-compte/doctogreed-hackathon.git
cd doctogreed-hackathon
```
2. (Optional) Update the environment variables in `docker-compose.yaml` if necessary (e.g., `DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.).
3. Create a .env file and set the correct API key and URL. Example: `https://api.scaleway.ai/c98de2b2-feb7-4780-a578-4c5276194bf4/v1`.
4. Launch Docker Compose:
```bash
docker-compose up --build
```

## To use our logic:

1. Create a user:

```bash
curl -X POST http://127.0.0.1:8000/create/patient/ -H "Content-Type:application/json" -d '{"nom":"votre_nom"}'
```

2. Simulate their appointment in the `patient chatbot` section.
3. Take the doctor's place to compare patients `docteur`.

This will launch:

- The backend service on port `8000`
- The frontend service on port `8501`
- The db service (PostgreSQL) on port `5432`
4. Access the applications:

    - Backend (FastAPI): http://localhost:8000/docs for auto-doc (Swagger).
    - Frontend (Streamlit): http://localhost:8501 for the user interface.
5. Check the database:

    - By default, the PostgreSQL container is accessible on port `5432`.
    - The credentials (e.g., `user / password`) are defined in `docker-compose.yaml`.
6. Stop the environment:
```bash
docker-compose down
```

## Contribution & License

- Contributions: PRs, issues, and suggestions are welcome.
- License: This project is under a free license (to be specified according to your needs: MIT, Apache 2.0, etc.).

For more details, refer to the specific READMEs:

- `backend.md` in the `backend` folder.
- `frontend.md` in the `frontend` folder.

---
