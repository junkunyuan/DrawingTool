import numpy as np
class BaseDataItem():
    def __init__(self,name,data) -> None:
        self.name = name
        assert (data is not None) and (not isinstance(data, (int, float, str)))
        self.data = data
        if isinstance(self.data, (list, tuple)):
            self.data = np.array(self.data)

    @property
    def max(self):
        return max(self.data)

    @property
    def min(self):
        return min(self.data)
    
    @staticmethod
    def from_dict(dict_datas):
        baseitems = []
        names = dict_datas['names']
        datas = dict_datas['datas']
        for name,data in zip(names,datas):
            baseitems.append(BaseDataItem(name,data))
        return baseitems

class HistDataItem(BaseDataItem):
    def __init__(self, name, data, color) -> None:
        super().__init__(name,data)
        self.color = color
    
    @staticmethod
    def from_dict(dict_datas):
        histitems = []
        for name,data,color, in zip(dict_datas['names'],dict_datas['datas'],dict_datas['colors']):
            histitems.append(HistDataItem(name,data,color))
        return histitems

class LineDataItem(BaseDataItem):
    """Restructure the data."""
    def __init__(self, name, data, var, marker, color, mcolor=None) -> None:
        super().__init__(name,data)
        self.var = var
        if isinstance(self.var, (list, tuple)):
            self.var = np.array(self.var)

        self.marker = marker
        self.color = color
        self.mcolor = mcolor if mcolor is not None else self.color

    @staticmethod
    def from_dict(dict_datas):
        lineitems = []
        for name,data,var,marker,color,mcolor in zip(dict_datas['names'],dict_datas['datas'],dict_datas['vars'],dict_datas['markers'],dict_datas['colors'],dict_datas['mcolors']):
            lineitems.append(LineDataItem(name,data,var,marker,color,mcolor))
        return lineitems

