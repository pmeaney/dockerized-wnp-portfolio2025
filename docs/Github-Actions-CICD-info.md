
# Secrets setup

- Add the following Secrets to the Repo:
  - "RESPOSITORY SECRETS"
    - GH_PAT (in this project, it's called "GHPAT_021425_CICD_GHCR_REPO_WORKFLOW_WRDPACKAGES", so be sure to update this value with the name you give your GH PAT)
      - which is a Github Personal Access Token with persmissions for:
        - repo (all)
        - workflow
        - wite:packages (includes read:packages)
    - LINUX_SERVER_IP
    - LINUX_SSH_PRIVATE_KEY
      - (The private key associated with the public key on your remote server. In my case, added to server via terraform upon creation.  Remote server's Pub key is used to verify private key during ssh by user logging in, such as a human or cicd bot, hence, the CICD Runner needs the priv key.)
    - LINUX_USER_DEVOPS
      - (I typically create two users on the remote server-- One for human use, one for CICD use. Both added to the server via terraform upon creation. The purpose of these secrets is for CICD to ssh in, therefore of course, I use the username of the CICD user)
  - "ENVIRONMENT SECRETS" -- I give it the name "production" then add these secrets to the newly created "production environment" section of Github Actions Environment Secrets.  (or, you can just add these as Repo Secrets)
    - POSTGRES__SECRET_ENV_FILE
    - WAGTAIL__SECRET_ENV_FILE
    - NEXTJS__SECRET_ENV_FILE
    - 
# Regarding workflow_call and access to github secrets

When you use the `workflow_call` trigger to invoke one workflow from another, secrets are not automatically passed to the called workflow. This is a security feature in GitHub Actions that prevents secrets from being unintentionally exposed.


# Regarding CICD ssh-in

Each GitHub Actions step runs in a fresh environment, so SSH configurations don't automatically persist between steps even though they're in the same CICD workflow file. Let me explain why:

In GitHub Actions, each "step" in your workflow is essentially its own execution context. When a step completes, any changes it made to the environment (like creating SSH configurations) don't automatically carry over to subsequent steps.

Therefore, for each step requiring ssh access to the server, that step must be configured to setup its ssh config prior to its ability to ssh in and run commands.

# Regarding Workflow calls

### Passing environment secrets files from one workflow to another

the main.yml file calls the FrontEnd Deploy file.
In order to access the github actions secrets for 'production' environment,
it must pass `with:   environment: production`, and the file it calls must receive the environment string in its section `inputs:   environment:  required: true ... `, as shown in the following two file snippets: 

main.yml

```yml
name: Main Deployment Pipeline
on:
  push:
    branches: [main]
jobs:
  # Deploy frontend if needed
  frontend:
    needs: cms
    uses: ./.github/workflows/frontend-deploy.yml
    with:
      environment: production
```


frontend-deploy.yml

```yml
name: Frontend Check.  If changes detected, Deploy new image

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
        description: "The deployment environment to use"
```