from typing import List

def get_projects_by_repo(client, repo_name, org_id=None) -> List:
    if org_id is None:
        orgs = client.organizations.all()
        all_projects = [project for org in orgs for project in org.projects.all()]
    else:
        all_projects = client.organizations.get(org_id).projects.all()

    projects = [project for project in all_projects if project.name.find(repo_name) != -1]
    return projects 
