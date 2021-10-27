import sys
sys.path.append('..')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from datas import loaditem
from color import *
from util import *
plt.subplots()
font_config = {
    'font.family': ['Times New Roman']
}
rcParams.update(font_config)


def draw(dataitems, cfg, savename=None):
    ylims = cfg['ylims']

    x = np.arange(len(cfg['labels']))
    total_width, n = 0.9, len(cfg['labels'])
    width = total_width/n
    x = x-(total_width-width)/2
    fig, ax = plt.subplots(1, 1, figsize=cfg['figsize'])

    for i, item in enumerate(dataitems):
        ax.bar(x+width*i, item.data, width=width-0.01, label=item.name, color=item.color)
        for x1, y in zip(x, item.data):
            ax.text(x1+width*i, y+0.05, '%.2f' % y, ha='center', va='bottom', size=cfg['ax']['textsize'])

    if 'title' in cfg:
        ax.set_title(cfg['title'], size=cfg['title_size'])
    plt.ylim(*ylims)
    plt.xlabel(cfg['xlabel'], size=cfg['xl_size'])
    plt.ylabel(cfg['ylabel'], size=cfg['yl_size'])
    plt.xticks(np.arange(len(cfg['labels'])), cfg['labels'])

    ax.grid(**cfg['grid'])
    ax.spines['right'].set_visible(False)       # right bound transparency
    ax.spines['top'].set_visible(False)         # upper bound transparency
    ax.tick_params(**cfg['ax']['tick_params'])
    
    plt.legend(**cfg['legend'])
    savename = cfg['title'] if savename is None else savename
    plt.savefig('{}.pdf'.format(savename), bbox_inches='tight')


if __name__ == '__main__':
    # Load data.
    dataitems = loaditem('../data/data.json','histogram', colors1)
    
    # Load config.
    cfg = loadcfg('../configs/histogram.yaml')
    
    # Set title.
    cfg['title'] = 'Accuracy on PACS'
    # Set ylims.
    cfg['ylims'] = mm_datas(dataitems)             

    # Draw figure.
    draw(dataitems, cfg,savename='../histogram')    
