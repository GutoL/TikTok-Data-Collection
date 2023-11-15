import requests
import json
import pandas as pd

class TikTokClient():
    def __init__(self, config_file) -> None:
        
        f = open(config_file)
        self.config = json.load(f)
        f.close()
    
    def get_client_token(self):
        # https://developers.tiktok.com/doc/client-access-token-management
        rerquest_config = {
            'client_key': self.config['client_key'],
            'client_secret': self.config['client_secret'],
            'grant_type': self.config['grant_type']
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache',
        }
        
        x = requests.post(self.config['token_url'], headers=headers, data=rerquest_config)

        bearer_token_content = dict(x.json())
        self.bearer_token = bearer_token_content['access_token']

        return bearer_token_content

    def run_query(self, query, fields, content_type):
        headers = {
            'authorization': 'bearer '+self.bearer_token,
            'Content-Type':'application/json'
        }

        data = json.dumps(query, indent=4)

        response = requests.post(self.config[content_type+'_url']+fields, headers=headers, data=data)

        print(response.json())
        
        return response.status_code, response.json()
    
    def collect_video(self, query, fields, result_file):

        keep_collecting = True

        result_video_dataframe = pd.DataFrame()

        while keep_collecting:
            code, data = self.run_query(query, fields, 'videos')

            if code == 429:
                break
            
            elif code != 200:
                continue
            
            keep_collecting = data['data']['has_more']
            result_video_dataframe = pd.concat([result_video_dataframe, pd.json_normalize(data['data']['videos'])])

            query['cursor'] = data['data']['cursor']
            query['search_id'] = data['data']['search_id']


        if result_file:
            result_video_dataframe.to_csv(result_file, index=False)

        return result_video_dataframe
    
    def collect_comments(self, query, fields, result_file):

        keep_collecting = True

        result_comment_dataframe = pd.DataFrame()

        while keep_collecting:
            code, data = self.run_query(query, fields, 'comments')
            
            if code == 429:
                break
            
            elif code != 200:
                continue
            
            keep_collecting = data['data']['has_more']

            result_comment_dataframe = pd.concat([result_comment_dataframe, pd.json_normalize(data['data']['comments'])])

            query['cursor'] = data['data']['cursor']

        if result_file:
            result_comment_dataframe.to_csv(result_file, index=False)

        return result_comment_dataframe
    

    def collect_users_list(self, users_list, fields, result_file):
        
        users_list_dataframe = pd.DataFrame()
        users_with_error_dataframe = pd.DataFrame()
        users_names = []
        users_names_error = []

        for user in users_list:
            print('Collecting user:', user)
            
            query = {"username": user}
            code, data = self.collect_user(query, fields, None)

            if code == 429:
                break
            
            elif code != 200:
                users_with_error_dataframe = pd.concat([users_with_error_dataframe, data])
                users_names_error.append(user)
                continue

            users_list_dataframe = pd.concat([users_list_dataframe, data])
            users_names.append(user)

        users_list_dataframe['username'] = users_names
        users_with_error_dataframe['username'] = users_names_error
        
        if result_file:
            users_list_dataframe.to_csv(result_file, index=False)
        
        return users_list_dataframe, users_with_error_dataframe

    def collect_user(self, query, fields, result_file):
        code, data  = self.run_query(query, fields, 'users')

        if code == 429 or code != 200:
            return code, pd.json_normalize(data['error'])
            
        result_users_dataframe = pd.json_normalize(data['data'])

        if result_file:
            result_users_dataframe.to_csv(result_file, index=False)
        
        return code, result_users_dataframe
    

