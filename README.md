# Telegram-бот
Этот репозиторий содержит Telegram бота, реализованного на Python с использованием библиотеки Telebot.

## Требования
* Python 3.x
* Библиотека Telebot
* NLTK (Natural Language Toolkit) библиотека
* Библиотека dotenv

## Установка
1. Клонируйте этот репозиторий на ваш компьютер.
```bash
git clone <repository-url>
```

2. Установите необходимые зависимости с помощью pip.
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` в корневом каталоге и добавьте в него токен вашего Telegram бота.

```env
BOT_TOKEN=<ваш-токен-бота>
```

4. Запустите скрипт бота.
```bash
python bot.py
```

## Функциональность
Этот бот предоставляет ряд функций для взаимодействия с пользователями Telegram:

Отправка пожеланий на день: Бот может отправлять случайные пожелания пользователям при запросе.
Ответы на вопросы:

 Бот реагирует на сообщения "Привет", "Как дела?" и другие, предоставляя соответствующие ответы.
Показ текущей даты: 

Бот отображает текущую дату по запросу пользователя.

Использование

После запуска бота пользователи могут взаимодействовать с ним через Telegram, отправляя текстовые сообщения. Бот обрабатывает команды `/start`, а также отвечает на обычные текстовые сообщения в соответствии с реализованной логикой.

Дополнительная информация

Дополнительную информацию о разработке и настройке бота вы можете найти в исходном коде и комментариях к нему.

Автор
Этот проект разработан и поддерживается [@bnka1993](https://t.me/viktoria_geo)