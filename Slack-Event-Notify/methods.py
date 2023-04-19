import requests
import json
from datetime import datetime
import os

github_token = os.environ['REMIND_GITHUB_TOKEN']
org = os.environ['REMIND_GITHUB_ORG']

def get_headers():
    return {
        'Authorization': f'Basic {github_token}'
    }

def filter_pull_requests(pull_requests, repo_name):
    filtered_pulls = []
    for pull_request in pull_requests:
        if pull_request['user']['login'] != 'dependabot[bot]':
            updated_date = pull_request['created_at'].split('T', 1)[0].replace("-", "/")
            pr_duration = datetime.today() - datetime.strptime(updated_date, '%Y/%m/%d')

            if pr_duration.days >= 0:
                message = f':git-1957: <https://github.com/{org}/{repo_name}/pull/{pull_request["number"]}|{repo_name}:> {pull_request["title"]}'
                filtered_pulls.append(message)
    return filtered_pulls

def get_pulls(repo_name):
    url = f'https://api.github.com/repos/{org}/{repo_name}/pulls'
    response = requests.request("GET", url, headers=get_headers(), data='')

    if not str(response.status_code).startswith('2'):
        response = json.loads(response.text)
        raise Exception(f"Exception calling Github: {response.message}")

    pull_requests = json.loads(response.text)
    return filter_pull_requests(pull_requests, repo_name)

def get_repository_list():
    with open('repos.txt', 'r') as textfile:
        repositories = textfile.readlines()
    return [repo.strip() for repo in repositories]

def get_correct_prs():
    open_pulls = []
    repositories = get_repository_list()

    for repository in repositories:
        pull_requests = get_pulls(repository)
        open_pulls.extend(pull_requests)

    return open_pulls
