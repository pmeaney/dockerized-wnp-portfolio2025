## Old notes

### These notes are from before I re-organized my approach to docker project directory structures

Based on src: https://medium.com/@elifront/best-next-js-docker-compose-hot-reload-production-ready-docker-setup-28a9125ba1dc

To run locally for development, you need:

- the postgres instance running (via docker or locally)
- run `npm run dev`. sure, you could run the docker-compose.dev.yml to boot it into a docker container, but you don't really need to-- because it'll be done on deployment. But, if you want to, it's there as an option: `make build-watch`

- Build & run in background, so you can view logs:
  - `make build-watch`
- Run dev nextjs container and run in background
  - `make build`
- Stop container
  - `make rm`
- Run prod nextjs container

### Information on the production build.

Note: The production build only takes place in the Github Actions CICD workflow. So, you can mostly disregard it. However, for reference, setting things up, debugging, etc, here are some notes on the prod deployment worjflow:

- If you want to build & run the Prod image locally, (which you shouldn't need to do-- itll be done in cicd) you can run this:
  - `docker compose -f docker-compose.prod.yml up -d --build`
  - Need to actually do this it seems-- specify the platform, on build step:
  - `DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose -f ./docker-compose.prod.yml build`
  - This is tags the local image with the name of the container registry image location (might be optional?)
  - `docker tag pmeaney-portfolio-pmeaney-portfolio-prod:latest ghcr.io/pmeaney/pmeaney-portfolio-prod:latest`
  - To publish: `docker push ghcr.io/pmeaney/pmeaney-portfolio-prod:latest`
  - To run (i.e. on server-- away from docker-compose.prod.yml which we package somewhere else, such as laptop or cicd): `docker run -d -p 3000:3000 --name pmeaney-portfolio-prod --network ccc-nginx-certbot_default ghcr.io/pmeaney/pmeaney-portfolio-prod:latest`

### Project Description

PMeaney.com portfolio

- Frontend: NextJS
- Backend: Payload CMS

### Project creation process

- Basic example created via `npx create-next-app@latest nextjs-pmeaney-portfolio-2025`

### Styling

- Main style framework: BulmaCSS
- BulmaCSS projects used or referenced:
  - Project: https://bulmatemplates.github.io/bulma-templates/templates/personal.html
    - css source: https://bulmatemplates.github.io/bulma-templates/css/personal.css
