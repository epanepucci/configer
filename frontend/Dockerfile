# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application in development mode
RUN npm run dev -- --host --mode development

# Or alternatively, directly modify the build command
# RUN NODE_ENV=development npm run build

# Production stage
FROM nginx:alpine

# Copy the built app to nginx server
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
