

from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyDr8Q-jj963mzYItql3s2u1pSy1NBinvHw'
channel_ids = ['UCekyMtsUuTBxInGbeSX3EUg','UCb-xXZ7ltTvrh9C6DgB9H-Q','UCmtjH4p-qik5RLqcU-Fox_Q']

youtube = build('youtube', 'v3', developerKey=api_key)

def get_channel_details(youtube,channel_ids):
    all_channels=[]
    request=youtube.channels().list(
        part="snippet,contentDetails,statistics",id=",".join(channel_ids))
    response=request.execute()
    for i in range(len(response['items'])):
        data=dict(channel_name=response['items'][i]['snippet']['title'],
                  total_views=response['items'][i]['statistics']['viewCount'],
                  subscribers=response['items'][i]['statistics']['subscriberCount'],
                  video_count=response['items'][i]['statistics']['videoCount'],
                  uploads=response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                  )
        all_channels.append(data)
    print(all_channels)
    return all_channels

x=get_channel_details(youtube, channel_ids)

chanels=pd.DataFrame(x)
# prasad_tech='UCb-xXZ7ltTvrh9C6DgB9H-Q'
# few_chanels=['UCekyMtsUuTBxInGbeSX3EUg','UCb-xXZ7ltTvrh9C6DgB9H-Q','UCmtjH4p-qik5RLqcU-Fox_Q']
uploads='UUekyMtsUuTBxInGbeSX3EUg'
def get_video_ids(youtube,uploads):
    request=youtube.playlistItems().list(
        part='contentDetails',playlistId=uploads
        ,maxResults=50)
    response=request.execute()
    # return response
    
    video_ids=[]
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token=response.get('nextPageToken')
    more_pages=True
    
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request=youtube.playlistItems().list(
                part='contentDetails',playlistId=uploads
                ,maxResults=50,
                pageToken=next_page_token)
            response=request.execute()
            
            
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
                next_page_token=response.get('nextPageToken')
    return video_ids
ids=get_video_ids(youtube,uploads)
print(ids)

def get_videos_details(youtube,ids):
    total_videos_data=[]
    for i in range(0,len(ids),50):
        request=youtube.videos().list(
            part='snippet,statistics',
            id=','.join(ids[i:i+50])
            )
        response=request.execute()
        
        for video in response['items']:
            video_details=dict(
                title=video['snippet']['title'],
                date=video['snippet']['publishedAt'],
                views=video['statistics']['viewCount'],
                likeCount=video['statistics']['likeCount'],
                dis_like=video['statistics']['favoriteCount'],
                commentCount=video['statistics']['commentCount'],
                )
            total_videos_data.append(video_details)
        
        
    return total_videos_data
        
one_channel=get_videos_details(youtube,ids)


all_videos=pd.DataFrame(one_channel)
all_videos.columns

all_videos['date']=pd.to_datetime(all_videos['date']).dt.date
    
all_videos['views']=pd.to_numeric(all_videos['views'])
all_videos['likeCount']=pd.to_numeric(all_videos['likeCount'])
all_videos['dis_like']=pd.to_numeric(all_videos['dis_like'])
all_videos['commentCount']=pd.to_numeric(all_videos['commentCount'])

top_10_videos=all_videos.sort_values(by='views',ascending=False).head(10)

graph_1=sns.barplot(x='views',y='title',data=top_10_videos)










