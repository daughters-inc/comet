import os

import googleapiclient.discovery
from pororo import Pororo


def extract_comment(item):
    return item.get("textOriginal")


def sentiment_analysis(str):
    sentanal = Pororo(task="sentiment_analysis", lang="ko")
    result = sentanal(str, show_probs=True)
    return result


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get("youtubeapikey")

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet,replies",
        videoId="zinDxJqDgfI"
    )
    response = request.execute()
    items = response.get("items")
    comment_list = list()
    for item in items:
        if item.get("replies"):
            for i in item.get("replies").get("comments"):
                comment_list.append(extract_comment(i.get("snippet")))
        comment = item.get("snippet").get("topLevelComment").get("snippet")
        comment_list.append(extract_comment(comment))
    for cm in comment_list:
        sentanal = sentiment_analysis(cm)
        print(cm, sentanal)


if __name__ == "__main__":
    main()
