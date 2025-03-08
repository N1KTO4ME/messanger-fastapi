let socket;
let user_id = prompt("Введите ваш ID:");

function connect() {
    socket = new WebSocket(`ws://127.0.0.1:8000/ws/${user_id}`);

    socket.onmessage = function(event) {
        let chatBox = document.getElementById("chatBox");
        let messageData = event.data.split(": ");
        let sender_id = messageData[0];
        let messageText = messageData.slice(1).join(": ");

        let messageElement = document.createElement("div");
        messageElement.classList.add("message");

        if (sender_id == user_id) {
            messageElement.classList.add("user");
        } else {
            messageElement.classList.add("other");
            let avatar = document.createElement("div");
            avatar.classList.add("avatar");
            avatar.textContent = sender_id[0].toUpperCase(); // Первая буква ID
            messageElement.appendChild(avatar);
        }

        let textNode = document.createElement("span");
        textNode.textContent = messageText;
        messageElement.appendChild(textNode);
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
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

// Переключение темы
const themeToggle = document.getElementById("themeToggle");
themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");

    // Сохраняем состояние темы в localStorage
    const isDark = document.body.classList.contains("dark-theme");
    localStorage.setItem("darkTheme", isDark);

    // Меняем текст кнопки
    themeToggle.textContent = isDark ? "☀️ Светлая тема" : "🌙 Темная тема";
});

// Устанавливаем тему при загрузке
window.onload = function () {
    connect();
    if (localStorage.getItem("darkTheme") === "true") {
        document.body.classList.add("dark-theme");
        themeToggle.textContent = "☀️ Светлая тема";
    }
};
