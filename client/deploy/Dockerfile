FROM node:lts as build

WORKDIR /app

RUN npm install -g npm@latest

# RUN yarn set version stable

# COPY app/yarn.lock .

FROM build as dev

COPY app/package*.json .

RUN npm install

CMD npx vite

FROM build as prod

COPY app/ /app

RUN npm install



# WORKDIR /app/dist

CMD npm run build





# WORKDIR /react-vite-app

# EXPOSE 3000

# COPY package.json package-lock.json ./

# RUN npm install --silent

# COPY . ./

# CMD ["npm", "run", "dev"]




