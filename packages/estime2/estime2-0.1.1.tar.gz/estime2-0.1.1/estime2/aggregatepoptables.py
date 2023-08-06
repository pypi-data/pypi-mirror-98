
from estime2.age import Age
from estime2.config import (
    get_option,
    set_option
)
from estime2.poptable import (
    get_other_comp,
    get_L
)
from estime2.subpoptables import (
    apply_L,
    ProvPopTable,
    SubProvPopTable,
    return_goption_if_None
)
from estime2.poptable_resultswrapper import PopTableResultsWrapper
from functools import reduce
from typing import (
    List, 
    Optional,
    Union
)
import numpy as np
import pandas as pd



class AggregateProvPopTable():
    '''
    A list of `ProvPopTable`s.
    '''

    def __init__(
        self, 
        tbls: Union[dict, List[ProvPopTable]]
    ):
        '''
        Create an instance of AggregateProvPopTable.

        Usage
        -----
        AggregateProvPopTable(tbls: Union[dict, List[ProvPopTable]])

        Arguments
        ---------
        * `tbls`: a list of length at least 2, or a dict; a list/dict of
            `ProvPopTables` where each table has the same composition of 
            components.
        
        Details
        -------
        This class aims to fix negative populations in ProvPopTables of
        `tbls` by applying corrections to all the available components 
        in each table, including the interprovincial components. Dealing
        with interprovincial components in one table will involve 
        interprovincial components in other tables of `tbls`. 
        
        The following conditions apply when creating an instance of
        `AggregateProvPopTable`:

            1. The length of `tbls` should be at least 2.
            2. Each `ProvPopTable` in `tbls` should share the same name
                for the same component. 
            3. A component that exists in one table also has to exist in
                all the other tables as well. For example, if "Death" is
                one of the components in the table of `tbls`, then all the
                other tables in `tbls` must also have the "Death"
                component with the same name.
        '''

        assert len(tbls) >= 2, \
            "The `tbls` should contain at least 2 `ProvPopTable`s, " +\
            f"not {len(tbls)}."

        if isinstance(tbls, list):
            for i0, item in enumerate(tbls):
                if not isinstance(item, ProvPopTable):
                    raise TypeError(
                        f"The item of tbls at index {i0} "
                        f"is not a ProvPopTable but a {type(item)}."
                    )
            tbls = {k: tbls[k] for k in range(len(tbls))}
        elif isinstance(tbls, dict):
            for k, v in tbls.items():
                if not isinstance(v, ProvPopTable):
                    raise TypeError(
                        f"The value of tbls at key {k} "
                        f"is not a ProvPopTable but a {type(v)}."                
                    )
        else:
            raise NotImplementedError

        self.__tbls_dict = tbls
    
    def fix_all_issues(
        self, 
        method: Optional[str] = None,
        return_all_mods: bool = False
    ):
        '''
        Refer to the docstring of the `fix_all_issues(poptbls = self, 
        method = method, return_all_mods = return_all_mods)` function.
        '''

        return fix_all_issues(self, method, return_all_mods)

    def get_tbls_dict(self):
        '''
        Return `self.__tbls_dict`, the `dict` of all `ProvPopTable`s of
        `self`.

        Usage
        -----
        `self.get_tbls_dict()`
        '''

        return self.__tbls_dict

class AggregateSubProvPopTable():
    '''
    A list of `SubProvPopTable`s.
    '''

    def __init__(
        self, 
        tbls: Union[dict, List[SubProvPopTable]]
    ):
        '''
        Create an instance of AggregateSubProvPopTable.

        Usage
        -----
        AggregateSubProvPopTable(tbls: Union[dict, List[ProvPopTable]])

        Arguments
        ---------
        * `tbls`: a list of length at least 2; a list of 
            `SubProvPopTable`s where each table has the same composition of
            components.
        
        Details
        -------
        This class aims to fix negative populations in SubProvPopTables of
        `tbls` by applying corrections to all the available components 
        in each table, including the interprovincial components. Dealing
        with interprovincial components in one table will involve 
        interprovincial components in other tables of `tbls`. 
        
        The following conditions apply when creating an instance of
        `AggregateSubProvPopTable`:

            1. The length of `tbls` should be at least 2.
            2. Each `SubProvPopTable` in `tbls` should share the same 
                name for the same component. 
            3. A component that exists in one table also has to exist in
                all the other tables as well. For example, if "Death" is
                one of the components in the table of `tbls`, then all the
                other tables in `tbls` must also have the "Death"
                component with the same name.
        '''

        assert len(tbls) >= 2, \
            "The `lst_tbl` should contain at least 2 " +\
            "`SubProvPopTable`s, " +\
            f"not {len(tbls)}."

        if isinstance(tbls, list):
            for i0, item in enumerate(tbls):
                if not isinstance(item, SubProvPopTable):
                    raise TypeError(
                        f"The item of tbls at index {i0} "
                        f"is not a SubProvPopTable but a {type(item)}."
                    )
            tbls = {k: tbls[k] for k in range(len(tbls))}
        elif isinstance(tbls, dict):
            for k, v in tbls.items():
                if not isinstance(v, SubProvPopTable):
                    raise TypeError(
                        f"The value of tbls at key {k} "
                        f"is not a SubProvPopTable but a {type(v)}"
                    )
        else:
            raise NotImplementedError

        self.__tbls_dict = tbls

    def fix_all_issues(
        self, 
        method: Optional[str] = None,
        return_all_mods: bool = False
    ):
        '''
        Refer to the docstring of the `fix_all_issues(poptbls = self, 
        method = method, return_all_mods = return_all_mods)` function.
        '''

        return fix_all_issues(self, method, return_all_mods)

    def get_tbls_dict(self):
        '''
        Return `self.__tbls_dict`, the `dict` of all `SubProvPopTable`s of
        `self`.

        Usage
        -----
        `self.get_tbls_dict()`
        '''

        return self.__tbls_dict

