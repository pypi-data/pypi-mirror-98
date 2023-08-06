import pr0gramm

# this is a higher level api interface for simplified usage of the api


class Pr0gramm:
    def __init__(self, username="", password=""):
        self.api = pr0gramm.Api(username, password)
