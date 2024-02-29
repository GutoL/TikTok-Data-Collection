from tiktok_client import TikTokClient
import os
import pandas as pd

tiktok_client = TikTokClient('config.json')
bearer_token = tiktok_client.get_client_token()

#   Get videos comments
fields = 'id,like_count,create_time,text,video_id,parent_comment_id'

query = {
  "video_id": 7268318245755587873,
  "max_count": 50,
  "cursor": 150
}

tiktok_client.collect_comments(query, fields, 'comments.csv')