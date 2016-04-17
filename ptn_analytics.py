import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from csv import reader
from igraph import *
import powerlaw
import os

############################################################################
# Statistical Analysis plots
############################################################################


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


def data_frame3(df1):
    filenames1 = []
    concat_list1 = []
    # path that will be collected
    os.chdir(r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/paths")
    # Find any file that ends with ".txt"
    for files in os.listdir("."):
        if files.endswith(".txt"):
            filenames1.append(files)  # apeend files names to a list

    def readfile1(path):
        with open(path) as data:
            rho = int(path[path.rfind("path") + 4:len(path) - 4])
            dict_total = dict(df1["Nós totais"])
            n_node = int(dict_total[rho])
            searcher = reader(data, delimiter=',', quotechar='"')
            for line in searcher:
                path = float(line[0])
                freq = int(line[2])
                freq_norm = freq / n_node
                concat_list1.append((rho, path, freq, freq_norm, n_node))

    for fname in filenames1:
        location = r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/paths/" + fname
        readfile1(location)

    df3 = pd.DataFrame(concat_list1, columns=["rho", "path", "freq", "freq_norm", "n_node"])
    return df3


def plot_global_measures(df1):
    # sns.set_style("darkgrid", {"axes.facecolor": ".91"})
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 10), dpi=300)

    # getting separated data from pandas frameworks
    plt.subplot(331)
    plt.plot(df1.iloc[:, 1:2])
    plt.title('Qtd. links (a)')

    plt.subplot(332)
    plt.plot(df1.iloc[:, 0:1])
    plt.title('Qtd. nós (b)')

    plt.subplot(333)
    plt.plot(df1.iloc[:, 15:16])
    plt.title('Coef. assortatividade - grau (c)')
    plt.ylim(0, 1)

    plt.subplot(334)
    plt.plot(df1.iloc[:, 13:14])
    plt.title('Qtd. clusters - fraco (d)')

    plt.subplot(335)
    plt.plot(df1.iloc[:, 14:15])
    plt.title('Qtd. clusters - forte (e)')

    plt.subplot(336)
    plt.plot(df1.iloc[:, 16:17])
    plt.title('Coef. clusterização (f)')
    plt.ylim(0, 0.20)

    plt.subplot(337)
    plt.plot(df1.iloc[:, 12:13])
    plt.ylim(0, 60)
    plt.title('Comprimento médio caminho (g)')
    plt.xlabel('rho')

    plt.subplot(338)
    plt.plot(df1.iloc[:, 3:4])
    plt.ylim(0, 180)
    plt.title('Diâmetro rede (h)')
    plt.xlabel('rho')

    plt.subplot(339)
    plt.plot(df1.iloc[:, 17:18])
    plt.title('Coef. densidade (i)')
    plt.xlabel('rho')

    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=1.7)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_measures.pdf"
    plt.savefig(figure)


