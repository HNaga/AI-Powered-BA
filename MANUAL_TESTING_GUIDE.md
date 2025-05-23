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

To ensure seamless API calls from the frontend JavaScript to the Flask backend (and avoid Cross-Origin Resource Sharing - CORS - issues), it's **highly recommended to serve `index.html` from the Flask application itself.**

*   **Recommended Method: Serve `index.html` via Flask**

    1.  **Modify `app.py`:**
        Add a new route to your `app.py` to serve `index.html`.
        ```python
        from flask import Flask, request, jsonify, send_from_directory # Add send_from_directory

        app = Flask(__name__)

        # ... (your existing /api/process_statement route) ...

        @app.route('/api/process_statement', methods=['POST'])
        def process_statement():
            # ... (existing code for this endpoint) ...
            try:
                data = request.get_json()
            except Exception as e:
                return jsonify({"error": "Invalid JSON format", "details": str(e)}), 400

            if not data or 'problem_statement' not in data:
                return jsonify({"error": "Missing 'problem_statement' in request JSON"}), 400

            problem_statement = data['problem_statement']

            if not isinstance(problem_statement, str):
                return jsonify({"error": "'problem_statement' must be a string"}), 400
                
            first_word = ""
            if problem_statement and problem_statement.strip(): 
                first_word = problem_statement.split(' ')[0]
            else: 
                problem_statement = "[No statement provided]" 
                first_word = "empty_statement"

            summary = f"Summary of '{problem_statement[:30]}...': This statement needs careful analysis and further refinement."
            keywords = ["analysis", "requirements", "stakeholder_input", f"{first_word.lower()}"]
            response_data = {
                "original_statement": problem_statement if problem_statement != "[No statement provided]" else data.get('problem_statement', ''),
                "summary": summary,
                "keywords": keywords,
                "processing_status": "success_mock"
            }
            return jsonify(response_data), 200

        @app.route('/') # This will be our route for index.html
        def home():
            # The 'filename' argument to send_from_directory should be 'index.html'.
            # The first argument is the directory where the file is located.
            # Assuming index.html is in the same directory as app.py (project root).
            return send_from_directory('.', 'index.html')


        if __name__ == '__main__':
            app.run(debug=True, port=5000)
        ```
        **Note:** Ensure `index.html` is in the same directory as `app.py` (the root of your project) for `send_from_directory('.', 'index.html')` to work directly. If it's in a subdirectory (e.g., `static`), you'd adjust the path like `send_from_directory('static', 'index.html')`. For this MVP, the root is fine.

    2.  **Access in Browser:**
        After modifying `app.py` and ensuring the Flask server is running (restart it if it was already running), open your web browser and navigate to:
        ```
        http://127.0.0.1:5000/
        ```
        This should load `index.html`.

*   **Alternative Method: Open `index.html` Directly (Not Recommended for API Testing)**
    You can open `index.html` directly in your browser by navigating to its file path (e.g., `file:///path/to/your/project/index.html`).
    *   **Caveat - CORS Errors:** If you use this method, the JavaScript `fetch` call from `index.html` (served from `file://`) to `http://127.0.0.1:5000/api/process_statement` will **very likely be blocked by the browser's Same-Origin Policy (CORS)**. You will see errors in the browser's developer console. This method is not suitable for testing the full end-to-end API interaction.

## 3. Testing Steps

Ensure the Flask backend (`app.py`) is running and you have loaded `index.html` in your browser (preferably via the Flask-served route `http://127.0.0.1:5000/`).

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

