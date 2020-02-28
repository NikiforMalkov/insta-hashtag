class Link(object):
    def __init__(self, link):
        self.link = link

    def __repr__(self):
        return "<Link ('%s')>" % self.link

    def __str__(self):
        return "<Link ('%s')>" % self.link
