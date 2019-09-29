# Recipe app (unnamed)

## Update Log

### Tyler Hughes - 9/29/2019

Added functionality to ETL FDA data from flat csv files to ETL schema and tables in Postgres database. The database is running on localhost.

To run this code, here's what you'll need to do:

1. Download PostgreSQL
   1. When you run the installation, it'll have you configure some stuff. I did all the defaults, so the user is postgres and the port it runs on is 5432
   2. It should download pgAdmin as well. That's how you can view the data in tables and everything.
   3. Since this is running on localhost, it won't be persistent. You'll have to rerun the code to repopulate everything

2. Setup pipenv
   1. I've been using PipEnv lately for environment management rather than conda or virtualenv, and I really like it. You'll see the Pipfile and Pipfile.lock in this repo.
   2. *In your root python installation (no environment activated)* run **pip install pipenv**. This will get you ready to use the module.
   3. From the root of this repository, run **pipenv install** to setup a virtual environment with all the packages you'll need.
   4. All commands you want to use should be preceded by **pipenv** in order to use this environment.
      1. To install *requests*, for instance, you'd run **pipenv install requests**
      2. This updates the pipfile and sha hashes in Pipfile.lock automatically.
   5. If you want to enter a python shell using the configured environment, you can run **pipenv shell**
      1. I will commonly run **pipenv shell** then **ipython** to enter the ipython shell within the configured environment.

3. Update appsettings.json with your local configuration.
   1. You can follow the structure I'm using. I just put my Postgres configuration under the key Tyler. We can redo this later if we need to.
  
4. Drop the FDAData directory into **/data**. I didn't want to include that in the git repo. It's just a folder called FDAData with all of the output from our FDA data pull.

5. From the root of the repository, run **pipenv run load_nutrition_data.py**.

6. Check the output in pgAdmin. You should see a new schema called etl and a table for each file. We can worry about making that more usable later.

I think that's about it for today. I tried to keep things organized so that it's easy to build off of. Let me know if you have any questions.
