
import estime2
import os
import pandas as pd



# Specify the path of the file to `tbl_path`
tbl_path = "../"
tbl_names = [fl for fl in os.listdir('../') if fl[:12] == "Gabarit_Donn"]
assert len(tbl_names) == 1, \
    'There are more than one file in the parent directory ' +\
    'that starts with "Gabarit_Donn". Make sure ' +\
    "there's only one of such file, or give a specific path " +\
    "to that file to the `tbl_path` variable in this script."
tbl_path += tbl_names[0]


# Functions and variables
PRSA = ['ProvCode', 'RegionCode', 'Sex', 'Age']
def arrange_by_lvl(df, levels, value_name):
    age_cols = [col for col in df if col.startswith('A_')]
    result =\
        pd.melt(
            df[levels + age_cols],
            id_vars = levels,
            value_vars = age_cols,
            var_name = 'Age',
            value_name = value_name
        )\
        .assign(
            Age = lambda df: \
                df.Age.apply(lambda x: int(x[(x.index('A_') + 2):]))
        )
    return result


# Read sheets
sheets = pd.read_excel(tbl_path, sheet_name = None)
pops = sheets['Population']
bths = sheets['Births']
dths = sheets['Deaths']
imms = sheets['Immigrants']
emis = sheets['Emigrants']
rems = sheets['Ret.Emi']
ntes = sheets['Net temp emi']
nprs = sheets['Net NPR']
interprov_in = sheets['Interpro IN']
interprov_out = sheets['Interpro OUT']
intraprov_in = sheets['Intrapro IN']
intraprov_out = sheets['Intrapro OUT']


# Mutate sheets
## pops
pops_melted = arrange_by_lvl(pops, ['RefDate'] + PRSA[:3], 'POP')
years = pops_melted['RefDate'].unique()
assert len(years) == 2, \
    f'A supplied number of years is not 2, but {len(years)}.'
years.sort()
pops_beg = pops_melted\
    .query(f"RefDate == {years[0]}")\
    [PRSA + ['POP']]\
    .rename(columns = {'POP': f'POP_{years[0]}'})
pops_end = pops_melted\
    .query(f"RefDate == {years[1]}")\
    [PRSA + ['POP']]\
    .rename(columns = {'POP': f'POP_{years[1]}'})

## bths
bths = bths\
    [PRSA[:3] + ['Total']]\
    .assign(Age = -1)\
    .rename(columns = {'Total': 'BTH'})\
    [PRSA + ['BTH']]

## nprs
nprs_melted = arrange_by_lvl(nprs, PRSA[:3], 'NPR')\
    .assign(NPR_in = lambda df: df.NPR.apply(lambda x: max(x, 0)))\
    .assign(NPR_out = lambda df: df.NPR.apply(lambda x: -min(x, 0)))
nprs_in = nprs_melted[PRSA + ['NPR_in']]
nprs_out = nprs_melted[PRSA + ['NPR_out']]

## dths, imms, emis, rems, ntes, interprovs and intraprovs
dths = arrange_by_lvl(dths, PRSA[:3], 'DTH')
imms = arrange_by_lvl(imms, PRSA[:3], 'IMM')
emis = arrange_by_lvl(emis, PRSA[:3], 'EMI')
rems = arrange_by_lvl(rems, PRSA[:3], 'REM')
ntes = arrange_by_lvl(ntes, PRSA[:3], 'NTE')
interprov_in = arrange_by_lvl(interprov_in, PRSA[:3], 'IMI')
interprov_out = arrange_by_lvl(interprov_out, PRSA[:3], 'IMO')
intraprov_in = arrange_by_lvl(intraprov_in, PRSA[:3], 'IRI')
intraprov_out = arrange_by_lvl(intraprov_out, PRSA[:3], 'IRO')


# Merge sheets
tbls = pops_beg\
    .merge(bths, on = PRSA, how = 'outer')\
    .sort_values(PRSA)\
    .fillna(0)
