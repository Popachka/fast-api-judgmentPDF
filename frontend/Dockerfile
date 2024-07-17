# Стадия: Сборка приложения
FROM node:18-alpine as build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package.json ./
COPY package-lock.json ./

# Устанавливаем зависимости
RUN npm install --silent

# Копируем остальные файлы
COPY . ./

# Собираем приложение
RUN npm run build

# Опционально: Указываем директорию, в которую будут сохраняться сгенерированные файлы
# Вы можете использовать эту директорию для копирования файлов на ваш сервер
RUN mkdir -p /app/dist && cp -R /app/build/* /app/dist
