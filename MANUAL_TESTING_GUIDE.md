# Manual Testing Guide for MVP End-to-End Flow

This guide provides instructions for manually testing the Minimum Viable Product (MVP) which includes the Flask backend (`app.py`) and the HTML/JavaScript frontend (`index.html`).

## 1. How to Run the Backend

The backend is a Flask application (`app.py`) that provides the `/api/process_statement` endpoint.

*   **Command to Run:**
    Open your terminal or command prompt, navigate to the root directory of the project where `app.py` is located, and execute the following command:
    ```bash
    python app.py
    ```

*   **Expected Output:**
    You should see output similar to the following, indicating the Flask development server is running:
    ```
     * Serving Flask app 'app'
     * Debug mode: on
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    ```
    The key part is `Running on http://127.0.0.1:5000`.

## 2. How to Run/Access the Frontend

The Flask application (`app.py`) is configured to serve the `index.html` file directly. This is the **primary and recommended method** for accessing the frontend, as it ensures seamless API calls and avoids Cross-Origin Resource Sharing (CORS) issues.

*   **Accessing the Application:**
    1.  Ensure the Flask backend (`app.py`) is running (see Section 1).
    2.  Open your web browser and navigate to:
        ```
        http://127.0.0.1:5000/
        ```
        or
        ```
        http://localhost:5000/
        ```
    3.  This should load `index.html`, served directly by the Flask application. Because both the frontend and the `/api/process_statement` endpoint are served from the same origin (`http://127.0.0.1:5000`), CORS issues should not occur.

*   **Alternative Method: Open `index.html` Directly (Strongly Discouraged for API Testing)**
    You *can* open `index.html` directly in your browser by navigating to its file path (e.g., `file:///path/to/your/project/index.html`).
    *   **Caveat - CORS Errors:** If you use this method, the JavaScript `fetch` call from `index.html` (served from `file://`) to `http://127.0.0.1:5000/api/process_statement` will **be blocked by the browser's Same-Origin Policy (CORS)**. You will see errors in the browser's developer console. This method is **not suitable** for testing the full end-to-end API interaction.

## 3. Testing Steps

Ensure the Flask backend (`app.py`) is running and you have loaded `index.html` in your browser by navigating to `http://127.0.0.1:5000/`.

1.  **Locate Input Area:** In the center panel of the loaded `index.html` page, find the textarea labeled "Describe the problem or opportunity...".
2.  **Enter Text:** Type a sample problem statement into the textarea. For example:
    `"Our customer support team is overwhelmed with inquiries about order status. We need a system that allows customers to track their orders online without needing to call support."`
3.  **Submit:** Click the "Analyze Statement" button.
4.  **Observe Frontend (Browser):**
    *   Immediately after clicking, your entered problem statement should appear in the "AI Assistant Chat" panel on the right, prefixed as a "user" message (e.g., "Problem Statement Submitted: ...").
    *   An "AI is analyzing the statement..." message should appear in the chat panel from the "assistant".
    *   After a brief moment (simulating API processing), the "AI is analyzing..." message in the chat should be updated with:
        *   A summary of your statement.
        *   A list of keywords.
    *   Simultaneously, in the center panel, the "AI Analysis" section (which was previously hidden) should become visible and display:
        *   **Original Statement:** The text you entered.
        *   **Summary:** The mock summary from the API.
        *   **Keywords:** The mock keywords from the API, joined by commas.
        *   **Status:** "success_mock".
    *   The problem statement textarea in the center panel should be cleared.
5.  **Observe Backend (Flask Console):**
    Look at the terminal where `app.py` is running. You should see a log entry for the POST request, similar to:
    ```
    127.0.0.1 - - [DD/Mon/YYYY HH:MM:SS] "POST /api/process_statement HTTP/1.1" 200 -
    ```
    This indicates the API endpoint was successfully called.

## 4. Expected Outcomes & Verification

*   **Successful Data Display:** The mock AI summary and keywords (e.g., "Summary of 'Our customer support team is ...': This statement needs careful analysis and further refinement.", Keywords: "analysis, requirements, stakeholder_input, our") are correctly displayed in both the center panel's "AI Analysis" section and updated in the right-hand chat panel.
*   **No JavaScript Errors:** Open your browser's developer console (usually F12, then check the "Console" tab). There should be no errors related to the `fetch` API call or subsequent JavaScript processing.
*   **Successful API Response:** The Flask app console shows a `POST /api/process_statement HTTP/1.1" 200 -` log, indicating a successful HTTP 200 OK response.
*   **Input Cleared:** The problem statement textarea is cleared after successful submission.

## 5. Potential Issues & Troubleshooting

*   **Flask App Not Running / Not Reachable:**
    *   **Symptom:** Browser shows "Unable to connect", "Site can't be reached", or the `fetch` call in JavaScript fails with a network error when trying to access `http://127.0.0.1:5000/`.
    *   **Troubleshooting:**
        *   Ensure you have executed `python app.py` in your terminal.
        *   Check that the Flask app is running on `http://127.0.0.1:5000` as expected (look for the "Running on http://127.0.0.1:5000" message).
        *   Verify no other application is using port 5000.
        *   Check your firewall settings if applicable (though less likely for localhost).

*   **`index.html` Not Found (404 Error when accessing `/`):**
    *   **Symptom:** When navigating to `http://127.0.0.1:5000/`, you get a 404 Not Found error.
    *   **Troubleshooting:**
        *   Ensure `index.html` is located in the **same directory** as `app.py` (the project root). The `send_from_directory('.', 'index.html')` command in `app.py` assumes this.

*   **Incorrect API URL in JavaScript (`index.html`):**
    *   **Symptom:** `fetch` call results in a 404 Not Found error for `/api/process_statement` (visible in browser console and Flask logs).
    *   **Troubleshooting:**
        *   The `fetch` URL in `index.html` should be relative: `fetch('/api/process_statement', ...)` since both `index.html` and the API are served from the same origin. Double-check this if you encounter issues.

*   **JSON Errors / Malformed Request:**
    *   **Symptom:** Flask console might show a 400 error for the `/api/process_statement` call. The browser might receive an error response.
    *   **Troubleshooting:**
        *   The `app.py` endpoint expects `{"problem_statement": "your text here"}`. While the current JavaScript in `index.html` should be sending this correctly, if modifications were made, this could be a source of error.
        *   The current `app.py` has basic error handling for missing `problem_statement` or invalid JSON, so check the JSON response in the browser's network tab for error details.

*   **Problem Statement Textarea Not Clearing / UI Not Updating as Expected:**
    *   **Symptom:** UI elements don't behave as described after submission.
    *   **Troubleshooting:** Check the browser's JavaScript console for any errors that might have occurred after the API call but during UI manipulation.

By following these steps, you should be able to test the basic end-to-end flow of submitting a problem statement and receiving a mock AI analysis. Remember to restart the Flask server if you make changes to `app.py`.
