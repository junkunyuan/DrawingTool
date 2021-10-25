import os
import numpy as np
import os
import json

__all__ = ['loaditem', 'markers', 'colors1', 'colors2', 'colors3']

red = ['#F08080', '#FF5510', '#FF0000']
blue = ['#56BCBC', '#00BFFF', '#6495ED', '#4169E1']
green = ['#3CB371', '#32CD32', '#009933', '#2E8B57']
purple = ['#9966CC']
yellow = ['#F4B183', '#FFA500', '#FF8C00', '#AA7700', '#D2691E']
grey = ['#696969']
black = ['#000000']

markers = ['.', 'P', '<', '^', '*', 'X', 'p', 'D']
colors1 = [black[0], blue[2], blue[0], green[2], purple[0], yellow[2], red[1]]
colors2 = ['#666666', green[1], '#369CFF', '#CC6600', '#FF6666', red[1]]
colors3 = [yellow[1], blue[1], green[3], red[0], yellow[1], blue[0]]


class DataItem():
    """Restructure the data."""
    def __init__(self, name, data, var, marker, color, mcolor=None) -> None:
        self.name = name

        assert (data is not None) and (not isinstance(data, (int, float, str)))
        self.data = data
        if isinstance(self.data, (list, tuple)):
            self.data = np.array(self.data)

        self.var = var
        if isinstance(self.var, (list, tuple)):
            self.var = np.array(self.var)

        self.marker = marker
        self.color = color
        self.mcolor = mcolor if mcolor is not None else self.color

    @property
    def max(self):
        return max(self.data)

    @property
    def min(self):
        return min(self.data)


def parse_txt(path, colors=None, markers=None, mcolors=None):
    dataitems = []
    with open(path, 'r', encoding='utf8') as f:
        contents = f.readlines()

    count = 0
    for line in contents:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        content = line.split('|')

        marker = content[3] if (len(content) > 3 and content[3] != '') else markers[count]
        color = content[4] if (len(content) > 4 and content[4] != '') else colors[count]
        mcolor = content[5] if (len(content) > 5 and content[5] != '') else mcolors[count]

        item = DataItem(name=content[0],
                        data=[float(i) for i in content[1].split(',')],
                        var=[float(i) for i in content[2].split(',')],
                        marker=marker,
                        color=color,
                        mcolor=mcolor
                        )
        dataitems.append(item)
        count += 1
        if count != 0:
            assert len(
                dataitems[-1].data) == len(dataitems[0].data), "The {}-th data number is different from the 1st data number, please check the data file.".format(count)

    return dataitems


def parse_json(path, colors=None, markers=None, mcolors=None):
    """Parse json file."""
    dataitems = []
    with open(path, 'r', encoding='utf-8') as f:
        contents = json.load(f)
    count = 0
    for _, item in contents.items():
        marker = item['marker'] if ('marker' in item and item['marker'] != '') else markers[count]
        color = item['color'] if ('color' in item and item['color'] != '') else colors[count]
        mcolor = item['mcolor'] if ('mcolor' in item and item['mcolor'] != '') else mcolors[count]
        var = item['var'] if 'var' in item else None
        data = [item['data']] if not isinstance(item['data'], list) else item['data']
        ditem = DataItem(
            name=item['name'],
            data=data,
            var=var,
            marker=marker,
            color=color,
            mcolor=mcolor
        )
        dataitems.append(ditem)
        count += 1
        if count != 0:
            assert len(
                dataitems[-1].data) == len(dataitems[0].data), "The {}-th data number is different from the 1st data number, please check the data file.".format(count)
    return dataitems


def loaditem(path, colors=None, markers=None, mcolors=None):
    """Parse data file in txt or json format."""
    filetype = os.path.splitext(path)[-1][1:]
    if filetype == 'txt':
        return parse_txt(path, colors, markers, mcolors)
    elif filetype == 'json':
        return parse_json(path, colors, markers, mcolors)
