from jira import JIRA
import json, sys, pprint

def create_tickets(source, project, login, password):
   outdated_dep = []
   with open(source) as file:
      data = file.read()
      outdated_dep = filter(lambda entry: 'is_latest' in entry and not entry.get('is_latest'), json.loads(data))
   grouped_by_groupd_id = {}
   for i in outdated_dep:
      id = i.get('declared').get('group_id')
      dependencies_by_group = grouped_by_groupd_id.get(id, [])
      dependencies_by_group.append(i)
      grouped_by_groupd_id[id] = dependencies_by_group
   send_tickets(grouped_by_groupd_id, project, login, password)

def send_tickets(grouped_by_groupd_id, project, login, password):   
   options = {"server": "https://jira.onap.org"}
   jira = JIRA(options, auth=(login, password))
   
   epic_dict = {
      'project': project,
      'summary': "The subsequent stories are generated per group id of outdated dependencies",
      'description': "Outdated dependencies",
      'customfield_10003': 'Outdated dependencies',
      'issuetype': {'name': 'Epic'},
   }
   epic_issue = jira.create_issue(epic_dict)

   for key in grouped_by_groupd_id:
      description = ""
      summary = "[automatically generated] Outdated dependency " + str(key)
      for i_key in grouped_by_groupd_id[key]:         
         description += "\n-= Take this result with a grain of salt, use your own judgment, and check for CVE =-\n"
         description += "\nartifact:         " + str(i_key['declared']['artifact_id'])
         description += "\npackage:          " + str(i_key['declared']['package'])
         description += "\ndeclared version: " + str(i_key['declared']['version'])
         description += "\nlatest   version: " + str(i_key['latest_version'])
         description += "\nuri checked:      " + str(i_key['uri'])
      
      issue = jira.create_issue(project=project, description=description, summary=summary, issuetype={'name': 'Story'})
      jira.add_issues_to_epic(epic_issue.id, [issue.key])
      print("created: " + str(issue.permalink()))

if __name__ == "__main__":
    print(create_tickets(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])) if (len(sys.argv) == 5) else sys.exit(
        "Incorrect number of arguments (1 expected). Please point me the result of the depencencies analysis")