def apply_Ns(
    tbl: Union[ProvPopTable, SubProvPopTable],
    t: int,
    comp: str,
    method: str,
    other_tbls: dict,
    comps_modifieds: dict
):
    '''
    Apply the modified L-vector of `tbl` (i.e. `comp_O`) to `tbl`, and the
    exact transferrables (i.e. `comp_N`s) of `other_tbls` to each of them. 
    Modify `comps_modifieds` whenever "comp_N" of each table actually 
    modifies itself.
    '''

    # Settings
    comp_L = f"{comp}_L"
    comp_N = f"{comp}_N"
    comp_O = f"{comp}_O"
    other_comp = get_other_comp(tbl, comp)
    other_comp_in_neg = other_comp in tbl.get_comp_neg()
    pop_groups = tbl.get_pop_groups()
    pop_age = pop_groups[1]
    comp_in_comp_end = comp in tbl.get_comp_end()
    to_transfer_ages = calculate_ages_to_transfer(
        tbl,
        comp,
        method,
        other_tbls
    )
    to_transfer_ages_pop_end = to_transfer_ages['age.to_transfer_pop_end']
    to_transfer_ages_comp = to_transfer_ages['age.to_transfer_comp']
    problematic_age = Age(to_transfer_ages_pop_end[-1])
    age_is_max = problematic_age.is_max()
    all_cols = tbl.columns.tolist()
    show_pop_end = tbl.get_pop_end() in all_cols
    is_subprov = tbl.is_subprov()

    # Get the L-vector of tbl
    L_df = get_L(tbl, comp, method, other_tbls)
    if (L_df[comp_L].values == 0).all():
        return tbl, other_tbls
    rearranging_col = [str(a) for a in L_df[pop_age].values]
    filtered_L_from_tbl = L_df[
        L_df[pop_age]\
            .apply(Age.get_showing_age)\
            .apply(str)\
            .isin([str(sc) for sc in to_transfer_ages_comp])
    ]

    # Get the sum of `comp_N`s of other_tbls
    exact_transferrables = get_Ns(tbl, comp, method, other_tbls)
    tbl_index = list(exact_transferrables.keys())
    sample_key = tbl_index[0]
    nrow = len(exact_transferrables[sample_key].index)
    comp_N_sum = np.repeat([0], nrow)
    for v in exact_transferrables.values():
        comp_N_sum += v[comp_N].values

    # Get the actual L vector (i.e. comp_O) to apply to tbl
    correction_to_tbl =\
        pd.DataFrame({
            'a': abs(filtered_L_from_tbl[comp_L].values),
            'b': abs(comp_N_sum)
        })\
        .min(axis = 1)\
        .values
    signs_for_receiver = calculate_signs(
        nrow, 
        age_is_max, 
        comp_in_comp_end, 
        other_comp_in_neg
    )
    signs_for_sender =\
        -signs_for_receiver if comp == other_comp else signs_for_receiver
    correction_to_tbl *= signs_for_sender
    if (correction_to_tbl == 0).all():
        return tbl, other_tbls
    filtered_L_from_tbl[comp_O] = correction_to_tbl
    comp_O_df = filtered_L_from_tbl.copy()
    del comp_O_df[comp_L]
    comp_O_df[pop_age] = comp_O_df[pop_age].apply(str)

    # Apply correction to tbl, and record any correction made to 
    # comps_modifieds[t].
    tbl_cp = tbl.copy()
    tbl_cp[pop_age] = tbl_cp[pop_age].apply(str)
    tbl_cp = tbl_cp.merge(comp_O_df, on = pop_groups, how = 'left')
    tbl_cp.fillna(0, inplace = True)
    tbl_cp[comp_O] = tbl_cp[comp_O].apply(int)
    if (tbl_cp[comp_O].values != 0).any():
        correction = tbl_cp[pop_groups + [comp_O]]
        df_list = []
        for rc in rearranging_col:
            df_list.append(correction[correction[pop_age] == rc])
        correction = pd.concat(df_list)
        comps_modifieds[t].append([correction, 'O', 'itself and other(s)'])
    tbl_cp[comp] += tbl_cp[comp_O]
    del tbl_cp[comp_O]
    if is_subprov:
        tbl_cp = SubProvPopTable(
            tbl_cp,
            reorder_cols = False,
            show_pop_end = show_pop_end,
            flag = False
        )
    else:
        tbl_cp = ProvPopTable(
            tbl_cp,
            reorder_cols = False,
            show_pop_end = show_pop_end,
            flag = False
        )

    # Apply correction to other_tbls, and record any correction made to
    # comps_modifieds[i], where i in tbl_index
    other_tbls_cp = other_tbls.copy()
    for i in tbl_index:
        other_tbl = other_tbls_cp[i].copy()
        other_tbl[pop_age] = other_tbl[pop_age].apply(str)
        comp_N_to_apply = exact_transferrables[i].copy()
        comp_N_to_apply[pop_age] = comp_N_to_apply[pop_age].apply(str)
        other_tbl = other_tbl\
            .merge(
                comp_N_to_apply, 
                on = pop_groups, 
                how = "left"
            )
        other_tbl.fillna(0, inplace = True)
        other_tbl[comp_N] = other_tbl[comp_N].apply(int)
        if (other_tbl[comp_N].values != 0).any():
            other_comp_P = f"{other_comp}_P"
            correction = other_tbl[pop_groups + [comp_N]]\
                .rename(columns = {comp_N: other_comp_P})
            df_list = []
            for rc in rearranging_col:
                df_list.append(correction[correction[pop_age] == rc])
            correction = pd.concat(df_list)
            comps_modifieds[i].append([correction, 'P', t])
        other_tbl[other_comp] += other_tbl[comp_N]
        del other_tbl[comp_N]
        if is_subprov:
            other_tbl = SubProvPopTable(
                other_tbl,
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False
            )
        else:
            other_tbl = ProvPopTable(
                other_tbl,
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False
            )
        other_tbls_cp[i] = other_tbl

    return tbl_cp, other_tbls_cp

