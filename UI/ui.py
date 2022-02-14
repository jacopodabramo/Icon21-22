"""
    File per gestire la User Interface
"""

import pandas as pd
import pyswip as psw
from os import path
from sys import argv



prg = psw.Prolog()




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

def correct_input(a):
    command = input().lower().strip()
    while(command != a[0] and command != a[1]):
        print("Wrong command,you can insert ",a)
        command = input().lower().strip()
    return command

def help():
    print("This is a list of command:")
    print("'query' to insert a query in KB")
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
        else:
            print("Wrong command")
            help()

main()
# main("../datasets/kb.pl")
