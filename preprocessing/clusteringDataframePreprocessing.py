import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from amenities import amenities_matrix



def clustering_preprocessing(dataframe,cleaned_dataframe):
    """
    :param dataframe: di output da utilizzare per il clustering
    :param cleaned_dataframe: dataframe pulito per creare le amenities
    :return:dataframe pronto per il clustering
    """

    amenities = amenities_matrix(cleaned_dataframe, (len(dataframe) / 3))

    to_drop = list(dataframe.select_dtypes(['O']).columns) + ['neighbourhood_cleansed']
    dataframe.drop(to_drop, axis=1, inplace=True)
    dataframe = dataframe.reset_index()
    dataframe.drop('index', axis=1, inplace=True)

    amenities = amenities.reset_index()
    amenities.drop('index', axis=1, inplace=True)
    dataframe = pd.concat([dataframe, amenities], axis=1)

    # numero massimo id componenst sono 30
    pca = PCA(n_components=20)
    pca.fit(dataframe)
    features = pca.transform(dataframe)
    dataframe = pd.DataFrame(features)
    scaler = MinMaxScaler()
    print("Min Max scaler ....")
    dataframe = pd.DataFrame(scaler.fit_transform(dataframe), columns=dataframe.columns)
    dataframe.round(10)
    print("Scaler Done.")

    return dataframe