import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#----Importing CSV----
tax = pd.read_csv('Open Data Tax Receipts Source.csv')
live_reg = pd.read_csv('Live Register.csv')
unemp8315 = pd.read_csv('Unemployment 19832015.csv')
unemp9821 = pd.read_csv('Unemployment 19982021.csv')
unempcovid = pd.read_csv('Unemployment Covid.csv')

pd.set_option('display.max_columns',50)
pd.set_option('display.max_rows',50)

#----Checking Tax CSV----
#print(tax.head())
#print(tax.shape)

#----Insert column names----
cols = ['Year', 'MonthLong', 'Actual/Projected', 'Tax Head', 'Amount (000s)']
tax_cols = pd.read_csv('Open Data Tax Receipts Source.csv', names=cols)

#----Checking dataframe post column insertion / looking for one extra row----
#print(tax_cols.head())
#print(tax_cols.shape)

#----Creating a combined date column----
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#----Checking for errors brings up 510 errors----
#print(tax_cols.isna().sum())

#----Checked the data set and there is some whitespace after 'December  ' which is removed by this----
tax_cols['MonthLong'] = tax_cols['MonthLong'].apply(lambda x: x.strip())

#----Running this again to ensure the FullDate column is filled in full. I would normally remove the date line above but keeping it as an example that I check the errors----
date = pd.to_datetime(tax_cols['Year'].astype(str) + tax_cols['MonthLong'], format='%Y%B', errors='coerce')
tax_cols['FullDate'] = date + pd.offsets.MonthEnd()

#----Checking for errors again to ensure none are pulled through - all is ok----
#print(tax_cols.isna().sum())

#----Create abbreviated column for ease of charting----
tax_heads = tax_cols['Tax Head'].unique()

tax_heads_list = []

for i in tax_heads:
        tax_heads_list.append(i)

#----Change tax collected to rounded millions----

tax_cols['Amount (MM)'] = (tax_cols['Amount (000s)'] / 1000).astype(int)

#print(tax_heads_list)

#----Creating a short hand list for the main tax heads----
tax_dict = {'Tax Head': tax_heads_list,
        'Tax Heads Short': ['OTHER','EXD','CGT','SD','IT','CORP','VAT','OTHER','OTHER','UNA','OTHER','OTHER']}

tax_dict_pd = pd.DataFrame(data=tax_dict)
#print(tax_dict_pd)

tax_cols_short = tax_cols.merge(tax_dict_pd, on='Tax Head', how='left')
#print(tax_cols_short)

#----Removing the projected rows and 2021 (not complete data) and Unallocated Tax Recipts----

actual_filter = (tax_cols_short['Actual/Projected'] == 'Actual Outturn') & (tax_cols_short['Year'] != 2021) & (tax_cols_short['Tax Heads Short'] != 'UNA')
tax_final = tax_cols_short[actual_filter]

#print(tax_final['Actual/Projected'].unique())
#print(tax_final)

#----Looking at live register data----
#print(live_reg.head())

#----Adding a full date column to the live reg info so I can match the tax table with live reg table----
date_live_reg = pd.to_datetime(live_reg['Month'], format='%YM%M')
live_reg['FullDate'] = date_live_reg + pd.offsets.MonthEnd()

#----Checking live reg table for errors----

#print(live_reg.isna().sum())
#print(live_reg['VALUE'].isna().groupby(live_reg['NewYear']).sum())

live_reg_clean = live_reg.dropna(axis=0)

#----Creating a maak filter that just contains all ages, both sexes, all classes----
live_reg_filter = ((live_reg_clean['Age Group'] == 'All ages') & (live_reg_clean['Sex'] == 'Both sexes') & (live_reg_clean['Social Welfare Scheme'] == 'All classes'))

#----Checking the mask works----
live_reg_final = live_reg_clean[live_reg_filter]

#print(live_reg_final['VALUE'].isna().groupby(live_reg_final['NewYear']).sum())

#print(live_reg_final)

#----Merging the tables----
tax_live_reg_final = pd.merge_asof(tax_final, live_reg_final, on='FullDate', direction='forward')
#print(tax_live_reg_final)

#----Checking there are no errors----
#print(tax_live_reg_final.isna().sum())

#----Creating smaller tables and dropping rows I don't need so it's easier to merge----
unemp8315_filter = unemp8315[['Month','VALUE']]
unemp1 = unemp8315_filter.drop(unemp8315_filter.index[180:388])

unemp9821_filter = unemp9821[['Month','VALUE']]
unemp2 = unemp9821_filter.drop(unemp9821_filter.index[266:277])

