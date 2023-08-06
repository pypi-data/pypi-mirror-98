
import estime2
import os
import pandas as pd
from datetime import datetime as dt
from openpyxl import load_workbook


# Specify the path of the file to `tbl_path`
start_time = dt.now()
tbl_path = "../"
tbl_names = [
    fl for fl in os.listdir('../') \
    if (fl[:4] == "Donn" and 'prev' not in fl)
]
assert len(tbl_names) == 1, \
    'There are more than one file in the parent directory ' +\
    'that starts with "Donn". Make sure ' +\
    "there's only one of such file, or give a specific path " +\
    "to that file to the `tbl_path` variable in this script."
tbl_path += tbl_names[0]
result_path = tbl_path[:-5] + '_result.xlsx'


# Functions and variables
PRSA = ['ProvCode', 'RegionCode', 'Sex', 'Age']
name_pops_beg = 'Population_beginning'
name_pops_end = 'Population_end'
name_bths = 'Births'
name_dths = 'Deaths'
name_imms = 'Immigrants'
name_emis = 'Emigrants'
name_rems = 'Ret.Emi'
name_ntes = 'Net temp emi'
name_ipis = 'Interpro IN'
name_ipos = 'Interpro OUT'
name_iris = 'Intrapro IN'
name_iros = 'Intrapro OUT'
name_nprs_in = 'Stocks NPR_end'
name_nprs_out = 'Stocks NPR_beginning'
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
pops_beg = sheets[name_pops_beg]
bths = sheets[name_bths]
dths = sheets[name_dths]
imms = sheets[name_imms]
emis = sheets[name_emis]
rems = sheets[name_rems]
ntes = sheets[name_ntes]
interprov_in = sheets[name_ipis]
interprov_out = sheets[name_ipos]
intraprov_in = sheets[name_iris]
intraprov_out = sheets[name_iros]
nprs_in = sheets[name_nprs_in]
nprs_out = sheets[name_nprs_out]
pops_end = pd.read_excel(
    tbl_path, 
    sheet_name = name_pops_end, 
    skiprows = 4
)
name_pops_beg = name_pops_beg.replace(' ', '_')
name_pops_end = name_pops_end.replace(' ', '_')
name_bths = name_bths.replace(' ', '_')
name_dths = name_dths.replace(' ', '_')
name_imms = name_imms.replace(' ', '_')
name_emis = name_emis.replace(' ', '_')
name_rems = name_rems.replace('.', '_')
name_ntes = name_ntes.replace(' ', '_')
name_ipis = name_ipis.replace(' ', '_')
name_ipos = name_ipos.replace(' ', '_')
name_iris = name_iris.replace(' ', '_')
name_iros = name_iros.replace(' ', '_')
name_nprs_in = name_nprs_in.replace(' ', '_')
name_nprs_out = name_nprs_out.replace(' ', '_')


# Mutate sheets
## pops
year_beg = pops_beg['RefDate'].unique()[0]
year_end = pops_end['RefDate'].unique()[0]
name_pops_year_beg = f"POP_{year_beg}"
name_pops_year_end = f"POP_{year_end}"
pops_beg = arrange_by_lvl(pops_beg, PRSA[:3], name_pops_year_beg)
pops_end = arrange_by_lvl(pops_end, PRSA[:3], name_pops_year_end)

## bths
bths = bths\
    [PRSA[:3] + ['Total']]\
    .assign(Age = -1)\
    .rename(columns = {'Total': name_bths})\
    [PRSA + [name_bths]]

## nprs
nprs_out = arrange_by_lvl(nprs_out, PRSA[:3], name_nprs_out)
nprs_in = arrange_by_lvl(nprs_in, PRSA[:3], name_nprs_in)

