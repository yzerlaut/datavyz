import numpy as np

from datavyz import ge

fig, ax = ge.plot(Y=np.random.randn(4, 10),
	          sY=np.random.randn(4, 10),
                  xlabel='xlabel (xunit)',
                  ylabel='ylabel (yunit)',
                  title='datavyz demo plot')
ge.savefig(fig, 'docs/demo.png')
ge.show()
