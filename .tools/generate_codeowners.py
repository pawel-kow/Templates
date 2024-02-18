import json
import os
import requests

GITHUB_TOKEN = '***'

errors = []
providerIdsContributors = {}
for file_to_check in [r for r in os.listdir(os.curdir) if r.endswith('.json')]:
    with open(file_to_check) as f:
        template_json = json.load(f)
        prov_id = template_json['providerId'].lower()
        if prov_id not in providerIdsContributors:
            providerIdsContributors[prov_id] = []

        url = f"https://api.github.com/repos/Domain-Connect/Templates/commits?path={file_to_check}"
        payload = {}
        headers = {
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'CODEOWNERS generator',
            'Authorization': f'Bearer {GITHUB_TOKEN}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json is not None:
                for commit in resp_json:
                    try:
                        if "author" in commit and "login" in commit["author"]:
                            committer = commit["author"]["login"]
                            if committer not in providerIdsContributors[prov_id]:
                                providerIdsContributors[prov_id] += [committer]
                    except Exception as e:
                        pass
            else:
                raise ValueError(f"resp_json is empty for {file_to_check}")
        else:
            raise OverflowError(f"Cannot get commits for {file_to_check}. Status: {response.status_code}, Txt: {response.text}")

for prov in providerIdsContributors.keys():
    committers = ', '.join([f'@{x}' for x in providerIdsContributors[prov]])
    print(f"{prov}.*.json {committers}")