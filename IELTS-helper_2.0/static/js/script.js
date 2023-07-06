// Speech recognition variables
let recognition;
let isListening = false;

// Start speech to text recognition
function startSpeechToText() {
    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = function () {
            isListening = true;
            document.getElementById('1speechToTextButton').innerHTML = 'Stop';
            document.getElementById('2speechToTextButton').innerHTML = 'Stop';
            startSoundWaveAnimation();
        };

        recognition.onresult = function (event) {
            const result = event.results[event.results.length - 1][0].transcript;
            document.getElementById('input_paragraph').value += result;
            document.getElementById('2input_paragraph').value += result;
        };

        recognition.onend = function () {
            isListening = false;
            document.getElementById('1speechToTextButton').innerHTML = 'Speech to Text';
	    document.getElementById('2speechToTextButton').innerHTML = 'Speech to Text';
            stopSoundWaveAnimation();
        };
    }

    if (isListening) {
        recognition.stop();
        isListening = false;
        document.getElementById('1speechToTextButton').innerHTML = 'Speech to Text';
        document.getElementById('2speechToTextButton').innerHTML = 'Speech to Text';
        stopSoundWaveAnimation();
    } else {
        recognition.start();
    }
}
function startSoundWaveAnimation() {
    // Add a class to the button to trigger the animation
    document.getElementById('1speechToTextButton').classList.add('recording');
    document.getElementById('2speechToTextButton').classList.add('recording');
}

// Function to stop sound wave animation
function stopSoundWaveAnimation() {
    // Remove the class from the button to stop the animation
    document.getElementById('1speechToTextButton').classList.remove('recording');
    document.getElementById('2speechToTextButton').classList.remove('recording');
}

// Function to show the selected form and update the active button
function showForm(formName) {
  // Hide all forms
  var forms = document.querySelectorAll('form');
  forms.forEach(function(form) {
    form.classList.remove('active');
  });

  // Show the selected form
  var selectedForm = document.getElementById(formName + 'Form');
  selectedForm.classList.add('active');

  // Update the active button
  var buttons = document.querySelectorAll('.option-board button');
  buttons.forEach(function(button) {
    if (button.id === formName + 'Button') {
      button.classList.add('active');
    } else {
      button.classList.remove('active');
    }
  });

  // Store the active form in localStorage
  localStorage.setItem('activeForm', formName);
}

// Check if there is a stored active form and show it
document.addEventListener('DOMContentLoaded', function() {
  var storedForm = localStorage.getItem('activeForm');
  if (storedForm) {
    showForm(storedForm);
  }
});

function fetchRandomTask() {
    fetch("/random_task")
        .then(response => response.text())
        .then(data => {
            document.getElementById("taskData").innerHTML = data;
            
            // Store the random task data in sessionStorage
            sessionStorage.setItem("randomTaskData", data);
        });
}

function approveReplace(button) {
    // Get the parent element of the highlighted text
    var highlightElement = button.parentNode.parentNode;

    // Get the text content inside the popup element
    var popupText = highlightElement.querySelector('.popup.replace').textContent;

    // Remove the desired text using regular expressions
    var modifiedText = popupText.replace(/ApproveIgnore/g, '');

    // Create a new text node with the modified text content
    var newText = document.createTextNode(modifiedText);

    // Replace the highlightElement with the newText
    highlightElement.parentNode.replaceChild(newText, highlightElement);
}

function ignoreReplace(button) {
    // Get the parent element of the highlighted text
    var highlightElement = button.parentNode.parentNode;

    // Get the text content inside the highlight element only
    var highlightedText = highlightElement.childNodes[0].textContent;

    // Remove the desired text using regular expressions
    var modifiedText = highlightedText.replace(/ApproveIgnore/g, '');

    // Create a new text node with the modified text content
    var newText = document.createTextNode(modifiedText);

    // Replace the highlightElement with the newText
    highlightElement.parentNode.replaceChild(newText, highlightElement);
}

function approveInsert(button) {
    // Get the parent element of the highlighted text
    var highlightElement = button.parentNode.parentNode;

    // Get the text content inside the highlight element only
    var highlightedText = highlightElement.childNodes[0].textContent;

    // Remove the desired text using regular expressions
    var modifiedText = highlightedText.replace(/ApproveIgnore/g, '');

    // Create a new text node with the modified text content
    var newText = document.createTextNode(modifiedText);

    // Replace the highlightElement with the newText
    highlightElement.parentNode.replaceChild(newText, highlightElement);
}

function ignoreInsert(button) {
    // Get the parent element of the highlighted text
    var highlightElement = button.parentNode.parentNode;

    // Remove the highlightElement from its parent
    highlightElement.parentNode.removeChild(highlightElement);
}

function approveDelete(button) {
    // Get the parent element of the highlighted text
    var highlightElement = button.parentNode.parentNode;

    // Remove the highlightElement from its parent
    highlightElement.parentNode.removeChild(highlightElement);
}

function ignoreDelete(button) {
    // Get the parent element of the highlighted text
    var highlightElement = button.parentNode.parentNode;

    // Get the text content inside the highlight element only
    var highlightedText = highlightElement.childNodes[0].textContent;

    // Remove the desired text using regular expressions
    var modifiedText = highlightedText.replace(/ApproveIgnore/g, '');

    // Create a new text node with the modified text content
    var newText = document.createTextNode(modifiedText);

    // Replace the highlightElement with the newText
    highlightElement.parentNode.replaceChild(newText, highlightElement);
}