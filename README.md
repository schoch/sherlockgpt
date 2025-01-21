# SherlockGPT - An AI-Driven Murder Mystery

This game experiment is inspired by "WhoDunit" by Henrik Kniberg:
https://blog.crisp.se/2023/08/26/henrikkniberg/whodunit-ai-game-development-on-steroids

It was (mostly) live-coded on Twitch by Wolfgang Schoch: https://www.twitch.tv/herrschoch

Have fun exploring the code.

## Detective Game Backend

This project is an example of a backend for a detective game using Flask and the OpenAI API.

### Installation

#### Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install the dependencies:

```sh
pip install -r requirements.txt
```

#### Create a .env file in the root directory and add your OpenAI API key

```sh
touch .env && echo "OPENAI_API_KEY=your_openai_api_key" > .env
```

#### Start the application:

```sh
python backend/sherlockgpt/app.py
```

#### Open the game in your browser

http://127.0.0.1:5000

## Notes

- All game data is stored in a SQLite database: `sherlockgpt/instance/scenarios.db`. There is a sample database with game data that corresponds to the provided images and JSON files. It is named `scenarios.db.example`. Simply rename it to `scenarios.db` and place it in `sherlockgpt/instance/` to get started.
- There are some helper methods to rebuild the database, etc. Look for the `/admin` endpoints in `routes.py`.
- Don't forget: this is just a little experiment and not a full game. 😉
