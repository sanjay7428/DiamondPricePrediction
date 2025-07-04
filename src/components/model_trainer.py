import numpy as np
import pandas as pd
import os, sys
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression ,Ridge, Lasso , ElasticNet
from sklearn.tree import DecisionTreeRegressor
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initate_model_trainer(self, train_array, test_array):
        try:
            logging.info('Splitting Depandent and Indepandant variable from traon and test data')
            X_train,y_train, X_test, y_test =(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )  

            models={
                'Linear Regression': LinearRegression(),
                'Ridge': Ridge(),
                'Lasso': Lasso(),
                'ElasticNet': ElasticNet(),
                'Decision Tree Regressor': DecisionTreeRegressor()
            }
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models)
            print(model_report)
            print('\n==============================================================================================\n')
            logging.info(f'model report: {model_report}')

            #to get the best model score from the model report

            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model=models[best_model_name]

            print(f'Best Model found, Model Name: {best_model_name}, R2 Score : {best_model_score}')
            print('\n==============================================================================================\n')
            logging.info(f'Best Model found, Model Name: {best_model_name}, R2 Score : {best_model_score}')

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

        except Exception as e:
            logging.info('Exception occured in model Trainer')
            raise CustomException(e ,sys)




