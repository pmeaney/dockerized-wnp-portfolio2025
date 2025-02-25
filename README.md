# WNP portfolio project

>Dockerized Wagtail CMS, NextJS, PostgreSQL (For Wagtail use) for a portfolio website

Stack: Wagtail CMS, NextJS FE, Postgres DB

Try it out:

```bash
git clone git@github.com:pmeaney/dockerized-wnp-portfolio2025.git && \
cd dockerized-wnp-portfolio2025 && \
docker compose -f docker-compose.dev.yml up
```


# Secrets setup

- Add the following Secrets to the Repo:
  - "RESPOSITORY SECRETS"
    - GH_PAT
      - A GH Personal Access Token with persmissions for:
        - repo (all)
        - workflow
        - wite:packages (includes read:packages)
    - LINUX_SERVER_IP
    - LINUX_SSH_PRIVATE_KEY
      - (The private key associated with the public key on your remote server. In my case, added to server via terraform)
    - LINUX_USER_DEVOPS
      - (I typically create two users on the remote server-- One for human use, one for CICD use. Both created via terraform. The purpose of these secrets is for CICD to ssh in, therefore of course, I use the username of the CICD user)
  - "ENVIRONMENT SECRETS" -- I give it the name "production" then add these secrets to the newly created "production environment" section of Github Actions Environment Secrets.  (or, you can just add these as Repo Secrets)
    - POSTGRES__SECRET_ENV_FILE
    - WAGTAIL__SECRET_ENV_FILE
    - NEXTJS__SECRET_ENV_FILE