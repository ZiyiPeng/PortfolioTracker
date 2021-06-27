from python.analyze.data_helper import collect_stocks_data
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# hard constraint: all the weights add up to 1
weight_constraint = {'type': 'eq', 'fun': lambda x: 1 - sum(x)}


# maximize return/vol
def optimal(x, R, C, alpha=1.0):
    """
    @param weights: the weight vector to be optimized
    @param R: a vector of expected stock return
    @param C: covariance matrix of stock return
    @param alpha: risk aversion factor (default to 1)
    @return: -(expected_return / volatility)
    """
    W = np.array(x)
    return -(R.dot(W) / (W.dot(C.dot(W)) * alpha))


def min_variance(x, C):
    W = np.array(x)
    return W.dot(C.dot(W))


def max_return(x, R):
    W = np.array(x)
    return -(R.dot(W))


# soft constrain:

class Analyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.df, self.price_df = collect_stocks_data(tickers)

    def optimize(self, rule='optimal'):
        C = self.df.cov()
        R = self.df.mean().to_numpy()
        # TODO: soft constraint no shorting
        num_of_stock = self.df.shape[1]
        bounds = [(0, 1)] * num_of_stock
        weights = [1.0 / num_of_stock] * num_of_stock
        if rule == 'min_var':
            weights = minimize(min_variance, args=C, x0=weights,
                               constraints=[weight_constraint], bounds=bounds, tol=1e-50)['x']
        elif rule == 'max_return':
            weights = minimize(max_return, args=R, x0=weights,
                               constraints=[weight_constraint], bounds=bounds, tol=1e-50)['x']
        elif rule == 'optimal':
            weights = minimize(optimal, args=(R, C, 1), x0=weights,
                               constraints=[weight_constraint], bounds=bounds, tol=1e-50)['x']
        else:
            raise Exception("Unsupported optimization rule".format(rule))
        weights = np.round(weights, 3)
        weight_dict = dict(zip(self.df.columns, weights))
        exp_return = R.dot(weights)
        vol = np.sqrt(weights.dot(C.dot(weights)))
        return weight_dict, exp_return, vol

    def optimal_comp(self, rule, total_amount):
        weight_dict, exp_return, vol = self.optimize(rule)
        comp = {}
        total_value = 0
        for ticker, weight in weight_dict.items():
            amount = total_amount * weight
            last_price = self.price_df[ticker].iloc[-1]
            num_share = round(amount/last_price)
            value = num_share * last_price
            comp[ticker] = {'value': value, 'num_share': num_share, 'price': last_price}
            total_value += value
        return weight_dict, exp_return, vol, comp, total_value










