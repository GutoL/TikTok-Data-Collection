from tiktok_client import TikTokClient
import os
import pandas as pd

tiktok_client = TikTokClient('config.json')
bearer_token = tiktok_client.get_client_token()



# https://developers.tiktok.com/doc/research-api-specs-query-user-info/
query = { "query": 
                    {"and": [
                            { "operation": "IN", "field_name": "region_code", "field_values": ["US", "CA"] },                  
                            { "operation": "EQ", "field_name": "keyword", "field_values": ["hello world"] }
                        ]
                    }, 
                    "start_date": "20220615", "end_date": "20220628", "max_count": 10
                }


# # Get user description
# fields = 'display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count'

# users_list = []
# file_folder = 'users_files/'
# result_file_name = 'results/diet_influencers.csv'
# error_file_name = 'results/diet_influencers_error.csv'

# if os.path.isfile(result_file_name):
#     result_df = pd.read_csv(result_file_name)
# else:
#     result_df = pd.DataFrame(columns=['username'])

# if os.path.isfile(error_file_name):
#     users_with_error_df = pd.read_csv(error_file_name)
# else:
#     users_with_error_df = pd.DataFrame(columns=['username'])

# already_collected_users = result_df['username'].to_list()
# already_collected_users += users_with_error_df['username'].to_list()

# for file_name in os.listdir(file_folder):
#     df = pd.read_excel(file_folder+file_name)
#     users_list += df['Username'].to_list()

# users_list = list(set(users_list)) # removing duplicates

# users_list = [user for user in users_list if user not in already_collected_users]

# print('Collecting ', len(users_list), 'users')

# # users_list = users_list[:50]

# users_list_df, users_with_error_dataframe = tiktok_client.collect_users_list(users_list=users_list, fields=fields, result_file=None)

# result_df = pd.concat([result_df, users_list_df])
# result_df.to_csv(result_file_name, index=False)

# users_with_error_df = pd.concat([users_with_error_df, users_with_error_dataframe])
# users_with_error_df.to_csv(error_file_name, index=False)

#-------------------------------------------------------------------------------------------------------------------------------

# https://developers.tiktok.com/doc/research-api-specs-query-user-info/
# query = {"username": "stephgrassodietitian"}
# tiktok_client.collect_user(query, fields, 'stephgrassodietitian.csv')


# #   Get videos comments
# fields = 'id,like_count,create_time,text,video_id,parent_comment_id'
# query = {
#   "video_id": 7268318245755587873,
#   "max_count": 50,
#   "cursor": 150
# }

# tiktok_client.collect_comments(query, fields, 'comments.csv')

#-------------------------------------------------------------------------------------------------------------------------------
# # Get videos
# #Display API
# fields = 'id,video_description,create_time, region_code,share_count,view_count,'+'embed_html, embed_link,'
# fields += 'like_count,comment_count, music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text'

# Research API
fields = 'id,video_description,create_time, region_code,share_count,view_count,like_count,comment_count,' 
fields += 'music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text'


# query = {"query": {
#                     "and": [
#                             {
#                                 "operation": "IN",
#                                 "field_name": "region_code",
#                                 "field_values": ["JP", "US"]
#                             },
                        
                        
#                             {
#                                 "operation":"EQ",
#                                 "field_name":"hashtag_name",
#                                 "field_values":["animal"]
#                             },
#                             {
#                                 "operation": "EQ",
#                                 "field_name": "keyword",
#                                 "field_values": ["alligator"]

#                             }      
                           
#                     ],
#                     "not": [
#                         {
#                             "operation": "EQ",
#                             "field_name": "video_length",
#                             "field_values": ["SHORT"]
#                         }
#                     ]
#     },
#     "max_count": 100,
#     "cursor": 0,
#     "start_date": "20230101",
#     "end_date": "20230115"
# }


query = {
    "query":{
            "and": [
                {
                    "operation": "IN",
                    "field_name": "region_code",
                    "field_values": ["CAN", "US", "GBR",]
                },
                {
                    "operation": "EQ",
                    "field_name": "username",
                    "field_values": ["themoodyfoody"]
                }
            ]            
    },
    "max_count": 100,
    "start_date": "20230101",
    "end_date": "20230115"
}


df = pd.read_csv('diet_influencers.csv')

df = df[df['Content_Creator/Account'] == 'Content_Creator']

print(df)

# tiktok_client.collect_video(query=query, fields=fields, result_file='videos.csv')