unempcovid_filter = (unempcovid['Lower and Upper Bound'] == 'Upper Bound (COVID-19 Adjusted MUR)')
unemp_covid_filter2 = (unempcovid[unempcovid_filter])
unemp3 = unemp_covid_filter2[['Month','VALUE']]

unemp_final = pd.concat([unemp1, unemp2, unemp3], axis=0)
unemp_final.reset_index(inplace=False)
#unemp_final.set_index('Month', inplace=True)
#print(unemp_final)

#----Merging the unemployed %----
final_data = pd.merge(tax_live_reg_final, unemp_final, on='Month', suffixes=['_#', '_%'])

print(final_data)

#----Updating Unemployent numbers for 2020 to include the pandemic unemployment payment----

unemp2020 = np.array([[183900,182500,209400,216900,227900,213700,226100,213700,216000,211600,203100,193700],[0,0,283129,602107,543164,438933,274578,224956,217142,329991,351424,335599]])

total_unemployed_pup = (final_data.groupby(['Year'])['VALUE_#'].max())

unemp2020_max = unemp2020.max()

total_unemployed_pup.iloc[-1] = unemp2020_max

#print(total_unemployed_pup)

#----Charts----

#----Tax chart----
tax_live_reg_chart1 = (final_data.groupby(['Year'])['Amount (MM)'].sum())
tax_live_reg_chart1.plot(kind='bar', color='limegreen', width=0.6)
plt.xlabel('Year')
plt.ylabel('Tax revenue (€ millions)')
plt.title('Tax revenue per year')
#plt.show()

#----Unemployment Chart----
tax_live_reg_chart2 = (final_data.groupby(['Year'])['VALUE_%'].mean())
tax_live_reg_chart2.plot(color='limegreen', marker='o', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Unemployment %')
plt.title('Unemployment % per year')
#plt.show()

#----Combined tax and unemployment chart----
time = final_data['Year'].unique()
tax_data= (final_data.groupby(['Year'])['Amount (MM)'].sum())
unemployment_data = (final_data.groupby(['Year'])['VALUE_%'].mean())

plt.style.use('ggplot')
fig1, ax1 = plt.subplots()

color = 'mediumseagreen'
ax1.set_title('Irish tax revenue and unemployment trend')
ax1.set_xlabel('Year')
ax1.set_ylabel('Tax revenue (€ millions)')
ax1.bar(time, tax_data, color = color)
ax1.tick_params(axis='y', labelcolor = color)

ax2 = ax1.twinx()

color2 = 'coral'
ax2.set_ylabel('Average unemployment %')
ax2.plot(time, unemployment_data, color=color2, marker='.', linestyle='--')
ax2.tick_params(axis='y', labelcolor = color2)

fig1.savefig('Irish tax revenue and unemployment trend', dpi=100)

plt.show()


#----unemployed barchart----
total_unemployed_pup.plot(kind='bar', color='mediumseagreen', width=0.6)
plt.xlabel('Year')
plt.ylabel('Number of people on the live register')
plt.title('Highest number of people on the live register')

plt.savefig('Number of people on the live register', dpi=100, bbox_inches='tight')

plt.show()

#----Tables----
print(final_data.groupby(['Year'])['VALUE_%'].mean().sort_values(ascending=False))
print(final_data.groupby(['Year'])['VALUE_#'].min().sort_values(ascending=False))
print(final_data.groupby(['Tax Heads Short'])['Amount (MM)'].sum().sort_values(ascending=False))
print(final_data.groupby(['Year'])['Amount (MM)'].sum().sort_values(ascending=False))
print(np.sort(total_unemployed_pup))

#----Percentage calculations----
pct1 = (final_data.groupby(['Tax Heads Short'])['Amount (000s)'].sum().sort_values(ascending=False))
pct1['PCT'] = ((pct1 / pct1.sum()) * 100)
print(pct1['PCT'])


tax_2020_filter = (final_data['Year'] == 2020)
tax_filter_final = final_data[tax_2020_filter]
pct2020 = (tax_filter_final.groupby(['Tax Heads Short'])['Amount (MM)'].sum().sort_values(ascending=False))
print(pct2020)
pct2020['PCT'] = ((pct2020 / pct2020.sum()) * 100)
print(pct2020['PCT'])

tax_1984_filter = (final_data['Year'] == 1984)
tax_filter_final = final_data[tax_1984_filter]
pct1984 = (tax_filter_final.groupby(['Tax Heads Short'])['Amount (MM)'].sum().sort_values(ascending=False))
print(pct1984)
pct1984['PCT'] = ((pct1984 / pct1984.sum()) * 100)
print(pct1984['PCT'])
