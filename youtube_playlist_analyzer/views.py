from django.shortcuts import render
from apiclient.discovery import build
import json
import os
import statistics

# YouTube Data API V3 Key
YT_API_KEY = os.environ['YOUTUBE_DATA_API_V3']


# Function to get basic playlist details
def basic_playlist_details(playlist_id, youtube_obj):
    basic_details = dict()
    request = youtube_obj.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()
    basic_details["Playlist_Title"]= response["items"][0]["snippet"]["title"] 
    basic_details["Channel_Title"]= response["items"][0]["snippet"]["channelTitle"] 
    return basic_details

# Function to get the video IDs of each video of the playlist
def get_vid_ids_from_playlist(playlist_id, youtube_obj):
    vid_ids = list()
    next_page_token = ""
    # Accessing each of the videos of the plylist - 1 page at a time
    # Each page contains the details of 50 videos
    while next_page_token is not "NA":
        request = youtube_obj.playlistItems().list(
            part="contentDetails",
            maxResults="50",
            pageToken=next_page_token,
            playlistId=playlist_id
        )
        response = request.execute()
        # print("\n\nPlaylist json response:")
        # print(json.dumps(response, indent=4))
        vid_items = response["items"]
        for vid_item in vid_items:
            vid_ids.append(vid_item["contentDetails"]["videoId"])
        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            next_page_token = "NA"
            break
    return vid_ids

# Function to get the duration of each video
def get_vid_details(vid_ids, youtube_obj):
    vid_details = dict()
    for vid_id in vid_ids:
        request = youtube_obj.videos().list(
        part="snippet,contentDetails,statistics",
        id=vid_id
        )
        response = request.execute()
        #print(json.dumps(response, indent=4))
        title = response["items"][0]["snippet"]["title"]
        duration = response["items"][0]["contentDetails"]["duration"][2:]
        likes = response["items"][0]["statistics"]["likeCount"]
        dislikes = response["items"][0]["statistics"]["dislikeCount"]
        views = response["items"][0]["statistics"]["viewCount"]
        stats = dict()
        stats["Duration"] = duration
        stats["Views"] = views
        stats["Likes"] = likes
        stats["Dislikes"] = dislikes        
        
        vid_details[title] = stats
    return vid_details


def convert_secs_to_h_m_s(count_secs):
    duration = dict()
    hrs_count = int(count_secs/3600)
    count_secs = count_secs % 3600
    mins_count = int(count_secs/60)
    count_secs = count_secs % 60
    secs_count = int(count_secs)
    duration["Hours"] = hrs_count
    duration["Mins"] = mins_count
    duration["Secs"] = secs_count
    return duration

def test(request):
    return render(request, 'youtube_playlist_analyzer/test.html')


