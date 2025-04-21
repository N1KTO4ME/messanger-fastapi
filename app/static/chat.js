let socket;
let username = localStorage.getItem("username") || prompt("Введите ваше имя:");

if (!username) {
    alert("Имя обязательно!");
    window.location.reload();
} else {
    localStorage.setItem("username", username);
}

document.getElementById("currentUser").textContent = `(${username})`;

function loadUsers() {
    fetch("/users/list")
        .then(response => response.json())
        .then(users => {
            let userList = document.getElementById("userList");
            userList.innerHTML = '<option value="global">🌍 Общий чат</option>';
            users.forEach(user => {
                if (user.username !== username) {
                    let option = document.createElement("option");
                    option.value = user.username;
                    option.textContent = user.username;
                    userList.appendChild(option);
                }
            });
            connect();  // Подключаемся к чату сразу
        })
        .catch(error => console.error("Ошибка загрузки пользователей:", error));
}

function connect() {
    let receiver = document.getElementById("userList").value;
    if (!receiver) return;

    if (socket) socket.close();
    socket = new WebSocket(`ws://127.0.0.1:8000/ws/${encodeURIComponent(username)}/${encodeURIComponent(receiver)}`);

    socket.onmessage = function (event) {
        let chatBox = document.getElementById("chatBox");
        let message = document.createElement("p");
        message.textContent = event.data;
        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Сохраняем историю сообщений
        let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || {};
        if (!chatHistory[receiver]) chatHistory[receiver] = [];
        chatHistory[receiver].push(event.data);
        localStorage.setItem("chatHistory", JSON.stringify(chatHistory));
    };

    socket.onclose = function (event) {
        console.warn(`Соединение закрыто (${event.code}): ${event.reason || "нет причины"}`);
    };

    socket.onerror = function (error) {
        console.error("Ошибка WebSocket:", error);
    };

    // Загружаем историю
    let chatHistory = JSON.parse(localStorage.getItem("chatHistory")) || {};
    let chatBox = document.getElementById("chatBox");
    chatBox.innerHTML = "";
    if (chatHistory[receiver]) {
        chatHistory[receiver].forEach(msg => {
            let message = document.createElement("p");
            message.textContent = msg;
            chatBox.appendChild(message);
        });
    }
}

function sendMessage() {
    let messageInput = document.getElementById("messageInput");
    let message = messageInput.value;
    if (socket && message) {
        socket.send(message);
        messageInput.value = "";
    }
}

document.getElementById("logoutButton").addEventListener("click", () => {
    localStorage.removeItem("username");
    localStorage.removeItem("chatHistory");
    window.location.reload();
});

const themeToggle = document.getElementById("themeToggle");
if (localStorage.getItem("darkTheme") === "true") {
    document.body.classList.add("dark-theme");
    themeToggle.textContent = "☀️ Светлая тема";
}
themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
    localStorage.setItem("darkTheme", document.body.classList.contains("dark-theme"));
    themeToggle.textContent = document.body.classList.contains("dark-theme") ? "☀️ Светлая тема" : "🌙 Темная тема";
});

document.getElementById("userList").addEventListener("change", connect);

window.onload = loadUsers;
