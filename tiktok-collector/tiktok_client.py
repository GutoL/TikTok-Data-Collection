import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import os

class TikTokClient():
    def __init__(self, config_file) -> None:

        self.data_format = '%Y-%m-%d' # '%Y-%m-%d %H:%M:%S'

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


    def split_date_interval(self, start_date_str, end_date_str):

        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date_str, self.data_format)
        end_date = datetime.strptime(end_date_str, self.data_format)

        # Check if the interval is greater than 30 days
        if (end_date - start_date).days <= 30:
            return [(start_date_str, end_date_str)]

        # Initialize lists to store start and end dates of each interval
        start_dates = []
        end_dates = []

        # Divide the interval into periods of 30 days
        current_start_date = start_date

        while current_start_date < end_date:
            current_end_date = current_start_date + timedelta(days=30)
            if current_end_date > end_date:
                current_end_date = end_date

            start_dates.append(current_start_date.strftime(self.data_format))
            end_dates.append(current_end_date.strftime(self.data_format))

            current_start_date = current_end_date + timedelta(days=1)

        return list(zip(start_dates, end_dates))

    def run_query(self, query, fields, content_type, number_of_tries=5):
        headers = {
            'authorization': 'bearer '+self.bearer_token,
            'Content-Type':'application/json'
        }

        data = json.dumps(query, indent=4)

        while number_of_tries > 0:
            # print('Trying:', data)

            response = requests.post(self.config[content_type+'_url']+fields, headers=headers, data=data)

            if response.status_code == 500: # server error
                print('Error 500, try:', number_of_tries)

                number_of_tries -= 1
                time.sleep(1) # wait until try another request
            else:
                number_of_tries = 0

        if response.status_code == 200:
            status_code = response.status_code
            json_response = response.json()
            print(status_code, json_response)

        else:
            status_code = response.status_code
            json_response = {'Error': status_code, 'text':response.json()}
            print('*** Status code:', status_code)

        return status_code, json_response

    def get_last_time(self, path, end_date, date_column_name='create_date'):

        # files_name = [int(filename.split('_')[-1].replace('.csv', '')) for filename in os.listdir(path)]

        last_file = None
        last_index = 0

        for file_name in os.listdir(path):
            current_file_index = int(file_name.split('_')[-1].replace('.csv', ''))

            if current_file_index > last_index:
                last_index = current_file_index
                last_file = file_name

        if last_file:
          df = pd.read_csv(path+last_file)
          df[date_column_name] = pd.to_datetime(df[date_column_name])

          last_date = df.iloc[-1][date_column_name].strftime(self.data_format)

          if last_date < end_date:
              end_date = last_date

        return end_date, last_index


    def collect_video(self, query, start_date, end_date, fields, result_path, result_file_name, chunk_size_to_save=10000):

        end_date, batch_saved_number = self.get_last_time(path=result_path, end_date=end_date) # getting the date of the last video downloaded

        batch_saved_number += 1

        intervals = self.split_date_interval(start_date, end_date)

        keep_collecting = True

        result_video_dataframe = pd.DataFrame()

        for d_start, d_end in intervals:
            keep_collecting = True
            query.pop('search_id', None)
            query.pop('cursor', None)

            while keep_collecting:

                query['start_date'] = d_start.replace('-','')
                query['end_date'] = d_end.replace('-','')

                print('------------------------------------')
                # print(query)
                # code, data = self.run_query(query, fields, 'display_videos')
                code, data = self.run_query(query, fields, 'videos')
                time.sleep(0.25)

                if code == 429 or code == 500:
                    break

                elif code != 200:
                    continue

                keep_collecting = data['data']['has_more']
                result_video_dataframe = pd.concat([result_video_dataframe, pd.json_normalize(data['data']['videos'])])

                if keep_collecting:
                    query['cursor'] = data['data']['cursor']
                    # if 'search_id' in data['data']:
                    query['search_id'] = data['data']['search_id']


                if result_video_dataframe.shape[0] >= chunk_size_to_save:
                    print('Saving file:', result_path+result_file_name+'_'+str(batch_saved_number)+'.csv')

                    result_video_dataframe['create_date'] = pd.to_datetime(result_video_dataframe['create_time'], unit='s')
                    result_video_dataframe.to_csv(result_path+result_file_name+'_'+str(batch_saved_number)+'.csv', index=False)

                    result_video_dataframe = pd.DataFrame()
                    batch_saved_number += 1
                    time.sleep(4)


        if result_video_dataframe.shape[0] > 0:
            result_video_dataframe['create_date'] = pd.to_datetime(result_video_dataframe['create_time'], unit='s')
            result_video_dataframe.to_csv(result_path+result_file_name+'_'+str(batch_saved_number)+'.csv', index=False)

        fp = open(result_path+'finished.txt', 'w')
        fp.write('Done!')
        fp.close()

        return result_video_dataframe # '''

    def collect_comments(self, query, fields, result_file):

        keep_collecting = True

        result_comment_dataframe = pd.DataFrame()

        while keep_collecting:
            code, data = self.run_query(query, fields, 'comments')

            if code == 429:
                break

            elif code != 200 or code == 500:
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
