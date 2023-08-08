from argparse import ArgumentParser

from get_projects_by_repo import get_projects_by_repo

import snyk

def main():
    parser = ArgumentParser(prog='cli')
    parser.add_argument('api_token', help="The API token in your Snyk account settings")
    parser.add_argument('repo_name', help='The name of the repo that you want to search for')
    args = parser.parse_args()

    client = snyk.SnykClient(args.api_token)

    results = get_projects_by_repo(client, args.repo_name)

    print('\n'.join(project.name for project in results)) if len(results) else print('repo not found')


if __name__ == '__main__':
    main()