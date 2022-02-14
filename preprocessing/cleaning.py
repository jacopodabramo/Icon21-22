import pandas as pd
import re
from sys import argv
import numpy as np
from os import path

from sklearn.impute import SimpleImputer

"""
Knowledge base: prezzo,letti:(famigla ,ragazzi),numero bagni, superhost, centro, 
                rating,permanenza(breve,lunga) tra minimo notti,
                Rating = stampiamo per ordine di Rating


Belief Network: inserisce le proprietà che piacciono all'utente e predice quale potrebbe essere una stanza che potrebbero
                piacere all'utente
    Features: usiamo stesse features della Knowledge base 
              viene aggiunta la colonna di booleani che ci indica se un hotel si trova vicino al centro
            
Clustering: ?

"""

def is_center(column,center):
    """
    :param column: corrisponde al quartiere
    center:lista di quartieri del centro
    :return: True se il quartiere è in centro
            False altrimenti
    """

    for i in range(0,len(center)):
        if center[i] == column:
            return True
    return False

def cleaning_dataset(dataframe):
    """
    :param dataframe indica il dataset:
    :return il dataframe pulito con le tabelle eliminate e pronto per essere usato
    """
    print("Cleaning...")

    dataframe = dataframe.drop(["listing_url", "scrape_id", "last_scraped", "neighborhood_overview",
                          "picture_url", "host_id", "host_url", "host_name", "host_since", "host_location",
                          "host_about", "host_thumbnail_url", "host_picture_url", "host_neighbourhood",
                          "neighbourhood_group_cleansed", "latitude", "longitude", "bathrooms",
                          "minimum_minimum_nights", "maximum_minimum_nights",
                          "minimum_maximum_nights", "maximum_maximum_nights", "minimum_nights_avg_ntm",
                          "maximum_nights_avg_ntm", "calendar_updated", "availability_30",
                          "availability_60", "availability_90", "availability_365", "calendar_last_scraped",
                          "number_of_reviews_ltm", "number_of_reviews_l30d", "first_review", "last_review", "license",
                          "calculated_host_listings_count", "calculated_host_listings_count_entire_homes",
                          "calculated_host_listings_count_private_rooms",
                          "calculated_host_listings_count_shared_rooms", "reviews_per_month","host_has_profile_pic",
                          "host_acceptance_rate","host_listings_count","host_total_listings_count","review_scores_accuracy",
                          "review_scores_checkin","review_scores_communication"
                          ], axis=1)
    dataframe = dataframe[dataframe.property_type.isin(['Entire apartment', 'Private room in apartment',
                                               'Private room in house', 'Private room in townhouse',
                                               'Entire condominium', 'Entire house', 'Entire loft',
                                               'Entire townhouse', 'Entire rental unit'])]

    # elimino le colonne dove le bedrooms non sono inserite, non avrebbe senso prendere in
    # considerazioni hotel dove i letti non sono inseriti
    dataframe = dataframe.drop(dataframe[dataframe.bedrooms.isnull()].index)
    dataframe["bedrooms"] = dataframe["bedrooms"].astype('int')

    #elimino spazi sostituendoli con l'underscore
    dataframe['property_type'] = dataframe.property_type.apply(lambda c: re.sub(' ', '_', c))
    dataframe['room_type'] = dataframe.room_type.apply(lambda c: re.sub(' ', '_', c))

    #cancello tutto quello che sta dopo il trattino
    dataframe["neighbourhood_cleansed"] = dataframe["neighbourhood_cleansed"].apply(lambda c: re.sub('[\s][-][\s][\S]+', '', c))
    dataframe["neighbourhood_cleansed"] = dataframe["neighbourhood_cleansed"].apply(lambda c: re.sub("[']", '', c)).astype('category')
    #elimino il $ dal colonna presso e converto in float
    dataframe['price'] = dataframe.price.apply(lambda c: re.sub('[$,]', '', c)).astype('float')

    # nei letti inserisco valori numerici e inserisco la media per le celle vuote
    dataframe["beds"] = SimpleImputer(strategy='median').fit_transform(dataframe[["beds"]]).round()
    dataframe["beds"] = dataframe["beds"].astype('int')

    # nei bagni inserisco valori numerici e inserisco la media per le celle vuote arrotondandole
    most_frequent = SimpleImputer(strategy='most_frequent')
    dataframe.loc[:, 'bathrooms_text'] = most_frequent.fit_transform(dataframe[['bathrooms_text']])
    dataframe["bathrooms_text"] = dataframe.bathrooms_text.apply(lambda c : re.sub('[a-z]*', '', c)).astype('float').round()

    # Operazione discretizzazione sulle boolean

    dataframe['host_is_superhost'] = dataframe.host_is_superhost.apply(lambda c: 1 if c == 't' else 0)
    dataframe['has_availability'] = dataframe.has_availability.apply(lambda c: 1 if c == 't' else 0)
    dataframe['instant_bookable'] = dataframe.instant_bookable.apply(lambda c: 1 if c == 't' else 0)
    dataframe['host_identity_verified'] = dataframe.host_identity_verified.apply(lambda c: 1 if c == 't' else 0)

    # inserisco la media nei rating vuoti
    dataframe["review_scores_rating"] = SimpleImputer(strategy='median').fit_transform(dataframe[["review_scores_rating"]])

    # riutilizziamo una colonna dove inseriamo booleani per capire se un hotel è vicino o no al centro.
    dataframe = dataframe.rename(columns={'neighbourhood': 'is_center'})

    # quartieri del centro
    center = ["NAVIGLI", "SARPI", "BUENOS AIRES", "MAGENTA", "CENTRALE", "DUOMO", "BRERA", "TICINESE",
              "WASHINGTON", "GUASTALLA", "XXII MARZO", "ISOLA", "LORETO", "DE ANGELI",
              "BOVISASCA", "PORTA ROMANA", "TORTONA", "GARIBALDI REPUBBLICA", "GHISOLFA",
              "PORTELLO", "PAGANO", "FARINI", "SCALO ROMANA", "MACIACHINI", "TRE TORRI", "EX OM",
              "PARCO SEMPIONE", "PARCO AGRICOLO SUD", "GIARDINI PORTA VENEZIA"]
    dataframe["is_center"] = dataframe.neighbourhood_cleansed.apply(lambda c: 1 if is_center(c,center) else 0).astype('int')

    # inserisco la media nel host_response_rate
    dataframe["host_response_rate"] = dataframe.host_response_rate.astype('category')
    dataframe["host_response_rate"] = dataframe.host_response_rate.apply(lambda c: re.sub('[%]','',c))
    dataframe["host_response_rate"] = SimpleImputer(strategy='median').fit_transform(dataframe[["host_response_rate"]])
    print("Cleaning done.")
    return dataframe




def main():
    try:
        dataframe = pd.read_csv(argv[1])
        dataframe = cleaning_dataset(dataframe)
        dataframe.to_csv('./datasets/cleaned_dataset.csv', index=False)
        # inserire in seguito la creazione del cleaning per la Belief Network
    except FileNotFoundError as e:
        print(e)
        print("file not found or wrong directory")
    except Exception as e:
        print(e)
        print("Error...")

main()
