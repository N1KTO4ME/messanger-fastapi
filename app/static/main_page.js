// 🔹 Переключение темы
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
