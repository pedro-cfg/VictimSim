import pandas as pd
import numpy as np
import tensorflow as tf
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import sys
        
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
        model3.compile(optimizer='adam', loss='mean_squared_error')


        m1 = KerasRegressor(model1, batch_size=32, epochs=100, verbose=0)
        m2 = KerasRegressor(model2, batch_size=32, epochs=100, verbose=0)
        m3 = KerasRegressor(model3, batch_size=32, epochs=100, verbose=0)

        val_score1 = np.mean(cross_val_score(m1, X_train, T_train, cv=5))
        val_score2 = np.mean(cross_val_score(m2, X_train, T_train, cv=5))
        val_score3 = np.mean(cross_val_score(m3, X_train, T_train, cv=5))

        max_cv_score = max (val_score1, val_score2, val_score3)

        final_model = None

        if max_cv_score == val_score1:
           print("Modelo 1 escolhido")
           final_model = m1
        
        if max_cv_score == val_score2:
            print("Modelo 1 escolhido")
            final_model = m2

        if max_cv_score == val_score3:
            print("Modelo 3 escolhido")
            final_model = m3

        final_model.fit(X_test, T_test, verbose = 1)
        print("Modelo final treinado")
        # P_test = model.predict(TESTE_CEGO)
        # mean_squared_error(P_test, EXPECTED TESTE CEGO)

        # Treinando as redes
        # model1.fit(X_train, T_train, epochs=100, batch_size=32, validation_data=(X_test, T_test), verbose=2)
        # model2.fit(X_train, T_train, epochs=100, batch_size=32, validation_data=(X_test, T_test), verbose=2)
        # model3.fit(X_train, T_train, epochs=100, batch_size=32, validation_data=(X_test, T_test), verbose=2)
        
        # Avaliando os modelos
        # loss1 = model1.evaluate(X_test, T_test, verbose=0)
        # print(f'Mean Squared Error on Test Data (Model 1): {loss1}')
        
        # loss2 = model2.evaluate(X_test, T_test, verbose=0)
        # print(f'Mean Squared Error on Test Data (Model 2): {loss2}')
        
        # loss3 = model3.evaluate(X_test, T_test, verbose=0)
        # print(f'Mean Squared Error on Test Data (Model 3): {loss3}')
        
        sys.exit()