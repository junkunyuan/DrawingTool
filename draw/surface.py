import sys
sys.path.append('..')
from lib.color import *
from tool.util import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy import interpolate

from lib.dataloader import loaditem
from tool.util import loadcfg
font_config = {
    'font.family': ['Times New Roman']
}
rcParams.update(font_config)
 

def draw(dataitems,cfg,savename=None,contourf=False,colorbar=True,interp2d=True):
    fig = plt.figure(figsize=cfg['figsize'])
    ax = fig.add_subplot(111,projection='3d')
    item = dataitems[0]  # draw one figure
    cmap = getcmp(cfg['cmap'])

    data = np.array(item.data)
    xval,yval = cfg['xval'],cfg['yval']
    assert len(xval) * len(yval) == data.shape[0], 'number of data != len(x) * len(y)'
    data = np.reshape(data,(len(xval),len(yval)))

    if interp2d:  # if use interpolation
        f = interpolate.interp2d(xval,yval,data,kind=cfg['interp2d']['kind'])
        xval = np.linspace(xval[0],xval[-1],cfg['interp2d']['xnew'])
        yval = np.linspace(yval[0],yval[-1],cfg['interp2d']['ynew'])
        data = f(xval,yval)

    xval,yval = np.meshgrid(xval,yval)

    surf = ax.plot_surface(xval,yval,data,cmap=cmap)  # draw surface
    if contourf:  # if draw projection
        ccmap = cmap if cfg['contourf']['cmap'] is None else getcmp(cfg['contourf']['cmap'])
        ax.contourf(xval, yval, data, zdir='z', offset=cfg['contourf']['offset'],cmap=ccmap)
    if colorbar:  # if add colorbar
        fig.colorbar(surf, shrink=0.8)

    if ('title' in cfg) and ('title' != None):  # set title
        ax.set_title(cfg['title'], size = cfg['title_size'])
    ax.set_xlabel(cfg['xlabel'],size=cfg['xl_size'])  # set xlabel
    ax.set_ylabel(cfg['ylabel'],size=cfg['yl_size'])  # set ylabel
    ax.set_zlabel(cfg['zlabel'],size=cfg['zl_size'])  # set zlabel

    if cfg['tick']['x']:
        ax.set_xticks(cfg['tick']['x'])  # set xticks
    if cfg['tick']['y']:
        ax.set_yticks(cfg['tick']['y'])  # set yticks
    ax.set_zticks(cfg['tick']['z']) 
    if 'zlim' in cfg:  # set zticks
        ax.set_zlim(*cfg['zlim'])

    ax.tick_params(**cfg['tick_params'])  # set ticks labelsize
    ax.w_xaxis.set_pane_color(cfg['pane_color']['x'])  # set x background color
    ax.w_yaxis.set_pane_color(cfg['pane_color']['y'])  # set y background color


    savename = cfg['title'] if savename is None else savename
    plt.savefig('{}.pdf'.format(savename), bbox_inches='tight')

if __name__ == '__main__':
    dataitems = loaditem('../data/3d.json', 'base')

    cfg = loadcfg('../configs/surface.yaml')

    dataitems[0].data = dataitems[0].data * 200 + 80

    cfg['title'] = '3D figure'

    # set z ruler
    if cfg['tick']['z'] is None:
        cfg['tick']['z'] = init_yticks(dataitems, interval=2, low=5, up=0)

    z = cfg['tick']['z'][1] - cfg['tick']['z'][0]
    # set z_lim
    cfg['zlim'] = [cfg['tick']['z'][0] - z,cfg['tick']['z'][-1] + z]
    # set z projection location
    cfg['contourf']['offset'] = cfg['tick']['z'][0] - z/2  

    # Draw figure.
    draw(dataitems,cfg,savename='../test2', contourf=True, interp2d=True)