def plot_global_measures_sep(df1):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(12, 4))
    plt.subplot(131)
    plt.plot(df1.iloc[:, 1:2])
    plt.title('Qtd. links (a)')
    plt.xlabel('rho')

    plt.subplot(132)
    plt.plot(df1.iloc[:, 0:1])
    plt.title('Qtd. nós (b)')
    plt.xlabel('rho')

    plt.subplot(133)
    plt.plot(df1.iloc[:, 15:16])
    plt.title('Coef. assortatividade - grau (c)')
    plt.ylim(0, 1)
    plt.xlabel('rho')
    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=1.7)
    figure1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_degree.pdf"
    plt.savefig(figure1)
    ##########################


    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(12, 4))
    plt.subplot(131)
    plt.plot(df1.iloc[:, 13:14])
    plt.title('Qtd. clusters - fraco (a)')
    plt.xlabel('rho')

    plt.subplot(132)
    plt.plot(df1.iloc[:, 14:15])
    plt.title('Qtd. clusters - forte (b)')
    plt.xlabel('rho')

    plt.subplot(133)
    plt.plot(df1.iloc[:, 16:17])
    plt.title('Coef. clusterização (c)')
    plt.ylim(0, 0.20)
    plt.xlabel('rho')
    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=1.7)
    figure2 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_cluster.pdf"
    plt.savefig(figure2)
    ##########################


    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(12, 4))
    plt.subplot(131)
    plt.plot(df1.iloc[:, 12:13])
    plt.ylim(0, 60)
    plt.title('Comprimento médio caminho (a)')
    plt.xlabel('rho')

    plt.subplot(132)
    plt.plot(df1.iloc[:, 3:4])
    plt.ylim(0, 180)
    plt.title('Diâmetro rede (b)')
    plt.xlabel('rho')

    plt.subplot(133)
    plt.plot(df1.iloc[:, 17:18])
    plt.title('Coef. densidade (c)')
    plt.xlabel('rho')
    plt.tight_layout(pad=0.4, w_pad=0.7, h_pad=1.7)
    figure3 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_path.pdf"
    plt.savefig(figure3)


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
    plt.ylim(0, 70)
    plt.legend(loc=2)

    plt.subplot(122)
    plt.plot(df1.iloc[:, 7:8], label='k-all')
    plt.plot(df1.iloc[:, 8:9], label='k-in')
    plt.plot(df1.iloc[:, 9:10], label='k-out')
    plt.title('Mediana (b)')
    plt.xlabel('rho')
    plt.ylabel('grau')
    plt.ylim(0, 70)
    plt.legend(loc=2)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_node_measures.pdf"
    plt.savefig(figure)


def plot_hist_degree(df2):
    sns.set_context("talk", font_scale=0.9)
    grid = sns.FacetGrid(df2, col="rho", col_wrap=6, size=2.5)
    grid.map(plt.hist, "grau")
    grid.set(xscale="log", yscale="log")
    grid.set_axis_labels("Grau", "Frequência")
    grid.fig.tight_layout(w_pad=0.5, h_pad=0.5)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_hist_grid.pdf"
    plt.savefig(figure, dpi=300)


def plot_hist_path(df3):

    sns.set_context("talk", font_scale=0.9)
    grid = sns.FacetGrid(df3, col="rho", col_wrap=6, size=2.5, xlim=(0, 200), ylim=(0, 400))
    grid.map(plt.scatter, "path", "freq_norm", s=5, alpha=0.7)
    grid.set_axis_labels("caminho médio", "frequência")
    grid.fig.tight_layout(w_pad=0.5, h_pad=0.5)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_hist_path_grid.pdf"
    plt.savefig(figure, dpi=300)


def plot_power_law0(df2):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(6, 4))

    data0 = df2.grau[df2.rho == 0]
    fit = powerlaw.Fit(data0, discrete=True)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_ccdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_ccdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p (K ≥ k)")
    fig.set_xlabel("Grau")
    fig.set_title("rho = 0")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    # savefig(figname+'.eps', bbox_inches='tight')
    # savefig(figname+'.tiff', bbox_inches='tight', dpi=300)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law0.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law20(df2):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(6, 4))

    data20 = df2.grau[df2.rho == 20]
    fit = powerlaw.Fit(data20, discrete=True)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_ccdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_ccdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p (K ≥ k)")
    fig.set_xlabel("Grau")
    fig.set_title("rho = 20")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    # savefig(figname+'.eps', bbox_inches='tight')
    # savefig(figname+'.tiff', bbox_inches='tight', dpi=300)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law20.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law65(df2):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(6, 4))

    data65 = df2.grau[df2.rho == 65]
    fit = powerlaw.Fit(data65, discrete=True)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_ccdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_ccdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p (K ≥ k)")
    fig.set_xlabel("Grau")
    fig.set_title("rho = 65")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    # savefig(figname+'.eps', bbox_inches='tight')
    # savefig(figname+'.tiff', bbox_inches='tight', dpi=300)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law65.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law150(df2):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(6, 4))

    data150 = df2.grau[df2.rho == 150]
    fit = powerlaw.Fit(data150, discrete=True)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_ccdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_ccdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p (K ≥ k)")
    fig.set_xlabel("Grau")
    fig.set_title("rho = 150")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    # savefig(figname+'.eps', bbox_inches='tight')
    # savefig(figname+'.tiff', bbox_inches='tight', dpi=300)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law150.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law200(df2):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(6, 4))

    data200 = df2.grau[df2.rho == 200]
    fit = powerlaw.Fit(data200, discrete=True)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_ccdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_ccdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p (K ≥ k)")
    fig.set_xlabel("Grau")
    fig.set_title("rho = 200")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    # savefig(figname+'.eps', bbox_inches='tight')
    # savefig(figname+'.tiff', bbox_inches='tight', dpi=300)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law200.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


