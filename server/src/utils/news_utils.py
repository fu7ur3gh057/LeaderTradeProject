from urllib.parse import urlparse, parse_qs


def get_youtube_id(url):
    if url:
        if "v=" in url:
            return parse_qs(urlparse(url).query)["v"][0]
        if "embed/" in url:
            return urlparse(url).path.split("embed/")[1]
        if "shorts/" in url:
            return urlparse(url).path.split("/shorts/")[1]


def video_thumbnail(video_id):
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    return None


def get_embed_video_link(video_id):
    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return ""
