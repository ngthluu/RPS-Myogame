from __future__ import division
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import pickle


class DataTrainer:

    NUM_OF_SENSORS = 8
    NUM_OF_EACH_NGRAM = 5

    NUM_OF_INPUT_SAMPLE = 35
    NUM_OF_TRAINING_SAMPLE = 150
    MODEL_FILE_NAME = "User_Profile.sav"
    MODEL_FILE_PATH = "../Data/" + MODEL_FILE_NAME
    
    def __init__(self, train_data = []):

        self._train_data = np.array(train_data) # [[], [], []]
        self._train_label = [0, 1, 2]

        self._model = None

        if os.path.isfile(DataTrainer.MODEL_FILE_PATH):
            with open(DataTrainer.MODEL_FILE_PATH, 'rb') as f:
                self._model = pickle.load(f)
    
    def train(self):

        if self._model == None:

            # Define model
            RF_model = RandomForestClassifier(n_estimators=int(DataTrainer.NUM_OF_SENSORS * 1.5))

            # Prepare data
            X = list()
            y = list()
            for label_index, eachSample in enumerate(self._train_data):
                for i in range(eachSample.shape[0] - DataTrainer.NUM_OF_EACH_NGRAM + 1):
                    X.append(eachSample[i: i + DataTrainer.NUM_OF_EACH_NGRAM].flatten())
                    y.append(self._train_label[label_index])

            RF_model.fit(X, y)

            # Save model
            with open(DataTrainer.MODEL_FILE_PATH, 'wb') as f:
                pickle.dump(RF_model, f)
        
            self._model = RF_model

    def predict(self, input):
        input = np.reshape(input, (-1, DataTrainer.NUM_OF_EACH_NGRAM, DataTrainer.NUM_OF_SENSORS))
        input = [x.flatten() for x in input]
        
        results = self._model.predict(input)
        action = Counter(results).most_common(1)[0][0]

        return action