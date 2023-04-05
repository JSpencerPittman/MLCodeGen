from sklearn.metrics import mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class ModelData:
    def __init__(self, X_train:pd.DataFrame, y_train:pd.Series, 
                 X_test:pd.DataFrame, y_test:pd.Series):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        
    def fit_model(self, model):
        model.fit(self.X_train, self.y_train)
        
    def predict(self, model, fit=False):
        if fit:
            self.fit_model(model)

        self.y_train_pred = model.predict(self.X_train)
        self.y_test_pred = model.predict(self.X_test)
        
    def test_train_error_regression(self, model_name=''):
        if model_name != '':
            print(model_name)
        print("Testing Error MSE: ", mean_squared_error(self.y_test, self.y_test_pred))
        print("Training Error MSE: ", mean_squared_error(self.y_train, self.y_train_pred))
        print()

        x_range_test = np.linspace(0,100,self.y_test.shape[0])
        x_range_train = np.linspace(0,100,self.y_train.shape[0])
        
        test_res = np.array(sorted(zip(self.y_test, self.y_test_pred)))
        train_res = np.array(sorted(zip(self.y_train, self.y_train_pred)))
        
        _, axes = plt.subplots(nrows=2, figsize=(12,8))
        axes[0].plot(x_range_test, test_res[:,0], label='True')
        axes[0].plot(x_range_test, test_res[:,1], label='Predicted')
        axes[1].plot(x_range_train, train_res[:,0], label='True')
        axes[1].plot(x_range_train, train_res[:,1], label='Predicted')
        
        title = ['Testing', 'Training']
        if model_name != '':
            title = [f"{model_name} {t}" for t in title]
        
        axes[0].legend()
        axes[0].set_title(title[0])
        
        axes[1].legend()
        axes[1].set_title(title[1])
        
        plt.show()