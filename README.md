# WNP portfolio project

>Dockerized Wagtail CMS, NextJS, PostgreSQL (For Wagtail use) for a portfolio website

Stack: Wagtail CMS, NextJS FE, Postgres DB

Current focus: CICD Deployment
- Get CICD Deployment working in a good way
  - DB: just deploy once
  - CMS & FE: Check for changes in directories by comparing current vs most recent commit. Track most recent commit in github artifact file so it persists between deployments.

To Do:
- [ ] Finish CICD
- [ ] When CICD is done, make a copy of the project as a template & commit it to github.
- [ ] Once the template is separated out, Add in the Wagtail CMS schema for Portfolio Items.  Then incorporate that into the NextJS FE.
- [ ] Now that I have some experience with Wagtail, begin using it for other projects.

Potential future projects:
- Test Wagtail CMS's its limits on a cheap server-- e.g. 1vcpu, 2gb ram.  And perhaps on a server one step up.  Get some experience with it and see how efficient (re: human time, LOC, building speed, cognitive requirements (i.e. learning curve & dev experience)) & performant (re: user experience & server metrics (especially speed) vs available resource consumption, compared to alternative CMS) it is to build REST API with.

Try it out:

```bash
git clone git@github.com:pmeaney/dockerized-wnp-portfolio2025.git && \
cd dockerized-wnp-portfolio2025 && \
docker compose -f docker-compose.dev.yml up
```

See the ./docs directory for additional setup information, such as Github Secrets, and Env Vars