
from estime2.age import Age
from typing import (
    List,
    Optional
)
import matplotlib.pyplot as plt
import numpy as np



def plot_correction(
    result_fix_issues: List, 
    corrections_type: List,
    corrections_from: List,
    num: Optional[int] = None, 
    age_range: Optional[List[int]] = None,
    alpha: float = .5
):
    '''
    Get the barplot of ages vs. `num`-th correction made in 
    `result_fix_issues` filtered by `age_range`. Provide more information 
    about the selected correction in `result_fix_issues` via 
    `corrections_type` and `corrections_from`. Set `alpha` for 
    transparency.

    Usage
    -----
    `plot_correction(
        result_fix_issues, 
        corrections_type,
        corrections_from,
        num[, age_range, alpha]
    )`

    Argument
    --------
    * `result_fix_issues`: a list; return value of 
        `ProvPopTable.fix_issues(return_all_mods = True)` or
        `SubProvPopTable.fix_issues(return_all_mods = True)`.
    * `corrections_type`: a list of `str` ('L', 'O', or 'P') of length 
        `len(result_fix_issues) - 1`; a list specifying the type of each 
        correction in `result_fix_issues`
    * `corrections_from`: a list of `object`s of length
        `len(result_fix_issues) - 1`; a list specifying the source
        of each correction in `result_fix_issues`
    * `num`: an int, `None` by default; the order number of the correction 
        made. For example, `num = 3` means the function will display the
        3rd correction applied to the table. If left `None`, then the error
        is raised.
    * `age_range`: a list of two ints, `None` by default; only the records
        of the correction having Ages within the closed interval defined by
        this argument are used. If `None`, then all the Ages greater than 
            the minimum age of nonzero correction up to and including the 
            modification age are used in the plot.
    * `alpha`: a float, .5 by default; the argument to control transparency
        of a plot
    '''

    poptbl = result_fix_issues[0]
    pop_groups = poptbl.get_pop_groups()
    age = pop_groups[1]

    c_to_work_with = result_fix_issues[num].sort_values(pop_groups)
    c_type = corrections_type[num - 1]
    c_from = corrections_from[num - 1]
    p_sex = c_to_work_with.iloc[-1, :].values[0]
    comp_L = c_to_work_with.iloc[:, -1].name
    p_comp = comp_L[:-2]
    min_age_with_nonzero_correction =\
        c_to_work_with.loc[lambda df: df[comp_L] != 0][age].values[0]
    max_age_with_nonzero_correction =\
        c_to_work_with.loc[lambda df: df[comp_L] != 0][age].values[-1]

    if age_range is not None:
        c_to_work_with = c_to_work_with\
            .loc[lambda df: df[age].apply(Age) >= age_range[0]]\
            .loc[lambda df: df[age].apply(Age) <= age_range[1]]
    else:
        c_to_work_with = c_to_work_with\
            .loc[
                lambda df: df[age].apply(Age) >=\
                    min_age_with_nonzero_correction
            ]\
           .loc[
                lambda df: df[age].apply(Age) <=\
                    max_age_with_nonzero_correction
            ]

    plt.bar(
        c_to_work_with[age].apply(str),
        c_to_work_with[comp_L],
        alpha = alpha
    )
    plt.suptitle(f"Corrections made at {p_comp}, correction number {num}")
    plt.title(f"sex {p_sex} type {c_type} from {c_from}")
    plt.xlabel(f"{age}")
    plt.ylabel(f"Corrections in {p_comp}")

def plot_pop(
    poptbl, 
    sex = None,
    age_range: Optional[List[int]] = None, 
    alpha: float = .5
):
    '''
    Get the barplot of ages vs. end-of-period populations of `poptbl`
    filtered by `sex` and `age_range`. Set `alpha` for transparency.

    Usage
    -----
    `plot_pop(poptbl[, sex, age_range, alpha])`

    Argument
    --------
    * `poptbl`: a `ProvPopTable` or `SubProvPopTable`
    * `sex`: an object, `None` by default; use only records having the same
        `sex` in `poptbl`. If `None`, then the function checks if `poptbl`
        has an unique `sex`. If it does, it uses that `sex`; otherwise, it
        raises an error.
    * `age_range`: a list of two ints, `None` by default; only the records
        of `poptbl` having Ages within the closed interval defined by 
        this argument are used. If `None`, then all the Ages are used in
        the plot.
    * `alpha`: a float, .5 by default; the argument to control transparency
        of a plot
    '''

    pop_groups = poptbl.get_pop_groups()
    pop_sex = pop_groups[0]
    pop_age = pop_groups[1]
    pop_end = poptbl.get_pop_end()
    poptbl_pop = poptbl.calculate_pop()
    if sex is None:
        test_uniqueness = np.unique(poptbl[pop_sex])
        assert len(test_uniqueness) == 1, \
            "There are more than one sex in `poptbl`. " +\
            "Specification of `sex` argument is required."
        sex = test_uniqueness[0]
    if age_range is not None:
        poptbl_pop = poptbl_pop\
            .loc[lambda df: df[pop_age] >= age_range[0]]\
            .loc[lambda df: df[pop_age] <= age_range[1]]
    poptbl_pop = poptbl_pop.loc[lambda df: df[pop_sex] == sex]
    plt.bar(
        poptbl_pop[pop_age].apply(str),
        poptbl_pop[pop_end],
        alpha = alpha
    )
