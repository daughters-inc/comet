import os
import googleapiclient.discovery
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification


class YSCA:
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")

    def __init__(self, video_id):
        self.video_id = video_id

    @staticmethod
    def _extract_comment(item):
        return item.get("textOriginal")

    def _sentiment_analysis(self, comment, analysis_list):
        try:
            classifier = pipeline('sentiment-analysis', tokenizer=self.tokenizer, model=self.model)
            result = classifier(comment)[0]
            result["comment"] = comment
            # This feels very hacky... come up with a better one
            result["rating"] = int(list(filter(str.isdigit, result["label"]))[0])
            del result["label"]
            analysis_list.append(result)
        except RuntimeError:
            analysis_list.append({"error": "Exceeded the maximum number of tokens.", "comment": comment})
            pass

    def analyze(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = os.environ.get("youtubeapikey")

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY, cache_discovery=False)

        request = youtube.commentThreads().list(
            part="id,snippet,replies",
            videoId=self.video_id,
            max_results=100
        )
        response = request.execute()
        items = response.get("items")
        result = list()
        for item in items:
            if item.get("replies"):
                for i in item.get("replies").get("comments"):
                    comment = self._extract_comment(i.get("snippet"))
                    self._sentiment_analysis(comment, result)
            comment = self._extract_comment(item.get("snippet").get("topLevelComment").get("snippet"))
            self._sentiment_analysis(comment, result)
        return result

    def pretty(self):
        result = self.analyze()
        sum = int()
        for i in result:
            if i.get("rating"):
                sum += i.get("rating")
        return sum / len(result)
