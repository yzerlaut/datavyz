ENVIRONMENTS = {
    'manuscript': {
	'fontsize':9,
	'default_color':'k',
        'single_plot_size':(28., 20.), # mm
        'hspace_size':12., # mm
        'wspace_size':16., # mm
        'left_size':20., # mm
        'right_size':4., # mm
        'top_size':5., # mm
        'bottom_size':19., # mm
    },
    'screen': {
        'size_factor': 1.5,
    },
    'wide_screen': {
	'fontsize':12,
	'default_color':'k',
        'single_plot_size':(200.*16./9., 200.), # mm
        'hspace_size':1., # mm
        'wspace_size':1., # mm
        'left_size':1., # mm
        'right_size':1., # mm
        'top_size':1., # mm
        'bottom_size':1., # mm
    }
}

def set_env_variables(cls, key):

    if 'size_factor' in ENVIRONMENTS[key]:
        size_factor = ENVIRONMENTS[key]['size_factor']
        ENVIRONMENTS[key] = ENVIRONMENTS['manuscript']
    else:
        size_factor = 1.
        
    cls.FONTSIZE = size_factor*ENVIRONMENTS[key]['fontsize']
    cls.default_color = ENVIRONMENTS[key]['default_color']
    cls.single_plot_size = [s*size_factor for s in ENVIRONMENTS[key]['single_plot_size']]
    cls.hspace_size = size_factor*ENVIRONMENTS[key]['hspace_size']
    cls.wspace_size = size_factor*ENVIRONMENTS[key]['wspace_size']
    cls.left_size = size_factor*ENVIRONMENTS[key]['left_size']
    cls.right_size = size_factor*ENVIRONMENTS[key]['right_size']
    cls.top_size = size_factor*ENVIRONMENTS[key]['top_size']
    cls.bottom_size = size_factor*ENVIRONMENTS[key]['bottom_size']
    
           
if __name__=='__main__':

    from datavyz.main import graph_env
    ge = graph_env('wide_screen')

    fig, _ = ge.figure()
    ge.show()