def calculate_ages_to_transfer(
    tbl: Union[ProvPopTable, SubProvPopTable],
    comp: str,
    method: Optional[str],
    other_tbls: Optional[dict] = None
):
    '''
    Return the age(s) of end-of-period populations and `comp` to transfer 
    values from `tbl` (to other tbls) based on the `method` specified and
    absorbables based on `other_tbls`.

    Returns
    -------
    A `dict` of {`str`: `numpy.array` of `int`s}.
    '''

    comp_L = f"{comp}_L"
    comp_in_comp_end = comp in tbl.get_comp_end()
    pop_groups = tbl.get_pop_groups()
    pop_age = pop_groups[1]

    I = tbl.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :]
    problematic_age = problematic[pop_age]
    age_max = get_option('age.max')
    age_is_max = problematic_age.is_max()

    # When computing L, it has to include other_tbls into consideration. 
    # That is:
    #     1. Apply get_J() to tables of other_tbls (using problematic_age
    #         from tbl) so that it computes maximum counter-adjustable 
    #         values for each table of other_tbls
    #     2. Sum up maximum counter-adjustables at each neighbouring age
    #     3. Use get_K() based on the sum of maximum counter-adjustables
    #         to compute exact counter-adjustables for tbl
    #     4. Use get_L() to get the combined DataFrame of exact 
    #         counter-adjustables and exact modifiables for tbl

    filtered_L =\
        get_L(tbl, comp, method, other_tbls).query(f"{comp_L} != 0")

    # to_transfer_ages_comp is `numpy.array` of `Age`s here
    to_transfer_ages_comp = filtered_L.copy()[pop_age].values
    if age_is_max and (not comp_in_comp_end):
        # If age_is_max, then old_neigh is disabled.
        to_transfer_ages_comp = np.append(
            to_transfer_ages_comp,
            np.array([Age(age_max), Age(age_max + 1)])
        )
        to_transfer_ages_comp = pd.unique(to_transfer_ages_comp)

    # to_transfer_ages_pop_end is also `numpy.array` of `Age`s here
    to_transfer_ages_pop_end = to_transfer_ages_comp.copy()
    if not comp_in_comp_end:
        to_transfer_ages_pop_end += 1
    to_transfer_ages_pop_end = pd.unique(to_transfer_ages_pop_end)

    # Conversion from `Age` to `int` required
    result = {}
    result['age.to_transfer_comp'] =\
        np.array([a1.get_showing_age() for a1 in to_transfer_ages_comp])
    result['age.to_transfer_pop_end'] =\
        np.array([a2.get_showing_age() for a2 in to_transfer_ages_pop_end])

    return result

def calculate_agg_rem(
    filtered_L_from_tbl: pd.DataFrame, 
    comp_Ms_sum: np.array, 
    age_is_max: bool, 
    comp_in_comp_end: bool,
    other_comp_in_neg: bool
):
    '''
    Calculate the "aggregate remainder". It is computed by first taking
    element-wise minimums of the L-column of `filtered_L_from_tbl` and 
    `comp_Ms_sum`, then some numbers change their signs depending on the 
    condition of `age_is_max`, `comp_in_comp_end`, and `other_comp_in_neg`.

    Returns
    -------
    A `numpy.array` of `int`s.
    '''

    comp_L_abs = abs(filtered_L_from_tbl.iloc[:, -1].values)
    comp_Ms_sum_abs = abs(comp_Ms_sum)
    agg_rem =\
        pd.DataFrame({
            'a': comp_L_abs,
            'b': comp_Ms_sum_abs
        })\
        .min(axis = 1)\
        .values
    signs = calculate_signs(
        len(agg_rem), 
        age_is_max, 
        comp_in_comp_end,
        other_comp_in_neg
    )
    agg_rem *= signs
    
    return agg_rem

def calculate_signs(
    length: int, 
    age_is_max: bool, 
    comp_in_comp_end: bool, 
    other_comp_in_neg: bool
):
    '''
    Return the `np.array` of 1's of length `length` with possibly different
    signs at each element based on information of `age_is_max`,
    `comp_in_comp_end`, and `other_comp_in_neg`.

    Preconditions
    -------------
    1. If `age_is_max` is `True` and `comp_in_comp_end` is `False`, then
        `length` must be greater than or equal to 3 (since the last two 
        slots of the returning `numpy.array` are reserved for modifiable 
        values, and counter-adjustments have to be made in other preceding
        slots).
    2. Otherwise, `length` must be greater than or equal to 2 (since the 
        last slot of the returning `numpy.array` are reserved for the
        modifiable value, and counter-adjustments have to be made in other
        preceding slots).

    Returns
    -------
    A `numpy.array` of `1`s and `-1`s.
    '''

    vec1 = np.repeat([1], length)
    vec1[-1] = -1
    if age_is_max and (not comp_in_comp_end):
        vec1[-2] = -1

    return -vec1 if other_comp_in_neg else vec1

