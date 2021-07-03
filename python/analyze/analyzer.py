from collections import defaultdict

from python.analyze.data_helper import collect_stocks_data, collect_stock_info
import numpy as np
import pandas as pd
from scipy.optimize import minimize, LinearConstraint

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

class Analyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.df, self.price_df = collect_stocks_data(tickers)
        stocks_info = collect_stock_info(tickers)
        industries = [stocks_info[t]['industry'] for t in self.tickers]
        sectors = [stocks_info[t]['sector'] for t in self.tickers]
        self.info_dict = {'industry': industries, 'sector': sectors}
        
    # [{'bounds': {'lower': ..., 'upper': ...}, 
    #   'field': 'industry/sector/stock'
    #   'name': 'str'
    #   }]

    def generate_constraints(self, cons_args):
        bounds = [(0, 1)] * len(self.tickers)
        constraints = [weight_constraint]
        for cons in cons_args:
            bounds_arg, field, name = cons['bounds'], cons['field'], cons['name']
            lower = bounds_arg['lower'] if 'lower' in bounds_arg else -1
            upper = bounds_arg['upper'] if 'upper' in bounds_arg else 1
            if field == 'stock':
                idx = self.tickers.index(name)
                bounds[idx] = (lower, upper)
            else:
                vec = np.array(list(map(lambda sec: int(sec == name), self.info_dict[field])))
                constraint = LinearConstraint(vec, lower, upper, keep_feasible=False)
                constraints.append(constraint)
        return bounds, constraints
        
    def optimize(self, rule='optimal', cons_args=[]):
        C = self.df.cov()
        R = self.df.mean().to_numpy()
        num_of_stock = self.df.shape[1]
        weights = [1.0 / num_of_stock] * num_of_stock
        bounds, constraints = self.generate_constraints(cons_args)
        if rule == 'min_var':
            weights = minimize(fun=min_variance, args=C, x0=weights,
                               constraints=constraints, bounds=bounds)['x']
        elif rule == 'max_return':
            weights = minimize(fun=max_return, args=R, x0=weights,
                               constraints=constraints, bounds=bounds)['x']
        elif rule == 'optimal':
            weights = minimize(fun=optimal, args=(R, C, 1), x0=weights,
                               constraints=constraints, bounds=bounds)['x']
        else:
            raise Exception("Unsupported optimization rule".format(rule))
        weights = np.round(weights, 3)
        exp_return = R.dot(weights)
        vol = np.sqrt(weights.dot(C.dot(weights)))
        return weights, exp_return, vol

    def optimal_comp(self, rule, total_amount, cons_args=[]):
        weights, exp_return, vol = self.optimize(rule, cons_args)
        weight_dict = dict(zip(self.df.columns, weights))
        sec_comp, ind_comp = defaultdict(float), defaultdict(float)
        comp = {}
        total_value = 0
        for ticker, weight in weight_dict.items():
            amount = total_amount * weight
            last_price = self.price_df[ticker].iloc[-1]
            num_share = round(amount/last_price)
            value = num_share * last_price
            comp[ticker] = {'value': value, 'num_share': num_share, 'price': last_price}
            total_value += value
        for idx, w in enumerate(weights):
            sec_comp[self.info_dict['sector'][idx]] += w
            ind_comp[self.info_dict['industry'][idx]] += w
        return {'weights': weight_dict,
                'expected_return': exp_return,
                'volatility': vol,
                'detail': comp,
                'total_value': total_value,
                'sec_comp': dict(sec_comp),
                'industry_comp': dict(ind_comp)}










