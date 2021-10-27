import sys
sys.path.append('..')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from datas import loaditem
from color import *
from util import *
font_config = {
    'font.family': ['Times New Roman']
}
rcParams.update(font_config)


def draw(dataitems, cfg, savename=None, usevar=True, usemk=True):
    """
    Draw line char.
    Args:
        dataitems ([type]): data items.
        cfg ([str]): config file.
        savename (str, optional): the file name of the generated figure. Default: './out'.
        usevar (bool, optional): draw variance. Default: True.
    """
    _, ax = plt.subplots(1, 1, figsize=cfg['figsize'])
    uvar = use_var(dataitems) and usevar
    for item in dataitems:
        data = np.array(item.data)
        if uvar:
            var = np.array(item.var)
            ax.fill_between(cfg['xticks'], data, data + var, color = item.color, alpha = cfg['ax']['alpha'])
            ax.fill_between(cfg['xticks'], data - var, data, color = item.color, alpha = cfg['ax']['alpha'])
        if usemk:
            ax.plot(cfg['xticks'], data, color = item.color, lw = cfg['ax']['lw'], label="{}".format(item.name), marker=item.marker,
                    markersize=cfg['ax']['markersize'], markerfacecolor = item.mcolor, markeredgecolor =  item.mcolor)
        else:
            ax.plot(cfg['xticks'], data, color = item.color, lw = cfg['ax']['lw'], label = "{}".format(item.name))
    if ('title' in cfg) and ('title' != None):
        ax.set_title(cfg['title'], size = cfg['title_size'])
    plt.xticks(cfg['xticks'])
    plt.yticks(cfg['yticks'])
    ax.set_xlabel(cfg['xlabel'], size = cfg['xl_size'])
    ax.set_ylabel(cfg['ylabel'], size = cfg['yl_size'])
    ax.tick_params(**cfg['ax']['tick_params'])
    ax.grid(**cfg['grid'])
    # ax.set_xlim()
    y_int = cfg['yticks'][1] - cfg['yticks'][0]
    ax.set_ylim(min(cfg['yticks']) - y_int / 2, max(cfg['yticks']) + y_int / 2)
    plt.legend(**cfg['legend'])
    savename = cfg['title'] if savename is None else savename
    plt.savefig('{}.pdf'.format(savename), bbox_inches='tight')
    # plt.savefig('{}.jpg'.format(savename), bbox_inches='tight')


if __name__ == '__main__':
    # Load data with paras [data_path, line color, marker, marker color].
    dataitems = loaditem(
        path='../data/data.json',
        itemtype='line',
        colors=colors1, 
        markers=markers, 
        mcolors=colors1)
    
    # Load configure.
    cfg = loadcfg('../configs/line.yaml')

    # Set figure title.
    cfg['title'] = None

    # Set yticks.
    if cfg['yticks'] is None:
        cfg['yticks'] = init_yticks(dataitems, interval=2, low=0, up=0)

    # Draw figure.
    draw(dataitems, cfg, savename='../home-act-avg', usevar=True)       
   