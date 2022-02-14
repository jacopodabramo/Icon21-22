import traceback

import pandas as pd
from os import path, remove
from sys import argv


class KnowledgeBase:
    """
    Classe per la gestione della Knowledge Base
    Attributi di classe: boolean,skip,list,categories che rappresentano le liste delle features
    """
    boolean = ['has_availability', 'instant_bookable', 'host_identity_verified', 'host_is_superhost','is_center']
    skip = ['description', 'neighbourhood_group_cleansed','host_response_time','review_scores_location','review_scores_value','review_scores_cleanliness']
    list = ['host_verifications', 'amenities']
    categories = ['name','property_type','room_type','neighbourhood_cleansed','cluster']


    def __init__(self,dataframe):
        self.dataframe = dataframe
        if path.exists('.\datasets\kb.pl'):
            remove('.\datasets\kb.pl')
        self.kbPath = '.\datasets\kb.pl'

    def KbCreation(self,max=-1):
        file = open(self.kbPath, "a")
        pd.set_option('display.max_rows', 1000)

        print("Creating Knowledge Base...")

        features = self.dataframe.columns
        for i in range(0, len(features)):
            count = 0
            try:
                for row in self.dataframe.iterrows():
                    count = count + 1
                    if 0 <= max < count:
                        break

                    value = row[1]

                    if features[i] in KnowledgeBase.skip:
                        continue
                    elif features[i] == 'id':
                        file.write('room(' + str(value["id"]) + ').\n')
                    elif features[i] in KnowledgeBase.categories:
                        if features[i] == 'neighbourhood_cleansed':
                            value[features[i]] = value[features[i]].replace('.', '')
                        to_write = str(value[features[i]]).lower().replace('"','').replace("<b>", "").replace("</b>", "").replace("<br />", "").replace("\\", '').strip()
                        file.write(features[i] + "(" + str(value["id"]) + ',"' + to_write + '").\n')
                    elif features[i] in KnowledgeBase.list:
                        cleaned_list = value[features[i]].replace('[', '').replace(']', "").replace('"','').replace("'",'').replace("\\", '').split(",")
                        for p in cleaned_list:
                            file.write(features[i] + "(" + str(value["id"]) + ',"' + str(p).lower().strip() + '").\n')
                    elif features[i] in KnowledgeBase.boolean:
                        if value[features[i]] == 1:
                            file.write(features[i] + '(' + str(value["id"]) + ').\n')
                    else:
                        if value[features[i]] != "nan":
                            file.write(features[i] + "(" + str(value["id"]) + ',' + str(value[features[i]]).strip() + ').\n')
            except Exception as e:
                print("Exception " + str(value['id'])  + str(e))

        file.close()

    def RulesCreation(self):
        # creazione delle regole all'interno della base di conoscenza

        file = open(self.kbPath, "a")
        print('Creating Rules...')

        #regole per la permanenza
        file.write('max(Room,Range):-  maximum_nights(Room,Maximum_nights), Maximum_nights >= Range.\n')
        file.write('min(Room,Range):- minimum_nights(Room,Minimum_nights), Minimum_nights =< Range.\n')
        file.write('stay_range(Room,Range) :- min(Room,Range),max(Room,Range). \n')

        # query per chiedere se si puo prenotare una casa in base agli ospiti e range di giorni, e lista di stanze che rispettano tali parametri
        file.write('min_accomodates(Room,Range) :-  accommodates(Room,Accomodate),Range =< Accomodate.\n')
        file.write('is_room_bookable(Room,Accomodate,Range) :- stay_range(Room,Range), min_accomodates(Room,Accomodate).\n')
        file.write('bookable_rooms(Result,Accomodate,Range) :- findall(X, is_room_bookable(X,Accomodate,Range),Result).\n')


        #regole per un host particolarmente affidabile
        # da aggiustare
        #file.write('reviews(Room,Reviews) :- number_of_reviews(Room,Reviews), Reviews >= 50.\n')
        #file.write('response(Room,Response) :- host_response_rate(Room,Response), Response >= 95.\n')
        file.write('is_host_top_quality(Room) :-  host_is_superhost(Room), number_of_reviews(Room,Reviews), host_response_rate(Room,Response),Reviews >= 50, Response >=95 .\n')
        file.write('best_hosts(Result) :- findall(Room, is_host_top_quality(Room), Result).\n')

        #regole per il prezzo
        file.write('class("top_level",P) :- P>675.0.\n')
        file.write('class("expensive",P) :- P>200.0,P=<675.0 .\n')
        file.write('class("medium",P) :- P>55.0,P=<200.0 .\n')
        file.write('class("affordable",P) :- P>40.0,P=<50.0 .\n')
        file.write('class("economy",P) :- P=<40.0 .\n')
        file.write('same_price_range(R1,R2) :- price(R1,P1), price(R2,P2), class(C1,P1), class(C2,P2), C1=C2.\n')
        file.write('same_amenities(R1,R2,A) :- amenities(R1,A), amenities(R2,A).\n')
        file.write('price_range(Room,Range) :- price(Room,Price), class(Range,Price).\n')

        #regole per verificare se si possa cucinare in una stanza dato l'id e le stanze che presentano come amenities "Kitchen", "Oven", "Cooking_basics"
        file.write('room_cooking(Room) :-  amenities(Room,"kitchen"), amenities(Room,"cooking basics"), amenities(Room,"oven").\n')
        file.write('cooking(Result) :- findall(X,room_cooking(X),Result).\n')


        #Data una camera si vogliono sapere i numeri di letti
        file.write('few_beds(Room) :- beds(Room,Beds), Beds =< 3.\n')
        file.write('many_beds(Room) :- beds(Room,Beds), Beds > 3.\n')


        # Capire se un appartemanto ha tante camera da letto
        file.write('few_bedrooms(Room) :- bedrooms(Room,Bedrooms), Bedrooms =< 2.\n')
        file.write('many_bedrooms(Room) :- bedrooms(Room,Bedrooms), Bedrooms > 3.\n')

        #Capire se un appartamento ha tanti bagni
        file.write('few_bathrooms(Room) :- bathrooms_text(Room,Bath), Bath < 2.\n')
        file.write('many_bathrooms(Room) :- bathrooms_text(Room,Bath), Bath >= 2.\n')

        # lista delle stanze con pochi e molti bagni
        file.write('rooms_few_bathrooms(Result) :-  findall(X, few_bathrooms(X), Result).\n')
        file.write('rooms_many_bathrooms(Result) :-  findall(X, many_bathrooms(X), Result).\n')

        #capire se una camera è grande o piccola
        file.write('big_room(Room) :- many_bedrooms(Room), many_beds(Room), many_bathrooms(Room).\n')
        file.write('small_room(Room) :- few_bedrooms(Room), few_beds(Room), few_bathrooms(Room).\n')

        #camere particolari
        file.write('room_for_couples(X) :- bedrooms(X,1.0), room_type(X,"private_room").\n')
        file.write('is_available(X):- has_availability(X), instant_bookable(X).\n')

        # Trovare tutte le camere grandi e piccole
        file.write('big_rooms(Result) :- findall(X, big_room(X), Result).\n')
        file.write('small_rooms(Result) :- findall(X, small_room(X), Result).\n')

        # Data una camera capire se è grande e piccola e se rispetta il prezzo inserito
        file.write('big_room_price(Room,Range) :- many_bedrooms(Room), many_beds(Room), price_range(Room,Range).\n')
        file.write('small_room_price(Room,Range) :- few_bedrooms(Room), few_beds(Room), price_range(Room,Range).\n')

        #servizi
        file.write('room_for_family(Room,Children) :- beds(Room,Beds), Beds is (1.0+Children).\n')
        file.write('connections(X,Y) :- amenities(X,Y),member(Y,["wifi","cable tv"]).\n')

        # Trovare tutte le camere in base alla dimensione e alla classe di prezzo
        file.write('big_rooms_price(Range,Result) :- findall(X, big_room_price(X,Range), Result).\n')
        file.write('small_rooms_price(Range,Result) :- findall(X, small_room_price(X,Range), Result).\n')

        # tipi di camere
        file.write('family_room(Room,People) :- bedrooms(Room,Bedrooms),beds(Room,Beds),Beds is (People), Bedrooms is (2) .\n')
        file.write('family_rooms(People,Result) :- findall(X, family_room(X,People), Result).\n')

        # camere ugali
        file.write('equal_beds_rooms(f_Room,s_Room):- beds(f_Room,f_beds),beds(s_Room,s_beds), f_beds = s_beds.\n')
        file.write('equal_bedrooms_rooms(f_Room,s_Room):- bedrooms(f_Room,f_bedr),beds(s_Room,s_bedr), f_bedr = s_bedr.\n')

        # camere per anziani
        file.write('eldery_room(Room) :- beds(Room,Beds), amenities(Room,"elevator"),Beds = 2.\n')

        # camere in centro
        file.write('centered_rooms(Result) :- findall(X, is_center(X,1), Result).\n')
        file.write('centered_room_price_range(Room,Range) :- is_center(Room,1),price_range(Room,Range) .\n')
        file.write('centered_rooms_price_range(Range,Result) :- findall(X, centered_room_price_range(X,Range), Result).\n')

        file.write('similar_rooms(X,Y) :- cluster(X,C), cluster(Y,D), C = D.')
        file.close()


def main():
    try:
        dataframe = pd.read_csv(argv[1])
        kb = KnowledgeBase(dataframe)
        kb.KbCreation()
        kb.RulesCreation()
        print("Knowledge Base done.")
    except FileNotFoundError as e:
        print(e)
        print("Error file")

main()
