# GitHub London Users Data Analysis

- **Data Collection**: I used the GitHub API to gather data on users in London with over 500 followers and their repositories.
I accessed GitHub’s API using a Personal Access Token (PAT) to bump the rate limit to 5,000 requests per hour. I started by searching for users in London with over 500 followers, then scraped for each user, like their company, location, bio, and hireable status.
Next, I pulled up to 500 recent repositories per user, capturing each repository's name, creation date, star count, language, and license. All this data was saved to users.csv and repositories.csv for easy analysis, carefully handling rate limits, pagination, and any missing fields along the way.
- **Interesting Fact**: Surprisingly, many top users have a diverse mix of programming languages showcasing the flexibility of their skills.
- **Recommendation**: Developers should maintain active profiles with engaging content to attract more followers and increase visibility which is already a given.

### Project Overview
This project aims to collect data on GitHub users in London with more than 500 followers, along with details on their public repositories. The data is saved in two CSV files: `users.csv` and `repositories.csv`.

### Files in This Repository
- **users.csv**: Contains user data, including GitHub ID (`login`), full name, company (cleaned up to remove `@` and converted to uppercase), location, email, and other details.
- **repositories.csv**: Contains data on each user's repositories, such as the repository's name, creation date, number of stars, programming language, and more.
