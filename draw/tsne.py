import sys
sys.path.append('..')
import numpy as np
from tool.util import loadcfg
from lib.color import colors7_2,colors4_1
from lib.tsne import T_SNE
from lib.dataloader import loadtsnedata

def demo(datas,cfg):
    tsne = T_SNE(datas,cfg,feature_name='embeds',output_dir='../output')

    """Draw data in domain1 with label1. You will get one figure."""
    markers = ['o','o','o','o','o','o','x']                                 # different classes with different marekr
    tsne.draw(colors7_2,'domain1','label1',merge=False,markers=markers)

    """Draw data merged from domain1 and domain2 with label1. You will get one figure."""
    tsne.draw(colors7_2,['domain1','domain2'],'label1',merge=True)

    """Draw data from domain1 and domain2 with label1 respectively. You will get two figure."""
    tsne.draw(colors7_2,['domain1','domain2'],'label1',merge=False)

if __name__ == '__main__':
    """
    You can load data from data path. The data struction must be as follow：
    data = {
        'domain1':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        'domain2':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        'domain3':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        ……
    }
    You can change the 'domainX','embeds','label1','label2' to other key.
    """
    
    """
    This is the test data used in demo.
    datas = {
        'domain1':{'embeds':np.random.rand(1000,100),'label1':np.random.randint(0,7,size=(1000,)),'label2':np.random.randint(0,4,size=(1000,))},
        'domain2':{'embeds':np.random.rand(1000,100),'label1':np.random.randint(0,7,size=(1000,)),'label2':np.random.randint(0,4,size=(1000,))}
    }
    """
    datas = loadtsnedata('../data/test.npy')            # load data
    cfg = loadcfg('../configs/tsne.yaml')
    demo(datas,cfg)
