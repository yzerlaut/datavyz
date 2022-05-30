from datavyz import graph_env
import numpy as np

ge = graph_env('screen')

fig, AX = ge.figure(axes_extents=[\
                                 [[3,2], [1,2] ],
                                 [[1,1], [1,1], [2,1] ] ],
                 # left=.3, bottom=.4, hspace=1.4, wspace=1.2,
                 figsize=[1,1])

ge.plot(Y=[
    np.random.randn(20),
    np.random.randn(20),
    np.random.randn(20),
    np.random.randn(20)],
     sY=[
         np.ones(20),
         np.ones(20),
         np.random.randn(20),
         np.random.randn(20)],
     ax=AX[0][0],
     COLORS=[ge.red, ge.purple, ge.blue, ge.green],
     legend_args={'frameon':False},
     ylabel='value (v)',
     axes_args={'spines':['left']})

ge.scatter(X=np.random.randn(4,5), Y=np.random.randn(4,5),
        sX=np.random.randn(4,5),sY=np.random.randn(4,5),
        ax=AX[1][0],
        bar_legend_args={},
        bar_label='condition')

ge.plot(np.random.randn(20), sy=np.random.randn(20),
     ax=AX[1][2])
ge.scatter(np.random.randn(20), sy=np.random.randn(20),
        ax=AX[1][2])
ge.plot(np.random.randn(20), sy=np.random.randn(20),
        ax=AX[1][2], color=ge.red)
ge.scatter(np.random.randn(20), sy=np.random.randn(20),
        ax=AX[1][2], color=ge.red)
ge.plot(np.sin(np.linspace(0,1,30)*3*np.pi)*2,
     ax=AX[1][2], color=ge.purple)
ge.plot(np.cos(np.linspace(0,1,30)*3*np.pi)*2,
     ax=AX[1][2], color=ge.green)

ge.hist(np.random.randn(200), ax=AX[0][1],\
     orientation='vertical',
     axes_args={'ylim':AX[0][0].get_ylim(), 'spines':['left']})

AX[1][1].axis('off')
ge.show()
