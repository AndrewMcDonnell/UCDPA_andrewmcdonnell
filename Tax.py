import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#Importing CSV
tax = pd.read_csv('Open Data Tax Receipts Source.csv')

#Checking CSV
print(tax.head())
print(tax.shape)

#After checking data we need to insert column names
cols = ['Year', 'MonthLong', 'Actual/Projected', 'Tax Head', 'Amount (000s)']
tax_cols = pd.read_csv('Open Data Tax Receipts Source.csv', names=cols)

#Checking dataframe post column insertion / looking for one extra row
print(tax_cols.head())
print(tax_cols.shape)

#This removes the whitespace after December so the full date column fills out
tax_cols['MonthLong'] = tax_cols['MonthLong'].apply(lambda x: x.strip())

#Adding the last day of each month
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#After looking at file it turns out December has a few blank spaces after it.
print(tax_cols.head())
print(tax_cols.isna().any())
print(tax_cols.isna().sum())

