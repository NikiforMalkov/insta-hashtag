# TODO: возможно стоит вынести в отдельный пакет
class Post(object):
    def __init__(self, login, description, image_url, link, date):
        self.description = description
        self.image_url = image_url
        self.link = link
        self.date = date
        self.login = login

    def __repr__(self):
        return "<Post('%s', '%s','%s', '%s', '%s')>" % (self.login, self.description, self.image_url, self.link, self.date)

    def __str__(self):
        return "<Post('%s', '%s','%s', '%s', '%s')>" % (self.login, self.description, self.image_url, self.link, self.date)
