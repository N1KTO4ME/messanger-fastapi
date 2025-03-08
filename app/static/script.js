let socket;
let username = "";

function connect() {
    username = document.getElementById("username").value;
    if (!username) {
        alert("Введите имя пользователя!");
        return;
    }

    socket = new WebSocket(`ws://127.0.0.1:8000/ws/${username}`);

    socket.onmessage = function(event) {
        let chat = document.getElementById("chat");
        let message = document.createElement("p");
        message.textContent = event.data;
        chat.appendChild(message);
        chat.scrollTop = chat.scrollHeight;
    };
}

function sendMessage() {
    let messageInput = document.getElementById("messageInput");
    let message = messageInput.value;
    if (socket && message) {
        socket.send(message);
        messageInput.value = "";
    }
}
