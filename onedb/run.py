from app import *
from app.models import Experiment, User, Metric
import sqlalchemy as sa
import random
import string

class Run():
    def __init__(self, username: str, project: str, name: str = None,) -> None:
        with app.app_context():
            user = db.first_or_404(sa.select(User).where(User.username == username))
            experiment = Experiment(project=project, name=name, user_id = user.id)
            if name is None:
                name = self._get_random_name()
            db.session.add(experiment)
            db.session.commit()
            self.experiment = db.first_or_404(sa.select(Experiment).where(Experiment.name == name))

    def log(self, values: dict):
        with app.app_context():
            for key in values:
                metric = Metric(metric=key, value = values[key], experiment_id=self.experiment.id)
                db.session.add(metric)
                db.session.commit()

    def _get_random_name(name_len=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=name_len))