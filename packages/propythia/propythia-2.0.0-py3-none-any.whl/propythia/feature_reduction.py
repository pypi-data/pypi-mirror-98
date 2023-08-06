# -*- coding: utf-8 -*-
"""
##############################################################################

File containing a class used for reducing the number of features on a dataset based
on unsupervised techniques.

Authors: Ana Marta Sequeira

Date: 06/2019 altered 12/2020

Email:

##############################################################################
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA, SparsePCA, MiniBatchSparsePCA,TruncatedSVD
import matplotlib.pyplot as plt
import seaborn as sns
import inspect
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from propythia.src.propythia.adjuv_functions.ml_deep.utils import timer

# from scores import score_methods
sns.set()


class FeatureDecomposition:
    """
    The Feature Reduction class aims to Reduce the number of features on a dataset based on unsupervised techniques.
    pca statistical procedure that orthogonally transforms the original n coordinates of a data set into a new set of
    n coordinates called principal components. Principal components are a combination of features that capture well the
    variance of the original features.
    Based on scikit learn
    """

    def __init__(self, fps_x, report_name=None, classes=None):
        """	constructor """
        self.fps_x = fps_x
        self.pca = None
        self.x_pca = None
        self.n_components = None
        self.labels = None # to distinguish pca to sdv

        self.classes = classes #columns names
        self.report_name = report_name
        if self.report_name:
            self.report(str(self.report_name))

    def report(self, info):
        filename = str(self.report_name)
        with open(filename, 'a+') as file:
            # print(info.type)
            if isinstance(info, str):
                file.writelines(info)
            else:
                for l in info:
                    file.writelines('\n{}'.format(l))

    @timer
    def run_pca(self, n_components=None, random_state=None, **params):
        """
        Function that realizes the pca analysis
        :param dataset: data on to perform pca
        # :param scaler: scaler to scale data. standard scaler by default
        :param n_components: Number of components to keep. if n_components is not set all components are kept
        :param copy:
        :param whiten:
        :param svd_solver:  string {‘auto’, ‘full’, ‘arpack’, ‘randomized’}
        :param tol:
        :param iterated_power:
        :param random_state:
        :return:
        For more information: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
        """
        saved_args = locals()
        # performing pca
        pca_ = PCA(n_components, random_state, **params)
        x_pca_ = pca_.fit_transform(self.fps_x)

        # analysis
        s1 = "Original shape: {}".format(str(self.fps_x.shape))
        s2 = "Reduced shape: {}".format(str(x_pca_.shape))
        s3 = "Variance explained by the PC: {}".format(sum(pca_.explained_variance_ratio_))
        s4 = "Number of components: {}".format(pca_.n_components_)
        s5 = "pca components by explained variance ratio:\n{}".format(pca_.components_)

        print('{}\n{}\n{}\n{}'.format(s1, s2, s3, s4))

        self.pca = pca_
        self.x_pca = x_pca_
        self.n_components = pca_.n_components_
        self.labels = 'PC-'

        if self.report_name:
            self.report([self.run_pca.__name__, saved_args, s1, s2, s3, s4, s5])

        return self.pca, self.x_pca
        # it is possible to access all the information in scikit learn

    @timer
    def run_batch_sparse_pca(self, n_components, alpha=1, batch_size=50, **params):
        # PCA's main weakness is that it tends to be highly affected by outliers in the data. For this reason, many robust variants' \
        #    ' of PCA have been developed, many of which act to iteratively discard data points that are poorly described by the ' \
        #    'initial components. Scikit-Learn contains a couple interesting variants on PCA, including RandomizedPCA and SparsePCA, ' \
        #    'both also in the sklearn.decomposition submodule. RandomizedPCA, which we saw earlier, uses a non-deterministic method t' \
        #    'o quickly approximate the first few principal components in very high-dimensional data, while SparsePCA introduces ' \
        #    'a regularization term (see In Depth: Linear Regression) that serves to enforce sparsity of the components.
        # https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
        # randomized, o solver do PCA ja faz autmaticamente consoante tamanho  if the input data is larger than 500x500 and
        # the number of components to extract is lower than 80% of the smallest dimension of the data, then the more
        # efficient ‘randomized’ method is enabled
        # performing pca
        # todo try to add explained_variance_ratio
        saved_args = locals()

        pca_ = MiniBatchSparsePCA(n_components, alpha=alpha, batch_size=batch_size, **params)
        x_pca_ = pca_.fit_transform(self.fps_x)

        # analysis
        s1 = "Original shape: {}".format(str(self.fps_x.shape))
        s2 = "Reduced shape: {}".format(str(x_pca_.shape))
        s4 = "Number of components: {}".format(pca_.n_components_)
        s5 = "pca components by explained variance ratio:\n{}".format(pca_.components_)

        print('{}\n{}\n{}'.format(s1, s2, s4))
        if self.report_name:
            self.report([self.run_batch_sparse_pca.__name__, saved_args, s1, s2, s4, s5])

        self.pca = pca_
        self.x_pca = x_pca_
        self.n_components = pca_.n_components_
        self.labels = 'spPC-'

        return self.pca, self.x_pca

    @timer
    def run_truncated_svd(self, n_components, n_iter=5,random_state=42, **params):
        """
        This transformer performs linear dimensionality reduction by means of
        truncated singular value decomposition (SVD). Contrary to PCA, this
        estimator does not center the data before computing the singular value
         decomposition. This means it can work with sparse matrices efficiently.


        https://machinelearningmastery.com/singular-value-decomposition-for-dimensionality-reduction-in-python/
         SVD is typically used on sparse data.
        This includes data for a recommender system or a bag of words model for
        text. If the data is dense, then it is better to use the PCA method.


        :param n_components:
        :param n_iter:
        :param random_state:
        :param params:
        :return:
        """
        saved_args = locals()

        # performing svd
        svd = TruncatedSVD(n_components=n_components, n_iter=n_iter, random_state=random_state)
        x_svd = svd.fit_transform(self.fps_x)

        # analysis
        s1 = "Original shape: {}".format(str(self.fps_x.shape))
        s2 = "Reduced shape: {}".format(str(x_svd.shape))
        s3 = "Variance explained by the PC: {}".format(sum(svd.explained_variance_ratio_)) # Percentage of variance explained by each of the selected components
        s4 = "Number of components: {}".format(svd.components_)
        s5 = "pca components by explained variance ratio:\n{}".format(svd.components_)

        print('{}\n{}\n{}\n{}'.format(s1, s2, s3, s4))

        self.pca = svd
        self.x_pca = x_svd
        self.n_components = len(svd.components_)
        self.labels = 'SV'

        if self.report_name:
            self.report([self.run_truncated_svd.__name__, saved_args, s1, s2, s3, s4, s5])

        return self.pca, self.x_pca

    #####################################################################################################
    def variance_ratio_components(self):
        """
        measures the variance ratio of the principal components
        :param x_pca:
        :return: variance ratio of principal components
        """

        ex_variance = np.var(self.x_pca, axis=0)
        ex_variance_ratio = ex_variance / np.sum(ex_variance)
        if self.report_name:
            self.report([self.variance_ratio_components.__name__, ex_variance_ratio])

        return ex_variance_ratio

    def contribution_of_features_to_component(self):
        """
        Function that retrieves a dataframe containing the contribution of each feature (rows) for component
        As unsupervised learning does not represent the importance of features but representing the directions
        of maximum variance in the data.
        :param data: dataset as dataframe
        :param pca: dataset fit to pca
        :param x_pca: dataset transformed to pca
        :return: dataframe containing the contribution of each feature (rows) for component
        """
        # does not work with sparse
        #todopass this to the init
        original_columns=[]
        if self.classes is not None:
            original_columns = self.classes
        else:
            try:
                original_columns = self.fps_x.columns
            except Exception as e:
                print(e)

        coef = self.pca.components_.T
        columns = []
        for x in range(self.n_components):
            columns.append(str(self.labels + str(x + 1)))
        result = pd.DataFrame(coef, columns=columns, index=original_columns)
        if self.report_name:
            self.report([self.contribution_of_features_to_component.__name__, result])
        return result

    def pca_bar_plot(self, show=True, path_save='pca_bar_plot.png', title='Percentage of explained variance ratio by PCA',
                     width=1, data=None, color='b', edgecolor='k', linewidth=0,
                     tick_label=None, **params):
        """
        function that derives a bar plot representing the percentage of explained variance ratio by pca
        :param pca: dataset fit to pca
        :param height: scalar or sequence of scalars. The height(s) of the bars.
        :param width:  scalar or array-like, optional. The width(s) of the bars
        :param data:
        :param color: scalar or array-like, optional. The colors of the bar faces.
        :param edgecolor:  scalar or array-like, optional. The colors of the bar edges.
        :param linewidth: scalar or array-like, optional. Width of the bar edge(s). If 0, don't draw edges.
        :param tick_label: string or array-like, optional. The tick labels of the bars. Default: None
        :return: bar plot representing the percentage of explained variance ratio by pca
        For more information please see https://matplotlib.org/api/_as_gen/matplotlib.pyplot.bar.html
        """
        # does not work with sparse
        plt.clf()
        plt.bar(range(self.n_components), height=self.pca.explained_variance_ratio_ * 100, width=width, data=data,
                color=color,
                edgecolor=edgecolor, linewidth=linewidth, tick_label=tick_label, **params)
        plt.xlabel(str(self.labels))
        plt.ylabel('Percentage of explained variance')
        plt.title(title)
        if path_save is not None: plt.savefig(fname=path_save)
        if show is True: plt.show()
        plt.clf()

    def pca_cumulative_explain_ratio(self, show=True, path_save='pca_cumulative_explain_ratio.png'):
        # A vital part of using PCA in practice is the ability to estimate how many components are needed to describe the
        # data. This can be determined by looking at the cumulative explained variance ratio as a function of the number
        # of components:
        # https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
        plt.clf()
        plt.plot(np.cumsum(self.pca.explained_variance_ratio_))
        plt.xlabel('number of components')
        plt.ylabel('cumulative explained variance')
        if path_save is not None: plt.savefig(fname=path_save)
        if show is True: plt.show()
        plt.clf()

    def pca_scatter_plot(self, target, pca1=0, pca2=1, title=None, show=True, path_save='pca_scatter_plot.png'):
        """
        change this
        Scatter plot of the labels based on two components (by default the first ones)
        :param title: string. title of the scatter plot
        :param data: dataset. dataframe
        :param pca: dataset fit to pca
        :param x_pca: dataset transformed to pca
        :param target: labels of dataset
        :param pca1: first pca to be considered. default PCA1
        :param pca2: second pca to be considered. default PCA2
        :return: graph showing the positions of labels according of the two chosen components
        """
        plt.clf()
        projected = self.x_pca

        n_color=len(np.unique(target))
        # Get Unique ec
        color_labels = np.unique(target)

        # List of colors in the color palettes
        rgb_values = sns.color_palette("nipy_spectral", n_color) # 'set2'

        # Map ec to the colors
        color_map = dict(zip(color_labels, rgb_values))

        # Finally use the mapped values
        plt.scatter(projected[:, pca1], projected[:, pca2],
                    c=target.map(color_map))

        # create legend
        # classes  - colour labels
        # class_colours rgb values
        recs = []
        from matplotlib.lines import Line2D

        for i in range(0, n_color):
            recs.append(Line2D((0,0.75),(0,0), color=rgb_values[i], marker='o', linestyle=''))
            # recs.append(mpatches.Circle((0, 0), 0.5, fc=rgb_values[i]))

        n_col = int(n_color/23)+1

        lgd = plt.legend(recs, color_labels, bbox_to_anchor=(1,1), loc="upper left",
                   fontsize='xx-small', ncol = n_col, shadow=False, title='classes')
        # add labels and title
        plt.xlabel(str(self.labels + '-1'))
        plt.ylabel(str(self.labels + '-2'))
        if title is None:
            title = ' Scatter plot of 2 {}'.format(str(self.labels))
        plt.title(title)

        # save and empty plt
        if path_save is not None:
            plt.savefig(fname=path_save,bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
        if show is True:
            plt.show()
        plt.clf()

        # plt.scatter(projected[:, pca1], projected[:, pca2],
        #             c=target,
        #             edgecolor='none', alpha=0.5)
        #             # ,
        # palette=sns.color_palette('nipy_spectral', n_color))
        # cmap=plt.cm.get_cmap('nipy_spectral',n_color))
        # plt.colorbar()
        # plt.legend(legend1,loc='best', shadow=False)

    def pca_scatter_plot3d(self, target, pca1=0, pca2=1, pca3=2, title=None, show=True, path_save='pca_scatter_plot.png'):
        """
        Scatter plot of the labels based on two components (by default the first ones)
        """
        plt.clf()
        projected = self.x_pca

        n_color=len(np.unique(target))
        # Get Unique ec
        color_labels = np.unique(target)

        # List of colors in the color palettes
        rgb_values = sns.color_palette("nipy_spectral", n_color) # 'set2'

        # Map ec to the colors
        color_map = dict(zip(color_labels, rgb_values))
        # Finally use the mapped values
        from mpl_toolkits import mplot3d
        ax = plt.axes(projection ="3d")

        ax.scatter3D(projected[:, pca1], projected[:, pca2],projected[:, pca3],
                    c=target.map(color_map))
        # create legend
        # classes  - colour labels
        # class_colours rgb values
        recs = []

        for i in range(0, n_color):
            recs.append(Line2D((0,0.75),(0,0), color=rgb_values[i], marker='o', linestyle=''))
            # recs.append(mpatches.Circle((0, 0), 0.5, fc=rgb_values[i]))

        n_col = int(n_color/23)+1

        lgd = plt.legend(recs, color_labels, bbox_to_anchor=(1,1), loc="upper left",
                         fontsize='xx-small', ncol = n_col, shadow=False, title='classes')
        # add labels and title
        ax.set_xlabel(str(self.labels + '-1'), fontweight ='bold')
        ax.set_ylabel(str(self.labels + '-2'), fontweight ='bold')
        ax.set_zlabel(str(self.labels + '-3'), fontweight ='bold')
        if title is None:
            title = ' Scatter plot of 3 {}'.format(str(self.labels))
        plt.title(title)

        # save and empty plt
        if path_save is not None:
            plt.savefig(fname=path_save,bbox_extra_artists=(lgd,), bbox_inches='tight', pad_inches=0)
        if show is True:
            plt.show()
        plt.clf()


# todo change name file to feature decomposition
# todo write comments

# https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html

# add others decomposition? SVD NMF  dictionary learning?????
