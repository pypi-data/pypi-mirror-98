from octis.models.model import Abstract_Model


import octis.configuration.citations as citations
import octis.configuration.defaults as defaults


class TSNTM(Abstract_Model):

    def __init__(self, num_topics=100):
        self.hyperparameters["num_topics"]=num_topics


    def train_model(self, dataset, hyperparameters={}, top_words=10):
        return "ciao"

