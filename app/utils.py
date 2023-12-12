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
        fig = go.Figure()
        fig_json = fig.to_json()

        template = """<div id='divPlotly'>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script>
    var plotly_data = {}
    Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
</script>
</div>"""

        with open('app/static/images/new_plot.html', 'w') as f:
            f.write(template.format(fig_json))
        pass

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
    nrows_fig = len(metrics) + 1
    
    # plt.clf()
    cmap = plt.get_cmap('plasma')
    cmap_arr = cmap(np.linspace(0, 1, len(runs)))
    titles = []
    for metric in metrics:
        titles.append(metric)
    fig = make_subplots(rows=nrows_fig, subplot_titles=titles)
    fig.update_layout(
        autosize=False,
        width=800,
        height=500 * nrows_fig,
        legend_tracegroupgap = 420
    )
    plt.figure(figsize=(15, 5 * nrows))
    for i, metric in enumerate(metrics):
        plt.subplot(nrows, 2, i + 1)
        plt.tight_layout()
        for j, run in enumerate(runs):
            # values = list(map(float, db.lrange(_make_name(project, run, log), 0, -1)))
            if (run.id, metric) in logs.keys():
                values = logs[(run.id, metric)]
                if values != []:
                    # x = [k for k in range(len(values))] #[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
                    fig.add_trace(
                        go.Scattergl(x=[k for k in range(len(values))], 
                                     y=values, name=run.name,
                                     legendgroup = str(i+1)), # lambda k: k in range(len(values))
                        row=i+1, col=1
                    )
                    plt.plot(values, label=run.name, c=cmap_arr[j])
                    # fig = px.scatter(x=range(10), y=range(10))
                    # fig.write_html("app/static/images/graph.html")
        plt.title(metric)
        plt.legend()
    plt.savefig("app/static/images/plots.png")
    # create a simple plot
    # bar = plotly.graph_objs.Bar(x=['giraffes', 'orangutans', 'monkeys'], 
    #                             y=[20, 14, 23])
    # layout = plotly.graph_objs.Layout()
    # fig = plotly.graph_objs.Figure([bar], layout)
    # convert it to JSON
    fig_json = fig.to_json()

    template = """<div id='divPlotly'>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        var plotly_data = {}
        Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
    </script>
</div>"""

    with open('app/static/images/new_plot.html', 'w') as f:
        f.write(template.format(fig_json))
    pass

# def _make_name(project, run = None, log = None):
#     if run is None:
#         return project + ':*'
#     if log is None:
#         return project + ':' + run + ':*'
#     return project + ':' + run + ':' + log
