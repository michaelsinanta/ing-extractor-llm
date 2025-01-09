# Nutrition Facts Extractor

This project provides a system to extract nutrition facts from images using OpenAI's API and Streamlit for the user interface.

## Setup Instructions

1. Clone the repository:

   ```sh
   git clone https://github.com/michaelsinanta/ing-extractor-llm.git
   ```

2. Navigate to the project directory:

   ```sh
   cd ing-extractor-llm
   ```

3. Create a virtual environment:

   ```sh
   virtualenv .venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```sh
     .\.venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```sh
     source .venv/bin/activate
     ```

5. Install the required packages:
    ```sh
    poetry install
    ```

## Configuration

1. Create a `.env` file in the project root and add the following:
   ```sh 
    # Flask
    LOG_LEVEL=ERROR
    HOST=0.0.0.0
    PORT=4001
    ANOTHER_ENV_VARIABLE=value
    DEBUG=true
    ENVIRONMENT=develop
   
    # OpenAI
    OPENAI_API_KEY=your_openai_api_key_here
    OPENAI_MODEL_NAME=gpt-4

    # Claude
    CLAUDE_API_KEY=your_claude_api_key_here
    CLAUDE_MODEL_NAME=claude-3-5-sonnet-20240620
    LLM_PROVIDER=claude
    ```

## Usage

1. Run the application:
   ```sh
   poetry run streamlit run streamlit.py 
   ```