## dths, imms, emis, rems, ntes, interprovs, and intraprovs
dths = arrange_by_lvl(dths, PRSA[:3], name_dths)
imms = arrange_by_lvl(imms, PRSA[:3], name_imms)
emis = arrange_by_lvl(emis, PRSA[:3], name_emis)
rems = arrange_by_lvl(rems, PRSA[:3], name_rems)
ntes = arrange_by_lvl(ntes, PRSA[:3], name_ntes)
interprov_in = arrange_by_lvl(interprov_in, PRSA[:3], name_ipis)
interprov_out = arrange_by_lvl(interprov_out, PRSA[:3], name_ipos)
intraprov_in = arrange_by_lvl(intraprov_in, PRSA[:3], name_iris)
intraprov_out = arrange_by_lvl(intraprov_out, PRSA[:3], name_iros)


# Merge sheets
tbls = pops_beg\
    .merge(bths, on = PRSA, how = 'outer')\
    .sort_values(PRSA)\
    .fillna(0)
tbls[name_pops_year_beg] = tbls[name_pops_year_beg].apply(int)
tbls[name_bths] = tbls[name_bths].apply(int)
tbls = tbls\
    .merge(ntes, on = PRSA, how = 'inner')\
    .merge(emis, on = PRSA, how = 'inner')\
    .merge(nprs_out, on = PRSA, how = 'outer')\
    .merge(dths, on = PRSA, how = 'inner')\
    .merge(interprov_out, on = PRSA, how = 'inner')\
    .merge(intraprov_out, on = PRSA, how = 'inner')\
    .merge(rems, on = PRSA, how = 'inner')\
    .merge(nprs_in, on = PRSA, how = 'outer')\
    .merge(imms, on = PRSA, how = 'inner')\
    .merge(interprov_in, on = PRSA, how = 'inner')\
    .merge(intraprov_in, on = PRSA, how = 'inner')\
    .fillna(0)
tbls[name_nprs_out] = tbls[name_nprs_out].apply(int)
tbls[name_nprs_in] = tbls[name_nprs_in].apply(int)