def fix_all_issues(
    poptbls: Union[AggregateProvPopTable, AggregateSubProvPopTable],
    method: Optional[str] = None,
    return_all_mods: bool = False
):
    '''
    Apply modifications and counter-adjustments to `PopTable`s 
    of `self.__tbls_dict` so that there are no negative end-of-period 
    populations. In case of dealing with interprovincial components,
    "transfer and absorption" are also considered. Figures for 
    counter-adjustments in neighbouring ages are different based on 
    `method` specified. Set `return_all_mods` to `True` to get all the
    modifications and counter-adjustments made to each table of 
    `self.__tbls_dict`.

    Usage
    -----
    `fix_all_issues(
        poptbls: Union[AggregateProvPopTable, AggregateSubProvPopTable],
        method: Optional[str] = None,
        return_all_mods: bool = False
    )`

    Arguments
    ---------
    * `poptbls`: either an `AggregateProvPopTable` or 
        `AggregateSubProvPopTable` object
    * `method`: the same argument as in `PopTable.get_K()`
    * `return_all_mods`: a bool (`False` by default); if `True`, this 
        will return all the modifications and counter-adjustments made
        to each table of `self.__tbls_dict`.

    Returns
    -------
    If `return_all_mods` is `False`, then it returns a `dict` of fixed
    versions of `PopTable`s of `self.__tbls_dict`. Keys are 
    indices of those tables in `self.__tbls_dict`, and values are fixed
    tables.
    If `return_all_mods` is `True`, then regardless of whether or not
    there are corrections made to the tables, it returns a `dict` of 
    `PopTableResultsWrapper`s of each table of `self.__tbls_dict`. 
    Keys are indices of those tables in `self.__tbls_dict`, and values 
    are `PopTableResultsWrapper` of each table.
    '''

    tbls_dict = poptbls.get_tbls_dict().copy()
    tbls_dict_sample_key = list(tbls_dict.keys())[0]
    tbl_1st = tbls_dict[tbls_dict_sample_key]
    is_subprov = tbl_1st.is_subprov()
    poptbl_class = SubProvPopTable if is_subprov else ProvPopTable
    
    common_args = tbl_1st.get_args()
    prevs = {}
    for k, v in common_args.items():
        prevs[k] = get_option(k)
        set_option(k, v)
        
    comp_neg_to_use = tbl_1st.get_comp_neg()
    comp_pos_to_use = tbl_1st.get_comp_pos()
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = tbl_1st.get_pop_groups()
    pop_sex = pop_groups[0]
    pop_age = pop_groups[1]
    all_cols = tbl_1st.columns.tolist()
    show_pop_end = tbl_1st.get_pop_end() in all_cols
    sexes = np.unique(tbl_1st[pop_sex])
    method = return_goption_if_None('method', method)

    comps_modifieds = {rl2: [] for rl2 in tbls_dict.keys()}
    muon_pal = [(False, 1), (True, 1), (False, 0), (True, 0)]

    # set_option(...) statement here shows that the predefined values of
    # `method_use.old_neigh` and `pop.at_least` will NOT be used.
    # That is, whatever you defined outside of this function will NOT be
    # used; only values in `muon_pal` will be used.
    set_option(
        'method_use.old_neigh', muon_pal[0][0],
        'pop.at_least', muon_pal[0][1]
    )
    fixed_tables = produce_fixed_tables(
        tbls_dict, 
        sexes, 
        pop_sex,
        pop_age,
        poptbl_class,
        is_subprov,
        show_pop_end,
        comps,
        method,
        comps_modifieds
    )
    still_has_neg = []
    for r in fixed_tables.keys():
        still_has_neg.append(
            (fixed_tables[r].calculate_pop().iloc[:, -1].values < 0).any()
        )
    has_neg = any(still_has_neg)
    mp = 1
    while has_neg and mp != len(muon_pal):
        set_option(
            'method_use.old_neigh', muon_pal[mp][0],
            'pop.at_least', muon_pal[mp][1]
        )
        fixed_tables = produce_fixed_tables(
            fixed_tables, 
            sexes, 
            pop_sex,
            pop_age,
            poptbl_class,
            is_subprov,
            show_pop_end,
            comps,
            method,
            comps_modifieds
        )
        still_has_neg = []
        for r in fixed_tables.keys():
            still_has_neg.append(
                (fixed_tables[r].calculate_pop().iloc[:, -1].values < 0)\
                .any()
            )
        has_neg = any(still_has_neg)
        mp += 1

    set_option(
        'method_use.old_neigh', muon_pal[0][0],
        'pop.at_least', muon_pal[0][1]
    )
    for k2, v2 in prevs.items():
        set_option(k2, v2)

    if return_all_mods:
        if method == '1dist':
            musp = get_option("method_use.second_pass")
            museq = get_option("method_use.seq")
            aps = get_option("age.prop_size")
            pass2 = ", 2nd pass" if musp else ""
            pass2seq =\
                f", {aps}-year sequence" if (musp and museq) else ""
            method = f"{method}{pass2}{pass2seq}"
        result = {
            rl4: PopTableResultsWrapper(
                orig_table = tbls_dict[rl4],
                result_fix_issues = [tbl4] + comps_modifieds[rl4],
                method = method
            ) \
            for rl4, tbl4 in fixed_tables.copy().items()
        }
        return result
    else:
        return fixed_tables

