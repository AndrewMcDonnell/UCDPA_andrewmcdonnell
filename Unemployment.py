import pandas as pd

unemp8315 = pd.read_csv('Unemployment 19832015.csv')
unemp9821 = pd.read_csv('Unemployment 19982021.csv')
unempcovid = pd.read_csv('Unemployment Covid.csv')

#pd.set_option('display.max_columns',10)
#pd.set_option('display.max_rows',400)


#Creating smaller tables and dropping rows I don't need so it's easier to merge
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
print(unemp_final)

check = (len(unemp1) + len(unemp2) + len(unemp3))

if len(unemp_final) == check:
    print('OK')
else:
    print('ERROR')

#Didn't use the below in the end
#full_unemp = pd.concat([unemp8315, unemp9821, unempcovid], axis=0)
#clean_month_list = full_unemp['Month'].drop_duplicates()

#clean_month_list2 = pd.DataFrame(data=clean_month_list, columns=['Month'])

#unemp8315 1983M01 to 2015M04 - drop rows 1998M01 (180) to 2015M04 (up to 388)
#unemp9821 1998M01 to 2021M01 - drop rows 2020M03 (266) to 2021M01 (up to 277)
#unempcovid 2020M03 to 2021M01