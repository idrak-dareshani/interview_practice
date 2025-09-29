# AI Interview Practice

A Streamlit web app that generates multiple-choice interview questions tailored to your role, skills, and experience using Anthropic's Claude API. Get instant feedback and suggestions for improvement after completing your quiz.

## Features

- Generate custom MCQs for any tech role and skillset
- Interactive quiz interface with answer checking
- AI-powered feedback on your performance, strengths, and weaknesses

## Requirements

- Python 3.8+
- [Anthropic API key](https://docs.anthropic.com/claude/docs/access-claude-api)
- See [requirements.txt](requirements.txt) for dependencies

## Setup

1. **Clone the repository**

    ```sh
    git clone <your-repo-url>
    cd interview_practice
    ```

2. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up your Anthropic API key**

    - Copy your API key into a `.env` file in the project root:

        ```
        ANTHROPIC_API_KEY="your-anthropic-api-key"
        ```

## Usage

Run the Streamlit app:

```sh
streamlit run app.py
```

Open the provided local URL in your browser to use the app.

## File Structure

- [app.py](app.py): Main Streamlit application
- [requirements.txt](requirements.txt): Python dependencies
- [.env](.env): API key (not tracked in git)
- [.gitignore](.gitignore): Ignores `.env` file

## License

This project is for educational and personal use only.