def get_Ms(
    tbl: Union[ProvPopTable, SubProvPopTable],
    comp: str,
    method: Optional[str],
    other_tbls: dict
):
    '''
    Compute the maximum amount that is transferrable from `comp` of `tbl`
    to the "other_comp" of `other_tbls` based on `method` specified.

    Arguments
    ---------
    * `tbl`: a `ProvPopTable` or `SubProvPopTable`
    * `comp`: a `str`; either:
        1. `tbl.get_interprov_out()` or `tbl.get_interprov_in()` if `tbl`
            is `ProvPopTable`
        2. any (negative or positive) component if `tbl` is 
            `SubProvPopTable`
    * `other_tbls`: a `dict` of:
        1. {`int`: `ProvPopTable`} if `tbl` is `ProvPopTable`
        2. {`int`: `SubProvPopTable`} if `tbl` is `SubProvPopTable`
    * `method`: a `str`; an argument of `tbl.get_L(comp, method)`

    Details
    -------
    1. If `tbl` is `ProvPopTable`: for a given interprovincial migration 
        component `comp`, the function computes the maximum transferrable 
        values for each `ProvPopTable` of `other_tbls`. That is, the 
        function computes how much of a possible correction to be made in 
        `tbl[comp]` (e.g. interprovincial migration OUT) is actually 
        transferrable (or "counter-counter-adjustable") using the opposite
        interprovincial migration components (e.g. interprovincial
        migration IN) of tables in `other_tbls`.
    2. If `tbl` is `SubProvPopTable`: for a given `tbl`, a 
        `SubProvPopTable`, the function computes the maximum transferrable
        values from `tbl[comp]` to:
            + `other_tbls[i][comp]` for an index i if `comp` is neither
                "intraprovincial migration OUT" nor "intraprovincial 
                migration IN", i.e. "other_comp" is the same as `comp` if 
                `tbl` is `SubProvPopTable` and `comp` is neither of the
                intraprovincial components of `tbl`;
            + `other_tbls[i][other_comp]` for an index i, where 
                `other_comp` is "intraprovincial migration IN" if `comp` is
                "intraprovincial migration OUT", and "intraprovincial 
                migration OUT" if `comp` is "intraprovincial migration IN",
                i.e. it behaves the same as `ProvPopTable` if `comp` is
                either of the intraprovincial components of `tbl`

    Returns
    -------
    Two `dict`s:
    1. A `dict` of {`int`: `pandas.DataFrame`}, where each DataFrame has 
        three columns: `pop.sex`, `pop.age`, and `comp_M` which stores 
        maximum transferrable values (at each record) from `tbl[comp]` to 
        `other_tbls[i][other_comp]` for an integer `i`;
    2. A `dict` of {`int`: `pandas.DataFrame`}, where each DataFrame has
        three columns: `pop.sex`, `pop.age`, and the column with the name
        "max_peal_0", which is computed as `max(pop.end - at.least, 0)`
        for each table.
    '''

    # Define constants
    to_transfer_ages = calculate_ages_to_transfer(
        tbl,
        comp,
        method,
        other_tbls
    )
    to_transfer_ages_pop_end = to_transfer_ages['age.to_transfer_pop_end']
    to_transfer_ages_comp = to_transfer_ages['age.to_transfer_comp']
    at_least = get_option('pop.at_least')
    pop_groups = tbl.get_pop_groups()
    pop_age = pop_groups[1]
    pop_end = tbl.get_pop_end()
    comp_L = f"{comp}_L"
    comp_M = f"{comp}_M"
    other_comp = get_other_comp(tbl, comp)
    problematic_age = Age(to_transfer_ages_pop_end[-1])
    comp_in_neg = comp in tbl.get_comp_neg()
    comp_in_comp_end = comp in tbl.get_comp_end()

    # Get exact amount to be corrected in tbl
    L_df = get_L(tbl, comp, method, other_tbls)
    filtered_L_from_tbl = L_df[
        L_df[pop_age]\
            .apply(Age.get_showing_age)\
            .apply(str)\
            .isin([str(sc) for sc in to_transfer_ages_comp])
    ]

    # Get respective end-of-period populations of other_tbls
    others_tbl_pop_end = {
        i0: tb0.calculate_pop()[
            tb0.calculate_pop()[pop_age]\
                .apply(Age.get_showing_age)\
                .apply(str)\
                .isin([str(sp) for sp in to_transfer_ages_pop_end])
        ] \
        for i0, tb0 in other_tbls.copy().items()        
    }
    otpe_sample_key = list(others_tbl_pop_end.keys())[0]
    no_need_for_rearranging =\
        (
            others_tbl_pop_end[otpe_sample_key][pop_age].values ==\
            to_transfer_ages_pop_end
        )\
        .all()
    if not no_need_for_rearranging:
        others_tbl_pop_end = rearrange_rows(
            others_tbl_pop_end, 
            to_transfer_ages_pop_end,
            pop_age
        )
    others_pop_end = {
        i1: tb1.assign(
            max_peal_0 = lambda df: df[pop_end].apply(
                lambda x: max(x - at_least, 0)
            )
        )\
        [pop_groups + ['max_peal_0']] \
        for i1, tb1 in others_tbl_pop_end.copy().items()
    }

    # Get respective correctable amounts in other_comp of other_tbls
    others_other_comp = {
        i2: tb2[
            tb2[pop_age]\
                .apply(Age.get_showing_age)\
                .apply(str)\
                .isin([str(sc) for sc in to_transfer_ages_comp])
        ]\
        [pop_groups + [other_comp]] \
        for i2, tb2 in other_tbls.copy().items()
    }
    if not no_need_for_rearranging:
        others_other_comp = rearrange_rows(
            others_other_comp,
            to_transfer_ages_comp,
            pop_age
        )
    max_transferrables_to_other_comp = {
        i2_1: tbl2_1[pop_groups] \
        for i2_1, tbl2_1 in others_other_comp.copy().items()
    }

    case_where_other_comp_is_neg = None
    if other_comp == comp:
        # subprov given
        # neither intraprov_out nor intraprov_in
        case_where_other_comp_is_neg = True if comp_in_neg else False
    else:
        # if prov, then comp is either interprov_out or interprov_in
        # if subprov, then comp is either intraprov_out or intraprov_in
        case_where_other_comp_is_neg = False if comp_in_neg else True    

    if problematic_age.is_max() and (not comp_in_comp_end):
        filtered_L_from_tbl_ca = filtered_L_from_tbl[comp_L].values[:-2]
        filtered_L_from_tbl_ms = filtered_L_from_tbl[comp_L].values[-2:]
        for i4 in others_pop_end.copy().keys():
            # other_tbl_max_peal_0_ca =\
            #     others_pop_end[i4]['max_peal_0'].values[:-1]
            other_tbl_max_peal_0_m =\
                others_pop_end[i4]['max_peal_0'].values[-1]
            other_tbl_other_comp_ca =\
                others_other_comp[i4][other_comp].values[:-2]
            other_tbl_other_comp_ms =\
                others_other_comp[i4][other_comp].values[-2:]
            transferrable_vals = get_Ms_case1(
                filtered_L_from_tbl_ca,
                filtered_L_from_tbl_ms,
                other_tbl_other_comp_ca,
                other_tbl_other_comp_ms,
                other_tbl_max_peal_0_m,
                case_where_other_comp_is_neg
            )
            max_transferrables_to_other_comp[i4][comp_M] =\
                transferrable_vals
    else:
        filtered_L_from_tbl_ca = filtered_L_from_tbl[comp_L].values[:-1]
        filtered_L_from_tbl_m = filtered_L_from_tbl[comp_L].values[-1]
        for i3 in others_pop_end.copy().keys():
            other_tbl_max_peal_0_m =\
                others_pop_end[i3]['max_peal_0'].values[-1]
            other_tbl_other_comp_ca =\
               others_other_comp[i3][other_comp].values[:-1]
            other_tbl_other_comp_m =\
                others_other_comp[i3][other_comp].values[-1]
            transferrable_vals = get_Ms_case2(
                filtered_L_from_tbl_ca,
                filtered_L_from_tbl_m,
                other_tbl_other_comp_ca,
                other_tbl_other_comp_m,
                other_tbl_max_peal_0_m,
                case_where_other_comp_is_neg
            )
            max_transferrables_to_other_comp[i3][comp_M] =\
                transferrable_vals

    return max_transferrables_to_other_comp, others_pop_end

