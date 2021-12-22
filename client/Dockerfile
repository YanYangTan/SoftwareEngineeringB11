FROM node:13.12.0-alpine

WORKDIR /usr/src/app2

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8024:8024
CMD [ "npm", "run", "serve"]