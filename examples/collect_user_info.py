from tiktok_client import TikTokClient
import os
import pandas as pd

tiktok_client = TikTokClient('config.json')
bearer_token = tiktok_client.get_client_token()

# Get user description
fields = 'display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count'

users_list = []
file_folder = 'users_files/'
result_file_name = 'results/influencers.csv'
error_file_name = 'results/influencers_error.csv'

if os.path.isfile(result_file_name):
    result_df = pd.read_csv(result_file_name)
else:
    result_df = pd.DataFrame(columns=['username'])

if os.path.isfile(error_file_name):
    users_with_error_df = pd.read_csv(error_file_name)
else:
    users_with_error_df = pd.DataFrame(columns=['username'])

already_collected_users = result_df['username'].to_list()
already_collected_users += users_with_error_df['username'].to_list()

for file_name in os.listdir(file_folder):
    df = pd.read_excel(file_folder+file_name)
    users_list += df['Username'].to_list()

users_list = list(set(users_list)) # removing duplicates

users_list = [user for user in users_list if user not in already_collected_users]

print('Collecting ', len(users_list), 'users')

# users_list = users_list[:50]

users_list_df, users_with_error_dataframe = tiktok_client.collect_users_list(users_list=users_list, fields=fields, result_file=None)

result_df = pd.concat([result_df, users_list_df])
result_df.to_csv(result_file_name, index=False)

users_with_error_df = pd.concat([users_with_error_df, users_with_error_dataframe])
users_with_error_df.to_csv(error_file_name, index=False)