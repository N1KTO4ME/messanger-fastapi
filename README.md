# Messenger на FastAPI с WebSocket и SQLite

##  Описание
Этот проект — система обмена сообщениями на **FastAPI** с **WebSocket** и **SQLite**.  
Поддерживает **общий чат** и **личные сообщения между пользователями**.

##  Функциональность
Подключение к **общему чату** при входе  
1. **Выбор собеседника** и личные сообщения  
2. **Сохранение истории** чатов в базе данных  
3. **Темная тема** с переключением  
4. **Выход из профиля**  
5. **REST API** для управления пользователями  

## Технологии
> **FastAPI** — серверный фреймворк
> 
> **WebSocket** — двухсторонее соеденение
> 
> **SQLite** — база данных
> 
> **Jinja2** — шаблоны HTML
> 
> **JavaScript** — фронтенд логика
> 


## Установка и запуск
1. **Клонируем репозиторий**
   ```bash
    git clone https://github.com/N1KTO4ME/messanger-fastapi.git
   ```
2. **Устанавливаем зависимости**
   ```bash
    pip install -r requirements.txt
   ```
3. **Запускаем проект**
   ```bash
    uvicorn app.main:app --reload
   ```
## Демострация работы веб-приложения
![{04B4E160-AAF2-4C92-A42E-C4C645D1E3F6}](https://github.com/user-attachments/assets/501ea2bc-7c9f-4c5f-aa11-784ccff0a54b)
