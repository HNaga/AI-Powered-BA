# AI-Powered Business/System Analyst Platform

## Description
A platform designed to assist Business/System Analysts by leveraging AI for tasks like requirements gathering, documentation generation, and analysis.

## Current Status
**MVP Phase 1.5 Completed**

This Minimum Viable Product (MVP) phase integrates with the OpenAI API for problem statement processing. It builds upon the initial MVP by replacing mock AI responses with real AI-generated summaries and keywords.

## Features
*   **Basic Project Representation:** In-memory simulation of project data.
*   **Web Dashboard Interface:** A static HTML/CSS structure (`index.html`) for user interaction.
*   **OpenAI Integration:** The backend Flask endpoint (`/api/process_statement`) now processes problem statements using the OpenAI GPT-3.5-turbo model.
*   **Frontend Interaction:** JavaScript in the dashboard sends problem statements to the API and displays the AI-generated response.
*   **Manual Testing Guide:** Instructions (`MANUAL_TESTING_GUIDE.md`) for running and verifying the MVP.
*   **Environment Configuration:** Uses `.env` files for API key management.

## How to Run
This application requires Python, Flask, OpenAI, and python-dotenv.

1.  **Clone the repository** (if applicable).
2.  **Navigate to the project directory.**
3.  **Configuration - API Key Setup:**
    *   This project requires an OpenAI API key to function.
    *   A file named `.env.example` is included in this repository. Copy this file to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file with a text editor and replace `YOUR_OPENAI_API_KEY_HERE` with your actual OpenAI API key.
        ```
        OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
    *   **IMPORTANT:** The `.env` file contains sensitive API keys and should **NEVER** be committed to Git. Ensure `.env` is listed in your `.gitignore` file.

4.  **Install Dependencies:**
    *   It is recommended to use a virtual environment.
    *   The required packages are Flask, openai, and python-dotenv.
    *   You can create a `requirements.txt` file with the following content:
        ```
        Flask
        openai
        python-dotenv
        ```
    *   Then, install the dependencies using pip:
        ```bash
        pip install -r requirements.txt
        ```
    *   Alternatively, you can install them individually:
        ```bash
        pip install Flask openai python-dotenv
        ```

5.  **Run the Backend Flask Application:**
    *   Execute the following command in your terminal:
        ```bash
        python app.py
        ```
    *   The application should start, typically on `http://127.0.0.1:5000/`. The console will confirm this.

6.  **Access the Application:**
    *   Open your web browser and navigate to `http://127.0.0.1:5000/`.
    *   The `app.py` is configured to serve the `index.html` file, so this URL will load the main interface.

## Technology Stack
*   **Backend:** Python, Flask, OpenAI API (gpt-3.5-turbo)
*   **Frontend:** HTML, CSS, JavaScript (Vanilla)
*   **Environment Management:** python-dotenv, `.env` files
*   **Data Storage:** In-memory (for project data in this MVP)

## Future Steps
This is an evolving MVP. Future development will focus on:
*   Refining AI prompts and response parsing for more robust and structured outputs.
*   Implementing robust database storage for projects, requirements, and other artifacts.
*   Developing user management and authentication.
*   Expanding Business Analyst features as per the detailed design specification (e.g., BRD/SRS generation, diagramming assistance).
*   Adding more comprehensive error handling and UI/UX refinements.
*   Exploring different AI models and techniques for specific BA/SA tasks.
