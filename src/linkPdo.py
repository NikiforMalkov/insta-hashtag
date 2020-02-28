from src.link import Link


class LinkPdo(object):

    def __init__(self, session):
        self.session = session

    # TODO: более объектынй подход
    def get_all(self):
        link_collection = self.session.query(Link)
        return link_collection
        # print("print post to console")
        # print(repr(post))
