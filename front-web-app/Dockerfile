FROM node:lts-alpine
LABEL maintainer="dmozh58@gmail.com"

COPY ./stock-chart-demo ./app
# устанавливаем простой HTTP-сервер для статики
RUN npm install -g http-server
# делаем каталог 'app' текущим рабочим каталогом
WORKDIR /app
RUN ls
# устанавливаем зависимости проекта
RUN npm install

# копируем файлы и каталоги проекта в текущий рабочий каталог (т.е. в каталог 'app')
COPY . .

# собираем приложение для production с минификацией
RUN npm run build

CMD [ "http-server", "dist" ]