import os
from .utils import parse_json,parse_txt
from . import items
items_dict = {
    'basedataitem':'BaseDataItem',
    'linedataitem':'LineDataItem',
    'histdataitem':'HistDataItem',
    'base':'BaseDataItem',
    'line':'LineDataItem',
    'histogram':'HistDataItem'
}
def loaditem(path,itemtype,colors=None, markers=None, mcolors=None):
    """Parse data file in txt or json format."""
    filetype = os.path.splitext(path)[-1][1:]

    if filetype == 'txt':
        rets = parse_txt(path, colors, markers, mcolors)
    elif filetype == 'json':
        rets = parse_json(path, colors, markers, mcolors)
    
    return getattr(items,items_dict[itemtype.lower()]).from_dict(rets)
