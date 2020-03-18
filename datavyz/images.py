import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from datavyz.dependencies import *

from skimage import color, io

def load(image_path):

    img = color.rgb2gray(io.imread(image_path))
    
    return np.rot90(np.array(img), k=3) # needs rotation


if __name__=='__main__':


    from datavyz.main import graph_env
    ge = graph_env('visual_stim')
    ge.image(load(sys.argv[-1]))
    ge.matrix(load(sys.argv[-1]))
    ge.show()
    
