import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from csv import reader
from igraph import *
import powerlaw
import os

############################################################################
# Statistical global measures rho
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
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
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
    sns.set_context("talk", font_scale=1, rc={"lines.linewidth": 1.5})
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
    plt.tight_layout(pad=0.4)
    figure1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_degree.pdf"
    plt.savefig(figure1, bbox_inches='tight', dpi=300)
    ##########################


    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1, rc={"lines.linewidth": 1.5})
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
    plt.tight_layout(pad=0.4)
    figure2 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_cluster.pdf"
    plt.savefig(figure2, bbox_inches='tight', dpi=300)
    ##########################


    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1, rc={"lines.linewidth": 1.5})
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
    plt.tight_layout(pad=0.4)
    figure3 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_path.pdf"
    plt.savefig(figure3, bbox_inches='tight', dpi=300)


def plot_global_efficiency(df1):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(8, 5))

    efficiency = (df1.index + 1) * df1['Tamanho médio do caminho']
    peak = efficiency.max() - 20

    plt.subplot(111)
    plt.plot(df1.index, efficiency)
    plt.fill_between(df1.index, 0, 4000, where=efficiency > peak, facecolor='r', alpha=0.3)
    plt.annotate('pico: 3876,12', xy=(185, 3876), xytext=(135, 3150))
    plt.xlabel('rho')
    plt.ylabel('eficiência')
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_global_efficiency.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_node_measures(df1):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(10, 4), dpi=300)

    plt.subplot(121)
    plt.plot(df1.iloc[:, 4:5], label='k-all')
    plt.plot(df1.iloc[:, 5:6], label='k-in')
    plt.plot(df1.iloc[:, 6:7], label='k-out')
    plt.title('Média (a)')
    plt.xlabel('rho')
    plt.ylabel('grau do nó')
    plt.ylim(0, 70)
    plt.legend(loc=2)

    plt.subplot(122)
    plt.plot(df1.iloc[:, 7:8], label='k-all')
    plt.plot(df1.iloc[:, 8:9], label='k-in')
    plt.plot(df1.iloc[:, 9:10], label='k-out')
    plt.title('Mediana (b)')
    plt.xlabel('rho')
    plt.ylabel('grau do nó')
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


def plot_hist_path_5(df3):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(8, 6))

    path_0 = df3.path[df3.rho == 0]
    freq_0 = df3.freq_norm[df3.rho == 0]
    path_20 = df3.path[df3.rho == 20]
    freq_20 = df3.freq_norm[df3.rho == 20]
    path_65 = df3.path[df3.rho == 65]
    freq_65 = df3.freq_norm[df3.rho == 65]
    path_150 = df3.path[df3.rho == 150]
    freq_150 = df3.freq_norm[df3.rho == 150]
    path_200 = df3.path[df3.rho == 200]
    freq_200 = df3.freq_norm[df3.rho == 200]

    with sns.color_palette("muted"):
        plt.plot(path_0, freq_0, 'b', label='rho 0', alpha=.3)
        plt.fill_between(path_0, freq_0, color='b', alpha=.3)
        plt.plot(path_20, freq_20, 'g', label='rho 20', alpha=.7)
        plt.fill_between(path_20, freq_20, color='g', alpha=.5)
        plt.plot(path_65, freq_65, 'r', label='rho 65', alpha=.7)
        plt.fill_between(path_65, freq_65, color='r', alpha=.7)
        plt.plot(path_150, freq_150, 'c', label='rho 150', alpha=1)
        plt.fill_between(path_150, freq_150, color='c', alpha=1)
        plt.plot(path_200, freq_200, 'm', label='rho 200', alpha=1)
        plt.fill_between(path_200, freq_200, color='m', alpha=1)
        plt.xlabel('caminho médio')
        plt.ylabel('frequência')
        plt.legend()

    plt.tight_layout()
    # plt.xlabel('caminho médio')
    # plt.ylabel('frequência')
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_hist_path_5.pdf"
    plt.savefig(figure, dpi=300)


