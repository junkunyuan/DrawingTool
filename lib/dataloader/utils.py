import json

def parse_txt(path, colors=None, markers=None, mcolors=None):
    with open(path, 'r', encoding='utf8') as f:
        contents = f.readlines()
    
    def parse(content,num,ks,count):
        if len(content) > num and content[num] != '':
            return content[num]
        elif ks is not None:
            return ks[count]
        else:
            return None

    count = 0
    rets = {
        'names':[],
        'datas':[],
        'vars':[],
        'markers':[],
        'colors':[],
        'mcolors':[],
    }
    for line in contents:
        line = line.strip()
        if not line or line[0] == '#':
            continue
        content = line.split('|')
        # marker = content[3] if (len(content) > 3 and content[3] != '') else markers[count]
        # color = content[4] if (len(content) > 4 and content[4] != '') else colors[count]
        # mcolor = content[5] if (len(content) > 5 and content[5] != '') else mcolors[count]

        marker = parse(content,3,markers,count)
        color = parse(content,4,colors,count)
        mcolor = parse(content,5,mcolors,count)

        rets['names'].append(content[0])
        rets['datas'].append([float(i) for i in content[1].split(',')])
        rets['vars'].append([float(i) for i in content[2].split(',')])
        rets['markers'].append(marker)
        rets['colors'].append(color)
        rets['mcolors'].append(mcolor)
        count += 1
        if count != 0:
            assert len(rets['datas'][-1]) == len(rets['datas'][0]), "The {}-th data number is different from the 1st data number, please check the data file.".format(count)
    del contents
    return rets


def parse_json(path, colors=None, markers=None, mcolors=None):
    """Parse json file."""
    with open(path, 'r', encoding='utf-8') as f:
        contents = json.load(f)

    def parse(k,_dict,ks,count):
        if k in _dict:
            return _dict[k]
        elif ks is not None:
            return ks[count]
        else:
            return None

    rets = {
        'names':[],
        'datas':[],
        'vars':[],
        'markers':[],
        'colors':[],
        'mcolors':[],
    }
    count = 0
    for _, item in contents.items():
        # marker = item['marker'] if ('marker' in item and item['marker'] != '') else markers[count]
        # color = item['color'] if ('color' in item and item['color'] != '') else colors[count]
        # mcolor = item['mcolor'] if ('mcolor' in item and item['mcolor'] != '') else mcolors[count]

        marker = parse('marker',item,markers,count)
        color = parse('color',item,colors,count)
        mcolor = parse('mcolor',item,mcolors,count)
        var = item['var'] if 'var' in item else None
        data = [item['data']] if not isinstance(item['data'], list) else item['data']

        rets['names'].append(item['name'])
        rets['datas'].append(data)
        rets['vars'].append(var)
        rets['markers'].append(marker)
        rets['colors'].append(color)
        rets['mcolors'].append(mcolor)
        count += 1
        if count != 0:
            assert len(rets['datas'][-1]) == len(rets['datas'][0]), "The {}-th data number is different from the 1st data number, please check the data file.".format(count)
    del contents
    return rets

