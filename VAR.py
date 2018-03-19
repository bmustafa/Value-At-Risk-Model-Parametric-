# Name : Bilal Mustafa
# Date 3/19/2018
# Project: VAR - Parametric Method

import matplotlib.mlab as mlab
import sys
from pandas_datareader import data
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


stock_list = []
# initialize list for stocks- to be used later on

try:
    numberofStocks = int(input("How many stocks would you like in your portfolio? \n"))
except:
    print('Error Wrong Type')
    sys.exit()
# ask for the number of stocks in the desired portfolio, only integers can be given

weight = np.ones(numberofStocks)
for i in range(numberofStocks):
    stock_list.append(input("Enter ticker for stock " + str(i+1) + ':\n'))
    new_weight = (float(input("Enter the weight for stock " + str(i + 1) + ' \
(i.e. 0.3, 0.7 ...):\n')))
    if new_weight > 1:
        print("Error Weight Too Large")
        sys.exit()
    weight[i] = new_weight
# ask for and create a list/array of the stock tickers and
# weights for the stock in our desired portfolio

if np.sum(weight) > 1 or np.sum(weight) < 1:
    print("Weights not equal to 1. Re-balancing")
    weight /= np.sum(weight)
# The weights must sum up to one

time_horizon = input("What is your time horizon? Enter 1 for a Day,  2 for a Month, \
3 for 6 Months or 4 for a Year or 5 if greater. \n")
time_scaler = 0
if time_horizon == '1':
    time_scaler = 1
elif time_horizon == '2':
    time_scaler = 21
elif time_horizon == '3':
    time_scaler = 126
elif time_horizon == '4':
    time_scaler = 252
elif time_horizon == '5':
    time_horizon = input("Choose a time horizon between 1 and 4 (years) \n")
    try:
        time_scaler = 252 * int(time_horizon)
        if int(time_horizon) > 4 or int(time_horizon) <= 0:
            print("Error. Too Large or small of a time horizon.")
            sys.exit()
    except:
        print("Error in entering time horizon")
        sys.exit()
else:
    print("Error wrong time horizon input")
    sys.exit()
# Establish the time horizon for which VAR will be calculated

try:
    confidence = (float(input("What is your confidence level? I.e. 98 for 98 % \n")))
    if confidence >= 100 or confidence <= 0:
        print("Error when entering confidence")
        sys.exit()
except:
    print("Error when entering confidence")
    sys.exit()
confidence = confidence / 100
check_losses_at = 1 - confidence
# Ask the user for their level of confidence


trigger = False
killer = 0
while(trigger == False):
    try:
        if(killer == 6):
            sys.exit()
        df = data.DataReader(stock_list, data_source='yahoo', \
                             start='01/01/2010')['Adj Close']
        trigger = True
    except:
        killer += 1
# pull historical price data for our list of stocks.
# If an error is given (happens randomly), try again atleast 6 times


df.sort_index(inplace=True)
stock_returns = df.pct_change()
mean_return = stock_returns.mean()
covariance_matrix = stock_returns.cov()
# Invert the dates for the data frame and calculate the returns and
# covariances of the stocks

portfolio_return = np.sum(mean_return * weight.T) * time_scaler
portfolio_std_dev = np.sqrt(np.dot(weight.T, np.dot(covariance_matrix, weight))) * np.sqrt(time_scaler)
# Use stock returns and covariances to calculate the portfolio return and std. dev

potential_loss = norm(portfolio_return, portfolio_std_dev).ppf(check_losses_at)
print("At the " + str(confidence * 100) + " percent level of confidence,\
 the portfolio may experience a return of "+ "{0:0.1f}".format(potential_loss * 100) +\
" or less.")
# Assign a value to potential loss equal to the return expected at our level of
# confidence (using a normal curve with a mean equal to our portfolio return
# and standard deviation equal to the standard deviation of our portfolio return

x = np.linspace(portfolio_return - 4*portfolio_std_dev,\
                portfolio_return + 4*portfolio_std_dev, 100)
plt.plot(x,mlab.normpdf(x, portfolio_return, portfolio_std_dev))
plt.title("Value At Risk")
plt.xlabel("Portfolio Return")
# Plot the normal curve and label the x axis and the graph

lower_limit = portfolio_return - 4 * portfolio_std_dev
upper_limit = portfolio_return + 4 * portfolio_std_dev
increment = (upper_limit - lower_limit)/150
# Establish the lower and upper limit of our normal curve that we plan to plot
# Initialize an increment value for countless intervals inbetween

height_at_critical = norm(portfolio_return, portfolio_std_dev).pdf(lower_limit)
plt.plot((lower_limit, lower_limit), (0, height_at_critical), 'r')
# Height_at_critical will measure the height of the normal curve at each interval
# At each interval, a vertical line will then be plotted from the axis to
# the curve

for i in range(150):
    lower_limit += increment
    height_at_critical = norm(portfolio_return, portfolio_std_dev).pdf(lower_limit)
    if lower_limit < potential_loss:
        plt.plot((lower_limit, lower_limit), (0, height_at_critical), 'r')
    else:
        plt.plot((lower_limit, lower_limit), (0, height_at_critical), 'b')
plt.show()
# At each interval, a vertical line will then be plotted from the axis to
# the curve
# If the line is made in the portion that represents a value lesser than the
# critical value, it will be red. Otherwise it will be blue