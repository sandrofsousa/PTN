import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from csv import reader
import math
import os


def plot_rho():
    data2 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/radius_0to200.txt"
    df2 = pd.read_csv(data2,
                      index_col=0,
                      names=['Nós totais',
                             'Links totais',
                             'Grau máximo',
                             'Diâmetro da rede',
                             'Grau médio',
                             'Caminho médio',
                             'Componentes',
                             'Assortatividade',
                             'Coef. de Clusterização',
                             'Densidade'])

    sns.set_style("darkgrid", {"axes.facecolor": ".91", 'text.color': '.15'})
    sns.set_context("talk")

    plt.figure(facecolor="white", figsize=(14, 16))

    # geting separated data from pandas framworks
    plt.subplot(521)
    plt.plot(df2.iloc[:,0:1])
    plt.title('Nós totais')

    plt.subplot(522)
    plt.plot(df2.iloc[:,1:2])
    plt.title('Links totais')

    plt.subplot(523)
    plt.plot(df2.iloc[:,2:3])
    plt.title('Grau máximo')

    plt.subplot(524)
    plt.plot(df2.iloc[:,3:4])
    plt.title('Diâmetro da rede')

    plt.subplot(525)
    plt.plot(df2.iloc[:,4:5])
    plt.title('Grau médio')

    plt.subplot(526)
    plt.plot(df2.iloc[:,5:6])
    plt.title('Caminho médio')

    plt.subplot(527)
    plt.plot(df2.iloc[:,6:7])
    plt.title('Componentes')

    plt.subplot(528)
    plt.plot(df2.iloc[:,7:8])
    plt.title('Assortatividade')

    plt.subplot(529)
    plt.plot(df2.iloc[:,8:9])
    plt.title('Coef. de Clusterização')
    plt.xlabel('Raio')

    plt.subplot(5,2,10)
    plt.plot(df2.iloc[:,9:10])
    plt.title('Densidade')
    plt.xlabel('Raio')

    plt.subplots_adjust(wspace=0.2, hspace=0.3)

    plt.savefig("/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/plot/plot_rho0to200", dpi=200)


def his_plot():
    global df3
    filenames = []
    concat_list = []
    # Your path will be different, please modify the path below.
    os.chdir(r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram")
    # Find any file that ends with ".xlsx"
    for files in os.listdir("."):
        if files.endswith(".txt"):
            filenames.append(files)

    def readfile(path):
        with open(path) as data:
            rho = int(path[path.rfind("hist")+4:len(path)-4])
            searcher = reader(data, delimiter=',', quotechar='"')
            for line in searcher:
                bin_in = math.log10(float(line[0]))
                freq = int(line[2])
                concat_list.append((bin_in,rho,freq))

    for fname in filenames:
        location = r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/" + fname

        readfile(location)

    df3 = pd.DataFrame(concat_list, columns=["bin", "rho", "freq"])

    # g = sns.FacetGrid(df3, col='rho', col_wrap=5, size=2, sharex=True, xlim=(0, 4))
    # g = g.map(sns.pointplot, 'freq', 'bin', scale=.7)
    # plt.show()

    g = sns.FacetGrid(df3, col='rho', col_wrap=5, sharex=True, xlim=(0, 7000), ylim=(0, 4))
    g.map(sns.pointplot, 'bin', 'freq')
    plt.show()

his_plot()
