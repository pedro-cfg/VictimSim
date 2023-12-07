import pandas as pd
import numpy as np
import tensorflow as tf
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import sys
import csv
        
class neural_net:
    def __init__(self):
        # Carregando os dados do CSV
        self.data = pd.read_csv('datasets/data_800vic/sinais_vitais_com_label.txt')

        # Separando os dados em características (X) e rótulos (y)
        self.X = self.data.iloc[:, 3:6].values  # Utilizando apenas as colunas 3, 4 e 5 (pressão, pulso, respiração)
        self.T = self.data.iloc[:, 6].values    # Rótulo é a coluna 6 (gravidade)

        # Normalizando os dados
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X)
        
        # Dividindo os dados em conjuntos de treinamento e teste
        X_train, X_test, T_train, T_test = train_test_split(self.X, self.T, test_size=0.2, random_state=42)
        
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
        model3.compile(loss='mean_squared_error')


        # Treinando as redes
        model1.fit(X_train, T_train, epochs=100, batch_size=32, validation_data=(X_test, T_test), verbose=2)

        # Fazendo previsões
        sample_data = pd.read_csv('datasets/teste_cego/sinais_vitais_teste.txt',header=None)
        print(sample_data)
        print(f"Tamanho da entrada = {len(sample_data)}")
        sample_data = sample_data.iloc[:, 1:4].values  # Utilizando apenas as colunas 3, 4 e 5 (pressão, pulso, respiração)
        print(f"Tamanho da entrada filtrada = {len(sample_data)}")
        sample_data = scaler.transform(sample_data)
        
        predicted_gravity1 = model1.predict(sample_data)
        print(f"Tamanho da saida = {len(predicted_gravity1)}")
        output = 'rn.txt'

        # Abrir o arquivo em modo de escrita
        with open(output, 'w') as file:
            # Escrever cada elemento do vetor em uma linha
            writer = csv.writer(file)
            writer.writerows(predicted_gravity1)

        sys.exit()