tbls[f'POP_{years[0]}'] = tbls[f'POP_{years[0]}'].apply(int)
tbls['BTH'] = tbls['BTH'].apply(int)
tbls = tbls\
    .merge(ntes, on = PRSA, how = 'inner')\
    .merge(emis, on = PRSA, how = 'inner')\
    .merge(nprs_out, on = PRSA, how = 'inner')\
    .merge(dths, on = PRSA, how = 'inner')\
    .merge(interprov_out, on = PRSA, how = 'inner')\
    .merge(intraprov_out, on = PRSA, how = 'inner')\
    .merge(rems, on = PRSA, how = 'inner')\
    .merge(nprs_in, on = PRSA, how = 'inner')\
    .merge(imms, on = PRSA, how = 'inner')\
    .merge(interprov_in, on = PRSA, how = 'inner')\
    .merge(intraprov_in, on = PRSA, how = 'inner')


# Group sheets by ProvCode and RegionCode
estime2.set_option(
    'pop.sex', 'Sex',
    'pop.age', 'Age',
    'pop.end', f'POP_{years[1]}',
    'pop.start', f'POP_{years[0]}',
    'pop.birth', 'BTH',
    'comp_neg.temp_out', 'NTE',
    'comp_neg.emi', 'EMI',
    'comp_neg.npr_out', 'NPR_out',
    'comp_neg.death', 'DTH',
    'comp_neg.interprov_out', 'IMO',
    'comp_neg.intraprov_out', 'IRO',
    'comp_neg.etc', [],
    'comp_pos.ret_emi', 'REM',
    'comp_pos.npr_in', 'NPR_in',
    'comp_pos.immi', 'IMM',
    'comp_pos.interprov_in', 'IMI',
    'comp_pos.intraprov_in', 'IRI',
    'comp_pos.etc', [],
    'comp.end', []
)
ProvCodes = tbls['ProvCode'].unique()
RegionCodes = {
    k: tbls.query(f"ProvCode == {k}")['RegionCode'].unique() \
    for k in ProvCodes
}
collections = {
    pc: {
        rc: estime2.SubProvPopTable(
            tbls.query(f"RegionCode == {rc}").iloc[:, 2:]
        ) \
        for rc in RegionCodes[pc]
    } \
    for pc in ProvCodes
}
PopTables = {
    prcode: estime2.AggregateSubProvPopTable(tbls_dict) \
        if len(tbls_dict) >= 2 \
        else estime2.SubProvPopTable(list(tbls_dict.values())[0]) \
    for prcode, tbls_dict in collections.items()
}


# Compute the end-of-period populations based on components of PopTables
# and see if they coincide with pops_end
wrongs = {}
for p, lst_r in RegionCodes.items():
    for rr in lst_r:
        pe1 = collections[p][rr].calculate_pop()
        pe2 = pops_end.query(f"RegionCode == {rr}")
        pe2 = pe2.sort_values(['Sex', 'Age'])
        diff_pop_end = pe1.iloc[:, -1].values != pe2.iloc[:, -1].values
        at_least_one_diff_pop_end = diff_pop_end.any()
        if at_least_one_diff_pop_end:
            info1 = pe1[diff_pop_end]
            info2 = pe2[diff_pop_end]
            wrongs[rr] = {
                'ds': info1['Sex'].values, 
                'da': info1['Age'].values,
                'ped': info2.iloc[:, -1].values,
                'pe2': info1.iloc[:, -1].values
            }
if wrongs == {}:
    print("All the end-of-period populations in the data coincide with ")
    print("what have been computed by the estime2 prototype.")
else:
    print("The following end-of-period populations are not matching:")
    for k, dv in wrongs.items():
        print(f"In RegionCode {k}:")
        for i in range(len(dv['ds'])):
            print(f"    * Sex: {dv['ds'][i]}, Age: {dv['da'][i]}")
            print(f"      End-of-period Pop. in data: {dv['ped'][i]}")
            print(f"      End-of-period Pop. by estime2: {dv['pe2'][i]}")
        print("")
