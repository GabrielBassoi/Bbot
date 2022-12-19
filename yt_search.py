from youtube_search import YoutubeSearch


class SearchYt():

    def __init__(self):
        super.__init__(self)

    def search(text):
        results = YoutubeSearch(text, max_results=1).to_dict()
        return "http://www.youtube.com" + results[0]["url_suffix"]
