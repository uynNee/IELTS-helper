from flask import Flask, render_template, request, redirect, session
import openai
import difflib
import random
import json
import os
import re

# Set up OpenAI API key
openai.api_key = "your-api-key"

# Set up API endpoint and model
model_engine = "text-davinci-003"
model="gpt-3.5-turbo"

# Set up request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}

app = Flask(__name__)

# Set the secret key for the Flask application
app.secret_key = "your_secret_key_here"

def get_reasoning(error_type, text, input_word, corrected_word):
    if error_type == 1:
        prompt = f"Logical explanation in 15 words of the writing error(s) why '{input_word}' is corrected to '{corrected_word}' in this paragraph: '{text}'"
    elif error_type == 2:
        prompt = f"Logical explanation in 15 words of the writing error(s) why '{input_word}' is removed in this paragraph: '{text}'"
    else:
        prompt = f"Logical explanation in 15 words of why '{input_word}' is required to avoid writing error(s) in this paragraph: '{text}'"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.3,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    reasoning = completion.choices[0].text.strip()
    return reasoning

def ielts_score(topic, text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "Score this IELTS Writing Task 2 response. Use the score scale from 1 to 9 and provide feedback."},
        {"role": "user", "content": "Topic:" + topic},
        {"role": "user", "content": "Response:" + text}
        ],
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    #score = completion.choices[0].text.strip()
    evaluation = response.choices[0].message.content.strip()
    return evaluation

# Get the current directory path
current_directory = os.path.dirname(os.path.abspath(__file__))

def fetch_random_task_data():
    # Specify the directory path for the JSON files
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_directory = os.path.join(current_directory, 'data')

    # List the available JSON files
    json_files = [
        os.path.join(json_directory, 'data.json')
    ]

    # Reset the random seed
    random.seed()

    # Select a random JSON file
    random_file = random.choice(json_files)

    # Read the contents of the JSON file
    with open(random_file) as file:
        task_data = json.load(file)

    # Select a random task from the JSON data
    random_task = random.choice(list(task_data.values()))

    return random_task

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/random_task")
def fetch_random_task():
    # Fetch a random task
    random_task_data = fetch_random_task_data()
    
    # Store the random task data in the session
    session["randomTaskData"] = random_task_data

    # Pass the random task data to the HTML template
    return random_task_data

@app.route("/compare", methods=["POST"])
def compare():
    # Get the user's input paragraph
    input_paragraph = request.form["input_paragraph"]

    # Check if input_paragraph is not empty
    if input_paragraph and input_paragraph.strip():
        # Generate a corrected version of the input paragraph using OpenAI's GPT API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "Please only correct any spelling errors:\n"},
            {"role": "user", "content": input_paragraph}
            ],
            temperature=0.9,
            max_tokens= len(input_paragraph) + 50,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6
        )
        corrected_paragraph = response.choices[0].message.content.strip()

        # Check if the IELTS score checkbox is checked
        calculate_ielts = 'ielts_checkbox' in request.form

        # Get the random task data from the form data
        random_task_data = session.get("randomTaskData")

        if calculate_ielts:
            ielts_score_result = ielts_score(random_task_data, input_paragraph)
        else:
            ielts_score_result = None

        # Split the input and corrected paragraphs into a list of words, including spaces
        input_words = re.findall(r"\S+|\s", input_paragraph)
        corrected_words = re.findall(r"\S+|\s", corrected_paragraph)
        
        # Remove '\n' from corrected_words and input_words
        corrected_words = [word for word in corrected_words if word not in ['\n']]
        input_words = [word for word in input_words if word not in ['\n']]

        # Replace '\r' with " " in corrected_words and input_words
        corrected_words = [word.replace('\r', " ") if word.isspace() else word for word in corrected_words]
        input_words = [word.replace('\r', " ") if word.isspace() else word for word in input_words]

        # Get the differences between the corrected paragraph and the input paragraph
        diffs = difflib.SequenceMatcher(None, input_words, corrected_words).get_opcodes()

        # Generate reasonings for each error
        reasonings = []
        for diff in diffs:
            if diff[0] == 'replace':
                error_word = ''.join(input_words[diff[1]:diff[2]])
                corrected_word = ''.join(corrected_words[diff[3]:diff[4]])
                reasoning = get_reasoning(1, input_paragraph, error_word, corrected_word)
                reasonings.append(reasoning)
            elif diff[0] == 'delete':
                error_word = ''.join(input_words[diff[1]:diff[2]])
                corrected_word = ''
                reasoning = get_reasoning(2, input_paragraph, error_word, corrected_word)
                reasonings.append(reasoning)
            elif diff[0] == 'insert':
                error_word = ''.join(corrected_words[diff[3]:diff[4]])
                corrected_word = ''
                reasoning = get_reasoning(3, input_paragraph, error_word, corrected_word)
                reasonings.append(reasoning)

        # Render the index.html template with the input and corrected paragraphs, and the highlighted differences
        return render_template("index.html", input_paragraph=input_paragraph, corrected_paragraph=corrected_paragraph, diffs=diffs, input_words=input_words, corrected_words=corrected_words, reasonings=reasonings, ielts_score=ielts_score_result)
    else:
        # Redirect the user to the home route
        return redirect("/")
    
