from app import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    classification = db.Column(db.String(64), unique=False)

    def __repr__(self):
        return '<Ingredient {} is {}>'.format(self.name, self.classification)
