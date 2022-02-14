import re
import pandas as pd
import numpy as np
from collections import Counter
from itertools import dropwhile, takewhile


def splitting_amenities(element):
    list_of_amenities = element.split(',')
    list_of_amenities = [word.lower() for word in list_of_amenities]
    return list_of_amenities

def amenities_matrix(dataframe, treshold):

    dataframe['amenities'] = dataframe['amenities'].apply(lambda x: x[1:-1])
    dataframe['amenities'] = dataframe['amenities'].apply(lambda x: x.replace(', ', ','))
    dataframe['amenities'] = dataframe['amenities'].apply(lambda x: x.replace(' , ', ','))
    dataframe['amenities'] = dataframe['amenities'].apply(lambda x: re.sub(r'(?<=[a-zA-Z0-9])[,](?=[a-zA-Z0-9])', ' ', x))


    #controllare la ridondanza
    w_count = Counter()
    dataframe['amenities'].str.lower().str.split(',').apply(w_count.update)
    w_count.most_common()
    lista = []
    for amenities in w_count:
        if w_count[amenities] <= treshold:
            lista.append(amenities)
    for element in lista:
        del w_count[element]
    bow = list(w_count.keys())

    #definisco un dizionario
    columnIndex = dataframe.columns.get_loc('amenities')
    to_add_row = []
    index = 0
    indexAmenities = {}

    for i in range(len(dataframe.amenities)):
        element = dataframe.iloc[i, columnIndex]
        list_of_amenities = splitting_amenities(element)
        list_of_amenities = list(set(list_of_amenities) & set(bow))
        to_add_row.append(list_of_amenities)
        for word in list_of_amenities:
            if word not in indexAmenities:
                indexAmenities[word] = index
                index += 1

    rows = len(dataframe.amenities)
    columns = len(indexAmenities)

    amenities_matrix = np.zeros((rows, columns))
    i = 0
    for row in to_add_row:
        amenities_matrix[i, :] = writer(row, columns, indexAmenities)
        i += 1

    amenities_dataframe = pd.DataFrame(amenities_matrix, columns=list(indexAmenities.keys())).astype("boolean")
    amenities_dataframe.columns = [cleaning_column(text) for text in list(amenities_dataframe.columns)]

    return amenities_dataframe


def writer(row, columns, indexes):
    written_columns = np.zeros(columns)
    for value in row:
        idx = indexes[value]
        written_columns[idx] = 1
    return written_columns


def cleaning_column(e):
    e = re.sub(r'[\s+]]*', '_', e)
    e = re.sub(r'[\"]', '', e)

    return e