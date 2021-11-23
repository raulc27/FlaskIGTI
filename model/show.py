from data import alchemy
from . import episodes

class ShowModel(alchemy.Model):
    __tablename__ = 'shows'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(80))


    episodes = alchemy.relationship(episodes.EpisodeModel, lazy='dynamic')

    def __init__(self, name):
        self.name = name
    
    def json(self):
        return {'id':self.id, 'name':self.name, 'episodes':[]}

    def save_to_db(self):
        alchemy.session.add(self)
        alchemy.session.commit()

    @classmethod
    def find_by_name(cls, name):
        cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,name):
        cls.query.filter_by(id=id).first()