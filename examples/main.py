import numpy as np
from onedb.run import Run

if __name__ == '__main__':
    username='user3'
    # projects = ['project 1', 'proj', 'projector']
    projects = ['oneformer_user3']
    logs = ['loss', 'accuracy', 'reward']
    for proj in projects:
        for i in range(np.random.choice(np.arange(4, 10))):
            run = Run(username, project=proj, name='run' + str(i))
            for i in range(np.random.choice(np.arange(40, 60))):
                run.log({np.random.choice(logs): np.random.randint(0, 10)})