from data import alchemy 

class EpisodeModel(alchemy.Model):
    __table__ = 'episode'

    id = alchemy.Column(alchemy.Integer, primary_key=True)
    name = alchemy.Column(alchemy.String(80))
    season = alchemy.Column(alchemy.Integer)

    show_id = alchemy.Column(alchemy.Integer, alchemy.ForeignKey('shows.id'))