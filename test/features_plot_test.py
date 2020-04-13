from datavyz import graph_env

ge = graph_env('screen')

import numpy as np
ge.plot(Y=np.random.randn(4, 10),sY=np.random.randn(4, 10),
        xlabel='xlabel (xunit)', ylabel='ylabel (yunit)',
        title='datavyz demo plot')

ge.show()
