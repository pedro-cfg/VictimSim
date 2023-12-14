import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
import sys
import csv
        
class neural_net:
    def __init__(self):
        # Carregando os dados do CSV
        self.data = pd.read_csv('datasets/data_800vic/sinais_vitais_com_label.txt', header=None)

        # Separando os dados em características (X) e rótulos (y)
        self.X = self.data.iloc[:, 3:6].values  # Utilizando apenas as colunas 3, 4 e 5 (pressão, pulso, respiração)
        self.T = self.data.iloc[:, 6].values    # Rótulo é a coluna 6 (gravidade)

        # Normalizando os dados
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)
        
        # Dividindo os dados em conjuntos de treinamento e teste
        #X_train, X_test, T_train, T_test = train_test_split(self.X, self.T, test_size=0.2, random_state=42)
        
        # descida de gradiente estocástico
        # Menos neuronios
        # Ativação Tangente Hiperbólica
        model1 = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='tanh', input_shape=(3,)),
            tf.keras.layers.Dense(4, activation='tanh'),
            tf.keras.layers.Dense(1)
        ])
        model1.compile(optimizer = tf.keras.optimizers.SGD(learning_rate=0.005), loss='mean_squared_error')

        # Root Mean Square Propagation
        # Mais neuronios
        # Ativação Unidade Linear Retificada
        model2 = tf.keras.Sequential([
            tf.keras.layers.BatchNormalization(input_shape=(3,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(1)
        ])
        model2.compile(optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001), loss='mean_squared_error')

        # Adam ? Achei na internet
        # Mais camadas e neuronios
        # Ativação Unidade Linear Retificada
        model3 = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(3,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(8, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        model3.compile(optimizer='adam', loss='mean_squared_error')

        models = [model1, model2, model3]

        best_model = self.choose_best_model(models)

        # Fazendo previsões
        sample_data = pd.read_csv('datasets/teste_cego/sinais_vitais_teste.txt',header=None)
        sample_data = sample_data.iloc[:, 1:4].values  # Utilizando apenas as colunas 3, 4 e 5 (pressão, pulso, respiração)
        sample_data = scaler.transform(sample_data)
        
        predicted_gravity1 = best_model.predict(sample_data)
        print(f"Tamanho da saida = {len(predicted_gravity1)}")
        output = 'rn.txt'

        # Abrir o arquivo em modo de escrita
        with open(output, 'w') as file:
            # Escrever cada elemento do vetor em uma linha
            writer = csv.writer(file)
            writer.writerows(predicted_gravity1)

        sys.exit()

    def choose_best_model(self, models):

        chosen_model = None
        chosen_error = 9999

        for model in models:

            error = self.cross_val(5, model)
            error_mean = sum(error) / len(error)

            if error_mean < chosen_error:
                chosen_error = error_mean
                chosen_model = model

        print(f"Errors from chosen: {chosen_error}")
        return chosen_model

    def cross_val(self, kf, model):

        num_folds = 5

        kf = KFold(n_splits=num_folds, shuffle=True, random_state=1)

        np_X = np.array(self.X)
        np_T = np.array(self.T)

        kf_split = kf.split(np_X, np_T)

        error = []

        fold = 0

        print(f"=============================")

        for train_index, val_index in kf_split:

            X_train =  np.array([np_X[i] for i in train_index])
            T_train =  np.array([np_T[i] for i in train_index])

            X_val = np.array([np_X[i] for i in val_index])
            T_val = np.array([np_T[i] for i in val_index])

            model.fit(X_train, T_train, epochs=100, batch_size=32, validation_data=(X_val, T_val), verbose=0)
            error.append(model.evaluate(X_val, T_val, verbose=0))

            print(f"Fold {fold} concluído!")

            fold += 1


        print(error)
        print(f"=============================")

        return error
