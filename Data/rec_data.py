from __future__ import division
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import pickle

class DataTrainer:
    
    def __init__(self, train_data = []):
       
        self.NUM_OF_SENSORS = 8
        self.NUM_OF_EACH_NGRAM = 5

        self.NUM_OF_INPUT_SAMPLE = 35
        self.MODEL_FILE_NAME = "User_Profile.sav"
        self.MODEL_FILE_PATH = "../Data/" + self.MODEL_FILE_NAME

        self._train_data = np.array(train_data) # [[], [], []]
        print(self._train_data)
        self._train_label = [0, 1, 2]

        self._model = None

        if os.path.isfile(self.MODEL_FILE_PATH):
            with open(self.MODEL_FILE_PATH, 'rb') as f:
                self._model = pickle.load(f)
    
    def train(self):

        if self._model == None:

            print ("TRAINING !")

            # Define model
            RF_model = RandomForestClassifier(n_estimators=int(self.NUM_OF_SENSORS * 1.5))

            # Prepare data
            X = list()
            y = list()
            for label_index, eachSample in enumerate(self._train_data):
                for i in range(eachSample.shape[0] - self.NUM_OF_EACH_NGRAM + 1):
                    X.append(eachSample[i: i + self.NUM_OF_EACH_NGRAM].flatten())
                    y.append(self._train_label[label_index])

            RF_model.fit(X, y)

            # Save model
            with open(self.MODEL_FILE_PATH, 'wb') as f:
                pickle.dump(RF_model, f)
        
            self._model = RF_model

            print("END TRAINING !")

    def predict(self, input):
        input = np.reshape(input, (-1, self.NUM_OF_EACH_NGRAM, self.NUM_OF_SENSORS))
        input = [x.flatten() for x in input]
        
        results = self._model.predict(input)
        action = Counter(results).most_common(1)[0][0]

        return action