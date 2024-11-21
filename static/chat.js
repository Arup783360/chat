const socket = io();

// Function to send a message
function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value;

    if (message.trim() !== '') {
        socket.emit('send_message', { sender: username, message: message });
        messageInput.value = '';
    }
}

// Receive message and display in chat box
socket.on('receive_message', function(data) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.textContent = `${data.sender}: ${data.message}`;
    messageElement.classList.add(data.sender === username ? 'right' : 'left');
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});

// Clear chat
function clearChat() {
    socket.emit('clear_chat');
}

// Handle chat clearing for all clients
socket.on('clear_chat', function() {
    document.getElementById('chat-box').innerHTML = '';
});
