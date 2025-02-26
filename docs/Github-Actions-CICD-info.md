# Regarding workflow_call and access to github secrets

When you use the `workflow_call` trigger to invoke one workflow from another, secrets are not automatically passed to the called workflow. This is a security feature in GitHub Actions that prevents secrets from being unintentionally exposed.


# Regarding CICD ssh-in

Each GitHub Actions step runs in a fresh environment, so SSH configurations don't automatically persist between steps even though they're in the same CICD workflow file. Let me explain why:

In GitHub Actions, each "step" in your workflow is essentially its own execution context. When a step completes, any changes it made to the environment (like creating SSH configurations) don't automatically carry over to subsequent steps.

Therefore, for each step requiring ssh access to the server, that step must be configured to setup its ssh config prior to its ability to ssh in and run commands.