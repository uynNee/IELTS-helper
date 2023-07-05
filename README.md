# IELTS-helper
# Flask OpenAI Application README

This README provides instructions on how to run the Flask application `app.py` that utilizes the OpenAI GPT-3.5 language model. The application is designed to correct and provide explanations for writing errors in a given paragraph.

## Installation

To run the Flask application, you need to install the necessary dependencies. Follow these steps:

### 1. Python

Ensure that you have Python installed on your system. The Flask application requires Python 3.6 or later. You can download Python from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 2. Flask

Install Flask, which is a lightweight web framework for Python:

```
pip install flask
```

### 3. OpenAI Python Library

Install the OpenAI Python library to interact with the GPT-3.5 language model:

```
pip install openai
```

## Configuration

Before running the application, you need to configure the OpenAI API key and other settings. Follow these steps:

### 1. Set OpenAI API Key

Replace `"your-api-key"` with your actual OpenAI API key. Find the line in `app.py`:

```python
openai.api_key = "your-api-key"
```

and replace `"your-api-key"` with your API key.

### 2. Configure the Flask application

Set the secret key for the Flask application:
Replace "your_secret_key_here" with your desired secret key in the following line of code:

```python
app.secret_key = "your_secret_key_here"
```

### 3. Set Request Headers

The application uses request headers for authentication. No changes are required for the headers configuration, as they are already set in the code:

```python
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}
```

## Usage

To run the Flask application, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the directory containing `app.py`.

3. Run the following command to start the Flask development server:

   ```bash
   flask run
   ```

4. Once the server is running, you will see output similar to:

   ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

5. Open a web browser and enter `http://127.0.0.1:5000/` in the address bar to access the application.

6. Use the application by entering a paragraph in the provided input field and submitting the form. The application will generate a corrected version of the paragraph and highlight the differences.

7. The application also provides explanations for each writing error. These explanations are generated using the OpenAI API.

## Acknowledgments

This Flask application utilizes the OpenAI GPT-3.5 language model. Special thanks to OpenAI for their contribution to natural language processing and generation.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