def get_Ms_case1(
    filtered_L_from_tbl_ca,
    filtered_L_from_tbl_ms,
    other_tbl_other_comp_ca,
    other_tbl_other_comp_ms,
    other_tbl_max_peal_0_m,
    case_where_other_comp_is_neg
):
    '''
    Calculate the maximum transferable values when:
    
        1. the problematic age is the maximum age, AND;
        2. comp is NOT an end-of-period component.
    '''

    if case_where_other_comp_is_neg:
        # comp_in_neg if other_comp_is_comp
        # else comp in [interprov_in, intraprov_in]
        df_transferrable_ca = pd.DataFrame({
            'b': abs(filtered_L_from_tbl_ca),
            'c': other_tbl_other_comp_ca
        })
        transferrable_vals_at_ca =\
            -df_transferrable_ca.min(axis = 1).values
        abs_sum_trans_val_ca =\
            abs(sum(transferrable_vals_at_ca))
        a = min(
            other_tbl_max_peal_0_m,
            abs(filtered_L_from_tbl_ms[0]),
            abs_sum_trans_val_ca
        )
        b = min(
            other_tbl_max_peal_0_m - a,
            abs(filtered_L_from_tbl_ms[1]),
            abs_sum_trans_val_ca - a
        )
        top_items =\
            [0 for i6 in range(len(transferrable_vals_at_ca))]\
            if (a == 0 and b == 0) \
            else list(transferrable_vals_at_ca)
    else:
        # not comp_in_neg if other_comp_is_comp
        # else comp in [interprov_out, intraprov_out]
        b = -min(
            other_tbl_max_peal_0_m,
            abs(filtered_L_from_tbl_ms[1]),
            other_tbl_other_comp_ms[1]
        )
        a = -min(
            other_tbl_max_peal_0_m - abs(b),
            abs(filtered_L_from_tbl_ms[0]),
            other_tbl_other_comp_ms[0]
        )
        top_items =\
            [0 for i5 in range(len(filtered_L_from_tbl_ca))] \
            if (a == 0 and b == 0) \
            else list(abs(filtered_L_from_tbl_ca))

    return top_items + [a, b]

def get_Ms_case2(
    filtered_L_from_tbl_ca,
    filtered_L_from_tbl_m,
    other_tbl_other_comp_ca,
    other_tbl_other_comp_m,
    other_tbl_max_peal_0_m,
    case_where_other_comp_is_neg
):
    '''
    Calculate the maximum transferable values when:

        1. the problematic age is NOT the maximum age, OR;
        2. comp is an end-of-period component.
    '''

    if case_where_other_comp_is_neg:
        # comp_in_neg if other_comp_is_comp
        # else comp in [interprov_in, intraprov_in]
        df_transferrable_ca = pd.DataFrame({
            'b': abs(filtered_L_from_tbl_ca),
            'c': other_tbl_other_comp_ca
        })
        transferrable_vals_at_ca =\
            -df_transferrable_ca.min(axis = 1).values
        transferrable_val_at_m = min(
            other_tbl_max_peal_0_m,
            abs(filtered_L_from_tbl_m),
            abs(sum(transferrable_vals_at_ca))
        )
        top_items =\
            [0 for i8 in range(len(transferrable_vals_at_ca))]\
            if (transferrable_val_at_m == 0) \
            else list(transferrable_vals_at_ca)
    else:
        # not comp_in_neg if other_comp_is_comp
        # else comp in [interprov_out, intraprov_out]
        transferrable_val_at_m = -min(
            other_tbl_max_peal_0_m,
            abs(filtered_L_from_tbl_m),
            other_tbl_other_comp_m
        )
        top_items =\
            [0 for i7 in range(len(filtered_L_from_tbl_ca))]\
            if (transferrable_val_at_m == 0) \
            else list(abs(filtered_L_from_tbl_ca))

    return top_items + [transferrable_val_at_m]