def plot_power_law0():

    degrees_0 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/hist0.txt"
    result_0 = []
    with open(degrees_0, "r") as degree:
        searcher = reader(degree, delimiter=',')
        for line in searcher:
            freq = int(line[2])
            result_0.append(freq)

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(6, 4))

    fit = powerlaw.Fit(result_0)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_pdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_pdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_pdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p(k)")
    fig.set_xlabel("grau (k)")
    fig.set_title("rho = 0")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law0.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law20():

    degrees_20 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/hist20.txt"
    result_20 = []
    with open(degrees_20, "r") as degree:
        searcher = reader(degree, delimiter=',')
        for line in searcher:
            freq = int(line[2])
            result_20.append(freq)

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(6, 4))

    fit = powerlaw.Fit(result_20)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_pdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_pdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_pdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p(k)")
    fig.set_xlabel("grau (k)")
    fig.set_title("rho = 20")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law20.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law65():

    degrees_65 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/hist65.txt"
    result_65 = []
    with open(degrees_65, "r") as degree:
        searcher = reader(degree, delimiter=',')
        for line in searcher:
            freq = int(line[2])
            result_65.append(freq)

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(6, 4))

    fit = powerlaw.Fit(result_65)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_pdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_pdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_pdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p(k)")
    fig.set_xlabel("grau (k)")
    fig.set_title("rho = 65")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law65.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law150():

    degrees_150 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/hist150.txt"
    result_150 = []
    with open(degrees_150, "r") as degree:
        searcher = reader(degree, delimiter=',')
        for line in searcher:
            freq = int(line[2])
            result_150.append(freq)

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(6, 4))

    fit = powerlaw.Fit(result_150)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_pdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_pdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_pdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p(k)")
    fig.set_xlabel("grau (k)")
    fig.set_title("rho = 150")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law150.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def plot_power_law200():
    degrees_200 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/hist200.txt"
    result_200 = []
    with open(degrees_200, "r") as degree:
        searcher = reader(degree, delimiter=',')
        for line in searcher:
            freq = int(line[2])
            result_200.append(freq)

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=1)
    plt.figure(facecolor="white", figsize=(6, 4))

    fit = powerlaw.Fit(result_200)
    fit.distribution_compare('power_law', 'lognormal')
    fig = fit.plot_pdf(linewidth=3, label='Dado empírico')
    fit.power_law.plot_pdf(ax=fig, color='r', linestyle='--', label='Power law fit')
    fit.lognormal.plot_pdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')

    fig.set_ylabel(u"p(k)")
    fig.set_xlabel("grau (k)")
    fig.set_title("rho = 200")
    handles, labels = fig.get_legend_handles_labels()
    fig.legend(handles, labels, loc=3)

    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/plot_power_law200.pdf"
    plt.savefig(figure, bbox_inches='tight', dpi=300)


def get_max_degree_nodes():

    graph_65 = Graph.Read_GraphML("/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net65.graphml")

    def grouped_stops():
        group_dict = dict()
        grouped = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/groups/grouped65.txt"
        with open(grouped, "r", newline='') as data:
            searcher = reader(data, delimiter=',')
            for line in searcher:
                stop_old = line[0]
                stop_new = line[1]
                group_dict[stop_old] = stop_new
        return group_dict

    def get_stop_names():
        stops_dict = dict()
        grouped = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stops.txt"
        with open(grouped, "r", newline='\n') as data:
            searcher = reader(data, delimiter=',')
            for line in searcher:
                stop_id = line[0]
                stop_name = str(line[1])
                stops_dict[stop_id] = stop_name
        return stops_dict

    def get_grouped_names(group_dict, stops_dict):
        max_nodes = []
        degrees = sorted(graph_65.degree(mode=ALL, loops=True), reverse=True)
        for degree in degrees[:10]:
            stops = graph_65.vs(_degree=degree)['name']
            for name in stops:
                for stop1, stop2 in group_dict.items():
                    if stop2 == name:
                        old_stop = group_dict[stop1]
                        desc = stops_dict[stop1]
                        max_nodes.append((stop1, stop2, degree, desc))
        return max_nodes

    def count_stops(max_nodes):
        counts = []
        for i in max_nodes:
            old = i[0]
            new = i[1]
            counts.append(new)
        result = dict(Counter(counts))
        return result

    stops = list(get_grouped_names(grouped_stops(), get_stop_names()))
    # count_stops(stops)
    return stops


