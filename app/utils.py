import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy as sa
from app.models import User, Experiment, Metric
from app import *
import plotly
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

def get_project_names(db, username):
    with app.app_context():
        user = db.session.scalar(
                sa.select(User).where(User.username == username))
        projects = set(db.session.scalars(sa.select(Experiment.project).where(Experiment.user_id == user.id)).all())
        return projects

def get_runs(db, username, project):
    with app.app_context():
        user = db.session.scalar(
                    sa.select(User).where(User.username == username))
        runs = db.session.scalars(sa.select(Experiment).where(Experiment.user_id == user.id).where(Experiment.project == project)).all()
        # for run in runs:
        #     print(run.name, run.project)
        return runs

def make_image(db, runs):
    if runs == []:
        plt.clf()
        plt.savefig("app/static/images/plots.png")
        # fig = px.scatter(x=range(10), y=range(10))
        # fig.write_html("graph.html")
        return

    logs = {}
    for run in runs:
        with app.app_context():
            metrics = set(db.session.scalars(sa.select(Metric.metric).where(Metric.experiment_id==run.id)).all())
            for metric in metrics:
                values = db.session.scalars(sa.select(Metric.value).where(Metric.experiment_id==run.id).where(Metric.metric==metric)).all()
                logs[(run.id, metric)] = values
            # keys = db.keys(_make_name(project, run))
            # _, _, a = _split_names(keys)
            # logs += a
    # logs = list(set(logs))
    nrows = (len(metrics) + 1) // 2
    
    # plt.clf()
    cmap = plt.get_cmap('plasma')
    cmap_arr = cmap(np.linspace(0, 1, len(runs)))
    plt.figure(figsize=(15, 5 * nrows))
    for i, metric in enumerate(metrics):
        plt.subplot(nrows, 2, i + 1)
        plt.tight_layout()
        for j, run in enumerate(runs):
            # values = list(map(float, db.lrange(_make_name(project, run, log), 0, -1)))
            if (run.id, metric) in logs.keys():
                values = logs[(run.id, metric)]
                if values != []:
                    plt.plot(values, label=run.name, c=cmap_arr[j])
                    fig = px.scatter(x=range(10), y=range(10))
                    fig.write_html("app/static/images/graph.html")
        plt.title(metric)
        plt.legend()
    plt.savefig("app/static/images/plots.png")
    # plt.show()
    pass

# def _make_name(project, run = None, log = None):
#     if run is None:
#         return project + ':*'
#     if log is None:
#         return project + ':' + run + ':*'
#     return project + ':' + run + ':' + log
