# Getting Started Scenario

## Add a user to an environment

Start the portal app (local pointing to dev environment)
Selected the Positron under Choose Institution
Admin > Funding Group > Add User
Add email and add All environments
Expand Funding Group 1 and Users
Add 100 tokens to the new user

## Add new Job

Go to Scientist > Environments
Under the funding group, expand an Environment

Following steps in Environment repo

- python venv setup
- install the cli from src? didn't work, installed from PyPi.
- login with the cli - this will add the user api key as the User Auth Token in a config file at ~/.positron/config.ini
- modify the siamese params to match the desired environment (auth_token not needed)

fixes

- need to swap cli args: `python3 main.py --positron-deploy --stream-stdout`
- need to update positron-decorator to `positron_networks`
- needed to pip install `torch torchvision numpy<2`
- should we `pip freeze`? And do we point local to `positron_networks`?

Run the job with the CLI (see above)
Open the Portal and go to Scientist > Jobs and you'll see your job.

If you're running the `siamese` example you won't see any stdout for up to 10 mins.

Questions - what's the dev workflow for the decorator?

- how do we test it locally without having to publish a new version?
