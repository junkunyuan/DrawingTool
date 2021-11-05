import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
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

class T_SNE(object):
    def __init__(self,datas,cfg,output_dir=None,feature_name='embeds'):
        self.datas = datas
        self.cfg = cfg
        self.domain_names,self.label_names = self.__parse_data(datas)
        self.feature_name = feature_name
        self.tsne = TSNE(n_components=2,init='pca')                           # tsne
        self.output_dir = './' if output_dir == None else output_dir          # output dir

    def __fit(self,datas):
        for _,val in datas.items():
            tsne_embeds = self.tsne.fit_transform(val[self.feature_name])
            if 'tsne-embeds' not in val.keys():
                val['tsne-embeds'] = tsne_embeds
        return datas
    
    def __parse_data(self,datas):
        """
        extract domain names and label names in data.
        """
        domain_names = list(datas.keys())
        label_names = list()
        for dname in domain_names:
            label_names.extend(list(datas[dname].keys()))
        label_names = list(set(label_names))
        return domain_names,label_names
    
    def __plot(self,embed,labels,colors,markers=None):
        print(embed.shape)
        """plot tsne figure"""
        plt.figure(figsize=self.cfg['figsize'],dpi=self.cfg['dpi'])
        fig = plt.figure(1)
        ax1 = plt.subplot(111)

        if colors is not None:
            assert len(set(self.label_names)) <= len(colors), 'The length of colors must be larger than the number of categories in the cluster.'

        """去掉坐标和刻度"""
        ax1.spines['bottom'].set_visible(self.cfg['visible']['bottom'])
        ax1.spines['top'].set_visible(self.cfg['visible']['top'])
        ax1.spines["left"].set_visible(self.cfg['visible']['left'])
        ax1.spines["right"].set_visible(self.cfg['visible']['right'])
        ax1.set_xticks([])
        ax1.set_yticks([])

        if self.cfg['xlabel']:
            ax1.set_xlabel(self.cfg['xlabel'])

        if markers is None:
            ax1.scatter(embed[:,0],embed[:,1],s=self.cfg['pointsize'],c=labels,marker=self.cfg['marker'],cmap=matplotlib.colors.ListedColormap(colors))
        else:
            assert len(markers) == len(colors)
            for label in np.unique(labels):
                indx = np.where(labels==label)
                ax1.scatter(embed[indx][:,0],embed[indx][:,1],s=self.cfg['pointsize'],c=colors[label],marker=markers[label])
        return fig

    def __prepare_datas(self,domain_names,label_name,merge=True):

        # 准备label_names
        assert label_name in self.label_names

        # 准备domain_names
        if not isinstance(domain_names,list):
            domain_names = (domain_names,)
        domain_names = [name for name in domain_names if name in self.domain_names]
        
        if merge and len(domain_names) > 1:                                                      # merge the data in all domains to show in a figure
            all_domain_names = '-'.join(domain_names)
            datas = {all_domain_names:{}}

            for ln in [label_name,self.feature_name]:
                temp = [self.datas[domain_name][ln] for domain_name in domain_names]
                datas[all_domain_names][ln] = np.concatenate(temp,axis=0)

            domain_names = (all_domain_names,)
        else:                                                                                    # extract data in each domain
            datas = {key:val for key,val in self.datas.items() if key in domain_names}

        return datas,label_name,domain_names

    def draw(self,colors,domain_names,label_name,merge=True,save_name='',markers=None):
        
        print('Prepare datas...')
        datas,label_name,domain_names = self.__prepare_datas(domain_names,label_name,merge)    # extract the required data
        print('Fit datas...')
        datas = self.__fit(datas)                                                                # fit data

        for domain_name in domain_names:
            fig = self.__plot(datas[domain_name]['tsne-embeds'],datas[domain_name][label_name],colors=colors,markers=markers)

            save_dir = osp.join(self.output_dir,domain_name)
            if not osp.exists(save_dir):
                os.makedirs(save_dir)
            save_path = osp.join(save_dir,'{}.pdf'.format('-'.join([save_name,label_name]) if save_name else label_name))
            with PdfPages(save_path) as pdf:
                pdf.savefig(fig)
            print('{} done!'.format(save_path))
            plt.cla()
    