*   **CORS Errors (Most Common if not serving `index.html` via Flask):**
    *   **Symptom:** No data appears on the frontend, and you see errors in the browser console mentioning "CORS", "Cross-Origin Request Blocked", or "Same-Origin Policy".
    *   **Cause:** The browser is blocking the JavaScript `fetch` call from `index.html` (served from `file://` or a different origin) to the Flask API at `http://127.0.0.1:5000`.
    *   **Solution:**
        1.  **Highly Recommended:** Use the method described in **Section 2 (Recommended Method)** to serve `index.html` from Flask. This aligns the origin of the frontend and backend.
        2.  (Less Ideal for this MVP) For development, you could configure Flask to allow CORS (e.g., using the `flask-cors` extension). However, serving from the same origin is simpler for this testing phase.

*   **Flask App Not Running / Not Reachable:**
    *   **Symptom:** Browser shows "Unable to connect", "Site can't be reached", or the `fetch` call in JavaScript fails with a network error.
    *   **Troubleshooting:**
        *   Ensure you have executed `python app.py` in your terminal.
        *   Check that the Flask app is running on `http://127.0.0.1:5000` as expected.
        *   Verify no other application is using port 5000.
        *   Check your firewall settings if applicable (though less likely for localhost).

*   **Incorrect API URL in JavaScript (`index.html`):**
    *   **Symptom:** `fetch` call results in a 404 Not Found error (visible in browser console and Flask logs).
    *   **Troubleshooting:**
        *   If serving `index.html` via Flask from the root route (`@app.route('/')`), the `fetch` URL in `index.html` should be relative: `fetch('/api/process_statement', ...)`
        *   If you were attempting a cross-origin request (not recommended), it would need to be absolute `http://localhost:5000/api/process_statement`.

*   **JSON Errors / Malformed Request:**
    *   **Symptom:** Flask console might show a 400 error. The browser might receive an error response.
    *   **Troubleshooting:**
        *   The `app.py` endpoint expects `{"problem_statement": "your text here"}`. Verify the JavaScript `fetch` call is correctly stringifying the JSON body.
        *   The current `app.py` has basic error handling for missing `problem_statement` or invalid JSON, so check the JSON response in the browser's network tab for error details.

*   **Problem Statement Textarea Not Clearing / UI Not Updating:**
    *   **Symptom:** UI elements don't behave as expected after submission.
    *   **Troubleshooting:** Check the browser's JavaScript console for any errors that might have occurred after the API call but during UI manipulation.

By following these steps, you should be able to test the basic end-to-end flow of submitting a problem statement and receiving a mock AI analysis. Remember to restart the Flask server if you make changes to `app.py`.
I have created the `MANUAL_TESTING_GUIDE.md` file.

It includes:
1.  **How to Run the Backend:** Command `python app.py` and expected server running message.
2.  **How to Run/Access the Frontend:**
    *   **Recommended Method:** Instructions to modify `app.py` by adding `send_from_directory` to serve `index.html` from the root route (`/`). Explains how to access it at `http://127.0.0.1:5000/`.
    *   **Alternative Method:** Briefly describes opening `index.html` directly via `file:///` and explicitly warns about the high probability of CORS errors, marking it as not ideal.
3.  **Testing Steps:** Detailed steps from locating the input area, entering text, clicking submit, and what to observe on both the frontend (center panel and chat) and backend (Flask console log).
4.  **Expected Outcomes & Verification:** Clear points on what constitutes a successful test, including data display, no JS errors, and a 200 OK from the API.
5.  **Potential Issues & Troubleshooting:** Covers CORS errors (with a strong recommendation to serve via Flask), Flask app not running, incorrect API URL, JSON errors, and UI update issues, along with basic troubleshooting advice for each.

The guide emphasizes serving `index.html` via Flask as the primary method for straightforward testing. The Python code snippet for modifying `app.py` to serve `index.html` is included directly in the guide.Okay, I have created the `MANUAL_TESTING_GUIDE.md` file with all the specified sections and content.
The guide emphasizes modifying `app.py` to serve `index.html` as the recommended method for testing to avoid CORS issues, and provides the necessary code snippet for this modification. It also details the steps for running the backend and frontend, the specific actions to perform during testing, expected outcomes for verification, and a list of potential issues with troubleshooting tips.