# Group sheets by ProvCode and RegionCode
estime2.set_option(
    'pop.sex', PRSA[2],
    'pop.age', PRSA[3],
    'pop.end', name_pops_year_end,
    'pop.start', name_pops_year_beg,
    'pop.birth', name_bths,
    'comp_neg.temp_out', name_ntes,
    'comp_neg.emi', name_emis,
    'comp_neg.npr_out', name_nprs_out,
    'comp_neg.death', name_dths,
    'comp_neg.interprov_out', name_ipos,
    'comp_neg.intraprov_out', name_iros,
    'comp_neg.etc', [],
    'comp_pos.ret_emi', name_rems,
    'comp_pos.npr_in', name_nprs_in,
    'comp_pos.immi', name_imms,
    'comp_pos.interprov_in', name_ipis,
    'comp_pos.intraprov_in', name_iris,
    'comp_pos.etc', [],
    'comp.end', [name_nprs_in]
)
ProvCodes = tbls[PRSA[0]].unique()
RegionCodes = {
    k: tbls.query(f"{PRSA[0]} == {k}")[PRSA[1]].unique() \
    for k in ProvCodes
}
collections = {
    pc: {
        rc: estime2.SubProvPopTable(
            tbls.query(f"{PRSA[1]} == {rc}").iloc[:, 2:]
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
        pe2 = pops_end.query(f"{PRSA[1]} == {rr}")
        pe2 = pe2.sort_values(PRSA[2:])
        diff_pop_end = pe1.iloc[:, -1].values != pe2.iloc[:, -1].values
        at_least_one_diff_pop_end = diff_pop_end.any()
        if at_least_one_diff_pop_end:
            info1 = pe1[diff_pop_end]
            info2 = pe2[diff_pop_end]
            wrongs[rr] = {
                'ds': info1[PRSA[2]].values, 
                'da': info1[PRSA[3]].values,
                'ped': info2.iloc[:, -1].values,
                'pe2': info1.iloc[:, -1].values
            }
if wrongs == {}:
    print("All the end-of-period populations in the data coincide with ")
    print("what have been computed by the estime2 prototype.")
else:
    print("The following end-of-period populations are not matching:")
    for k, dv in wrongs.items():
        print(f"In {PRSA[1]} {k}:")
        for i in range(len(dv['ds'])):
            print(f"    * {PRSA[2]}: {dv['ds'][i]}, {PRSA[3]}: {dv['da'][i]}")
            print(f"      End-of-period Pop. in data: {dv['ped'][i]}")
            print(f"      End-of-period Pop. by estime2: {dv['pe2'][i]}")
        print("")


# First fix: method_use.old_neigh = False, pop.at_least = 1
## Collect PopTableResultsWrapper for each region
PopTableResults = {}
standalones = [
    p for p in RegionCodes.keys() if len(RegionCodes[p]) == 1
]
for k, v in PopTables.items():
    print(f"Fixing SubProvPopTables of province {k}...  ")
    if k not in standalones:
        PopTableResults[k] = v.fix_all_issues(return_all_mods = True)
    else: # Not Aggregate...Table, but a standalone SubProvPopTable
        PopTableResults[k] = {
            RegionCodes[k][0]: v.fix_issues(return_all_mods = True)
        }
print("")
end_time = dt.now()

print(f"Runtime: {end_time - start_time}")
print("")

## Order tables by PRSA
pops_end = pops_end.sort_values(PRSA)
pops_end_cols = pops_end.columns.to_list()
pops_end_bone = {c: [] for c in pops_end_cols}
pops_end_corrected = pd.DataFrame(pops_end_bone)
tbls = tbls.sort_values(PRSA)
tbls_cols = tbls.columns.to_list()
tbls_bone = {c: [] for c in tbls_cols}
tbls_fixed = pd.DataFrame(tbls_bone)

## Save tables
pops_end.to_excel(
    result_path,
    sheet_name = f"{name_pops_year_end}_before_estime2",
    index = False
)
book = load_workbook(result_path)
writer = pd.ExcelWriter(result_path, engine = 'openpyxl')
writer.book = book
tbls.to_excel(
    writer,
    sheet_name = 'components_before_estime2',
    index = False
)

## Collect end-of-period populations of each region fixed by estime2
for p, lst_v in RegionCodes.items():
    print(f"Computing end-of-period pop. of province {p}...  ")
    for r in lst_v:
        tbl_fixed_r = PopTableResults[p][r].get_fixed_table()
        tbl_fixed_cols = tbl_fixed_r.columns.to_list()
        pops_end_region = tbl_fixed_r.calculate_pop().copy()
        tbl_fixed_region = tbl_fixed_r.copy()

        tbl_fixed_region[PRSA[0]] = p
        tbl_fixed_region[PRSA[1]] = r
        tbl_fixed_region = tbl_fixed_region[PRSA[:2] + tbl_fixed_cols]
        tbl_fixed_region[PRSA[3]] = tbl_fixed_region[PRSA[3]]\
            .apply(estime2.Age.get_showing_age)
        tbls_fixed = tbls_fixed\
            .append(tbl_fixed_region, ignore_index = True)

        pops_end_region[PRSA[0]] = p
        pops_end_region[PRSA[1]] = r
        pops_end_region = pops_end_region[PRSA + [name_pops_year_end]]
        pops_end_region[PRSA[3]] = pops_end_region[PRSA[3]]\
            .apply(estime2.Age.get_showing_age)
        pops_end_corrected = pops_end_corrected\
            .append(pops_end_region, ignore_index = True)
print("")
for cc in PRSA[:2] + tbl_fixed_cols:
    if cc != PRSA[3]: # Age
        tbls_fixed[cc] = tbls_fixed[cc].apply(int)
    else:
        tbls_fixed[cc] = tbls_fixed[cc].apply(str).apply(int)
for cc in PRSA + [name_pops_year_end]:
    pops_end_corrected[cc] = pops_end_corrected[cc].apply(int)

## Append tables to the created .xlsx file
pops_end_corrected.to_excel(
    writer, 
    sheet_name = f'{name_pops_year_end}_after_estime2', 
    index = False
)
tbls_fixed.to_excel(
    writer, 
    sheet_name = 'components_after_estime2', 
    index = False
)
print(f"Saving results to {result_path} ...")
writer.save()
print("Closing...")
writer.close()
