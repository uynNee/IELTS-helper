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
            document.getElementById('speechToTextButton').innerHTML = 'Stop';
            startSoundWaveAnimation();
        };

        recognition.onresult = function (event) {
            const result = event.results[event.results.length - 1][0].transcript;
            document.getElementById('input_paragraph').value += result;
        };

        recognition.onend = function () {
            isListening = false;
            document.getElementById('speechToTextButton').innerHTML = 'Speech to Text';
            stopSoundWaveAnimation();
        };
    }

    if (isListening) {
        recognition.stop();
        isListening = false;
        document.getElementById('speechToTextButton').innerHTML = 'Speech to Text';
        stopSoundWaveAnimation();
    } else {
        recognition.start();
    }
}
function startSoundWaveAnimation() {
    // Add a class to the button to trigger the animation
    document.getElementById('speechToTextButton').classList.add('recording');
}

// Function to stop sound wave animation
function stopSoundWaveAnimation() {
    // Remove the class from the button to stop the animation
    document.getElementById('speechToTextButton').classList.remove('recording');
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