# SherlockGPT - An AI-driven murder mystery

This game is inspired by WhoDunit by Henrik Kniberg 
https://blog.crisp.se/2023/08/26/henrikkniberg/whodunit-ai-game-development-on-steroids

It will be coded live on Twitch https://www.twitch.tv/herrschoch

# Detective Game Backend

This project is an example of a backend for a detective game using Flask and the OpenAI API.

## Installation

1. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

4. Start the application:
    ```sh
    python backend/app.py
    ```

## Endpoints

- **POST /new_case**: Generates a new criminal case and returns it as JSON.