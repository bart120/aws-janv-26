FROM node:20-alpine AS build
WORKDIR /app
COPY . .
RUN npm install -g @angular/cli && npm install && npm run build -- --configuration production

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
