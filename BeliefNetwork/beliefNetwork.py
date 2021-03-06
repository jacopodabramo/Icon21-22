from pgmpy.readwrite import XMLBIFReader
from pgmpy.inference import VariableElimination

class BeliefNetwork:
    model = None
    inference_method = None
    beliefNet_structure = None
    data_path = './datasets/bn_dataset.csv'

    def __init__(self,i):
        self.parents(i)
        reader = XMLBIFReader(self.beliefNet_structure)
        self.model = reader.get_model()
        self.inference_method = VariableElimination(self.model)

    def parents(self,i):
        if i == 1:
            self.beliefNet_structure = './datasets/belief_network_structure_1_parent.xml'
        elif i == 2:
            self.beliefNet_structure = './datasets/belief_network_structure_2_parents.xml'
        elif i == 3:
            self.beliefNet_structure = './datasets/belief_network_structure_3_parents.xml'

    def inference(self, preferences_dictionary):
        results_dictionary = {}
        result = self.inference_method.query(variables = ['review_scores_rating'], evidence = preferences_dictionary)
        results_dictionary['top_rating'] = result.get_value(review_scores_rating ='top_rating').round(4)
        results_dictionary['nice_rating'] = result.get_value(review_scores_rating='nice_rating').round(4)
        results_dictionary['good_rating'] = result.get_value(review_scores_rating='good_rating').round(4)
        results_dictionary['low_rating'] = result.get_value(review_scores_rating='low_rating').round(4)
        return results_dictionary

    def compute_query(self, input_string):
        input_string = input_string
        preferences_list = input_string.split(",")
        preferences_dictionary = {}
        for item in preferences_list:
            key = (item.split("=")[0])
            value = str(item.split("=")[1])
            preferences_dictionary[key] = value
        return preferences_dictionary



