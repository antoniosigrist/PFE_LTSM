#https://www.analyticsvidhya.com/blog/2018/10/predicting-stock-price-machine-learningnd-deep-learning-techniques-python/
# https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/

#import packages
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm

#to plot within notebook
import matplotlib.pyplot as plt
#%matplotlib inline

#setting figure size
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,10

#for normalizing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

#read the file

print("oi")
def LTSM(csv_file):

	df = pd.read_csv(csv_file)

	#print the head
	print(df.head())


	guess_space = 0.99 #percentual of data analysed before predicting


	data = df.sort_index(ascending=True, axis=0)


	train = data[:int(len(data)*guess_space)]
	valid = data[int(len(data)*guess_space):]

	training = train['Close']
	validation = valid['Close']


	from sklearn.preprocessing import MinMaxScaler
	from keras.models import Sequential
	from keras.layers import Dense, Dropout, LSTM

	#creating dataframe
	data = df.sort_index(ascending=True, axis=0)
	new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
	for i in range(0,len(data)):
	    new_data['Date'][i] = data['Date'][i]
	    new_data['Close'][i] = data['Close'][i]

	#setting index
	new_data.index = new_data.Date
	new_data.drop('Date', axis=1, inplace=True)

	#creating train and test sets
	dataset = new_data.values

	train = dataset[:int(len(data)*guess_space)]
	valid = dataset[int(len(data)*guess_space):]

	#converting dataset into x_train and y_train
	scaler = MinMaxScaler(feature_range=(0, 1))
	scaled_data = scaler.fit_transform(dataset)

	x_train, y_train = [], []
	for i in range(60,len(train)):
	    x_train.append(scaled_data[i-60:i,0])
	    y_train.append(scaled_data[i,0])
	x_train, y_train = np.array(x_train), np.array(y_train)

	x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

	# create and fit the LSTM network
	model = Sequential()
	model_units = 50
	model.add(LSTM(units=model_units, return_sequences=True, input_shape=(x_train.shape[1],1)))
	model.add(LSTM(units=model_units))
	model.add(Dense(1))

	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

	#predicting (246) values, using past 60 from the train data
	inputs = new_data[len(new_data) - len(valid) - 60:].values
	inputs = inputs.reshape(-1,1)
	inputs  = scaler.transform(inputs)

	X_test = []
	for i in range(60,inputs.shape[0]):
	    X_test.append(inputs[i-60:i,0])
	X_test = np.array(X_test)

	X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
	closing_price = model.predict(X_test)
	closing_price = scaler.inverse_transform(closing_price)

	print("Previsão dos próximos "+str(len(closing_price))+" dia:")
	print(closing_price)

	train = new_data[:int(len(data)*guess_space)]
	valid = new_data[int(len(data)*guess_space):]


	close_pr = []

	for i in range(0,len(train['Close'])-2):
		close_pr.append(None)
	close_pr.append(train['Close'][-1])
	for i in range(0,len(closing_price)-1):
		close_pr.append(closing_price[i])


	plt.plot(train['Close']) #dados que foram treinados
	plt.plot(valid['Close']) #dados que realmente aconteceram
	plt.plot(close_pr) #dados estimados
	plt.show()

	return 

file = "BVSP.csv"
file = "teste_padrao.csv"

LTSM(file)



