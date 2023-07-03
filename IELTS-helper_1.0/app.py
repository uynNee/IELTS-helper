from flask import Flask, request, render_template, redirect
import openai
import difflib
import os
import re

# Set up OpenAI API key
# Replace your-api-key with your GPT API key
openai.api_key = "your-api-key"

# Set up API endpoint and model
model_engine = "text-davinci-003"

# Set up request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
}

app = Flask(__name__)

def get_reasoning(error_type, text, input_word, corrected_word):
    if error_type == 1:
        prompt = f"Logical explanation in 15 words of the writing error(s) why '{input_word}' is corrected to '{corrected_word}' in this paragraph: '{text}'"
    elif error_type == 2:
        prompt = f"Logical explanation in 15 words of the writing error(s) why '{input_word}' is removed in this paragraph: '{text}'"
    else:
        prompt = f"Logical explanation in 15 words of why '{input_word}' is needed in this paragraph: '{text}'"
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    # Get the user's input paragraph
    input_paragraph = request.form["input_paragraph"]

    # Check if input_paragraph is not empty
    if input_paragraph and input_paragraph.strip():
        # Generate a corrected version of the input paragraph using OpenAI's GPT API
        prompt = "Correct this to standard English:\n" + input_paragraph + "\nCorrected paragraph: "
        paragraph1 = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            temperature=0.5,
            max_tokens=len(input_paragraph) + 50,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        corrected_paragraph = paragraph1.choices[0].text.strip()

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
        return render_template("index.html", input_paragraph=input_paragraph, corrected_paragraph=corrected_paragraph, diffs=diffs, input_words=input_words, corrected_words=corrected_words, reasonings=reasonings)
    else:
        # Redirect the user to the home route
        return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)
