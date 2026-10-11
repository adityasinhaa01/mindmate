
# MindMate — AI-Powered Student Mental Wellness Platform

![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-61DAFB?logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/Backend-Node.js%20%7C%20Express-339933?logo=node.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/AI%20Service-FastAPI-009688?logo=fastapi&logoColor=white)
![Machine Learning](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-47A248?logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Containerization-Docker-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey)

MindMate is a student-focused mental wellness and stress-tracking web application that combines daily wellness assessments, machine learning-based stress prediction, personalized coping recommendations, an AI wellness companion, and emergency contact notifications.

The platform is designed to help students reflect on their daily habits, recognize patterns in their well-being, and access supportive resources through a unified interface.

> **Important:** MindMate is an educational and wellness-support project, not a medical diagnostic system. Its predictions and recommendations should not replace professional mental health assessment or emergency assistance.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Application Architecture](#application-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Application Workflows](#application-workflows)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [AI Wellness Companion](#ai-wellness-companion)
- [Backend API Reference](#backend-api-reference)
- [FastAPI AI Service Reference](#fastapi-ai-service-reference)
- [Database Models](#database-models)
- [Emergency Notifications](#emergency-notifications)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Security and Privacy](#security-and-privacy)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

University life can involve academic pressure, irregular sleep, excessive screen exposure, approaching examinations, and emotional stress. MindMate provides a centralized interface for students to record these experiences and explore practical wellness strategies.

The application uses a modular architecture with three main application services:

1. **React frontend:** Provides the interactive user interface, wellness dashboard, assessments, visualizations, and AI companion.
2. **Node.js and Express backend:** Handles authentication, user profiles, persistent wellness records, emergency contacts, notifications, and communication with the AI service.
3. **Python and FastAPI AI service:** Runs the machine learning inference pipeline, produces stress classifications, generates recommendations, and provides AI companion responses.

MongoDB stores user accounts, daily assessments, and emergency contacts.

### Project Goals

- Make daily wellness tracking accessible to students.
- Identify potential stress patterns from self-reported information.
- Offer personalized, actionable coping recommendations.
- Provide a conversational interface for wellness support.
- Allow students to configure trusted emergency contacts.
- Present historical wellness information through visualizations.
- Demonstrate the integration of machine learning, generative AI, and a full-stack web application.

---

## Key Features

### 1. Student Dashboard

The dashboard brings together wellness information and navigation into a single interface.

Features include:

- Personalized dashboard and user profile.
- Daily wellness assessment.
- Current stress score and stress category.
- Recommended wellness activities.
- Historical trend visualizations.
- Navigation between application sections.
- Emergency SOS access.

### 2. Daily Wellness Check-In

Students can record lifestyle information and their current emotional state.

| Input | Description |
|---|---|
| Sleep duration | Hours slept during the day or night |
| Study duration | Hours spent studying |
| Screen exposure | Daily screen time in hours |
| Exam proximity | Number of days until the next examination |
| Mood | Self-reported emotional state |
| Notes | Optional personal observations |
| Nervousness | Self-reported nervousness or anxiety |
| Difficulty controlling worry | Self-reported difficulty managing worry |
| Worry | Self-reported excessive worry |
| Trouble relaxing | Difficulty relaxing |
| Restlessness | Self-reported restlessness |
| Irritability | Self-reported irritability |
| Fear | Self-reported fear or apprehension |

The seven psychological inputs use a four-point response scale:

- `0` — No
- `1` — Mild
- `2` — Moderate
- `3` — Severe

The frontend submits the assessment to the Express backend, which requests an analysis from the FastAPI service.

A student's assessment is saved to MongoDB with the resulting stress score, stress level, prediction details, and recommendations.

The backend supports creating or updating a user's check-in for the current date.

### 3. Machine Learning-Based Stress Prediction

MindMate includes a scikit-learn inference pipeline for classifying self-reported psychological symptoms into four prediction categories:

- No Stress
- Mild Stress
- Moderate Stress
- Severe Stress

The inference engine returns prediction probabilities, a confidence score, a primary contributing symptom, and a continuous regression score.

The AI service also converts the model output into the application's normalized stress score and user-facing stress category.

The project includes serialized model artifacts, a training script, a dataset, and stored evaluation metrics.

See [Machine Learning Pipeline](#machine-learning-pipeline) for details.

### 4. Personalized Wellness Recommendations

MindMate generates coping recommendations based on assessment results and lifestyle inputs.

Activities represented in the project include:

- Guided breathing exercises.
- Short walking breaks.
- Screen-rest reminders.
- Sleep hygiene suggestions.
- Pomodoro-style study sessions.

Recommendations contain a title, description, duration, identifier, and presentation metadata.

The AI service returns recommendation data alongside the stress assessment.

### 5. CalmFlow AI Wellness Companion

CalmFlow is the conversational wellness assistant integrated into MindMate.

It is designed to provide supportive, empathetic, and concise responses.

Capabilities include:

- Conversational wellness support.
- Context-aware responses using stress and lifestyle information.
- Suggestions for simple grounding and breathing exercises.
- Study and examination stress support.
- Sleep-related coping suggestions.
- Rule-based fallback responses when an AI provider is unavailable.
- Crisis-oriented responses for certain self-harm-related expressions.

The project supports an OpenAI-compatible AI provider configuration, including Groq-hosted models, and a Gemini integration path in the Node.js backend.

The actual provider used depends on the service configuration and available credentials.

**The AI companion is not a therapist, and its responses must not be treated as professional medical advice.**

### 6. Wellness History and Visualizations

MindMate uses Recharts to visualize wellness information.

The backend provides a historical check-in endpoint that returns up to seven stored records.

The frontend includes trend-oriented visualizations for tracking information such as sleep, study time, screen exposure, and stress scores.

Historical trends can help students reflect on changes over time. They should not be interpreted as clinical conclusions.

### 7. Emergency Contacts and SOS

Users can manage trusted contacts through the application.

Each contact can contain:

- Name.
- Relationship.
- Email address.
- Phone number.

Supported relationship categories are:

- Parent/Guardian.
- Close Friend.
- College Counselor.

The backend provides contact creation, listing, deletion, and a manual SOS endpoint.

The manual SOS implementation uses email notifications through Nodemailer and SMTP.

**Important:** The implemented emergency notification mechanism is email-based. A phone number is stored for each contact, but storing a phone number does not itself enable SMS delivery.

### 8. Consecutive High-Stress Notifications

The backend includes an alert service designed to evaluate consecutive high-stress days and notify configured emergency contacts when its conditions are met.

It maintains fields for the high-stress streak and the last alert timestamp.

SMTP configuration is required for actual email delivery. Without valid SMTP credentials, the service can use a logging or simulation path.

Notification behavior should be tested with the intended deployment configuration before being relied upon.

### 9. Authentication and User Profiles

The Express backend supports:

- User registration.
- User login.
- Password hashing with bcrypt.
- JWT-based authentication.
- Authenticated profile retrieval.
- Profile updates.
- Email format validation.
- Duplicate email checks.

Protected endpoints require a bearer token in the `Authorization` header.

### 10. Modular Backend and AI Services

The application separates web application responsibilities from machine learning and language model processing.

This separation makes it easier to develop and maintain the frontend, backend, and AI components independently.

The repository also includes Dockerfiles, Docker Compose configuration, environment examples, automated tests for the AI service, and deployment documentation.

---

## Application Architecture

```text
                         STUDENT
                            |
                            v
                +------------------------+
                | React + Vite Frontend |
                | Dashboard and UI      |
                +-----------+------------+
                            |
                            | HTTP / JSON
                            | JWT Bearer Token
                            v
                +------------------------+
                | Node.js + Express      |
                | REST API Gateway       |
                +-----------+------------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
       +-------------+ +----------+ +----------------+
       | MongoDB     | | Nodemailer| | FastAPI AI     |
       | Mongoose    | | SMTP     | | Microservice   |
       +-------------+ +----------+ +-------+--------+
                                              |
                               +--------------+--------------+
                               |                             |
                               v                             v
                     +------------------+        +------------------+
                     | scikit-learn     |        | AI Companion     |
                     | Stress Inference |        | LLM / Fallback   |
                     +------------------+        +------------------+
```

### Request Flow

**Authentication**

1. The frontend submits registration or login credentials.
2. Express validates the request.
3. Passwords are hashed during account creation.
4. Express issues a JWT after successful authentication.
5. The frontend stores the token in browser local storage.
6. Authenticated API requests include the token in the authorization header.

**Wellness Assessment**

1. The student completes the check-in.
2. The React client submits the data to Express.
3. Express validates the lifestyle inputs.
4. Express requests stress inference from FastAPI.
5. FastAPI validates the request and executes the trained model.
6. The AI service returns the prediction and recommendations.
7. Express stores the check-in in MongoDB.
8. The backend evaluates the high-stress notification logic.
9. The frontend displays the result.

**AI Conversation**

1. The frontend sends conversation messages and optional student context.
2. Express forwards the request to the AI service.
3. The AI service attempts to generate a contextual response.
4. A fallback response is used when the configured provider cannot be used.
5. Express returns the response to the frontend.

---

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React 18, Vite |
| UI development | JSX, CSS |
| Data visualization | Recharts |
| Icons | Lucide React |
| Frontend communication | Fetch API |
| Backend runtime | Node.js |
| Backend framework | Express 4 |
| Authentication | JSON Web Tokens |
| Password security | bcryptjs |
| Database | MongoDB |
| Database integration | Mongoose |
| HTTP communication | Axios |
| Email notifications | Nodemailer, SMTP |
| AI API | FastAPI |
| Python validation | Pydantic |
| Machine learning | scikit-learn |
| Data processing | Pandas, NumPy |
| Model serialization | Joblib and pickle |
| AI provider integration | OpenAI-compatible client, Groq configuration, Gemini integration |
| Testing | Pytest, HTTPX |
| Containerization | Docker, Docker Compose |
| Frontend build | Vite |

---

## Project Structure

```text
test-main-branch/
│
├── client/                              # React frontend
│   ├── public/
│   │   ├── favicon.svg
│   │   └── robots.txt
│   │
│   ├── src/
│   │   ├── assets/
│   │   │   └── logo.svg
│   │   │
│   │   ├── components/
│   │   │   ├── ErrorBoundary.jsx
│   │   │   ├── StressCard.jsx
│   │   │   └── index.js
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx                     # Main application UI
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── .env.example
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
│
├── server/                              # Node.js / Express API
│   ├── src/
│   │   ├── config/
│   │   │   ├── db.js                   # MongoDB connection
│   │   │   └── mailer.js                # SMTP transporter
│   │   │
│   │   ├── controllers/
│   │   │   ├── authController.js
│   │   │   ├── chatController.js
│   │   │   ├── contactController.js
│   │   │   └── wellnessController.js
│   │   │
│   │   ├── middleware/
│   │   │   ├── authMiddleware.js
│   │   │   └── errorMiddleware.js
│   │   │
│   │   ├── models/
│   │   │   ├── CheckIn.js
│   │   │   ├── Contact.js
│   │   │   └── User.js
│   │   │
│   │   ├── routes/
│   │   │   ├── authRoutes.js
│   │   │   ├── chatRoutes.js
│   │   │   ├── contactRoutes.js
│   │   │   └── wellnessRoutes.js
│   │   │
│   │   ├── services/
│   │   │   ├── aiService.js
│   │   │   └── alertService.js
│   │   │
│   │   ├── app.js                      # Express configuration
│   │   └── server.js                   # Server entry point
│   │
│   ├── .env.example
│   ├── Dockerfile
│   ├── package.json
│   └── package-lock.json
│
├── ai-service/                          # Python AI microservice
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py               # Configuration
│   │   │   └── llm.py                  # LLM client selection
│   │   │
│   │   ├── routes/
│   │   │   ├── chat.py
│   │   │   └── wellness.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── chat.py
│   │   │   └── wellness.py
│   │   │
│   │   ├── services/
│   │   │   ├── companion_engine.py
│   │   │   ├── stress_engine.py
│   │   │   ├── wearable_engine.py
│   │   │   └── wearable_feature_extraction.py
│   │   │
│   │   └── main.py
│   │
│   ├── data/
│   │   └── student_stress_dataset.csv
│   │
│   ├── models/
│   │   ├── model_metrics.json
│   │   ├── stress-classifier-model.pkl
│   │   ├── stress-model-regressor.pkl
│   │   ├── student_stress_rfc.joblib
│   │   ├── student_stress_regressor.joblib
│   │   └── student_stress_scaler.joblib
│   │
│   ├── tests/
│   │   ├── test_api_endpoints.py
│   │   └── test_stress_engine.py
│   │
│   ├── train_model.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── DEPLOYMENT_GUIDE.md
├── DEPLOYMENT_GUIDE.pdf
├── PROJECT_GUIDE.md
├── PROJECT_GUIDE.pdf
├── fileStructure.txt
└── README.md
```

Some directories and files, such as Python cache files and pytest cache data, may be present in a local working copy but are not required for normal application operation.

---

## Prerequisites

Install the following tools before starting local development:

- **Node.js:** A modern supported LTS release.
- **npm:** Included with Node.js.
- **Python:** Python 3.10 or later is a reasonable starting point; use a version compatible with the selected dependencies.
- **pip:** Python package installer.
- **MongoDB:** Local installation or MongoDB Atlas account.
- **Git:** For source control.
- **Docker and Docker Compose:** Optional, for containerized services.

You will also need credentials for whichever optional integrations you choose to enable:

- An LLM API key for cloud-based AI responses.
- SMTP credentials for actual email delivery.

The machine learning model artifacts are included in the repository, so model retraining is not necessary for ordinary inference if the included artifacts are compatible with the installed Python environment.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd test-main-branch
```

Replace `<YOUR_REPOSITORY_URL>` with the actual repository URL.

If you already have the project locally, navigate to its root directory instead.

### 2. Configure Environment Variables

Create local environment files from the examples:

```bash
cp server/.env.example server/.env
cp ai-service/.env.example ai-service/.env
cp client/.env.example client/.env
```

The backend and AI service read their own configuration. The frontend uses Vite environment variables during development and build.

Edit the generated files and replace placeholder values where required.

**Never commit real API keys, passwords, JWT secrets, SMTP credentials, or populated environment files.**

### 3. Start MongoDB

If using a local MongoDB installation, make sure the MongoDB service is running.

The default local connection string is:

```env
MONGO_URI=mongodb://localhost:27017/mindmate
```

Alternatively, create a MongoDB Atlas database and use its connection string.

Ensure that the database user and network access settings permit the backend to connect.

### 4. Install Frontend Dependencies

Open a terminal at the project root:

```bash
cd client
npm install
```

Start the development server:

```bash
npm run dev
```

Vite normally serves the application at:

```text
http://localhost:5173
```

### 5. Install Backend Dependencies

Open another terminal:

```bash
cd server
npm install
```

Configure `server/.env` with the MongoDB connection string and a strong JWT secret.

Start the Express backend:

```bash
npm run dev
```

The backend defaults to port `5000`.

Check the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "API Gateway active"
}
```

### 6. Set Up the Python AI Service

Open another terminal:

```bash
cd ai-service
python -m venv .venv
```

Activate the environment.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Configure `ai-service/.env` with the required AI provider settings.

Start FastAPI from the `ai-service` directory:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API should now be accessible at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

Health endpoint:

```bash
curl http://localhost:8000/health
```

### 7. Verify the Service Connection

For local development, the backend should point to:

```env
FASTAPI_SERVICE_URL=http://localhost:8000
```

The frontend should point to the Express API:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

Restart the relevant service after changing environment variables.

Vite environment variables are incorporated into the frontend build, so changing them in a deployed environment generally requires a new build and deployment.

### 8. Open MindMate

With MongoDB, Express, FastAPI, and Vite running, visit:

```text
http://localhost:5173
```

Register a test account and verify authentication before testing protected features.

---

## Environment Configuration

Environment variables are separated by service to keep configuration manageable.

### Root `.env.example`

The root example is a reference checklist covering variables for multiple services. It is not automatically loaded by all services.

Use the service-specific environment files when running the application locally.

### Backend: `server/.env`

| Variable | Purpose | Example |
|---|---|---|
| `PORT` | Express listening port | `5000` |
| `NODE_ENV` | Runtime environment | `development` |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/mindmate` |
| `JWT_SECRET` | Secret used to sign tokens | A strong random secret |
| `JWT_EXPIRES_IN` | Token lifetime | `7d` |
| `FASTAPI_SERVICE_URL` | Base URL of FastAPI | `http://localhost:8000` |
| `GEMINI_API_KEY` | Optional direct Gemini integration | Provider API key |
| `SMTP_HOST` | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USER` | SMTP account username | Your email address |
| `SMTP_PASS` | SMTP password or app password | Secret value |
| `SMTP_FROM` | Sender identity | `MindMate Support <alerts@example.com>` |
| `SERVE_STATIC` | Enable built frontend serving | `false` |

### AI Service: `ai-service/.env`

| Variable | Purpose | Example |
|---|---|---|
| `PORT` | AI service port | `8000` |
| `GEMINI_API_KEY` | Optional Gemini credential | Provider API key |
| `AI_PROVIDER` | Configured AI provider | `groq` |
| `AI_BASE_URL` | OpenAI-compatible API base URL | `https://api.groq.com/openai/v1` |
| `AI_API_KEY` | Configured provider credential | Provider API key |
| `AI_MODEL` | Configured model name | `qwen-2.5-32b` |
| `ALLOWED_ORIGINS` | Comma-separated allowed origins | Local development URLs |

The model name in the example is a configuration value. Actual availability depends on the selected provider and its current model catalog.

### Frontend: `client/.env`

| Variable | Purpose | Example |
|---|---|---|
| `VITE_API_BASE_URL` | Base URL for frontend API requests | `http://localhost:5000/api` |

For a separately hosted frontend:

```env
VITE_API_BASE_URL=https://your-backend.example.com/api
```

For a same-origin deployment:

```env
VITE_API_BASE_URL=/api
```

### Important Configuration Notes

- `JWT_SECRET` must be a strong, unique secret in production.
- Never expose server-side secrets through variables prefixed with `VITE_`.
- `FASTAPI_SERVICE_URL` must be reachable from the Node.js process.
- When using Docker Compose, service-to-service communication uses Docker service names rather than `localhost`.
- The SMTP settings must be valid before relying on email delivery.
- The root environment example is documentation, not a substitute for configuring each service.

---

## Running the Application

### Local Development

Run the services in separate terminals.

**Terminal 1 — MongoDB**

Start the local database service.

**Terminal 2 — FastAPI**

```bash
cd ai-service
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 3 — Express**

```bash
cd server
npm run dev
```

**Terminal 4 — React**

```bash
cd client
npm run dev
```

The frontend communicates with Express, and Express communicates with MongoDB and FastAPI.

### Production Frontend Build

To generate an optimized frontend bundle:

```bash
cd client
npm run build
```

The output is written to:

```text
client/dist/
```

Preview the production build locally:

```bash
npm run preview
```

The Vite preview server is intended for previewing a build, not as a complete production hosting strategy.

### Backend Production Mode

From the server directory:

```bash
npm start
```

The Express entry point loads environment variables, initiates the MongoDB connection, and starts listening on the configured port.

---

## Application Workflows

### User Registration and Login

1. The user enters account details.
2. The backend validates the email address and required fields.
3. The password is hashed using bcrypt before storage.
4. The backend issues a JWT after successful registration or login.
5. The client stores the token under the `mm_token` local storage key.
6. Subsequent protected API requests include the bearer token.

### Daily Assessment

1. The student opens the wellness assessment.
2. Lifestyle information and psychological responses are collected.
3. The frontend submits the data to `POST /api/wellness/checkin`.
4. The backend validates numeric inputs and calls the AI service.
5. The AI service performs inference using the trained artifacts.
6. The resulting assessment is stored in MongoDB.
7. The backend evaluates the configured high-stress notification logic.
8. The saved record is returned to the frontend.

A unique database index on the user and date prevents multiple separate records for the same user/date combination. The check-in endpoint uses an upsert to create or update that record.

### Chat Conversation

1. The student enters a message.
2. The frontend sends messages and optional wellness context.
3. Express normalizes the request and forwards it to the AI integration.
4. The AI service attempts to produce a contextual reply.
5. A fallback response can be returned if the LLM is unavailable.
6. The frontend displays the response.

### Emergency SOS

1. The user configures one or more trusted contacts.
2. The user initiates an SOS request.
3. The backend retrieves the selected contacts belonging to the authenticated user.
4. The alert service attempts to send an email through SMTP.
5. The backend returns a status message.

In a development configuration without usable SMTP credentials, notification dispatch may be simulated through server logs. A successful HTTP response must not be interpreted as proof that a real person received or acknowledged the alert.

---

## Machine Learning Pipeline

### Model Inputs

The main stress classifier uses seven psychological assessment features:

| Feature | Meaning |
|---|---|
| `Nervousness` | Nervousness or feeling on edge |
| `Unable to control` | Difficulty controlling worry |
| `Worry` | Excessive worry |
| `Trouble in Relaxation` | Difficulty relaxing |
| `Restlessness` | Restlessness |
| `Irritability` | Irritability |
| `Fear` | Fear or apprehension |

Each feature is represented on a scale from `0` to `3`.

Lifestyle features such as sleep, study time, screen exposure, and exam proximity are also accepted by the AI service, primarily for contextual processing and recommendation generation.

### Dataset

The repository includes:

```text
ai-service/data/student_stress_dataset.csv
```

The dataset contains 16,384 records according to the stored model metrics.

The training script uses the seven psychological features to predict the `Stress` target.

The provenance, licensing, representativeness, and clinical validation status of the dataset should be independently verified before the system is used beyond an educational or experimental context.

### Training Pipeline

The training script is located at:

```text
ai-service/train_model.py
```

Its workflow includes:

1. Loading the CSV dataset.
2. Selecting the psychological feature columns and target.
3. Fitting a `StandardScaler`.
4. Splitting the dataset into training and test partitions.
5. Training a Random Forest classifier.
6. Evaluating classification performance.
7. Training a Random Forest regressor.
8. Saving model artifacts and evaluation metrics.

The classifier configuration includes:

```python
RandomForestClassifier(
    n_estimators=120,
    max_depth=10,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```

The regression model uses a Random Forest Regressor.

The script saves the classifier, regressor, scaler, and metrics under `ai-service/models/`.

### Stored Model Artifacts

| File | Purpose |
|---|---|
| `student_stress_rfc.joblib` | Main Random Forest classifier |
| `student_stress_regressor.joblib` | Regression model |
| `student_stress_scaler.joblib` | Feature scaling |
| `model_metrics.json` | Stored evaluation metrics |
| `stress-classifier-model.pkl` | Additional serialized classifier artifact |
| `stress-model-regressor.pkl` | Additional serialized regressor artifact |

The primary inference engine loads the artifacts referenced by its implementation. The presence of additional pickle files does not imply that all artifacts are used during every request.

### Stored Evaluation Metrics

The included `model_metrics.json` reports:

| Metric | Stored value |
|---|---:|
| Accuracy | 85.20% |
| Weighted precision | 86.74% |
| Weighted recall | 85.20% |
| Weighted F1-score | 85.72% |
| Dataset samples | 16,384 |

These are the metrics recorded in the repository. They should not be interpreted as independently verified clinical performance or as a guarantee of real-world prediction accuracy.

The training script uses a fixed train/test split. These results are not, by themselves, evidence of cross-validation performance.

### Inference and Stress Levels

The AI service returns:

- A normalized score from 0 to 100.
- A user-facing stress level.
- Predicted class.
- Prediction confidence.
- Probabilities for the available classes.
- The primary contributing symptom.
- A regression severity score.
- Recommended wellness activities.

The user-facing application uses `Low`, `Moderate`, and `High` as stress levels, while the machine learning classifier uses `No Stress`, `Mild Stress`, `Moderate Stress`, and `Severe Stress`.

These are different representations. The service's mapping logic determines how model predictions are converted into the application's score and level.

### Retraining the Model

To retrain the included model:

```bash
cd ai-service
source .venv/bin/activate
python train_model.py
```

Review the output and generated artifacts before deploying a retrained model.

Because serialized model formats can depend on Python and scikit-learn versions, keep the training and inference environments compatible.

---

## AI Wellness Companion

The AI integration is separated into a provider configuration layer and a conversational service.

### Relevant Files

```text
ai-service/app/
├── core/
│   ├── config.py
│   └── llm.py
├── routes/
│   └── chat.py
├── schemas/
│   └── chat.py
└── services/
    └── companion_engine.py
```

The Node.js integration is located at:

```text
server/src/services/aiService.js
```

### Provider Configuration

The Python service supports an OpenAI-compatible client configuration and includes a Gemini configuration path.

Example Groq configuration:

```env
AI_PROVIDER=groq
AI_BASE_URL=https://api.groq.com/openai/v1
AI_API_KEY=your_provider_api_key
AI_MODEL=your_available_model
```

Use a model name supported by the selected provider.

If the LLM cannot be initialized or a request fails, the companion engine includes a rule-based fallback path.

### Conversation Context

The chat request can include:

- Stress level.
- Stress score.
- Sleep duration.
- Study duration.
- Screen exposure.
- Days until the next examination.

This information allows the companion to tailor its response to the submitted context.

### Safety Considerations

The companion includes basic keyword-based crisis handling and supportive response instructions.

Keyword detection is not a complete crisis detection system. It can miss indirect expressions, misunderstand context, or produce false positives.

The system should not be relied upon as the sole mechanism for crisis intervention. Users experiencing immediate danger should contact local emergency services or a qualified crisis support provider.

---

## Backend API Reference

The Express API base URL is:

```text
http://localhost:5000/api
```

The examples below assume that the backend is running locally.

### Authentication

Base path: `/api/auth`

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| `POST` | `/signup` | Public | Register an account |
| `POST` | `/login` | Public | Authenticate a user |
| `GET` | `/profile` | Required | Retrieve the authenticated profile |
| `PUT` | `/profile` | Required | Update profile details |

#### Register

```http
POST /api/auth/signup
Content-Type: application/json
```

Example body:

```json
{
  "name": "Example Student",
  "email": "student@example.com",
  "password": "replace-with-a-strong-password"
}
```

The password must be at least eight characters according to the user model.

#### Login

```http
POST /api/auth/login
Content-Type: application/json
```

Example body:

```json
{
  "email": "student@example.com",
  "password": "replace-with-a-strong-password"
}
```

Successful registration and login responses contain the user profile fields and a JWT.

#### Retrieve Profile

```http
GET /api/auth/profile
Authorization: Bearer YOUR_TOKEN
```

#### Update Profile

```http
PUT /api/auth/profile
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

Supported fields include:

- `name`
- `email`
- `college`
- `avatar`
- `preferences`
- `autoNotify`

The `preferences` field contains notification and tips preferences represented by the user schema.

### Wellness

Base path: `/api/wellness`

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| `POST` | `/checkin` | Required | Create or update today's assessment |
| `GET` | `/today` | Required | Retrieve today's assessment |
| `GET` | `/history` | Required | Retrieve up to seven recent assessments |

#### Submit a Check-In

```http
POST /api/wellness/checkin
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

Example body:

```json
{
  "sleep": 7,
  "study": 5,
  "screen": 6,
  "exam": 4,
  "mood": "okay",
  "note": "Preparing for upcoming examinations",
  "nervousness": 1,
  "unableToControl": 2,
  "worry": 2,
  "troubleInRelaxation": 1,
  "restlessness": 1,
  "irritability": 1,
  "fear": 1
}
```

The example values are illustrative, not a recommended self-assessment.

The psychological inputs are expected on the `0`–`3` scale. Lifestyle values must satisfy the validation rules enforced by the backend and AI service.

#### Retrieve Today's Assessment

```http
GET /api/wellness/today
Authorization: Bearer YOUR_TOKEN
```

The response contains the stored record or `null` when no assessment exists for the current date.

#### Retrieve Recent History

```http
GET /api/wellness/history
Authorization: Bearer YOUR_TOKEN
```

The endpoint returns up to seven records in chronological order.

### Emergency Contacts

Base path: `/api/contacts`

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| `GET` | `/` | Required | List the user's contacts |
| `POST` | `/` | Required | Add a trusted contact |
| `DELETE` | `/:id` | Required | Delete a trusted contact |
| `POST` | `/alert` | Required | Trigger an SOS email attempt |

#### Add a Contact

```http
POST /api/contacts
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

Example body:

```json
{
  "name": "Trusted Contact",
  "rel": "Parent/Guardian",
  "email": "contact@example.com",
  "phone": "+911234567890"
}
```

The `rel` value must be one of the relationship categories supported by the schema.

#### List Contacts

```http
GET /api/contacts
Authorization: Bearer YOUR_TOKEN
```

#### Delete a Contact

```http
DELETE /api/contacts/CONTACT_ID
Authorization: Bearer YOUR_TOKEN
```

A contact can only be deleted through this endpoint if it belongs to the authenticated user.

#### Trigger SOS

```http
POST /api/contacts/alert
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

Example body:

```json
{
  "contactIds": ["CONTACT_ID_1", "CONTACT_ID_2"]
}
```

The backend selects the authenticated user's contacts and, when IDs are supplied, filters to those IDs.

An empty or omitted contact selection can cause the alert service to use all of the user's saved contacts.

The endpoint's success response indicates that the server accepted or simulated the dispatch operation; it does not establish actual delivery or acknowledgment.

### Chat

Base path: `/api/chat`

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| `POST` | `/` | Optional | Submit a conversation request |
| `POST` | `/message` | Optional | Submit a conversation request |

Example request:

```http
POST /api/chat/message
Content-Type: application/json
```

Example body:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I am feeling stressed about my examinations."
    }
  ],
  "context": {
    "level": "Moderate",
    "score": 55,
    "sleep": 6,
    "study": 7,
    "screen": 8,
    "exam": 3
  }
}
```

Example response shape:

```json
{
  "reply": "An empathetic wellness response from the configured AI integration.",
  "source": "fastapi"
}
```

The `source` field depends on the actual response path. Other paths include Gemini or fallback handling.

The controller also accepts legacy-style single-message inputs and normalizes them into a message array.

### Health Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Express service health |
| `GET` | `/api/health` | Express service health |

Example:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "API Gateway active"
}
```

---

## FastAPI AI Service Reference

The AI service runs independently from the Express backend.

Default base URL:

```text
http://localhost:8000
```

Interactive documentation:

```text
http://localhost:8000/docs
```

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Reports service status and model readiness |
| `POST` | `/wellness/compute-stress` | Computes a stress prediction and recommendations |
| `POST` | `/chat/message` | Generates a conversational response |

### Stress Inference Request

```http
POST /wellness/compute-stress
Content-Type: application/json
```

Example body:

```json
{
  "sleep": 7,
  "study": 5,
  "screen": 6,
  "exam": 4,
  "mood": "okay",
  "note": "",
  "nervousness": 1,
  "unableToControl": 2,
  "worry": 2,
  "troubleInRelaxation": 1,
  "restlessness": 1,
  "irritability": 1,
  "fear": 1
}
```

The schema accepts numeric psychological responses from `0` to `3`. It also supports the strings `No`, `Mild`, `Moderate`, and `Severe`.

The response includes the score, level, recommendations, and ML prediction details.

If the inference engine is unavailable, the service returns an appropriate error rather than guaranteeing a successful prediction.

### Chat Request

```http
POST /chat/message
Content-Type: application/json
```

Example body:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Can you help me calm down before an exam?"
    }
  ],
  "context": {
    "level": "Moderate",
    "score": 50,
    "sleep": 7,
    "study": 6,
    "screen": 5,
    "exam": 1
  }
}
```

Example response:

```json
{
  "reply": "A supportive response generated by the companion service."
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

The response includes the configured provider, configured model name, and whether the stress model is loaded.

The health endpoint is useful for checking service startup, but provider configuration alone does not guarantee that external AI requests will succeed.

---

## Database Models

MindMate uses MongoDB with Mongoose schemas.

### User

File:

```text
server/src/models/User.js
```

The user model stores:

- Name.
- Email address.
- Hashed password.
- College.
- Avatar data.
- Notification and tip preferences.
- Automatic notification preference.
- Consecutive high-stress day count.
- Last alert timestamp.
- Creation and update timestamps.

Email addresses are normalized to lowercase, and the schema enforces uniqueness.

Passwords are hashed with bcrypt before saving.

### CheckIn

File:

```text
server/src/models/CheckIn.js
```

The check-in model stores:

- User ID.
- Date.
- Sleep duration.
- Study duration.
- Screen exposure.
- Exam proximity.
- Mood.
- Optional notes.
- Seven psychological assessment features.
- Normalized stress score.
- User-facing stress level.
- ML prediction details.
- Wellness recommendations.
- Creation and update timestamps.

A unique compound index on `userId` and `date` enforces one record per user per date.

### Contact

File:

```text
server/src/models/Contact.js
```

The contact model stores:

- User ID.
- Contact name.
- Relationship category.
- Email address.
- Phone number.
- Creation and update timestamps.

Contact queries are scoped to the authenticated user's ID.

### Data Relationships

```text
User
 ├── CheckIn[]
 │    └── One record per user per date
 │
 └── Contact[]
      └── Trusted emergency contacts
```

---

## Emergency Notifications

The emergency alert implementation is located in:

```text
server/src/services/alertService.js
server/src/config/mailer.js
```

### SMTP Configuration

Example:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_email_app_password
SMTP_FROM="MindMate Support <alerts@example.com>"
```

Use the authentication method recommended by your SMTP provider.

For Gmail, this may require an app password and an account with the appropriate security configuration.

### Manual SOS

The manual alert path attempts to send an email to the user's selected trusted contacts.

When placeholder credentials are detected, the implementation can log a simulated alert instead.

### Automatic High-Stress Alerts

The backend includes logic for consecutive high-stress days and alert timestamps.

Before production use, verify:

- The exact stress level that increments the streak.
- How a lower stress result resets or affects the streak.
- Whether duplicate alerts are suppressed.
- Whether notification preferences are enforced.
- How SMTP failures are reported and retried.
- Whether the contact and student consent flows are appropriate.

An email integration is not a substitute for a monitored emergency response service.

### SMS Support

The current backend does not implement an SMS provider integration.

To add SMS in the future, integrate a provider such as Twilio or another suitable messaging service, create a dedicated notification service, and configure the required credentials securely.

SMS delivery, provider charges, recipient consent, regional regulations, and delivery status must be handled separately.

---

## Docker Deployment

The repository includes:

```text
docker-compose.yml
```

The current Compose file defines three services:

- `mongodb`
- `ai-service`
- `server`

It does not define a standalone React frontend service.

### Configure Docker Environment Files

Create the environment files if they do not already exist:

```bash
cp server/.env.example server/.env
cp ai-service/.env.example ai-service/.env
```

Configure the necessary credentials and secrets.

### Start the Services

From the project root:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

View logs:

```bash
docker compose logs -f
```

View individual service logs:

```bash
docker compose logs -f server
docker compose logs -f ai-service
docker compose logs -f mongodb
```

Stop the services:

```bash
docker compose down
```

To remove the MongoDB data volume as well:

```bash
docker compose down -v
```

**Warning:** Removing volumes deletes the persisted database data stored in those volumes. Do not use `-v` if you need to preserve your database.

### Service URLs

| Service | Local URL |
|---|---|
| Express backend | `http://localhost:5000` |
| FastAPI AI service | `http://localhost:8000` |
| FastAPI documentation | `http://localhost:8000/docs` |
| MongoDB | `localhost:27017` |

### Docker Networking

Inside Docker Compose, the backend uses:

```env
MONGO_URI=mongodb://mongodb:27017/mindmate
FASTAPI_SERVICE_URL=http://ai-service:8000
```

These service names are resolvable within the Compose network.

Do not replace them with `localhost` inside the backend container. In a container, `localhost` refers to that same container.

### Running the Frontend with Docker

The frontend has its own Dockerfile and Nginx configuration.

It can be built separately:

```bash
docker build -t mindmate-client ./client
```

However, the final deployment must ensure that the frontend uses the correct `VITE_API_BASE_URL` for the reachable backend.

For a separately hosted frontend, configure the public backend URL during the Vite build.

For a same-origin deployment, configure the routing and proxy behavior so API requests reach Express correctly.

The frontend container is not automatically started by the repository's current Compose configuration.

---

## Production Deployment

Before deploying, choose the hosting architecture that matches the application's requirements.

### Option A: Separate Frontend and Backend

A possible architecture is:

| Component | Hosting option |
|---|---|
| React frontend | Vercel, Netlify, or static hosting |
| Express backend | Render, Railway, or a VPS |
| FastAPI service | Render, Railway, or a Python-capable host |
| Database | MongoDB Atlas |

Configure the frontend with the public backend URL:

```env
VITE_API_BASE_URL=https://your-backend.example.com/api
```

Configure the Express service with the public or private AI service URL, depending on the hosting topology:

```env
FASTAPI_SERVICE_URL=https://your-ai-service.example.com
```

Configure the FastAPI CORS allowlist as needed for browser origins. In this architecture, Express-to-FastAPI requests are server-to-server, so browser CORS settings alone do not control that connection.

### Option B: Unified Frontend and Backend

The Express application contains support for serving the built frontend when a valid `client/dist` directory is found and static serving is enabled or the runtime is in production mode.

Build the frontend and install backend dependencies:

```bash
npm --prefix client install
npm --prefix client run build
npm --prefix server install
```

Start the backend:

```bash
cd server
npm start
```

Configure:

```env
NODE_ENV=production
SERVE_STATIC=true
VITE_API_BASE_URL=/api
```

The frontend build must use the intended API base URL. Set `VITE_API_BASE_URL` before building the frontend.

The hosting platform must build the frontend and backend in the correct order, provide persistent external database connectivity, and configure the required environment variables.

### Production Checklist

Before publishing the application:

- [ ] Remove development credentials and placeholders.
- [ ] Use a strong, unique JWT secret.
- [ ] Configure MongoDB Atlas or another appropriate database deployment.
- [ ] Restrict database network access.
- [ ] Configure valid AI provider credentials.
- [ ] Configure and test SMTP delivery.
- [ ] Set the correct frontend API URL.
- [ ] Configure CORS for trusted frontend origins.
- [ ] Use HTTPS for public endpoints.
- [ ] Confirm that model artifacts are available to the AI service.
- [ ] Verify the FastAPI health endpoint and model readiness.
- [ ] Verify registration and login.
- [ ] Verify protected API access.
- [ ] Test check-in persistence and history.
- [ ] Test AI responses with and without valid provider credentials.
- [ ] Test SOS behavior with real SMTP and simulation configurations.
- [ ] Confirm that no secrets are included in Git history or frontend bundles.
- [ ] Test error handling and service restarts.
- [ ] Document the limitations of automated alerts and stress predictions.

Refer to `DEPLOYMENT_GUIDE.md` for the repository's existing deployment instructions.

---

## Testing

The Python AI service includes automated tests under:

```text
ai-service/tests/
├── test_api_endpoints.py
└── test_stress_engine.py
```

### Run the AI Service Tests

Activate the Python virtual environment:

```bash
cd ai-service
source .venv/bin/activate
```

Run:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest -v tests/test_api_endpoints.py
```

Or:

```bash
pytest -v tests/test_stress_engine.py
```

Some tests may require the model artifacts or service dependencies to be available.

### Manual Health Checks

Check Express:

```bash
curl http://localhost:5000/health
```

Check FastAPI:

```bash
curl http://localhost:8000/health
```

### Recommended Integration Tests

In addition to the existing tests, verify:

1. Registration with valid and invalid email addresses.
2. Rejection of duplicate accounts.
3. Password verification during login.
4. Rejection of missing or invalid JWTs on protected routes.
5. Validation of out-of-range lifestyle values.
6. Validation of psychological assessment values.
7. Creation and retrieval of a daily check-in.
8. Prevention of duplicate daily records.
9. Ownership checks for emergency contacts.
10. Chat behavior when the AI provider is unavailable.
11. Email delivery and SMTP failure handling.
12. Frontend behavior when a backend endpoint returns an error.

---

## Troubleshooting

### Frontend Cannot Reach the Backend

Check:

```env
VITE_API_BASE_URL=http://localhost:5000/api
```

Confirm that Express is running:

```bash
curl http://localhost:5000/health
```

If the frontend is deployed separately, `localhost` refers to the user's own device, not the deployed backend. Use the public backend URL instead.

Restart Vite after changing its environment variables.

### MongoDB Connection Failure

Check:

- Whether MongoDB is running.
- Whether `MONGO_URI` is correct.
- Whether the database user has the required permissions.
- Whether Atlas network access permits the connection.
- Whether credentials in the connection string are correctly URL-encoded.

### FastAPI Connection Failure

Check:

```env
FASTAPI_SERVICE_URL=http://localhost:8000
```

For Docker Compose, use:

```env
FASTAPI_SERVICE_URL=http://ai-service:8000
```

Confirm that FastAPI is running and that `/health` is reachable from the backend environment.

### ML Model Not Loaded

Check that the model files referenced by the inference engine exist under:

```text
ai-service/models/
```

Verify that the required Python dependencies are installed and compatible with the serialized artifacts.

Inspect the AI service startup logs and health response for model readiness.

### AI Chat Returns Fallback Responses

Check:

- AI provider configuration.
- API key validity.
- Model availability.
- Network connectivity.
- Provider rate limits and usage limits.
- AI service logs.
- Direct Gemini configuration if using the Node.js fallback path.

Fallback responses can be expected when a provider is not configured or is unavailable.

### Email Alerts Are Not Received

Check:

- SMTP hostname and port.
- SMTP username and password.
- App password or provider authentication requirements.
- Sender configuration.
- Recipient email addresses.
- Server logs for delivery errors.

Also check whether the application is using its simulated notification path because placeholder SMTP credentials are configured.

### Docker Service Cannot Find Another Service

Within Compose, use service names such as:

```text
mongodb
ai-service
```

Do not use `localhost` for another container's service address.

### Frontend Build or Deployment Problems

Run:

```bash
cd client
npm install
npm run build
```

Inspect build errors and ensure that environment variables are set correctly before building.

For unified deployment, verify that `client/dist` is available at a path the Express application can resolve.

---

## Security and Privacy

MindMate processes potentially sensitive wellness information. Security and privacy should be considered essential parts of deployment.

### Authentication

- Passwords are hashed with bcrypt.
- JWTs protect authenticated routes.
- The frontend stores the token in local storage.

Local storage is accessible to JavaScript running on the page, so cross-site scripting vulnerabilities could expose a token. A production deployment should evaluate stronger session protections, secure cookie-based authentication where appropriate, and comprehensive XSS prevention.

### Data Protection

Wellness check-ins contain self-reported psychological information and personal notes.

Recommended safeguards include:

- Use HTTPS.
- Restrict access to user-owned records.
- Apply least-privilege database credentials.
- Keep secrets outside the source repository.
- Avoid logging personal wellness content or credentials.
- Establish a clear retention and deletion policy.
- Provide appropriate user consent and privacy disclosures.
- Encrypt sensitive data at rest and in transit as appropriate.
- Establish backup and recovery procedures.

### API Security

The application should be reviewed for:

- Rate limiting.
- Request-size limits.
- Input validation and sanitization.
- Strict CORS configuration.
- Authentication and authorization coverage.
- Abuse prevention for AI and SOS endpoints.
- Safe error responses.
- Monitoring and audit logging.
- Protection against excessive API usage and denial-of-service conditions.

### Emergency Features

Emergency contact details should only be collected and used with appropriate consent.

Automated emails may fail, be delayed, or reach an unattended inbox. MindMate must not be represented as a guaranteed emergency dispatch system.

### Machine Learning Limitations

A model trained on a dataset is not automatically clinically validated. Its predictions may be affected by data quality, dataset bias, self-reporting errors, and differences between training data and real users.

The score should be presented as an estimate based on the application's inputs, not as a medical diagnosis.

---

## Known Limitations

The following points are important when evaluating the current repository:

1. **SMS delivery is not implemented.** The backend stores phone numbers but its SOS notification implementation is email-based.

2. **Docker Compose does not include the React frontend.** The current Compose file starts MongoDB, FastAPI, and Express. The frontend must be run or deployed separately unless the deployment uses the built frontend through Express.

3. **LLM behavior depends on configuration.** Actual responses depend on provider credentials, model availability, network connectivity, and usage limits.

4. **Crisis detection is limited.** Keyword-based handling cannot reliably identify every crisis situation.

5. **Model metrics are repository-reported values.** They are not independent proof of clinical validity or real-world performance.

6. **The system is not a medical device.** Stress estimates and wellness recommendations should not replace professional assessment.

7. **Automated notifications need deployment testing.** A successful backend response does not guarantee that an email has been delivered or read.

8. **Production security requires additional review.** Development-oriented defaults, permissive CORS, browser token storage, and externally exposed service ports should be evaluated before public deployment.

9. **Optional integrations may incur costs.** LLM APIs, email providers, hosting, databases, and future SMS integrations may have usage limits or charges.

10. **Wearable-related modules are present.** The repository includes wearable stress and feature-extraction modules, but their presence alone does not establish an integrated, production-ready wearable data pipeline.

---

## Future Improvements

Potential extensions include:

- Implement SMS notifications through a dedicated messaging provider.
- Add delivery-status tracking and controlled notification retries.
- Introduce configurable notification preferences and quiet hours.
- Improve authentication security and session management.
- Add comprehensive frontend and backend automated tests.
- Add API rate limiting and abuse protection.
- Introduce structured application logging and monitoring.
- Add model versioning and reproducible training pipelines.
- Evaluate the classifier using stronger validation methods.
- Document dataset provenance and limitations.
- Add more robust safety testing for the wellness companion.
- Improve accessibility and multilingual support.
- Integrate wearable data through a validated ingestion pipeline.
- Add account deletion, data export, and retention controls.
- Improve observability across the frontend, Express API, database, and AI service.

These are suggested improvements, not claims that the functionality already exists.

---

## Contributing

Contributions are welcome.

### Suggested Workflow

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change.
4. Run relevant tests.
5. Review environment and security implications.
6. Commit your changes with a meaningful message.
7. Open a pull request describing the change.

Example:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Do not commit `.env` files, credentials, virtual environments, generated caches, or other local-only files.

---

## License

No explicit license file was identified in the inspected project structure.

Until a license is added, do not assume that the repository grants permission to redistribute, modify, or commercially use the project.

If you intend to publish MindMate as an open-source project, add a `LICENSE` file specifying the intended terms.

---

## Acknowledgements

MindMate brings together several open-source technologies and machine learning tools, including:

- React and Vite.
- Node.js and Express.
- FastAPI and Pydantic.
- MongoDB and Mongoose.
- scikit-learn, Pandas, and NumPy.
- Recharts and Lucide React.
- Docker and Docker Compose.

Refer to the respective projects' documentation for installation guidance and licensing information.

---

## Final Note

MindMate demonstrates how a full-stack web application can combine wellness tracking, machine learning inference, conversational AI, data visualization, and configurable emergency notifications.

Its purpose is to support student self-awareness and make wellness resources easier to access—not to replace professional mental health care or guarantee emergency intervention.

**Built to help students understand their patterns, take small steps toward well-being, and seek support when they need it.**
