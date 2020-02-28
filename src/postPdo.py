from src.post import Post


class PostPdo(object):

    def __init__(self, session):
        self.session = session

    # TODO: более объектынй подход
    def add_post(self, login, comment, image_url, link, date):
        test_post = Post(str(login), str(comment), str(image_url), str(link), str(date))
        print("Add new post")
        print(repr(test_post))
        self.session.add(test_post)
        self.session.commit()

    def get_post(self, comment):
        post = self.session.query(Post).filter_by(comment=comment).first()
        print("print post to console")
        print(repr(post))

    def one_by_id(self, post_id):
        post = self.session.query(Post).filter_by(id=str(post_id)).first()
        print("print one post by id to console")
        print(repr(post))

    def one_by_link(self, link):
        post = self.session.query(Post).filter_by(link=str(link)).first()
        return post
