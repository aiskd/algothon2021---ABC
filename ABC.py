#!/usr/bin/env python

import numpy as np
import scipy.stats as sp
import pandas as pd

def getMyPosition(prcSoFar):
    nInst=100
    stocks = [0] * nInst    
    coeff_lst = []
    # a loop to iterate through all the columns in the file
    for instrument in prcSoFar:
        days_list = list(range(1, len(instrument) + 1)) # a list of integers from 1 to 250 representing the days
        p_corr_coeff = sp.pearsonr(days_list, instrument) # calculating the Pearson's Correlation Coefficient to determine relationship between vars
        coeff_lst.append(p_corr_coeff[0]) # sp.pearsonr() returns a tuple, the correlation coefficient is at index 0 of the tuple 
    
    # filtering the Pearson's Correlation Coefficients based on trends and strength 
    corr_array = [0] * 100 # making an array to store the correlation data

    # a loop to iterate through all the Pearson's Correlation Coeffiecients found previously 
    for cor_coeff in coeff_lst:
        coeff_index = coeff_lst.index(cor_coeff) # extracting the index of the coefficients
        if cor_coeff > 0: # positive relationship
            if cor_coeff >= 0.8 and cor_coeff <= 1.0: # strong correlation
                corr_array[coeff_index] = 'Positive Stable'
            elif cor_coeff >= 0.4 and cor_coeff < 0.8: # moderate correlation
                corr_array[coeff_index] = 'Positive Moderate'
            else: # weak correlation
                corr_array[coeff_index] = 'Positive Unstable'
        else: # negative relationship
            if (cor_coeff * -1) >= 0.8 and (cor_coeff * -1) <= 1.0: # strong correlation
                corr_array[coeff_index] = 'Negative Stable'
            elif (cor_coeff * -1) >= 0.4 and (cor_coeff * -1) < 0.8: # moderate correlation
                corr_array[coeff_index] = 'Negative Moderate'
            else: # weak correlation
                corr_array[coeff_index] = 'Negative Unstable'
    
    pos = []
    neg = []
    # Now, we separate the instrunments according to their trends
    for i in range(len(corr_array)):
        if corr_array[i] == 'Positive Stable' or corr_array[i] == 'Positive Moderate' or corr_array[i] == 'Positive Unstable':
            pos.append(i)
        else:
            neg.append(i)

    # Next, we apply our strategies according to their trends.
    for i in range(100):
        data_array = prcSoFar[i]
        current_array = [0] * len(data_array)
        num_stock = 0
        if i in pos:
            # If it's a positive trend, it will buy stocks (at the price of $8000) when the 
            # current price is higher than previous day's price.
            # It will then sell the stocks we bought when the current price is higher
            # than the price we bought it for.
            for j in range(1, len(data_array)):
                if num_stock == 0:
                    if data_array[j] < data_array[j-1]:
                        num_stock += int(8000/data_array[j])
                else:
                    if data_array[j] > data_array[j-1]:
                        num_stock = 0 
                current_array[j] = num_stock
        else:
            # For negative trends, it will sell the stocks first and buy the stocks back afterwards.
            for j in range(1, len(data_array)):
                if num_stock == 0:
                    if data_array[j] > data_array[j-1]:
                        num_stock -= int(8000/data_array[j])
                else:
                    if data_array[j] < data_array[j-1]:
                        num_stock = 0
                current_array[j] = num_stock

        stocks[i] = current_array[-1]
    return np.array(stocks)