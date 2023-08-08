from argparse import ArgumentParser
import functools
from typing import List
import sys

from query_yes_no import query_yes_no
from get_projects_by_repo import get_projects_by_repo

import snyk

# @functools.lru_cache(maxsize=32)
# def get_org_ids(client) -> List[str]:
#     result = client.organizations.all()
#     org_ids = [entry.id for entry in result]
#     return org_ids

def get_org_id(client, name) -> List[str]:
    result = client.organizations.all()
    org_id = [entry.id for entry in result if entry.name == name]
    if not org_id:
        raise ValueError('Org name not found')
    return org_id[0]


def main():
    parser = ArgumentParser(prog='cli')
    parser.add_argument('api_token', help="The API token in your Snyk account settings")
    parser.add_argument('org_name', nargs='?', help="Optional arg for narrowing search by organisation name")
    parser.add_argument('repo_name', help='The name of the repo that holds the Snyk projects you wish to update')
    parser.add_argument('key', help='The tag key you want to apply')
    parser.add_argument('value', help='The value of the tag you want to apply')
    #parser.add_argument('')
    args = parser.parse_args()

    client = snyk.SnykClient(args.api_token)

    org_id = get_org_id(client, args.org_name) if args.org_name else None
    
    projects = get_projects_by_repo(client, args.repo_name, org_id)
    
    for project in projects:
        if query_yes_no('Apply tag to %s?' % project.name):
            try:
                project.tags.add(args.key, args.value)
            except snyk.errors.SnykHTTPError as e:
                print('Couldn\'t add tags: %s' % str(e))


if __name__ == '__main__':
    main()