def get_Ns(
    tbl: Union[ProvPopTable, SubProvPopTable],
    comp: str,
    method: Optional[str],
    other_tbls: dict
):
    '''
    Calculate exact transferrables from `tbl[comp]` to other tables of 
    `other_tbls`. Values are based on `tbl`'s "comp_L vector" computed by 
    `method`.

    Returns
    -------
    A `dict` of `{int: pandas.DataFrame}` where keys of returning `dict` is
    the same as `other_tbls.keys()`, and values are `pandas.DataFrame` with
    the following column names: `pop.sex`, `pop.age`, and `comp_N`. 
    `comp_N` stores the exact values of correction at each record for each
    table of `other_tbls`.
    '''

    comp_M = f"{comp}_M"
    comp_N = f"{comp}_N"
    other_comp = get_other_comp(tbl, comp)
    other_comp_in_neg = other_comp in tbl.get_comp_neg()
    pop_groups = tbl.get_pop_groups()
    pop_age = pop_groups[1]

    to_transfer_ages = calculate_ages_to_transfer(
        tbl,
        comp,
        method,
        other_tbls
    )
    to_transfer_ages_comp = to_transfer_ages['age.to_transfer_comp']
    L_df = get_L(tbl, comp, method, other_tbls)
    filtered_L_from_tbl = L_df[
        L_df[pop_age]\
            .apply(Age.get_showing_age)\
            .apply(str)\
            .isin([str(sc) for sc in to_transfer_ages_comp])
    ]

    max_transferrables, other_tbls_max_peal_0 = get_Ms(
        tbl, 
        comp, 
        method, 
        other_tbls
    )
    tbl_index, sample_key = sort_tbl_index(other_tbls_max_peal_0)
    problematic_age = other_tbls_max_peal_0[sample_key][pop_age].values[-1]
    age_is_max = problematic_age.is_max()
    comp_in_comp_end = comp in tbl.get_comp_end()
    nrow = len(max_transferrables[sample_key].index)
    comp_Ms_sum = np.repeat([0], nrow)
    for v2 in max_transferrables.copy().values():
        comp_Ms_sum += v2[comp_M].values

    # Calculate the aggregate remainder using filtered_L and comp_Ms_sum
    agg_rem = calculate_agg_rem(
        filtered_L_from_tbl, 
        comp_Ms_sum, 
        age_is_max, 
        comp_in_comp_end,
        other_comp_in_neg
    )

    # Generate comp_N for each table of other_tbls
    # Note: max_transferrables have values so that the sum of absolute
    # values of counter-adjustables is ALWAYS greater than or equal to
    # the sum of absolute values of modifiables, i.e. `flag` of the 
    # while-loop will NECESSARILY become False at some point.
    exact_transferrables = max_transferrables.copy()
    for i0 in tbl_index:
        exact_transferrables[i0][comp_N] = 0

    # signs_for_receiver = (+ -) if the receiver is positive:
    #     e.g.1. (not is_subprov) comp is IOM (neg) 
    #         so other_comp is IIM (pos);
    #     e.g.2. (is_subprov) comp is IMM (pos) 
    #         so other_comp is also IMM (pos)
    # signs_for_receiver = (- +) if the receiver is negative:
    #     e.g.1. (not is_subprov) comp is IIM (pos)
    #         so other_comp is IOM (neg);
    #     e.g.2. (is_subprov) comp is DTH (neg)
    #         so other_comp is also DTH (neg)
    signs_for_receiver = calculate_signs(
        nrow, 
        age_is_max, 
        comp_in_comp_end,
        other_comp_in_neg
    )

    flag = True
    while flag:
        if age_is_max and (not comp_in_comp_end):
            for i1 in tbl_index:
                comp_M_local = exact_transferrables[i1][comp_M].values
                df_local = pd.DataFrame({
                    'abs_agg_rem': abs(agg_rem),
                    'abs_comp_M_local': abs(comp_M_local)
                })
                agg_rem_local = df_local.min(axis = 1).values
                agg_rem_local *= signs_for_receiver
                comp_N_local = np.repeat([0], nrow)
                local_rem = abs(agg_rem_local[-2:])
                at_least_one_to_ca = False
                if local_rem[-1] >= 1:
                    comp_N_local[-1] = 1 if other_comp_in_neg else -1
                    at_least_one_to_ca = True
                elif local_rem[-2] >= 1:
                    comp_N_local[-2] = 1 if other_comp_in_neg else -1
                    at_least_one_to_ca = True
                
                if at_least_one_to_ca:
                    for j1 in range(nrow - 3, -1, -1):
                        if abs(agg_rem_local[j1]) >= 1:
                            comp_N_local[j1] =\
                                -1 if other_comp_in_neg else 1
                            break
                agg_rem -= comp_N_local
                exact_transferrables[i1][comp_M] -= comp_N_local
                exact_transferrables[i1][comp_N] += comp_N_local
            flag = (agg_rem[-2:] != [0, 0]).any()
        else:
            for i2 in tbl_index:
                comp_M_local = exact_transferrables[i2][comp_M].values
                df_local = pd.DataFrame({
                    'abs_agg_rem': abs(agg_rem),
                    'abs_comp_M_local': abs(comp_M_local)
                })
                agg_rem_local = df_local.min(axis = 1).values
                agg_rem_local *= signs_for_receiver
                comp_N_local = np.repeat([0], nrow)
                local_rem = abs(agg_rem_local[-1])
                if local_rem >= 1:
                    comp_N_local[-1] = 1 if other_comp_in_neg else -1
                    for j2 in range(nrow - 2, -1, -1):
                        if abs(agg_rem_local[j2]) >= 1:
                            comp_N_local[j2] =\
                                -1 if other_comp_in_neg else 1
                            break
                agg_rem -= comp_N_local
                exact_transferrables[i2][comp_M] -= comp_N_local
                exact_transferrables[i2][comp_N] += comp_N_local
            flag = (agg_rem[-1] != 0)

    for i3 in tbl_index:
        del exact_transferrables[i3][comp_M]

    return exact_transferrables

