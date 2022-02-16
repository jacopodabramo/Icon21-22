from os import path
from sys import argv

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from matplotlib.pyplot import xlabel,ylabel,plot,show,title


def k_cluster(dataframe,k,max):
    """
    :param dataframe: dataframe con le features da utilizzare per il clustering
    :param k: numero di cluster
    :param max_it: numero massimo di iterate
    :return: i cluster crati
    """
    print("Creating clusters...")

    km = KMeans(n_clusters=k,max_iter=max)
    clusters = km.fit_predict(dataframe)
    return clusters

def elbow_plot(dataframe,it):
    """
    :param dataframe:
    :param it: numero di iterate
    questa funzione serve per trovare la lista delle somma al quadrato all'aumentare delle iterate
    per poi mostrare attraverso un grafico l'elbow
    L'elbow rappresenta il numero idela di cluster in base alle features e al dataframe
    All'aumentare delle iterate l'elbow sarà più preciso
    """
    sq = []
    l = range(1,it)

    for i in l:
        km = KMeans(n_clusters=i,max_iter=it)
        km.fit(dataframe)
        sq.append(km.inertia_) #inseriamo le somme degli errori al quadrato
    title("Elbow graphic")
    xlabel('k')
    ylabel('Sum of squared error')
    plot(l,sq,'-ok')
    show()


def main():
    try:
        dataframe = pd.read_csv(argv[1])
        k = int(argv[2])  # number of cluster
        it = int(argv[3]) # number of iterations
        clusters = k_cluster(dataframe, k, it)
        df_prolog = pd.read_csv('./datasets/prolog_dataframe.csv')
        df_prolog['cluster'] = clusters
        df_prolog.to_csv('./datasets/prolog_dataframe.csv',index = False)
        #elbow_plot(dataframe,it)
        print("Clustering Done.")

    except FileNotFoundError as e:
        print("File not found",e)
    except Exception as e:
        print(e)


main()