from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm

__all__ = ['newcmp','getcmp',
            'colors4_1',
            'colors6_1','colors6_2',
            'colors7_1','colors7_2',
            'markers']

markers = ['.', 'P', '<', '^', '*', 'X', 'p', 'D']

red = ['#F08080', '#FF5510', '#FF0000']
blue = ['#56BCBC', '#00BFFF', '#6495ED', '#4169E1']
green = ['#3CB371', '#32CD32', '#009933', '#2E8B57']
purple = ['#9966CC']
yellow = ['#F4B183', '#FFA500', '#FF8C00', '#AA7700', '#D2691E']
grey = ['#696969']
black = ['#000000']

"""
The rule for colors' name.
The color's name must be set to the following rule: colorsN_X
The N is the number for the color list. The X is the idx or label for color.
"""
colors4_1 = ["#FF99C8","#8FBC8F","#F4A460","#9ACD32"]
colors6_1 = ['#666666', green[1], '#369CFF', '#CC6600', '#FF6666', red[1]]              # original color2
colors6_2 = [yellow[1], blue[1], green[3], red[0], yellow[1], blue[0]]                  # original color3
colors7_1 = [black[0], blue[2], blue[0], green[2], purple[0], yellow[2], red[1]]        # original color1
colors7_2 = ["#00FF00","#00FFFF","#008000","#0000FF","#FF00FF","#FFD700","#FF0000"]

def newcmp(name,colorlist):
    """Create a new colormap."""
    return LinearSegmentedColormap.from_list(name,colorlist)

def getcmp(cmp,name='temp'):
    """if cmp exists in colormap, then return; then check if specifially set by user and create a new colormap."""
    if isinstance(cmp,str):
        return getattr(cm,cmp)
    elif isinstance(cmp,(list,tuple)):
        return newcmp(name,cmp)
    else:
        raise 'please enter legal cmp paras'
