import datavyz
ge = datavyz.graph_env('screen')

ge.plot(Y=np.random.randn(4, 10),
	sY=np.random.randn(4, 10),
        xlabel='xlabel (xunit)',
        ylabel='ylabel (yunit)',
        title='datavyz demo plot')

ge.show()
