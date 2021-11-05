import os
from .utils import parse_json,parse_txt
from . import items
import numpy as np

items_dict = {
    'basedataitem':'BaseDataItem',
    'linedataitem':'LineDataItem',
    'histdataitem':'HistDataItem',
    'base':'BaseDataItem',
    'line':'LineDataItem',
    'histogram':'HistDataItem'
}
def loaditem(path,itemtype,colors=None, markers=None, mcolors=None):
    """Parse data file in txt or json format.
        This function is used to load data for "line","histogram" and "surface" picture.
    """
    filetype = os.path.splitext(path)[-1][1:]

    if filetype == 'txt':
        rets = parse_txt(path, colors, markers, mcolors)
    elif filetype == 'json':
        rets = parse_json(path, colors, markers, mcolors)
    
    return getattr(items,items_dict[itemtype.lower()]).from_dict(rets)

def loadtsnedata(path):
    """This function if used to load data for "T-SNE" 
    The data struction must be as follow：
    data = {
        'domain1':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        'domain2':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        'domain3':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        ……
    }
    You can change the 'domainX','embeds','label1','label2' to other key.
    """
    assert os.path.exists(path), 'Please input valide path!'
    assert os.path.splitext(path)[-1] == '.npy', 'The file type must be ".npy" type'
    datas = np.load(path,allow_pickle=True).item()
    return datas