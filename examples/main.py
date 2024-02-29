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
