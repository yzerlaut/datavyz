import numpy as np
from skimage import color, io
from matplotlib.cm import binary_r

# # image plot
def image(self, X, cmap=binary_r, alpha=1., ax=None, title=''):
    if ax is None:
        fig, ax = self.figure()
    else:
        fig = plt.gcf()
    ax.imshow(X.T, cmap=cmap, alpha=alpha,
              interpolation=None,
              origin='lower',
              aspect='equal')
    ax.axis('off')
    if title!='':
        self.title(ax, title)
    return fig, ax

def load(image_path):

    img = color.rgb2gray(io.imread(image_path))
    
    return np.rot90(np.array(img), k=3) # needs rotation


if __name__=='__main__':


    import sys
    sys.path.append('./')
    from datavyz import graph_env

    ge = graph_env('visual_stim')
    ge.image(load(sys.argv[-1]))
    ge.matrix(load(sys.argv[-1]))
    ge.show()
    
