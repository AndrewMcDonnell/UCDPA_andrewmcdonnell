import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

#Importing CSV
tax = pd.read_csv('Open Data Tax Receipts Source.csv')
live_reg = pd.read_csv('Live Register.csv')
#pd.set_option('display.max_columns',50)

#Checking CSV
print(tax.head())
print(tax.shape)

#After checking data we need to insert column names
cols = ['Year', 'MonthLong', 'Actual/Projected', 'Tax Head', 'Amount (000s)']
tax_cols = pd.read_csv('Open Data Tax Receipts Source.csv', names=cols)

#Checking dataframe post column insertion / looking for one extra row
print(tax_cols.head())
print(tax_cols.shape)

#Amending the date so it shows as the last day of each month
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#Checking for errors brings up 510 errors
print(tax_cols.isna().sum())

#Checked the data set and there is some whitespace after 'December  ' which is removed by this
tax_cols['MonthLong'] = tax_cols['MonthLong'].apply(lambda x: x.strip())

#Running this again to ensure the FullDate column is filled in full
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#Checking for errors again to ensure none are pulled through - all is ok
print(tax_cols.isna().sum())

#Create abbreviated column for ease of charting
tax_heads = tax_cols['Tax Head'].unique()

tax_heads_list = []

for i in tax_heads:
        tax_heads_list.append(i)

print(tax_heads_list)

tax_dict = {'Tax Head': tax_heads_list,
        'Tax Heads Short': ['CUST','EXD','CGT','SD','IT','CORP','VAT','TEL','MOT','UNA','CAT','LPT']}

tax_dict_pd = pd.DataFrame(data=tax_dict)
print(tax_dict_pd)

tax_cols_short = tax_cols.merge(tax_dict_pd, on='Tax Head', how='left')
print(tax_cols_short)

#Looking at live register data
print(live_reg.head())

#Adding a full date column to the live reg info so I can match the tax table with live reg table
date_live_reg = pd.to_datetime(live_reg['Month'], format='%YM%M')
live_reg['FullDate'] = date_live_reg + pd.offsets.MonthEnd()

live_reg['NewYear'] = live_reg['FullDate'].dt.strftime('%Y')

print(live_reg.head)

#Checking live reg table for errors - a lot in the value column - can't figure out how to plot
print(live_reg.isna().sum())

#Creating a maak filter that just contains all ages, both sexes, all classes
filt = ((live_reg['Age Group'] == 'All ages') & (live_reg['Sex'] == 'Both sexes') & (live_reg['Social Welfare Scheme'] == 'All classes'))

#Checking the mask works
live_reg_merge = live_reg[filt]
print(live_reg_merge)

#Merging the tables
tax_live_reg_merge = pd.merge_asof(tax_cols_short, live_reg_merge, on='FullDate', direction='forward')
print(tax_live_reg_merge)

#Creating a filter to remove the projected figures
actual_filt = (tax_live_reg_merge['Actual/Projected'] == 'Actual Outturn')
tax_live_reg_actual = tax_live_reg_merge[actual_filt]

#Tables - need to adjust for profile v actual outturn in tax
total_tax_live_reg_actual = (tax_live_reg_actual.groupby(['Year'])['Amount (000s)'].sum())
total_tax_live_reg_actual.plot(kind='bar', color='limegreen', width=0.6)
plt.xlabel('Year')
plt.ylabel('Tax Revenue in €bn')
plt.title('Tax Revenue per Year')
#plt.show()

print(tax_live_reg_actual.columns)