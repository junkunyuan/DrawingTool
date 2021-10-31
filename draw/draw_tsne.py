import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from numpy.lib.npyio import save
from sklearn.manifold import TSNE
import os.path as osp
import os

"""
The data struction must be as follow：
data = {
    'domain1':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
    'domain2':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
    'domain3':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
    ……
}
"""
 

colors_classes = ["#00FF00","#00FFFF","#008000","#0000FF","#FF00FF","#FFD700","#FF0000"]
colors_domains = ["#FF99C8","#8FBC8F","#F4A460","#9ACD32"]

class T_SNE(object):
    def __init__(self,pth,datas=None,output_dir=None,feature_name='embeds'):
        assert pth is not None or datas is not None
        self.pth = pth          
        self.feature_name = feature_name
        self.tsne = TSNE(n_components=2,init='pca')                         # tsne
        self.__load_data(pth,datas)                                         # load data
        self.output_dir = self.__gene_output_dir(output_dir,datas)          # output dir

    def __gene_output_dir(self,output_dir,datas):
        if output_dir == None:
            return './' if datas is not None else osp.split(self.pth)[0]
        else:
            return output_dir

    def __fit(self,datas):
        for _,val in datas.items():
            tsne_embeds = self.tsne.fit_transform(val[self.feature_name])
            if 'tsne-embeds' not in val.keys():
                val['tsne-embeds'] = tsne_embeds

        return datas
    
    def __load_data(self,pth,datas):
        if datas is not None:
            self.datas = datas
            assert isinstance(datas,dict), 'Please input valide data!'
            for k,v in datas.items():
                assert isinstance(k,str), 'Please input valide data!'
                assert isinstance(v,dict), 'Please input valide data!'
                for k1,_ in v.items():
                    assert isinstance(k1,str), 'Please input valide data!'
        else:
            assert osp.exists(pth), 'Please input valide path!'
            assert osp.splitext(pth)[-1] == '.npy', 'The file type must be ".npy" type'
            self.datas = np.load(pth,allow_pickle=True).item()

        self.domain_names = list(self.datas.keys())
        self.label_names = list()
        for dname in self.domain_names:
            self.label_names.extend(list(self.datas[dname].keys()))
        self.label_names = list(set(self.label_names))
    
    def __plot(self,embed,labels,colors,setx=None,markers=None):
        
        plt.figure(figsize=(10,6),dpi=80)
        fig = plt.figure(1)
        ax1 = plt.subplot(111)

        if colors is not None:
            assert len(set(self.label_names)) <= len(colors), 'The length of colors must be larger than the number of categories in the cluster.'

        """去掉坐标和刻度"""
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax1.spines["left"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.set_xticks([])
        ax1.set_yticks([])

        if setx:
            ax1.set_xlabel(str(setx))

        if markers is None:
            ax1.scatter(embed[:,0],embed[:,1],s=5,c=labels,marker="o",cmap=matplotlib.colors.ListedColormap(colors))
        else:
            assert len(markers) == len(colors)
            for label in np.unique(labels):
                indx = np.where(labels==label)
                print(label,colors[label],markers[label])
                ax1.scatter(embed[indx][:,0],embed[indx][:,1],s=10,c=colors[label],marker=markers[label])

        return fig

    def __prepare_datas(self,domain_names=None,label_names=None,merge=True):

        # 准备label_names
        if label_names is not None:
            if not isinstance(label_names,list):
                label_names = (label_names,)
            label_names = [item for item in label_names if item in self.label_names]

        # 准备domain_names
        if domain_names is not None:
            if not isinstance(domain_names,list):
                domain_names = (domain_names,)
            domain_names = [name for name in domain_names if name in self.domain_names]
        
        if merge and len(domain_names) > 1:                                     # 将domain_names中指定domain的数据全部混在一起
            all_domain_names = '-'.join(domain_names)
            datas = {all_domain_names:{}}

            for label_name in label_names+[self.feature_name]:
                temp = [self.datas[domain_name][label_name] for domain_name in domain_names]
                datas[label_name] = np.concatenate(temp,axis=0)

            domain_names = (all_domain_names,)
        else:                                       # 将domain_names中依次取出并返回
            datas = {key:val for key,val in self.datas.items() if key in domain_names}

        return datas,label_names,domain_names

    def draw(self,colors,domain_names=None,label_names=None,merge=True,save_name='',markers=None):

        print('Prepare datas...')
        datas,label_names,domain_names = self.__prepare_datas(domain_names,label_names,merge)       # 从加载的数据里面，将需要的数据抽取出来
        print('Fit datas...')
        datas = self.__fit(datas)                                                                   # 先拟合数据

        for domain_name in domain_names:
            for label_name in label_names:
                fig = self.__plot(datas[domain_name]['tsne-embeds'],datas[domain_name][label_name],colors=colors,markers=markers)

                save_dir = osp.join(self.output_dir,domain_name)
                if not osp.exists(save_dir):
                    os.makedirs(save_dir)
                save_path = osp.join(save_dir,'{}.pdf'.format('-'.join([save_name,label_name]) if save_name else label_name))
                with PdfPages(save_path) as pdf:
                    pdf.savefig(fig)
                print('{} done!'.format(save_path))

if __name__ == '__main__':
    """Tutorial

    You can load data from "pth" or income the "datas". When bath get the "pth" and and the "datas", the procedure use the "datas" prioritily.
    data = {
        'domain1':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        'domain2':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        'domain3':{'embeds':np.array([num,dim]),'label1':np.array([num]),'label2':np.array([num]),...},
        ……
    }
    """
    data = {
        'domain1':{'embeds':np.random.rand(1000,100),'label1':np.random.randint(0,7,size=(1000,)),'label2':np.random.randint(0,4,size=(1000,))}
    }
    tsne = T_SNE(None,datas=data,feature_name='embeds')               # 以上面注释的data为例子
    # tsne.draw(['domain1','domain2'],'label1',mixup=False)             # 将会生成两个图,domain1中所有特征按照label1生成一张，domain2也生成一张
    # tsne.draw(['domain1','domain2'],'label1',mixup=True)              # 将会生成一张图，domain1和domain2中所有数据混在一起，按照label1生成一张

    markers = ['o','o','o','o','o','o','x']
    colors_classes = ["#00FF00","#00FFFF","#008000","#0000FF","#FF00FF","#FFD700","#000000"]
    tsne.draw(colors_classes,'domain1','label1',merge=False,markers=markers)
