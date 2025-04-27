
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv('startup_growth_investment_data.csv')

# One-hot encode
df = pd.get_dummies(df, columns=['Industry', 'Country'])

X = df.drop(['Growth Rate (%)', 'Startup Name'], axis=1)
y = df['Growth Rate (%)']

model = LinearRegression()
model.fit(X, y)

# Save model and feature names
with open('prediction_model.pkl', 'wb') as f:
    pickle.dump((model, X.columns.tolist()), f)

