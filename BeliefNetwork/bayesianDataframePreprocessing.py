import pandas as pd
import numpy as np
from preprocessing.amenities import amenities_matrix


def datasetBuilding(dataframe):
    amenities_reducted = amenities_matrix(dataframe, (len(dataframe) / 3)).astype("boolean")
    cols_to_be_dropped = [
                    "id",
                    "host_identity_verified",
                    "accommodates",
                    "bathrooms_text",
                    "bedrooms",
                    "beds",
                    "maximum_nights",
                    "minimum_nights",
                    "has_availability",
                    "review_scores_cleanliness",
                    "review_scores_location",
                    "review_scores_value",
                    "instant_bookable",
                    "name",
                    "description",
                    "host_response_time",
                    "host_verifications",
                    "property_type",
                    "room_type",
                    "amenities"]
    dataframe.drop(cols_to_be_dropped, axis=1, inplace=True)
    dataframe["neighbourhood_cleansed"] = dataframe["neighbourhood_cleansed"].apply(lambda x: x.replace('.', '').lower())
    dataframe["neighbourhood_cleansed"] = dataframe["neighbourhood_cleansed"].apply(lambda x: x.replace(' ', '_'))

    #discretizzazione del prezzo
    price_intervals = [
        (dataframe['price'] <= 40),
        (dataframe['price'] > 40) & (dataframe['price'] <= 55),
        (dataframe['price'] > 55) & (dataframe['price'] <= 200),
        (dataframe['price'] > 200) & (dataframe['price'] <= 675),
        (dataframe['price'] > 675)
    ]
    price_range = ['economy', 'affordable', 'medium', 'expensive', 'top_level']
    to_insert = np.select(price_intervals, price_range)
    dataframe.insert(0, 'class_of_price', to_insert)
    dataframe = dataframe.astype({'class_of_price': 'category'})
    dataframe.drop('price', axis=1, inplace=True)


    #discretizzazione di host response rate
    response_intervals = [
        (dataframe['host_response_rate'] <= 5),
        (dataframe['host_response_rate'] > 5) & (dataframe['host_response_rate'] <= 97.5),
        (dataframe['host_response_rate'] > 97.5) & (dataframe['host_response_rate'] <= 99.5),
        (dataframe['host_response_rate'] > 99.5)
    ]
    response_range = ['never_responds', 'usually_responds', 'often_responds', 'always_responds']
    to_insert = np.select(response_intervals, response_range)
    dataframe['host_response_rate'] = to_insert
    dataframe = dataframe.astype({'host_response_rate': 'category'})

    #discretizzazione di number of reviews
    reviews_intervals = [
        (dataframe['review_scores_rating'] <= 4.795),
        (dataframe['review_scores_rating'] > 4.795) & (dataframe['review_scores_rating'] <= 4.805),
        (dataframe['review_scores_rating'] > 4.805) & (dataframe['review_scores_rating'] <= 4.965),
        (dataframe['review_scores_rating'] > 4.965)
    ]
    reviews_range = ['low_rating', 'good_rating', 'nice_rating', 'top_rating']
    to_insert = np.select(reviews_intervals, reviews_range)
    dataframe['review_scores_rating'] = to_insert
    dataframe = dataframe.astype({'review_scores_rating': 'category'})

    #discretizzazione di review scores rating
    number_reviews_intervals = [
        (dataframe['number_of_reviews'] <= 1),
        (dataframe['number_of_reviews'] > 1) & (dataframe['number_of_reviews'] <= 2),
        (dataframe['number_of_reviews'] > 2) & (dataframe['number_of_reviews'] <= 19),
        (dataframe['number_of_reviews'] > 19)
    ]
    number_reviews_range = ['no_reviews', 'few_reviews', 'some_reviews', 'lot_of_reviews']
    to_insert = np.select(number_reviews_intervals, number_reviews_range)
    dataframe['number_of_reviews'] = to_insert
    dataframe = dataframe.astype({'number_of_reviews': 'category'})

    dataframe = dataframe.astype({'is_center': 'boolean'})
    dataframe = dataframe.astype({'host_is_superhost': 'boolean'})

    dataframe = dataframe.reset_index()
    dataframe.drop('index', axis=1, inplace=True)
    dataframe = pd.concat([dataframe, amenities_reducted], axis=1)

    #le features bedrooms,beds,bathrooms_text,accomodates.minumum nights sono gia verificabile tramite
    # query alla KB

    return dataframe



def main():
    dataframe = pd.read_csv("../datasets/cleaning_dataset.csv")
    print("dataset preprocessing for the belief network")
    bn_dataset = datasetBuilding(dataframe)

    bn_dataset.to_csv('../datasets/bn_dataset.csv', index=False)


if __name__ == '__main__':
    main()