# plot_global_measures(data_frame1())
# plot_global_measures_sep(data_frame1())
# plot_global_efficiency(data_frame1())
# plot_node_measures(data_frame1())
# plot_hist_degree(data_frame2())
# plot_hist_path(data_frame3(data_frame1()))
# plot_hist_path_5(data_frame3(data_frame1()))
# plot_power_law0()
# plot_power_law20()
# plot_power_law65()
# plot_power_law150()
# plot_power_law200()


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
    plt.plot(target_step_0, target_degree_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('grau máximo')
    plt.ylim(0, 140)
    plt.legend(loc=5)

    random_degree_20 = df_random.max_degree[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_degree_20 = df_target.max_degree[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_degree_20, label='aleatório')
    plt.plot(target_step_20, target_degree_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(0, 1000)
    plt.legend(loc=5)

    random_degree_65 = df_random.max_degree[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_degree_65 = df_target.max_degree[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_degree_65, label='aleatório')
    plt.plot(target_step_65, target_degree_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(0, 1200)
    plt.legend(loc=5)

    random_degree_150 = df_random.max_degree[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_degree_150 = df_target.max_degree[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_degree_150, label='aleatório')
    plt.plot(target_step_150, target_degree_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.ylabel('grau máximo')
    plt.xlabel('nós removidos')
    plt.ylim(0, 4000)
    plt.legend(loc=5)

    random_degree_200 = df_random.max_degree[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_degree_200 = df_target.max_degree[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_degree_200, label='aleatório')
    plt.plot(target_step_200, target_degree_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(0, 7000)
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
    plt.plot(target_step_0, target_link_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('quantidade de links')
    plt.ylim(40000, 100000)
    plt.legend(loc=3)

    random_link_20 = df_random.links[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_link_20 = df_target.links[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_link_20, label='aleatório')
    plt.plot(target_step_20, target_link_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(40000, 100000)
    plt.legend(loc=3)

    random_link_65 = df_random.links[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_link_65 = df_target.links[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_link_65, label='aleatório')
    plt.plot(target_step_65, target_link_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(40000, 100000)
    plt.legend(loc=3)

    random_link_150 = df_random.links[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_link_150 = df_target.links[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_link_150, label='aleatório')
    plt.plot(target_step_150, target_link_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('quantidade de links')
    plt.ylim(40000, 100000)
    plt.legend(loc=3)

    random_link_200 = df_random.links[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_link_200 = df_target.links[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_link_200, label='aleatório')
    plt.plot(target_step_200, target_link_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(40000, 100000)
    plt.legend(loc=3)

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
    plt.plot(target_step_0, target_diameter_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('diâmetro da rede')
    plt.ylim(50, 220)
    plt.legend(loc=3)

    random_diameter_20 = df_random.diameter[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_diameter_20 = df_target.diameter[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_diameter_20, label='aleatório')
    plt.plot(target_step_20, target_diameter_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(50, 220)
    plt.legend(loc=3)

    random_diameter_65 = df_random.diameter[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_diameter_65 = df_target.diameter[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_diameter_65, label='aleatório')
    plt.plot(target_step_65, target_diameter_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(50, 220)
    plt.legend(loc=3)

    random_diameter_150 = df_random.diameter[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_diameter_150 = df_target.diameter[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_diameter_150, label='aleatório')
    plt.plot(target_step_150, target_diameter_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('diâmetro da rede')
    plt.ylim(50, 220)
    plt.legend(loc=2)

    random_diameter_200 = df_random.diameter[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_diameter_200 = df_target.diameter[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_diameter_200, label='aleatório')
    plt.plot(target_step_200, target_diameter_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(50, 220)
    plt.legend(loc=2)

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
    plt.plot(target_step_0, target_path_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('caminho médio')
    plt.ylim(0, 65)
    plt.legend(loc=3)

    random_path_20 = df_random.path_length[df_random.rho == '20']
    random_step_20 = df_random.step[df_random.rho == '20']
    target_path_20 = df_target.path_length[df_target.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_path_20, label='aleatório')
    plt.plot(target_step_20, target_path_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(0, 65)
    plt.legend(loc=3)

    random_path_65 = df_random.path_length[df_random.rho == '65']
    random_step_65 = df_random.step[df_random.rho == '65']
    target_path_65 = df_target.path_length[df_target.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_path_65, label='aleatório')
    plt.plot(target_step_65, target_path_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(0, 65)
    plt.legend(loc=3)

    random_path_150 = df_random.path_length[df_random.rho == '150']
    random_step_150 = df_random.step[df_random.rho == '150']
    target_path_150 = df_target.path_length[df_target.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_path_150, label='aleatório')
    plt.plot(target_step_150, target_path_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('caminho médio')
    plt.ylim(0, 65)
    plt.legend(loc=3)

    random_path_200 = df_random.path_length[df_random.rho == '200']
    random_step_200 = df_random.step[df_random.rho == '200']
    target_path_200 = df_target.path_length[df_target.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_path_200, label='aleatório')
    plt.plot(target_step_200, target_path_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(0, 65)
    plt.legend(loc=3)

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
    plt.plot(target_step_0, target_cluster_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('componentes')
    plt.ylim(0, 250)
    plt.legend(loc=2)

    random_step_20 = df_random.step[df_random.rho == '20']
    target_step_20 = df_random.step[df_random.rho == '20']
    random_cluster_20 = df_random.cluster_weak[df_random.rho == '20']
    target_cluster_20 = df_target.cluster_weak[df_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_cluster_20, label='aleatório')
    plt.plot(target_step_20, target_cluster_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(0, 250)
    plt.legend(loc=2)

    random_step_65 = df_random.step[df_random.rho == '65']
    target_step_65 = df_random.step[df_random.rho == '65']
    random_cluster_65 = df_random.cluster_weak[df_random.rho == '65']
    target_cluster_65 = df_target.cluster_weak[df_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_cluster_65, label='aleatório')
    plt.plot(target_step_65, target_cluster_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(0, 250)
    plt.legend(loc=2)

    random_step_150 = df_random.step[df_random.rho == '150']
    target_step_150 = df_random.step[df_random.rho == '150']
    random_cluster_150 = df_random.cluster_weak[df_random.rho == '150']
    target_cluster_150 = df_target.cluster_weak[df_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_cluster_150, label='aleatório')
    plt.plot(target_step_150, target_cluster_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('componentes')
    plt.ylim(0, 250)
    plt.legend(loc=2)

    random_step_200 = df_random.step[df_random.rho == '200']
    target_step_200 = df_random.step[df_random.rho == '200']
    random_cluster_200 = df_random.cluster_weak[df_random.rho == '200']
    target_cluster_200 = df_target.cluster_weak[df_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_cluster_200, label='aleatório')
    plt.plot(target_step_200, target_cluster_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(0, 250)
    plt.legend(loc=2)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_clusters.pdf"
    plt.savefig(figure)


def plot_node_cuts():

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.9, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(6, 3))

    cuts_x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105,
              110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200]
    cuts_y = [13.45, 13.93, 15.14, 16.57, 17.01, 17.19, 17.09, 17.57, 17.19, 16.59, 16.56, 16.70, 16.38,
              15.84, 15.70, 15.62, 15.23, 14.98, 14.83, 14.59, 14.44, 14.26, 14.12, 13.97, 13.69, 13.27,
              13.03, 12.82, 12.62, 12.04, 12.00, 11.64, 11.34, 10.97, 10.79, 10.27, 9.72, 9.31, 8.91, 8.37, 8.17]

    plt.plot(cuts_x, cuts_y, label='% nós à remover')
    plt.xlabel('rho')
    plt.ylabel('porcentagem de nós [%]')
    plt.ylim(0, 20)
    plt.legend(loc=3)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_node_cuts.pdf"
    plt.savefig(figure)


# node_random = data_frame_node()[data_frame_node().attack_mode == "random"]
# node_target = data_frame_node()[data_frame_node().attack_mode == "target"]

# plot_node_max_degree(node_random, node_target)
# plot_node_links(node_random, node_target)
# plot_node_diameter(node_random, node_target)
# plot_node_path(node_random, node_target)
# plot_node_clusters(node_random, node_target)
# plot_node_cuts()


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
    plt.plot(target_step_0, target_degree_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('grau máximo')
    plt.ylim(0, 140)
    plt.legend(loc=3)

    random_degree_20 = df_link_random.max_degree[df_link_random.rho == '20']
    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_degree_20 = df_link_target.max_degree[df_link_target.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_degree_20, label='aleatório')
    plt.plot(target_step_20, target_degree_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(0, 1000)
    plt.legend(loc=3)

    random_degree_65 = df_link_random.max_degree[df_link_random.rho == '65']
    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_degree_65 = df_link_target.max_degree[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_degree_65, label='aleatório')
    plt.plot(target_step_65, target_degree_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(0, 1200)
    plt.legend(loc=3)

    random_degree_150 = df_link_random.max_degree[df_link_random.rho == '150']
    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_degree_150 = df_link_target.max_degree[df_link_target.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_degree_150, label='aleatório')
    plt.plot(target_step_150, target_degree_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.ylabel('grau máximo')
    plt.xlabel('nós removidos')
    plt.ylim(0, 4000)
    plt.legend(loc=3)

    random_degree_200 = df_link_random.max_degree[df_link_random.rho == '200']
    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_degree_200 = df_link_target.max_degree[df_link_target.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_degree_200, label='aleatório')
    plt.plot(target_step_200, target_degree_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(0, 7000)
    plt.legend(loc=3)

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
    plt.plot(target_step_0, target_diameter_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('diâmetro da rede')
    plt.ylim(0, 180)
    plt.legend(loc=3)

    random_diameter_20 = df_link_random.diameter[df_link_random.rho == '20']
    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_diameter_20 = df_link_target.diameter[df_link_target.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_diameter_20, label='aleatório')
    plt.plot(target_step_20, target_diameter_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(0, 180)
    plt.legend(loc=3)

    random_diameter_65 = df_link_random.diameter[df_link_random.rho == '65']
    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_diameter_65 = df_link_target.diameter[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_diameter_65, label='aleatório')
    plt.plot(target_step_65, target_diameter_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(120, 180)
    plt.legend(loc=6)

    random_diameter_150 = df_link_random.diameter[df_link_random.rho == '150']
    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_diameter_150 = df_link_target.diameter[df_link_target.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_diameter_150, label='aleatório')
    plt.plot(target_step_150, target_diameter_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('diâmetro da rede')
    plt.ylim(0, 180)
    plt.legend(loc=3)

    random_diameter_200 = df_link_random.diameter[df_link_random.rho == '200']
    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_diameter_200 = df_link_target.diameter[df_link_target.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_diameter_200, label='aleatório')
    plt.plot(target_step_200, target_diameter_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(0, 180)
    plt.legend(loc=3)

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
    plt.plot(target_step_0, target_path_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('caminho médio')
    plt.ylim(54.90, 55.2)
    plt.legend(loc=1)

    random_path_20 = df_link_random.path_length[df_link_random.rho == '20']
    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_path_20 = df_link_target.path_length[df_link_target.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_path_20, label='aleatório')
    plt.plot(target_step_20, target_path_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(50.90, 51.2)
    plt.legend(loc=1)

    random_path_65 = df_link_random.path_length[df_link_random.rho == '65']
    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_path_65 = df_link_target.path_length[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_path_65, label='aleatório')
    plt.plot(target_step_65, target_path_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(33, 36)
    plt.legend(loc=1)

    random_path_150 = df_link_random.path_length[df_link_random.rho == '150']
    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_path_150 = df_link_target.path_length[df_link_target.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_path_150, label='aleatório')
    plt.plot(target_step_150, target_path_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('caminho médio')
    plt.ylim(24.40, 24.60)
    plt.legend(loc=1)

    random_path_200 = df_link_random.path_length[df_link_random.rho == '200']
    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_path_200 = df_link_target.path_length[df_link_target.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_path_200, label='aleatório')
    plt.plot(target_step_200, target_path_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(18.90, 19.20)
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
    plt.plot(target_step_0, target_cluster_0, label='alvo determinístico')
    plt.title('rho = 0')
    plt.ylabel('componentes')
    plt.ylim(0, 16)
    plt.legend(loc=4)

    random_step_20 = df_link_random.step[df_link_random.rho == '20']
    target_step_20 = df_link_target.step[df_link_target.rho == '20']
    random_cluster_20 = df_link_random.cluster_weak[df_link_random.rho == '20']
    target_cluster_20 = df_link_target.cluster_weak[df_link_target.rho == '20']
    plt.subplot(232)
    plt.plot(random_step_20, random_cluster_20, label='aleatório')
    plt.plot(target_step_20, target_cluster_20, label='alvo determinístico')
    plt.title('rho = 20')
    plt.ylim(0, 16)
    plt.legend(loc=1)

    random_step_65 = df_link_random.step[df_link_random.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    random_cluster_65 = df_link_random.cluster_weak[df_link_random.rho == '65']
    target_cluster_65 = df_link_target.cluster_weak[df_link_target.rho == '65']
    plt.subplot(233)
    plt.plot(random_step_65, random_cluster_65, label='aleatório')
    plt.plot(target_step_65, target_cluster_65, label='alvo determinístico')
    plt.title('rho = 65')
    plt.xlabel('nós removidos')
    plt.ylim(0, 16)
    plt.legend(loc=1)

    random_step_150 = df_link_random.step[df_link_random.rho == '150']
    target_step_150 = df_link_target.step[df_link_target.rho == '150']
    random_cluster_150 = df_link_random.cluster_weak[df_link_random.rho == '150']
    target_cluster_150 = df_link_target.cluster_weak[df_link_target.rho == '150']
    plt.subplot(234)
    plt.plot(random_step_150, random_cluster_150, label='aleatório')
    plt.plot(target_step_150, target_cluster_150, label='alvo determinístico')
    plt.title('rho = 150')
    plt.xlabel('nós removidos')
    plt.ylabel('componentes')
    plt.ylim(0, 16)
    plt.legend(loc=1)

    random_step_200 = df_link_random.step[df_link_random.rho == '200']
    target_step_200 = df_link_target.step[df_link_target.rho == '200']
    random_cluster_200 = df_link_random.cluster_weak[df_link_random.rho == '200']
    target_cluster_200 = df_link_target.cluster_weak[df_link_target.rho == '200']
    plt.subplot(235)
    plt.plot(random_step_200, random_cluster_200, label='aleatório')
    plt.plot(target_step_200, target_cluster_200, label='alvo determinístico')
    plt.title('rho = 200')
    plt.xlabel('nós removidos')
    plt.ylim(0, 16)
    plt.legend(loc=1)

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

def plot_node_versus_link(df_target, df_link_target):
    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(11, 3))

    node_target_step_65 = df_target.step[df_target.rho == '65']
    node_target_cluster_65 = df_target.cluster_weak[df_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    target_cluster_65 = df_link_target.cluster_weak[df_link_target.rho == '65']
    plt.subplot(131)
    plt.plot(node_target_step_65, node_target_cluster_65, label='nós')
    plt.plot(target_step_65, target_cluster_65, label='links')
    plt.title('estratégia alvo determinístico rho 65 (a)')
    plt.xlabel('nós removidos')
    plt.ylabel('componentes')
    plt.ylim(0, 60)
    plt.legend(loc=4)

    node_target_path_65 = df_target.path_length[df_target.rho == '65']
    node_target_step_65 = df_target.step[df_target.rho == '65']
    target_path_65 = df_link_target.path_length[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(132)
    plt.plot(node_target_step_65, node_target_path_65, label='nós')
    plt.plot(target_step_65, target_path_65, label='links')
    plt.title('estratégia alvo determinístico rho 65 (b)')
    plt.xlabel('nós removidos')
    plt.ylabel('caminho médio')
    plt.ylim(0, 70)
    plt.legend(loc=4)

    node_target_diameter_65 = df_target.diameter[df_target.rho == '65']
    node_target_step_65 = df_target.step[df_target.rho == '65']
    target_diameter_65 = df_link_target.diameter[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(133)
    plt.plot(node_target_step_65, node_target_diameter_65, label='nós')
    plt.plot(target_step_65, target_diameter_65, label='links')
    plt.title('estratégia alvo determinístico rho 65 (c)')
    plt.xlabel('nós removidos')
    plt.ylabel('diâmetro da rede')
    plt.ylim(0, 200)
    plt.legend(loc=4)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_versus_global.pdf"
    plt.savefig(figure)


def plot_node_max_link(df_target, df_link_target):

    sns.set_style("darkgrid")
    sns.set_context("talk", font_scale=0.8, rc={"lines.linewidth": 1.5})
    plt.figure(facecolor="white", figsize=(5, 3))

    node_target_degree_65 = df_target.max_degree[df_target.rho == '65']
    node_target_step_65 = df_target.step[df_target.rho == '65']
    target_degree_65 = df_link_target.max_degree[df_link_target.rho == '65']
    target_step_65 = df_link_target.step[df_link_target.rho == '65']
    plt.subplot(111)
    plt.plot(node_target_step_65, node_target_degree_65, label='nós')
    plt.plot(target_step_65, target_degree_65, label='links')
    plt.title('estratégia alvo determinístico rho 65')
    plt.xlabel('nós removidos')
    plt.ylabel('grau máximo')

    # plt.ylim(0, 1200)
    plt.legend(loc=1)

    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.5)
    figure = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/attack_versus_max.pdf"
    plt.savefig(figure)

# plot_node_versus_link(node_target, link_target)
# plot_node_max_link(node_target, link_target)


