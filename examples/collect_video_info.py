from tiktok_client import TikTokClient
import os
import pandas as pd

tiktok_client = TikTokClient('config.json')
bearer_token = tiktok_client.get_client_token()


# # Get videos
# #Display API
# fields = 'id,video_description,create_time, region_code,share_count,view_count,'+'embed_html, embed_link,'
# fields += 'like_count,comment_count, music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text'

# Research API
fields = 'id,video_description,create_time, region_code,share_count,view_count,like_count,comment_count,' 
fields += 'music_id,hashtag_names, username,effect_ids,playlist_id,voice_to_text'

username_list = ["themoodyfoody"]

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
                    "field_values": username_list
                }
            ]            
    }
}

start_date = '2023-01-01'
end_date = '2023-01-15'

tiktok_client.collect_video(query=query, fields=fields, result_file='videos.csv')
videos = tiktok_client.collect_video(query=query, fields=fields,
                                        result_path='result_path/',
                                        result_file_name='videos_start_'+start_date+'_end_'+end_date,
                                        chunk_size_to_save=1000,
                                        start_date=start_date, end_date=end_date)