@app.route("/paraphrase", methods=["POST"])
def paraphrase():
    # Get the user's input paragraph
    input_paragraph = request.form["input_paragraph"]
    paraphrase_type = request.form["paraphrase_type"]

    # Check if input_paragraph is not empty
    if input_paragraph and input_paragraph.strip():
        if paraphrase_type == "standard":
            # Generate a corrected version of the input paragraph using OpenAI's GPT API
            prompt = "Improve this paragraph by rewording or restating poorly written phrases using different words and while maintaining each sentence structure and meaning:\n"
        elif paraphrase_type == "creative":
            # Generate a creative paraphrase of the input paragraph using OpenAI's GPT API
            prompt = "Improve this paragraph creatively by rewording or restating using different words and while maintaining the same overall meaning:\n"
        elif paraphrase_type == "IELTS":
            # Generate a creative paraphrase of the input paragraph using OpenAI's GPT API
            prompt = "Improve this paragraph longer in IELTS Writing style by rewording or restating using different words and while maintaining the same overall meaning:\n"
        elif paraphrase_type == "Formal":
            # Generate a creative paraphrase of the input paragraph using OpenAI's GPT API
            prompt = "Improve this paragraph longer in Formal-style by rewording or restating using different words and while maintaining the same overall meaning:\n"
        elif paraphrase_type == "Scientific":
            # Generate a creative paraphrase of the input paragraph using OpenAI's GPT API
            prompt = "Improve this paragraph longer in Scientific-research-style by rewording or restating using different words and while maintaining the same overall meaning:\n"
        else:
            # Handle invalid paraphrase type
            return redirect("/")
        paragraph1 = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_paragraph}
            ],
            temperature=0.9,
            max_tokens= len(input_paragraph) + 100,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6
        )
        corrected_paragraph = paragraph1.choices[0].message.content.strip()

        # Split the input and corrected paragraphs into a list of words, including spaces
        input_words = re.findall(r"\w+|[.,!?;]|\s", input_paragraph)
        corrected_words = re.findall(r"\w+|[.,!?;]|\s", corrected_paragraph)

        # Remove '\n' from corrected_words and input_words
        corrected_words = [word for word in corrected_words if word not in ['\n']]
        input_words = [word for word in input_words if word not in ['\n']]

        # Replace '\r' with " " in corrected_words and input_words
        corrected_words = [word.replace('\r', " ") if word.isspace() else word for word in corrected_words]
        input_words = [word.replace('\r', " ") if word.isspace() else word for word in input_words]

        # Get the differences between the corrected paragraph and the input paragraph
        diffs = difflib.SequenceMatcher(None, input_words, corrected_words).get_opcodes()

        # Render the index.html template with the input and corrected paragraphs, and the highlighted differences
        return render_template("index.html", input_paragraph=input_paragraph, corrected_paragraph=corrected_paragraph, diffs=diffs, input_words=input_words, corrected_words=corrected_words)
    else:
        # Redirect the user to the home route
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)