# Create your views here.
def index(request):
    context = dict()
    context['Playlist_Title'] = None
    context['Playlist_URL'] = None
    vid_durations = dict()
    vid_viewcounts = dict()
    if 'search' in request.GET:
        playlist_url = request.GET['search']
        context['Playlist_URL'] = playlist_url
        playlist_id = playlist_url.split("playlist?list=")[1]
        youtube_obj = build("youtube", "v3", developerKey=YT_API_KEY)
        # Get YouTube Playlist name, channel name
        playlist_details = basic_playlist_details(playlist_id, youtube_obj)
        print(f"\nPlaylist Title: {playlist_details['Playlist_Title']}\nChannel title: {playlist_details['Channel_Title']}\n")

        context["Playlist_Title"] = playlist_details['Playlist_Title']
        context["Channel_Title"] = playlist_details['Channel_Title']
        # Get all the video IDs which are part of the playlist
        vid_ids = get_vid_ids_from_playlist(playlist_id, youtube_obj)
        vid_details = get_vid_details(vid_ids, youtube_obj)
        # Get the duration of each of the videos given the video ID
        hours = 0
        mins = 0
        seconds = 0
        total_duration = 0
        count = 1
        #print("\n\nVideos in playlist:")
        #print(f"\nPlaylist has {len(vid_details)} videos listed below:\n")
        shortest_vid = dict()
        longest_vid = dict()
        shortest_vid_duration = 999999
        shortest_vid = ""
        longest_vid_duration = -999999
        longest_vid = ""
        most_popular_vid = ""
        most_popular_view_count = 0
        avg_views = 0
        avg_like_percentage = 0.0
        for title, stats in vid_details.items():
            like_percentage = 0.0
            time_count = 0
            duration = stats["Duration"]
            views = stats["Views"]
            likes = stats["Likes"]
            dislikes = stats["Dislikes"]
            like_percentage = round(int(likes)/(int(likes) + int(dislikes)) * 100, 2)
            avg_like_percentage += like_percentage 
            if int(views) > most_popular_view_count:
                most_popular_view_count = int(views)
                most_popular_vid = title
            avg_views += int(views)
            print(f"\n{count}. Title: {title}\nDuration: {duration}\nViews: {views}\nLikes: {likes}\nDislikes: {dislikes}")
            count += 1
            if "H" in duration:
                hours = int(duration.split("H")[0])
                time_count = 3600 * hours
                duration = duration.split("H")[1]
            if "M" in duration:
                mins = int(duration.split("M")[0])
                time_count += 60 * mins
                duration = duration.split("M")[1]
            if "S" in duration:
                seconds = int(duration.split("S")[0])
                time_count += seconds
            if time_count < shortest_vid_duration:
                shortest_vid_duration = time_count
                shortest_vid = title
            if time_count > longest_vid_duration:
                longest_vid_duration = time_count
                longest_vid = title
            vid_durations[time_count] = title
            vid_viewcounts[int(views)] = title
            total_duration += time_count
        list_durations = vid_durations.keys()
        list_viewcounts = vid_viewcounts.keys()
        
        min_view_count = min(list_viewcounts)
        max_view_count = max(list_viewcounts)
        median_view_count = statistics.median(list_viewcounts)
        mean_view_count = statistics.mean(list_viewcounts)
        min_duration = min(list_durations)
        max_duration = max(list_durations)
        median_duration = statistics.median(list_durations)
        mean_duration = statistics.mean(list_durations)
        for viewCount, vidTitle in vid_viewcounts.items():
            if viewCount == max_view_count:
                vid_most_views = vidTitle
            if viewCount == min_view_count:
                vid_least_views = vidTitle
        for durationCount, vidTitle in vid_durations.items():
            if durationCount == max_duration:
                vid_max_duration = vidTitle
            if durationCount == min_duration:
                vid_min_duration = vidTitle
        #print(f"Duration in seconds: {total_duration}\n")
        vid_count = len(vid_details)
        context["vid_count"] = vid_count
        print(f"\nPlaylist has {vid_count} videos\n")
        time = convert_secs_to_h_m_s(total_duration)
        print(f'\nTotal duration of playlist: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')
        context["total_h"] = time["Hours"]
        context["total_m"] = time["Mins"]
        context["total_s"] = time["Secs"]
        
        print(f"\nMost viewed video: {vid_most_views}\nCount: {max_view_count}")
        context["most_popular_vid"] = vid_most_views
        context["most_popular_vid_count"] = max_view_count

        print(f"\Least viewed video: {vid_least_views}\nCount: {min_view_count}")
        context["least_popular_vid"] = vid_least_views
        context["least_popular_vid_count"] = min_view_count

        #print(f"\nAverage Video View Count: {int(avg_views/vid_count)}")
        print(f"\Mean Video View Count: {mean_view_count}")
        context["mean_vid_views"] = mean_view_count

        print(f"\Median Video View Count: {median_view_count}")
        context["median_vid_views"] = median_view_count

        #time = convert_secs_to_h_m_s(int(total_duration/vid_count))
        time = convert_secs_to_h_m_s(mean_duration)
        print(f'\Mean video duration: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')

        context["mean_duration_graph"] = round(mean_duration/60, 2)
        context["median_duration_graph"] = round(median_duration/60, 2)
        
        time = convert_secs_to_h_m_s(max_duration)
        print(f'\nLongest Video : {vid_max_duration}\nDuration: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')

        context["longest_h"] = time["Hours"]
        context["longest_m"] = time["Mins"]
        context["longest_s"] = time["Secs"]
        context["longest_duration_graph"] = round(max_duration/60, 2)
        context["longest_vid"] = vid_max_duration

        time = convert_secs_to_h_m_s(min_duration)
        print(f'\Shortest Video : {vid_min_duration}\nDuration: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')

        context["shortest_h"] = time["Hours"]
        context["shortest_m"] = time["Mins"]
        context["shortest_s"] = time["Secs"]
        context["shortest_duration_graph"] = round(min_duration/60, 2)
        context["shortest_vid"] = vid_min_duration

        avg_like_percentage = round(avg_like_percentage / vid_count, 2)
        print(f'\nAverage Like Percentage: {avg_like_percentage}')

        context["avg_like_percent"] = avg_like_percentage
        context["avg_dislike_percent"] = 100 - avg_like_percentage
    return render(request, 'youtube_playlist_analyzer/index.html', context)

