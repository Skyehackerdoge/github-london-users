response = requests.get("https://api.github.com/rate_limit", headers=headers)

if response.status_code == 200:
    print("Token is working. Rate limit info:", response.json())
else:
    print("Token not working. Status code:", response.status_code, response.json())
import requests
import csv
import time
from collections import defaultdict

headers = {
    "Authorization": "Bearer ",  #I added my PAT here
    "Accept": "application/vnd.github+json"
}

# Function to get users in London with over 500 followers
def get_users(location="London", min_followers=500):
    users_data = []
    page = 1

    while True:
        url = f"https://api.github.com/search/users?q=location:{location}+followers:>{min_followers}&per_page=100&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            users = response.json().get('items', [])
            if not users:
                break  # Exit loop if no users are found on this page
            users_data.extend(users)
            page += 1
            time.sleep(1)  # Rate limiting
        else:
            print("Error fetching users:", response.json().get('message'))
            break

    return users_data

# Function to get detailed user data by username
def get_user_details(username):
    user_url = f"https://api.github.com/users/{username}"
    response = requests.get(user_url, headers=headers)
    return response.json() if response.status_code == 200 else {}

# Function to get up to 500 repositories for each user
def get_user_repositories(username):
    repos = []
    page = 1
    max_pages = 5  # To get up to 500 repositories (5 pages of 100)

    while page <= max_pages:
        repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(repos_url, headers=headers)

        if response.status_code == 200:
            repos_page = response.json()
            repos.extend(repos_page)
            if len(repos_page) < 100:
                break  # No more repos on next page
            page += 1
            time.sleep(1)
        else:
            print(f"Error fetching repositories for user {username}: {response.json().get('message', 'Unknown error')}")
            break

    return repos

# Fetch user data and repository data
users = []
repositories = []

for user in get_users():
    username = user['login']
    user_details = get_user_details(username)
    company = (user_details.get('company') or '').strip().lstrip('@').upper()
    
    user_data = {
        'login': username,
        'name': user_details.get('name', ''),
        'company': company,
        'location': user_details.get('location', ''),
        'email': user_details.get('email', ''),
        'hireable': str(user_details.get('hireable', '')).lower(),
        'bio': user_details.get('bio', ''),
        'public_repos': user_details.get('public_repos', 0),
        'followers': user_details.get('followers', 0),
        'following': user_details.get('following', 0),
        'created_at': user_details.get('created_at', '')
    }
    users.append(user_data)

    # Fetch repositories for the user
    user_repos = get_user_repositories(username)
    for repo in user_repos:
        repo_data = {
            'login': username,
            'full_name': repo.get('full_name', ''),
            'created_at': repo.get('created_at', ''),
            'stargazers_count': repo.get('stargazers_count', 0),
            'watchers_count': repo.get('watchers_count', 0),
            'language': repo.get('language', ''),
            'has_projects': str(repo.get('has_projects', False)).lower(),
            'has_wiki': str(repo.get('has_wiki', False)).lower(),
            'license_name': repo['license']['key'] if repo.get('license') else ''
        }
        repositories.append(repo_data)

# Write users data to users.csv
with open("users.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(users)

# Write repository data to repositories.csv
with open("repositories.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(repositories)

print("Data has been written to users.csv and repositories.csv")
