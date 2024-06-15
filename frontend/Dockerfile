# Build stage
FROM node:22-alpine3.19
WORKDIR /app
COPY Code/package*.json ./
COPY ./Config/Run.sh /Run.sh
RUN chmod +x /Run.sh
RUN rm -rf node_modules package-lock.json
RUN npm install -gs vite
RUN npm install --save tree
RUN npm install
COPY . .
# RUN npm run build