def search(request):
    context = dict()
    vid_durations = dict()
    vid_viewcounts = dict()
    if 'search' in request.GET:
        playlist_url = request.GET['search']
        playlist_id = playlist_url.split("playlist?list=")[1]
        youtube_obj = build("youtube", "v3", developerKey=YT_API_KEY)
        # Get YouTube Playlist name, channel name
        playlist_details = basic_playlist_details(playlist_id, youtube_obj)
        print(f"\nPlaylist Title: {playlist_details['Playlist_Title']}\nChannel title: {playlist_details['Channel_Title']}\n")

        context["Playlist_Title"] = playlist_details['Playlist_Title']
        context["Channel_Title"] = playlist_details['Channel_Title']
        # Get all the video IDs which are part of the playlist
        vid_ids = get_vid_ids_from_playlist(playlist_id, youtube_obj)
        vid_details = get_vid_details(vid_ids, youtube_obj)
        # Get the duration of each of the videos given the video ID
        hours = 0
        mins = 0
        seconds = 0
        total_duration = 0
        count = 1
        #print("\n\nVideos in playlist:")
        #print(f"\nPlaylist has {len(vid_details)} videos listed below:\n")
        shortest_vid = dict()
        longest_vid = dict()
        shortest_vid_duration = 999999
        shortest_vid = ""
        longest_vid_duration = -999999
        longest_vid = ""
        most_popular_vid = ""
        most_popular_view_count = 0
        avg_views = 0
        avg_like_percentage = 0.0
        for title, stats in vid_details.items():
            like_percentage = 0.0
            time_count = 0
            duration = stats["Duration"]
            views = stats["Views"]
            likes = stats["Likes"]
            dislikes = stats["Dislikes"]
            like_percentage = round(int(likes)/(int(likes) + int(dislikes)) * 100, 2)
            avg_like_percentage += like_percentage 
            if int(views) > most_popular_view_count:
                most_popular_view_count = int(views)
                most_popular_vid = title
            avg_views += int(views)
            print(f"\n{count}. Title: {title}\nDuration: {duration}\nViews: {views}\nLikes: {likes}\nDislikes: {dislikes}")
            count += 1
            if "H" in duration:
                hours = int(duration.split("H")[0])
                time_count = 3600 * hours
                duration = duration.split("H")[1]
            if "M" in duration:
                mins = int(duration.split("M")[0])
                time_count += 60 * mins
                duration = duration.split("M")[1]
            if "S" in duration:
                seconds = int(duration.split("S")[0])
                time_count += seconds
            if time_count < shortest_vid_duration:
                shortest_vid_duration = time_count
                shortest_vid = title
            if time_count > longest_vid_duration:
                longest_vid_duration = time_count
                longest_vid = title
            vid_durations[time_count] = title
            vid_viewcounts[int(views)] = title
            total_duration += time_count
        list_durations = vid_durations.keys()
        list_viewcounts = vid_viewcounts.keys()
        
        min_view_count = min(list_viewcounts)
        max_view_count = max(list_viewcounts)
        median_view_count = statistics.median(list_viewcounts)
        mean_view_count = statistics.mean(list_viewcounts)
        min_duration = min(list_durations)
        max_duration = max(list_durations)
        median_duration = statistics.median(list_durations)
        mean_duration = statistics.mean(list_durations)
        for viewCount, vidTitle in vid_viewcounts.items():
            if viewCount == max_view_count:
                vid_most_views = vidTitle
            if viewCount == min_view_count:
                vid_least_views = vidTitle
        for durationCount, vidTitle in vid_durations.items():
            if durationCount == max_duration:
                vid_max_duration = vidTitle
            if durationCount == min_duration:
                vid_min_duration = vidTitle
        #print(f"Duration in seconds: {total_duration}\n")
        vid_count = len(vid_details)
        context["vid_count"] = vid_count
        print(f"\nPlaylist has {vid_count} videos\n")
        time = convert_secs_to_h_m_s(total_duration)
        print(f'\nTotal duration of playlist: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')
        context["total_h"] = time["Hours"]
        context["total_m"] = time["Mins"]
        context["total_s"] = time["Secs"]
        
        print(f"\nMost viewed video: {vid_most_views}\nCount: {max_view_count}")
        context["most_popular_vid"] = vid_most_views
        context["most_popular_vid_count"] = max_view_count

        print(f"\Least viewed video: {vid_least_views}\nCount: {min_view_count}")
        context["least_popular_vid"] = vid_least_views
        context["least_popular_vid_count"] = min_view_count

        #print(f"\nAverage Video View Count: {int(avg_views/vid_count)}")
        print(f"\Mean Video View Count: {mean_view_count}")
        context["mean_vid_views"] = mean_view_count

        print(f"\Median Video View Count: {median_view_count}")
        context["median_vid_views"] = median_view_count

        #time = convert_secs_to_h_m_s(int(total_duration/vid_count))
        time = convert_secs_to_h_m_s(mean_duration)
        print(f'\Mean video duration: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')

        context["mean_duration_graph"] = int(mean_duration/60)
        context["median_duration_graph"] = int(median_duration/60)
        
        time = convert_secs_to_h_m_s(max_duration)
        print(f'\nLongest Video : {vid_max_duration}\nDuration: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')

        context["longest_h"] = time["Hours"]
        context["longest_m"] = time["Mins"]
        context["longest_s"] = time["Secs"]
        context["longest_duration_graph"] = int(max_duration/60)
        context["longest_vid"] = vid_max_duration

        time = convert_secs_to_h_m_s(min_duration)
        print(f'\Shortest Video : {vid_min_duration}\nDuration: {time["Hours"]} hours, {time["Mins"]} mins, {time["Secs"]} secs')

        context["shortest_h"] = time["Hours"]
        context["shortest_m"] = time["Mins"]
        context["shortest_s"] = time["Secs"]
        context["shortest_duration_graph"] = int(min_duration/60)
        context["shortest_vid"] = vid_min_duration

        avg_like_percentage = round(avg_like_percentage / vid_count, 2)
        print(f'\nAverage Like Percentage: {avg_like_percentage}')

        context["avg_like_percent"] = avg_like_percentage
        context["avg_dislike_percent"] = 100 - avg_like_percentage
    return render(request, 'youtube_playlist_analyzer/search.html', context)