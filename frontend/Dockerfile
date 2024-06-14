# Build stage
FROM node:22-alpine3.19
WORKDIR /app
COPY package*.json ./
RUN rm -rf node_modules package-lock.json
RUN npm install -gs vite
RUN npm install
COPY . .
RUN npm run build