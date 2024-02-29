# TikTok Data Collection using Python

## Description
This project utilizes the official TikTok API to collect data from the TikTok platform. It allows users to retrieve various types of data such as user information, videos, comments, and more.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/GutoL/TikTok-Project.git
   ```

2. Install the required dependencies using pip:
    ```bash
    pip install -r requirements.txt

3. Obtain your TikTok developer credentials from the TikTok Developer Dashboard. Update the configuration file config.json with your TikTok developer credentials:
   ```json
      {
        "client_key" : "your-api-key"
        "client_secret": "your-api-secret"
      }
   ```

## Usage
Run the Python scripts to collect TikTok data:

collect_user_info.py: Collect user information based on usernames.
collect_video_info.py: Collect video information based on video URLs.
collect_comments.py: Collect comments for a given video.
Each script may require different parameters such as usernames, video URLs, hashtags, etc. Ensure to provide the necessary inputs as per the script requirements.

Execute the scripts:
```python
python collect_video_info.py
```

## License
This project is licensed under the Apache License 2.0.
