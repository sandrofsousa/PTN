import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from csv import reader
import math
import os


def data_frame1():
    data1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/radius_0to200.txt"
    df1 = pd.read_csv(data1,
                      index_col=0,
                      names=['Nós totais',
                             'Links totais',
                             'Grau máximo',
                             'Diâmetro da rede',
                             'Grau médio',
                             'Grau médio - entrada',
                             'Grau médio - saída',
                             'Grau mediano',
                             'Grau mediano - entrada',
                             'Grau mediano - saída',
                             'Variância',
                             'Desvio padrão',
                             'Tamanho médio do caminho',
                             'Clusters - fraco',
                             'Clusters - forte',
                             'Assortatividade - grau',
                             'Coef. de Clusterização',
                             'Densidade'])
    return df1


def data_frame2():
    file_names = []
    concat_list = []
    # path that will be collected
    os.chdir(r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/degrees")
    # Find any file that ends with ".txt"
    for files in os.listdir("."):
        if files.endswith(".txt"):
            file_names.append(files)  # append files names to a list

    def readfile(path):
        with open(path) as data:
            rho = int(path[path.rfind("deg") + 3:len(path) - 4])  # get rho by indexing file name .../deg[rho].txt
            searcher = reader(data, delimiter=',', quotechar='"')  # read file
            for line in searcher:
                degree = int(line[0])
                concat_list.append((rho, degree))  # append two columns to list

    for fname in file_names:
        location = r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/degrees/" + fname
        readfile(location)
    df2 = pd.DataFrame(concat_list, columns=["rho", "grau"])
    return df2


def plot_global_measures(df1):
    # sns.set_style("darkgrid", {"axes.facecolor": ".91"})
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 10), dpi=300)

    # getting separated data from pandas frameworks
    plt.subplot(331)
    plt.plot(df1.iloc[:, 0:1])
    plt.title('Nós totais (a)')

    plt.subplot(332)
    plt.plot(df1.iloc[:, 12:13])
    plt.title('Tamanho médio caminho (b)')

    plt.subplot(333)
    plt.plot(df1.iloc[:, 3:4])
    plt.title('Diâmetro rede (c)')

    plt.subplot(334)
    plt.plot(df1.iloc[:, 1:2])
    plt.title('Links totais (d)')

    plt.subplot(335)
    plt.plot(df1.iloc[:, 13:14])
    plt.title('Cluster - fraco (e)')

    plt.subplot(336)
    plt.plot(df1.iloc[:, 14:15])
    plt.title('Cluster - forte (f)')

    plt.subplot(337)
    plt.plot(df1.iloc[:, 15:16])
    plt.title('Assortatividade - grau (g)')
    plt.xlabel('rho')

    plt.subplot(338)
    plt.plot(df1.iloc[:, 16:17])
    plt.title('Coef. Clusterização (h)')
    plt.xlabel('rho')

    plt.subplot(339)
    plt.plot(df1.iloc[:, 17:18])
    plt.title('Densidade (i)')
    plt.xlabel('rho')

    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=1.7)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_measures.pdf"
    plt.savefig(figure)


def plot_node_measures(df1):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 4), dpi=300)

    plt.subplot(121)
    plt.plot(df1.iloc[:, 4:5], label='k-all')
    plt.plot(df1.iloc[:, 5:6], label='k-in')
    plt.plot(df1.iloc[:, 6:7], label='k-out')
    plt.title('Média (a)')
    plt.xlabel('rho')
    plt.ylabel('grau')
    plt.legend(loc=2)

    plt.subplot(122)
    plt.plot(df1.iloc[:, 7:8], label='k-all')
    plt.plot(df1.iloc[:, 8:9], label='k-in')
    plt.plot(df1.iloc[:, 9:10], label='k-out')
    plt.title('Mediana (b)')
    plt.xlabel('rho')
    plt.ylabel('grau')
    plt.legend(loc=2)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_node_measures.pdf"
    plt.savefig(figure)


def plot_hist_degree(df2):
    sns.set_context("talk", font_scale=0.9)
    grid = sns.FacetGrid(df2, col="rho", col_wrap=6, size=2.5)
    grid.map(plt.hist, "grau")
    grid.set(xscale="log", yscale="log", )
    grid.fig.tight_layout(w_pad=0.5, h_pad=0.5)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_hist_grid.pdf"
    plt.savefig(figure, dpi=300)


# def plot_hist_path():


# plot_global_measures(data_frame1())
# plot_node_measures(data_frame1())
# plot_hist_degree(data_frame2())
