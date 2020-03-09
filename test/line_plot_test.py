import numpy as np

from datavyz.main import graph_env
ge = graph_env('screen')

fig, ax = ge.plot(Y=np.random.randn(4, 10),
	          sY=np.random.randn(4, 10),
                  xlabel='xlabel (xunit)',
                  ylabel='ylabel (yunit)',
                  title='datavyz demo plot')
fig.savefig('docs/demo.svg')
ge.show()
