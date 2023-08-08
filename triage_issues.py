from argparse import ArgumentParser
import functools
from typing import List
import sys
import re
from textops import *

from query_yes_no import query_yes_no

import snyk



def main():
    parser = ArgumentParser(prog='cli')
    parser.add_argument('api_token', help="The API token in your Snyk account settings")
    parser.add_argument('package_manager', help="The package manager belonging to the package where the issues are located")
    parser.add_argument('package_group_id', help="Maven only - leave blank otherwise")
    parser.add_argument('package_name', help="The name of the package you wish to triage for issues")
    parser.add_argument('package_version', help="")
    parser.add_argument('path', help="File search path")
    #parser.add_argument('')
    args = parser.parse_args()

    client = snyk.SnykClient(args.api_token)

    org = client.organizations.first()

    if args.package_manager == 'maven':
        file_extention = '*.java'
        vulns = org.test_maven(args.package_group_id, args.package_name, args.package_version).issues.vulnerabilities
    else:
        file_extention = None
        vulns = []
    
    vuln_amount = len(vulns)
    print('Found %s vulnerabilities' % vuln_amount)

    validated_vulns = []
    for count, vuln in enumerate(vulns):
        print('\n%s/%s:\n' % (count + 1, vuln_amount))
        possible_matches = re.findall('(.*)`(.*?)`', vuln.description)
        match = None
        for context, code in possible_matches:
            print(context + code)
            if code != 'BeanDeserializer':
                break
            else:
                match = code
            if query_yes_no('Search for %s?' % code):
                match = code
                break
        
        if match is not None:
            search_results = args.path | find(file_extention) | cat() | grep(match)
            results_count = 0
            for value in search_results:
                print('\033[91m' + value + '\033[0m')
                results_count += 1
            if results_count > 0:
                validated_vulns.append(vuln)

    print('\n' + [v.title for v in validated_vulns])    
        
        # if query_yes_no('Apply tag to %s?' % vuln.title):
            # pass
            # try:
            #     vuln.tags.add(args.key, args.value)
            # except snyk.errors.SnykHTTPError as e:
            #     print('Couldn\'t add tags: %s' % str(e))

if __name__ == '__main__':
    main()