# plot_global_measures(data_frame1())
# plot_global_measures_sep(data_frame1())
# plot_node_measures(data_frame1())
# plot_hist_degree(data_frame2())
# plot_hist_path(data_frame3(data_frame1()))
# plot_power_law0(data_frame2())
# plot_power_law20(data_frame2())
# plot_power_law65(data_frame2())
# plot_power_law150(data_frame2())
# plot_power_law200(data_frame2())


############################################################################
# Attack scenarios NODE analysis plots
############################################################################


def data_frame_node():
    filenames = []
    concat_list = []
    # path that will be collected
    os.chdir(r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks")
    # Find any file that ends with ".txt"
    for files in os.listdir("."):
        if files.startswith("node"):
            filenames.append(files)  # apeend files names to a list

    def readfile(path):
        with open(path) as data:
            rho = path[path.rfind("node") + 11:len(path) - 4]
            attack_mode = path[path.rfind("node") + 5:path.rfind("node") + 11]
            searcher = reader(data, delimiter=',', quotechar='"')  # read file
            for line in searcher:
                step = int(line[0])
                nodes = int(line[1])
                links = int(line[2])
                max_degree = int(line[3])
                diameter = int(line[4])
                path_length = float(line[5])
                cluster_weak = int(line[6])
                cluster_strong = int(line[7])
                assortativity = float(line[8])
                cluster_coef = float(line[9])
                density = float(line[10])
                node_name = str(line[11])
                concat_list.append(
                    (attack_mode, rho, step, nodes, links, max_degree, diameter, path_length, cluster_weak,
                     cluster_strong, assortativity, cluster_coef, density, node_name))

    for fname in filenames:
        location = r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/" + fname
        readfile(location)

    df3 = pd.DataFrame(concat_list,
                           columns=["attack_mode", "rho", "step", "nodes", "links", "max_degree", "diameter",
                                    "path_length", "cluster_weak", "cluster_strong", "assortativity",
                                    "cluster_coef", "density", "node_name"])
    return df3


def plot_node_max_degree(df_random, df_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_degree_0 = df_random.max_degree[df_random.rho == '0']
    random_step_0 = df_random.step[df_random.rho == '0']
    target_degree_0 = df_target.max_degree[df_target.rho == '0']
    target_step_0 = df_random.step[df_random.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_degree_0, label='aleatório')
    plt.plot(target_step_0, target_degree_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('grau máximo')
    plt.legend(loc=5)

    random_degree_20 = df_random.max_degree[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_degree_20 = df_target.max_degree[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_degree_20, label='aleatório')
    plt.plot(target_step_20, target_degree_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=5)

    random_degree_65 = df_random.max_degree[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_degree_65 = df_target.max_degree[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_degree_65, label='aleatório')
    plt.plot(target_step_65, target_degree_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=5)

    random_degree_150 = df_random.max_degree[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_degree_150 = df_target.max_degree[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_degree_150, label='aleatório')
    plt.plot(target_step_150, target_degree_150, label='alvo')
    plt.title('rho = 150')
    plt.ylabel('grau máximo')
    plt.xlabel('interações')
    plt.legend(loc=5)

    random_degree_200 = df_random.max_degree[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_degree_200 = df_target.max_degree[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_degree_200, label='aleatório')
    plt.plot(target_step_200, target_degree_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=5)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=0.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_max_degree.pdf"
    plt.savefig(figure)


def plot_node_links(df_random, df_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_link_0 = df_random.links[df_random.rho == '0']
    random_step_0 = df_random.step[df_random.rho == '0']
    target_link_0 = df_target.links[df_target.rho == '0']
    target_step_0 = df_random.step[df_random.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_link_0, label='aleatório')
    plt.plot(target_step_0, target_link_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('número de links')
    plt.legend(loc=5)

    random_link_20 = df_random.links[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_link_20 = df_target.links[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_link_20, label='aleatório')
    plt.plot(target_step_20, target_link_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=5)

    random_link_65 = df_random.links[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_link_65 = df_target.links[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_link_65, label='aleatório')
    plt.plot(target_step_65, target_link_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=5)

    random_link_150 = df_random.links[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_link_150 = df_target.links[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_link_150, label='aleatório')
    plt.plot(target_step_150, target_link_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('número de links')
    plt.legend(loc=5)

    random_link_200 = df_random.links[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_link_200 = df_target.links[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_link_200, label='aleatório')
    plt.plot(target_step_200, target_link_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=5)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_links.pdf"
    plt.savefig(figure)


def plot_node_diameter(df_random, df_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_diameter_0 = df_random.diameter[df_random.rho == '0']
    random_step_0 = df_random.step[df_random.rho == '0']
    target_diameter_0 = df_target.diameter[df_target.rho == '0']
    target_step_0 = df_random.step[df_random.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_diameter_0, label='aleatório')
    plt.plot(target_step_0, target_diameter_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('diâmetro da rede')
    plt.legend(loc=2)

    random_diameter_20 = df_random.diameter[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_diameter_20 = df_target.diameter[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_diameter_20, label='aleatório')
    plt.plot(target_step_20, target_diameter_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=2)

    random_diameter_65 = df_random.diameter[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_diameter_65 = df_target.diameter[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_diameter_65, label='aleatório')
    plt.plot(target_step_65, target_diameter_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=2)

    random_diameter_150 = df_random.diameter[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_diameter_150 = df_target.diameter[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_diameter_150, label='aleatório')
    plt.plot(target_step_150, target_diameter_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('diâmetro da rede')
    plt.legend(loc=2)

    random_diameter_200 = df_random.diameter[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_diameter_200 = df_target.diameter[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_diameter_200, label='aleatório')
    plt.plot(target_step_200, target_diameter_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=1)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_diameter.pdf"
    plt.savefig(figure)


def plot_node_path(df_random, df_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_path_0 = df_random.path_length[df_random.rho == '0']
    random_step_0 = df_random.step[df_random.rho == '0']
    target_path_0 = df_target.path_length[df_target.rho == '0']
    target_step_0 = df_random.step[df_random.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_path_0, label='aleatório')
    plt.plot(target_step_0, target_path_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('caminho médio')
    plt.legend(loc=2)

    random_path_20 = df_random.path_length[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_path_20 = df_target.path_length[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_path_20, label='aleatório')
    plt.plot(target_step_20, target_path_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=2)

    random_path_65 = df_random.path_length[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_path_65 = df_target.path_length[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_path_65, label='aleatório')
    plt.plot(target_step_65, target_path_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=2)

    random_path_150 = df_random.path_length[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_path_150 = df_target.path_length[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_path_150, label='aleatório')
    plt.plot(target_step_150, target_path_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('caminho médio')
    plt.legend(loc=2)

    random_path_200 = df_random.path_length[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_path_200 = df_target.path_length[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_path_200, label='aleatório')
    plt.plot(target_step_200, target_path_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=1)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_path.pdf"
    plt.savefig(figure)


def plot_node_clusters(df_random, df_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_step_0 = df_random.step[df_random.rho == '0']
    target_step_0 = df_random.step[df_random.rho == '0']
    random_cluster_0 = df_random.cluster_weak[df_random.rho == '0']
    target_cluster_0 = df_target.cluster_weak[df_target.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_cluster_0, label='aleatório')
    plt.plot(target_step_0, target_cluster_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('componentes')
    plt.legend(loc=2)

    random_step_20 = df_random.step[df_random.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    random_cluster_20 = df_random.cluster_weak[df_random.rho == '20']
    target_cluster_20 = df_target.cluster_weak[df_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_cluster_20, label='aleatório')
    plt.plot(target_step_20, target_cluster_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=2)

    random_step_65 = df_random.step[df_random.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    random_cluster_65 = df_random.cluster_weak[df_random.rho == '65']
    target_cluster_65 = df_target.cluster_weak[df_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_cluster_65, label='aleatório')
    plt.plot(target_step_65, target_cluster_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=2)

    random_step_150 = df_random.step[df_random.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    random_cluster_150 = df_random.cluster_weak[df_random.rho == '150']
    target_cluster_150 = df_target.cluster_weak[df_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_cluster_150, label='aleatório')
    plt.plot(target_step_150, target_cluster_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('componentes')
    plt.legend(loc=2)

    random_step_200 = df_random.step[df_random.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    random_cluster_200 = df_random.cluster_weak[df_random.rho == '200']
    target_cluster_200 = df_target.cluster_weak[df_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_cluster_200, label='aleatório')
    plt.plot(target_step_200, target_cluster_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=2)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_clusters.pdf"
    plt.savefig(figure)


# node_random = data_frame_node()[data_frame_node().attack_mode == "random"]
# node_target = data_frame_node()[data_frame_node().attack_mode == "target"]

# plot_node_max_degree(node_random, node_target)
# plot_node_links(node_random, node_target)
# plot_node_diameter(node_random, node_target)
# plot_node_path(node_random, node_target)
# plot_node_clusters(node_random, node_target)


############################################################################
# Attack scenarios LINK analysis plots
############################################################################


def data_frame_link_random():
    filenames_random = []
    concat_list_random = []
    # path that will be collected
    os.chdir(r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks")
    # Find any file that ends with ".txt"
    for files in os.listdir("."):
        if files.startswith("link_random"):
            filenames_random.append(files)  # apeend files names to a list

    def readfile_random(path):
        with open(path) as data:
            rho = path[path.rfind("link_random") + 11:len(path) - 4]
            attack_mode = path[path.rfind("link_random") + 5:path.rfind("link_random") + 11]
            searcher = reader(data, delimiter=',', quotechar='"')  # read file
            for line in searcher:
                step = int(line[0])
                nodes = int(line[1])
                links = int(line[2])
                max_degree = int(line[3])
                diameter = int(line[4])
                path_length = float(line[5])
                cluster_weak = int(line[6])
                cluster_strong = int(line[7])
                assortativity = float(line[8])
                cluster_coef = float(line[9])
                density = float(line[10])
                link_name = str(line[11])
                concat_list_random.append(
                    (attack_mode, rho, step, nodes, links, max_degree, diameter, path_length, cluster_weak,
                     cluster_strong, assortativity, cluster_coef, density, link_name))

    for fname in filenames_random:
        location = r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/" + fname
        readfile_random(location)

    df4 = pd.DataFrame(concat_list_random,
                                  columns=["attack_mode", "rho", "step", "nodes", "links", "max_degree", "diameter",
                                           "path_length", "cluster_weak", "cluster_strong", "assortativity",
                                           "cluster_coef", "density", "link_name"])
    return df4


def data_frame_link_target():
    filenames_target = []
    concat_list_target = []
    # path that will be collected
    os.chdir(r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks")
    # Find any file that ends with ".txt"
    for files in os.listdir("."):
        if files.startswith("link_target"):
            filenames_target.append(files)  # apeend files names to a list

    def readfile_target(path):
        with open(path) as data:
            rho = path[path.rfind("link_target") + 11:len(path) - 4]
            attack_mode = path[path.rfind("link_target") + 5:path.rfind("link_target") + 11]
            searcher = reader(data, delimiter=',', quotechar='"')  # read file
            for line in searcher:
                step = int(line[0])
                nodes = int(line[1])
                links = int(line[2])
                max_degree = int(line[3])
                diameter = int(line[4])
                path_length = float(line[5])
                cluster_weak = int(line[6])
                cluster_strong = int(line[7])
                assortativity = float(line[8])
                cluster_coef = float(line[9])
                density = float(line[10])
                link_weight = int(line[11])
                link_name = str(line[12])
                concat_list_target.append(
                    (attack_mode, rho, step, nodes, links, max_degree, diameter, path_length, cluster_weak,
                     cluster_strong, assortativity, cluster_coef, density, link_weight, link_name))

    for fname in filenames_target:
        location = r"/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/" + fname
        readfile_target(location)

    df5 = pd.DataFrame(concat_list_target,
                                  columns=["attack_mode", "rho", "step", "nodes", "links", "max_degree", "diameter",
                                           "path_length", "cluster_weak", "cluster_strong", "assortativity",
                                           "cluster_coef", "density", "link_weight", "link_name"])
    return df5


def plot_link_max_degree(df_link_random, df_link_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_degree_0 = df_link_random.max_degree[df_link_random.rho == '0']
    random_step_0 = df_link_random.step[df_link_random.rho == '0']
    target_degree_0 = df_link_target.max_degree[df_link_target.rho == '0']
    target_step_0 = df_link_target.step[df_link_target.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_degree_0, label='aleatório')
    plt.plot(target_step_0, target_degree_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('grau máximo')
    plt.legend(loc=5)

    random_degree_20 = df_link_random.max_degree[df_link_random.rho == '20']
    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_degree_20 = df_link_target.max_degree[df_link_target.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_degree_20, label='aleatório')
    plt.plot(target_step_20, target_degree_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=5)

    random_degree_65 = df_link_random.max_degree[df_link_random.rho == '65']
    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_degree_65 = df_link_target.max_degree[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_degree_65, label='aleatório')
    plt.plot(target_step_65, target_degree_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=5)

    random_degree_150 = df_link_random.max_degree[df_link_random.rho == '150']
    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_degree_150 = df_link_target.max_degree[df_link_target.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_degree_150, label='aleatório')
    plt.plot(target_step_150, target_degree_150, label='alvo')
    plt.title('rho = 150')
    plt.ylabel('grau máximo')
    plt.xlabel('interações')
    plt.legend(loc=5)

    random_degree_200 = df_link_random.max_degree[df_link_random.rho == '200']
    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_degree_200 = df_link_target.max_degree[df_link_target.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_degree_200, label='aleatório')
    plt.plot(target_step_200, target_degree_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=5)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_link_max_degree.pdf"
    plt.savefig(figure)


def plot_link_diameter(df_link_random, df_link_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_diameter_0 = df_link_random.diameter[df_link_random.rho == '0']
    random_step_0 = df_link_random.step[df_link_random.rho == '0']
    target_diameter_0 = df_link_target.diameter[df_link_target.rho == '0']
    target_step_0 = df_link_target.step[df_link_target.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_diameter_0, label='aleatório')
    plt.plot(target_step_0, target_diameter_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('diâmetro da rede')
    plt.legend(loc=2)

    random_diameter_20 = df_link_random.diameter[df_link_random.rho == '20']
    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_diameter_20 = df_link_target.diameter[df_link_target.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_diameter_20, label='aleatório')
    plt.plot(target_step_20, target_diameter_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=2)

    random_diameter_65 = df_link_random.diameter[df_link_random.rho == '65']
    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_diameter_65 = df_link_target.diameter[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_diameter_65, label='aleatório')
    plt.plot(target_step_65, target_diameter_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=2)

    random_diameter_150 = df_link_random.diameter[df_link_random.rho == '150']
    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_diameter_150 = df_link_target.diameter[df_link_target.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_diameter_150, label='aleatório')
    plt.plot(target_step_150, target_diameter_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('diâmetro da rede')
    plt.legend(loc=2)

    random_diameter_200 = df_link_random.diameter[df_link_random.rho == '200']
    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_diameter_200 = df_link_target.diameter[df_link_target.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_diameter_200, label='aleatório')
    plt.plot(target_step_200, target_diameter_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=1)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_link_diameter.pdf"
    plt.savefig(figure)


def plot_link_path(df_link_random, df_link_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_path_0 = df_link_random.path_length[df_link_random.rho == '0']
    random_step_0 = df_link_random.step[df_link_random.rho == '0']
    target_path_0 = df_link_target.path_length[df_link_target.rho == '0']
    target_step_0 = df_link_target.step[df_link_target.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_path_0, label='aleatório')
    plt.plot(target_step_0, target_path_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('caminho médio')
    plt.legend(loc=2)

    random_path_20 = df_link_random.path_length[df_link_random.rho == '20']
    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_path_20 = df_link_target.path_length[df_link_target.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_path_20, label='aleatório')
    plt.plot(target_step_20, target_path_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=2)

    random_path_65 = df_link_random.path_length[df_link_random.rho == '65']
    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_path_65 = df_link_target.path_length[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_path_65, label='aleatório')
    plt.plot(target_step_65, target_path_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=2)

    random_path_150 = df_link_random.path_length[df_link_random.rho == '150']
    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_path_150 = df_link_target.path_length[df_link_target.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_path_150, label='aleatório')
    plt.plot(target_step_150, target_path_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('caminho médio')
    plt.legend(loc=2)

    random_path_200 = df_link_random.path_length[df_link_random.rho == '200']
    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_path_200 = df_link_target.path_length[df_link_target.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_path_200, label='aleatório')
    plt.plot(target_step_200, target_path_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=1)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_link_path.pdf"
    plt.savefig(figure)


def plot_link_clusters(df_link_random, df_link_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 6))

    random_step_0 = df_link_random.step[df_link_random.rho == '0']
    target_step_0 = df_link_target.step[df_link_target.rho == '0']
    random_cluster_0 = df_link_random.cluster_weak[df_link_random.rho == '0']
    target_cluster_0 = df_link_target.cluster_weak[df_link_target.rho == '0']
    plt.subplot(231)
    plt.plot(random_step_0, random_cluster_0, label='aleatório')
    plt.plot(target_step_0, target_cluster_0, label='alvo')
    plt.title('rho = 0')
    plt.ylabel('componentes')
    plt.legend(loc=2)

    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    random_cluster_20 = df_link_random.cluster_weak[df_link_random.rho == '20']
    target_cluster_20 = df_link_target.cluster_weak[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_cluster_20, label='aleatório')
    plt.plot(target_step_20, target_cluster_20, label='alvo')
    plt.title('rho = 20')
    plt.legend(loc=2)

    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    random_cluster_65 = df_link_random.cluster_weak[df_link_random.rho == '65']
    target_cluster_65 = df_link_target.cluster_weak[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_cluster_65, label='aleatório')
    plt.plot(target_step_65, target_cluster_65, label='alvo')
    plt.title('rho = 65')
    plt.xlabel('interações')
    plt.legend(loc=2)

    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    random_cluster_150 = df_link_random.cluster_weak[df_link_random.rho == '150']
    target_cluster_150 = df_link_target.cluster_weak[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_cluster_150, label='aleatório')
    plt.plot(target_step_150, target_cluster_150, label='alvo')
    plt.title('rho = 150')
    plt.xlabel('interações')
    plt.ylabel('componentes')
    plt.legend(loc=2)

    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    random_cluster_200 = df_link_random.cluster_weak[df_link_random.rho == '200']
    target_cluster_200 = df_link_target.cluster_weak[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_cluster_200, label='aleatório')
    plt.plot(target_step_200, target_cluster_200, label='alvo')
    plt.title('rho = 200')
    plt.xlabel('interações')
    plt.legend(loc=2)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_link_clusters.pdf"
    plt.savefig(figure)


# link_random = data_frame_link_random()
# link_target = data_frame_link_target()

# plot_link_max_degree(link_random, link_target)
# plot_link_diameter(link_random, link_target)
# plot_link_path(link_random, link_target)
# plot_link_clusters(link_random, link_target)


############################################################################
# Comparison NODE vs LINK scenarios plots
############################################################################

