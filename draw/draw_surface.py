import sys
sys.path.append('..')
from color import *
from util import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy import interpolate

from datas import loaditem
from util import loadcfg
font_config = {
    'font.family': ['Times New Roman']
}
rcParams.update(font_config)
 

def draw(dataitems,cfg,savename=None,contourf=False,colorbar=True,interp2d=True):
    fig = plt.figure(figsize=cfg['figsize'])
    ax = fig.add_subplot(111,projection='3d')
    item = dataitems[0]                                             # 画敏感性分析的图只画一个
    cmap = getcmp(cfg['cmap'])

    data = np.array(item.data)
    xval,yval = cfg['xval'],cfg['yval']
    assert len(xval) * len(yval) == data.shape[0], 'number of data != len(x) * len(y)'
    data = np.reshape(data,(len(xval),len(yval)))

    if interp2d:                                                    # 如果使用插值就插值
        f = interpolate.interp2d(xval,yval,data,kind=cfg['interp2d']['kind'])
        xval = np.linspace(xval[0],xval[-1],cfg['interp2d']['xnew'])
        yval = np.linspace(yval[0],yval[-1],cfg['interp2d']['ynew'])
        data = f(xval,yval)

    xval,yval = np.meshgrid(xval,yval)


    surf = ax.plot_surface(xval,yval,data,cmap=cmap)                                                            # 画3D图
    if contourf:                                                                                                # 画映射面
        ccmap = cmap if cfg['contourf']['cmap'] is None else getcmp(cfg['contourf']['cmap'])
        ax.contourf(xval, yval, data, zdir='z', offset=cfg['contourf']['offset'],cmap=ccmap)
    if colorbar:
        fig.colorbar(surf, shrink=0.8)                                                                          # 在右边加个渐变条

    if ('title' in cfg) and ('title' != None):                                                                  # 设置title
        ax.set_title(cfg['title'], size = cfg['title_size'])
    ax.set_xlabel(cfg['xlabel'],size=cfg['xl_size'])                                                            # 设置xlabel
    ax.set_ylabel(cfg['ylabel'],size=cfg['yl_size'])                                                            # 设置ylabel
    ax.set_zlabel(cfg['zlabel'],size=cfg['zl_size'])                                                            # 设置zlabel

    if cfg['tick']['x']:
        ax.set_xticks(cfg['tick']['x'])                                                                         # 设置x轴数值展现刻度
    if cfg['tick']['y']:
        ax.set_yticks(cfg['tick']['y'])                                                                         # 设置y轴数值展现刻度
    ax.set_zticks(cfg['tick']['z']) 
    if 'zlim' in cfg:                                                            # 设置z轴数值展现刻度
        ax.set_zlim(*cfg['zlim'])

    ax.tick_params(**cfg['tick_params'])                                                                        # 设置ticks的labelsize
    ax.w_xaxis.set_pane_color(cfg['pane_color']['x'])                                                           # 设置x背景颜色
    ax.w_yaxis.set_pane_color(cfg['pane_color']['y'])                                                           # 设置y轴背景颜色


    savename = cfg['title'] if savename is None else savename
    plt.savefig('{}.pdf'.format(savename), bbox_inches='tight')

if __name__ == '__main__':
    dataitems = loaditem('../data/3d.json','base')

    cfg = loadcfg('../configs/surface.yaml')

    dataitems[0].data = dataitems[0].data * 200 + 80

    cfg['title'] = '3D figure'

    if cfg['tick']['z'] is None:                                                # 设置z轴可视化刻度
        cfg['tick']['z'] = init_yticks(dataitems, interval=2, low=5, up=0)

    z = cfg['tick']['z'][1]-cfg['tick']['z'][0]
    cfg['zlim'] = [cfg['tick']['z'][0]-z,cfg['tick']['z'][-1]+z]        # 设置z轴范围
    cfg['contourf']['offset'] = cfg['tick']['z'][0]-z/2                     # 设置映射平面展示的z轴坐标，必须比zlim的下界高，不然就看不到了

    draw(dataitems,cfg,savename='../test',contourf=True,interp2d=False)