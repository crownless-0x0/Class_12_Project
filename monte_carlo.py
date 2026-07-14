import random
import linear_regression as lr
import data_analysis as da

prices = da.import_close_values()
current_price = prices[-1]
mu = da.mean_return()
sigma = da.volatility()
predictions = []

for i in range(5000):
    z = random.gauss(0,1)
    daily_return = mu + sigma*z
    predicted_price = current_price*(1+daily_return)

    predictions.append(predicted_price)

prediction = sum(predictions)/len(predictions)

minimum = min(predictions)
maximum = max(predictions)

predictions.sort()

lower = predictions[int(0.025*len(predictions))]
upper = predictions[int(0.975*len(predictions))]

print(f'Current price: {current_price}')
print(f'Expected price: {prediction}')
print(f'Minimum: {minimum}')
print(f'Maximum: {maximum}')
print(lower)
print(upper)
