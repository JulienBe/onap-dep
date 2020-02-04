Very quick script to flag our outdated dependencies and create the associated JIRA ticket

# Requirements

You need to have `python` to run the scripts and `maven` to get your top level dependencies. 

# Use it

0. generate a dependency tree file with mvn dependency:tree > dep_file
1. run `flag_outdated_dep.py dep_file > outdated_dep_file` on your project to generate a json containing all the info needed about your outdated dependencies by parsing the dependency tree file
2. run `create_tickets.py outdated_dep_file JIRA_project_name JIRA_login JIRA_password` to create the actual JIRA tickets.

# Outcome

- It will create an **epic** which represents this executations.
- This epic will have **stories**
- Each story will be created per **group id**.
- In the description you will find **all dependencies** of this group id

# Welcome improvements

- A better way to handle JIRA authentication
- Check if the ticket already exists. If no ticket are required, don't create the epic
- Create the associated gerrit merge request
