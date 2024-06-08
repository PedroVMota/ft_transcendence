# Build stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install -gs vite
RUN npm install
COPY . .
RUN npm run build
