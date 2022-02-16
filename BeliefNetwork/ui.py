import pandas as pd
import pyswip as psw
from os import path
from sys import argv
import re

from beliefNetwork import BeliefNetwork

prg = psw.Prolog()



def BF_help():
    """
    print dell'help della Belief Network
    """

    print("discrete attributes available: \n"
          "- class_of_price  --> values{economy,affordable,medium,expensive,top_level} \n"
          "- host_response_rate --> values{never_responds,usually_responds,often_responds,always_responds}\n"
          "- number_of_reviews --> values{no_reviews,few_reviews,some_reviews,lot_of_reviews}\n"
          "- review_scores_rating --> values{low_rating,good_rating,nice_rating,top_rating}\n"
          "- neighbourhood_cleansed --> values{NAVIGLI,VIALE MONZA,BUENOS AIRES,CENTRALE,DUOMO,BRERA,TICINESE,WASHINGTON,LAMBRATE,VILLAPIZZONE,GUASTALLA,\n"
          "ISOLA,CITTA STUDI,GIAMBELLINO,DE ANGELI ROSA,BANDE NERE,TORTONA,XXII MARZO,GHISOLFA,PORTELLO,UMBRIA,PARCO FORLANINI,SARPI,BOVISA,MAGENTA VITTORE,\n"
          "LORETO,STADERA,VIGENTINA,GARIBALDI REPUBBLICA,LODI,TIBALDI,FORZE ARMATE,S. CRISTOFORO,PAGANO,PARCO LAMBRO,FARINI,PORTA ROMANA,GRECO,PADOVA,ORTOMERCATO,\n"
          "MACIACHINI,MAGGIORE,LORENTEGGIO,TRE TORRI,BARONA,ADRIANO,CORSICA,RONCHETTO SUL NAVIGLIO,SCALO ROMANA,QUARTO CAGNINO,EX OM,DERGANO,ROGOREDO,\n"
          "SELINUTE,GALLARATESE,MECENATE,QT 8,NIGUARDA GRANDA,RIPAMONTI,AFFORI,BAGGIO,PARCO MONLUE LAMBRO,GRATOSOGLIO,PARCO SEMPIONE,QUARTO OGGIARO,\n"
          "COMASINA,BOVISASCA,PARCO AGRICOLO SUD,PARCO NORD,BICOCCA,CHIARAVALLE,QUINTO ROMANO,TRIULZO SUPERIORE,BRUZZANO,FIGINO,PARCO DEI NAVIGLI,\n"
          "CANTALUPA,TRENNO,PARCO DELLE ABBAZIE,GIARDINI PORTA VENETA,PARCO BOSCO IN CITTÂ}\n")

    print("boolean attributes available:\n"
          "- host_is_superhost\n"
          "- is_center\n"
          "- cooking_basics\n"
          "- heating\n"
          "- long_term_stays_allowed\n"
          "- tv\n"
          "- iron\n"
          "- dishes_and_silverware\n"
          "- essentials\n"
          "- hangers\n"
          "- dedicated_worksapce\n"
          "- bed_linens\n"
          "- washer\n"
          "- hot_water\n"
          "- hair_dryer\n"
          "- kitchen\n"
         "- elevator \n"
         "- shampoo \n"
         "- air_conditioning\n"
         "- wifi\n"
         "- stove\n"
         "- refrigerator\n"
         "- oven\n"
         "- dishwasher\n"
         "- microwave\n"
         "- coffe_maker")

    print("Insert evidences for the belief network respecting the following format:")
    print("AttributeName = value, AttributeName = value, ...\n"
          "name of attributes must be written in lowercase \n")

def correct_input(a):
    command = input().lower().strip()
    while(command != a[0] and command != a[1]):
        print("Wrong command,you can insert ",a)
        command = input().lower().strip()
    return command

def dropping(answer):
    """
    :param answer:indica una query da eseguire sulla KB, sotto forma di lista
    :return: dataframe con le risposte esatte per quella query
    """
    dataframe = pd.DataFrame(answer)
    canc = set() #insiemre rappresentate le colonne da cancellare
    for index, row in dataframe.iterrows():
        for col in dataframe.columns:
            if isinstance(row[col], psw.Variable):
                canc.add(index)
                break
    dataframe.drop(index=canc, inplace=True)
    return dataframe


def BNetwork_query():
    """
    funzione per la gestione delle query che vengono effettuate alla Belief Network
    """
    print('Select number of parents for Belief Network (1,2,3):')
    while True:
        p = input()
        if p == '1' or p == '2' or p == '3':
            break
        else:
            print("Wrong number")

    b = BeliefNetwork(int(p))
    BF_help()
    while True:
        print("Insert your preferences: ")
        preferences = input().replace(' ', '')
        if re.match('((([a-z]+)([_]([a-z]+))*)([=])(([a-z|A-Z]+)([_]([a-z]+))*)([,]*))+', preferences):
            try:
                results = b.inference(b.compute_query(preferences))
                print("{:<15} {:<15}".format('RATING', 'PROBABILITY'))
                for key, value in results.items():
                    print("{:<15} {:<15}".format(key, value))
            except Exception as e:
                print("Error: " + e.__str__())

            print("Do you want to insert another query? [yes,no]")
            response = correct_input(['yes', 'no'])
            if response == 'no':
                break
        else:
            print("Incorrect string form")

def kbquery():
    """
    Funzione per la gestione e la stampa delle query della kb
    """
    try:
        # vera [{}], false[],  risposte [{X:...}]
        print("Insert a query for KnowledgeBase:")
        query = input()
        answer = prg.query(query)
        answer_list = list(answer)
        if len(answer_list) == 0:
            print("false")
        elif len(answer_list) == 1 and len(answer_list[0]) == 0:
            print("true")
        else:
            dataframe = dropping(answer_list)
            print("Answer:\n")
            print(dataframe)

    except Exception as e:
        print("Error" + str(e))


def help():
    #help generale per l'utente
    print("This is a list of command:")
    print("'query' to insert a query in KB")
    print("'inference' to do inference with Belief Network")
    print("'quit' to exit\n")


def main():
    print("Loading knowledge base...")
    prg.consult("./datasets/kb.pl")
    pd.set_option('display.max_rows', 3000, 'display.max_columns', 10)
    help()
    while (True):
        print("Insert command:")
        command = input()
        command = command.strip().lower()
        if command == 'quit':
            break
        elif command == 'help':
            help()
        elif command == 'query':
            while(True):
                kbquery()
                print("Do you want to insert another query? [yes,no]")
                cont = correct_input(['yes', 'no'])
                if cont == 'no':
                    break
        elif command == 'inference':
            BNetwork_query()
        else:
            print("Wrong command")
            help()

main()

