# AI-Powered Business/System Analyst Platform

## Description
A platform designed to assist Business/System Analysts by leveraging AI for tasks like requirements gathering, documentation generation, and analysis.

## Current Status
**MVP Phase 1 Completed**

This initial Minimum Viable Product (MVP) phase establishes a basic end-to-end flow for submitting a problem statement via a web interface and receiving a mock AI-processed response. It serves as the foundational architecture for future development.

## Features (MVP Phase 1)
*   **Basic Project Representation:** In-memory simulation of project data.
*   **Web Dashboard Interface:** A static HTML/CSS structure (`index.html`) for user interaction.
*   **Mock AI Processing API:** A backend Flask endpoint (`/api/process_statement`) that simulates AI processing of a problem statement.
*   **Frontend Interaction:** JavaScript in the dashboard to send problem statements to the API and display the mock response.
*   **Manual Testing Guide:** Instructions (`MANUAL_TESTING_GUIDE.md`) for running and verifying the MVP.

## How to Run
This application requires Python and Flask.

1.  **Clone the repository** (if applicable).
2.  **Navigate to the project directory.**
3.  **Install Dependencies:**
    *   Currently, Flask is the main dependency. If you have Python installed, you can install Flask using pip:
        ```bash
        pip install Flask
        ```
4.  **Run the Backend Flask Application:**
    *   Execute the following command in your terminal:
        ```bash
        python app.py
        ```
    *   The application should start, typically on `http://127.0.0.1:5000/`. The console will confirm this.
5.  **Access the Application:**
    *   Open your web browser and navigate to `http://127.0.0.1:5000/` (or the specific route configured in `app.py` to serve `index.html` - refer to `MANUAL_TESTING_GUIDE.md` for the exact method if `app.py` was modified to serve it).

## Technology Stack (MVP Phase 1)
*   **Backend:** Python, Flask
*   **Frontend:** HTML, CSS, JavaScript (Vanilla)
*   **Data Storage:** In-memory (for project data in this MVP)
*   **AI Processing:** Mock/Simulated (no external AI model integrated yet)

## Future Steps
This is an early-stage MVP. Future development will focus on:
*   Integrating actual AI/Large Language Model (LLM) capabilities for processing.
*   Implementing robust database storage for projects, requirements, and other artifacts.
*   Developing user management and authentication.
*   Expanding Business Analyst features as per the detailed design specification (e.g., BRD/SRS generation, diagramming assistance).
*   Adding more comprehensive error handling and UI/UX refinements.