def produce_fixed_tables(
    tbls_dict, 
    sexes, 
    pop_sex,
    pop_age,
    poptbl_class,
    is_subprov,
    show_pop_end,
    comps,
    method,
    comps_modifieds
):
    '''
    Produce fixed tables of `tbls_dict` and return those fixed_tables.
    Update `comps_modifieds` along the way.

    Arguments
    ---------
    * `tbls_dict`: a dict; the return value of 
        `Aggregate*PopTable.get_tbls_dict()`
    * `sexes`: a list-like; an array of all sexes in each table
    * `pop_sex`: a str; the name of sex column
    * `pop_age`: a str; the name of age column
    * `poptbl_class`: either `ProvPopTable` or `SubProvPopTable`
    * `is_subprov`: a bool; Is each table `SubProvPopTable`?
    * `show_pop_end`: a bool; Should each table show the end-of-period 
        populations?
    * `comps`: a list; a list of all components in each table
    * `method`: a str; one of "1dist", "filler", or "prop"
    * `comps_modifieds`: a dict of `{k: list-like}` where `k` is 
        `tbls_dict.keys()`
    '''

    fixed_tables = {
        rl1: {s: None for s in sexes} 
        for rl1 in tbls_dict.keys()
    }

    for sex in sexes:
        dict_all_tbls = {
            tt: [
                poptbl_class(
                    ttbl.copy().loc[lambda df: df[pop_sex] == sex],
                    reorder_cols = False, 
                    show_pop_end = show_pop_end,
                    flag = False
                )
            ] \
            for tt, ttbl in tbls_dict.items()
        }
        dat_keys = sort_tbl_index_simpler(dict_all_tbls)
        for t in dat_keys:
            # other_tbls is based on the result of previous 
            # iteration(s).
            other_tbls = dict_all_tbls.copy()
            tbl = other_tbls.pop(t)
            tbl = tbl[-1]
            interprovs = [
                tbl.get_interprov_out(),
                tbl.get_interprov_in()
            ]
            other_tbls = {
                t_other: tbl_other[-1] \
                for t_other, tbl_other in other_tbls.items()
            }
            flag = (sum(tbl.get_I()['I'].values != 0) != 0)
            i = 0
            num_zeros = sum(tbl.get_I()['I'].values == 0)
            masked_ages = []
            if flag:
                prob_ages =\
                    tbl.get_I().query('I != 0')[pop_age].values
                prob_ages = [str(a) for a in prob_ages.copy()]
            while flag:
                comp = comps[i]
                current_prob_age = str(
                    tbl.get_I().query('I != 0')[pop_age].values[0]
                )

                if is_subprov:
                    L_df = get_L(tbl, comp, method, other_tbls)
                    if (L_df.iloc[:, -1] != 0).any():
                        tbl, other_tbls = apply_Ns(
                            tbl,
                            t,
                            comp,
                            method,
                            other_tbls,
                            comps_modifieds
                        )
                else:
                    if comp in interprovs:
                        tbl, other_tbls = apply_Ns(
                            tbl,
                            t,
                            comp,
                            method,
                            other_tbls,
                            comps_modifieds
                        )
                    else:
                        tbl = apply_L(
                            tbl,
                            comp,
                            method,
                            comps_modifieds[t]
                        )
                
                I_vec = tbl.get_I()['I'].values
                new_num_zeros = sum(I_vec == 0)
                if all(I_vec == 0):
                    flag = False
                elif num_zeros != new_num_zeros:
                    i = 0
                    num_zeros = new_num_zeros
                elif i != (len(comps) - 1):
                    i += 1
                else:
                    # i.e. lack of values for corrections
                    # Correction could not be made to the problematic 
                    # record at the current problematic age.
                    if current_prob_age == prob_ages[-1]:
                        flag = False
                    else:
                        masked_ages.append(current_prob_age)
                        set_option('age.mask', masked_ages)
                        I_vec = tbl.get_I()['I'].values
                        new_num_zeros = sum(I_vec == 0)
                        i = 0
                        num_zeros = new_num_zeros
            set_option('age.mask', [])

            # Update dict_all_tbls after correcting tbl and 
            # (possibly) other_tbls
            for t1 in dat_keys:
                dict_all_tbls[t1].clear()
                if t1 == t:
                    dict_all_tbls[t1].append(tbl)
                else:
                    dict_all_tbls[t1].append(other_tbls[t1])

        # Update fixed_tables after applying corrections to all 
        # population tables of dict_all_tbls
        for t2 in fixed_tables.copy().keys():
            fixed_tables[t2][sex] = dict_all_tbls[t2][-1]

    # Bind rows of PopTables for each subdict in fixed_tables
    fixed_tables = {
        ind: reduce(
            lambda a, b: a.append(b, ignore_index = True),
            dict_tbl_by_sex.values()
        ) \
        for ind, dict_tbl_by_sex in fixed_tables.items()
    }

    # Convert DataFrames of fixed_tables into poptbl_class
    fixed_tables = {
        rl3: poptbl_class(
            tbl3.sort_values([pop_sex, pop_age]),
            reorder_cols = False, 
            show_pop_end = show_pop_end,
            flag = False
        ) \
        for rl3, tbl3 in fixed_tables.copy().items()
    }

    return fixed_tables

def rearrange_rows(dict_of_df, by, col):
    '''
    Rearrange rows of DataFrames in `dict_of_df` based on the array `by`
    and values in `df[col]`.

    Details
    -------
    Rows of each DataFrame in `dict_of_df` will be rearranged (or 
    reordered) by the values appeared in `by`. Rows will be reordered by
    matching values in `by` and the value in each `col`.
    '''

    result = {}
    for k, df in dict_of_df.copy().items():
        df_list = []
        for i in by:
            df_list.append(df[df[col] == i])
        result[k] = pd.concat(df_list)

    return result

def sort_tbl_index(other_tbls_pop_end: dict):
    '''
    Sort other_tbls_pop_end.keys() by:
        1. the end-of-period population at the problematic age, and;
        2. the sum of end-of-period populations of neighbouring ages
    in this order in descending orders.

    Returns
    -------
    Two items, in this order:
    1. A `numpy.array` of `int`s
    2. One of the keys of `other_tbls_pop_end`
    '''

    ind = []
    pe_problematic = []
    sum_nei = []
    sample_key = None
    for k, v in other_tbls_pop_end.items():
        ind.append(k)
        pe_problematic.append(v.iloc[:, -1].values[-1])
        sum_nei.append(v.iloc[:, -1].values[:-1].sum())
        sample_key = k

    index_tbl = {
        'ind': ind,
        'pe_problematic': pe_problematic,
        'sum_nei': sum_nei
    }
    index_tbl = pd.DataFrame(index_tbl)
    index_tbl = index_tbl\
        .sort_values(
            ['pe_problematic', 'sum_nei'],
            ascending = [False, False]
        )
    
    return index_tbl['ind'].values, sample_key

def sort_tbl_index_simpler(dict_all_tbls: dict):
    '''
    Sort keys of `dict_all_tbls` by the number of end-of-period population
    in the descending order.

    Returns
    -------
    A `list` of `object`s (dict_all_tbls.keys()).
    '''

    pops = {
        k: lst_v[-1].calculate_pop().iloc[:, -1].sum() \
        for k, lst_v in dict_all_tbls.items()
    }
    result_pops = {'keys': [], 'vals': []}
    for k2, v2 in pops.items():
        result_pops['keys'].append(k2)
        result_pops['vals'].append(v2)
    result_pops = pd.DataFrame(result_pops)
    result_pops = result_pops.sort_values(['vals'], ascending = [False])

    return result_pops['keys'].tolist()
