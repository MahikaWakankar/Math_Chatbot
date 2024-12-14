// Function to redirect the user to second.html with the selected operation
function goToSecondPage(operation) {
    localStorage.setItem('operation', operation); // Store the operation
    switch (operation) {
        case 'trigonometry':
            window.location.href = '/trigonometry';
            break;
        case 'differentiate':
            window.location.href = '/differentiation';
            break;
        case 'integrate':
            window.location.href = '/integration';
            break;
        case 'simplify':
            window.location.href = '/simplify';
            break;
        default:
            console.error('Unknown operation:', operation);
    }
}

// Function to send the message from second.html
function sendMessage() {
    var userMessage = document.getElementById("userInput").value;

    if (userMessage.trim() !== "") {
        // Append the user message to the chat box
        appendMessage(userMessage, 'user');
        
        // Clear the input field
        document.getElementById("userInput").value = "";

        // Get the selected operation from localStorage
        const operation = localStorage.getItem('operation');

        // Send the message and selected operation to the Flask backend
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage, operation: operation })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage(data.response, 'bot');
        })
        .catch(error => console.error('Error:', error));
    }
}

// Function to append messages to the chat box
function appendMessage(message, sender) {
    var chatContainer = document.getElementById("chat-box");
    var messageDiv = document.createElement("div");
    messageDiv.classList.add(sender);
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Auto-scroll to the bottom
}

// On page load for second.html, get the operation from localStorage
window.onload = function() {
    var operation = localStorage.getItem('operation');
    if (operation) {
        console.log('Selected operation: ' + operation);
    } else {
        console.log('No operation selected.');
    }
};
