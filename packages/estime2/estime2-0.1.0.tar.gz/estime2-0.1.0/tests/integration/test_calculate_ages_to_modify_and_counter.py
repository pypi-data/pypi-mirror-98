
import estime2
import pytest



class TestCalculateAgesToModifyAndCounter:
    '''
    Test behaviours of the 
    `estime2.poptable.calculate_ages_to_modify_and_counter` function.
    '''

    @pytest.mark.parametrize(
        "problematic_age, comp_in_comp_end, expecteds",
        [
            (
                estime2.Age('100+'), False, {
                    'TT': {'age.to_modify': [99, 100], 'age.to_counter': [50, 98]},
                    'TF': {'age.to_modify': [99, 100], 'age.to_counter': [59, 98]},
                    'FT': {'age.to_modify': [99, 100], 'age.to_counter': [50, 98]},
                    'FF': {'age.to_modify': [99, 100], 'age.to_counter': [59, 98]}
                }
            ),
            (
                estime2.Age('100+'), True, {
                    'TT': {'age.to_modify': 100, 'age.to_counter': [50, 99]},
                    'TF': {'age.to_modify': 100, 'age.to_counter': [60, 99]},
                    'FT': {'age.to_modify': 100, 'age.to_counter': [50, 99]},
                    'FF': {'age.to_modify': 100, 'age.to_counter': [60, 99]}
                }
            ),
            (
                estime2.Age(99), False, {
                    'TT': {'age.to_modify': 98, 'age.to_counter': [99, 100]},
                    'TF': {'age.to_modify': 98, 'age.to_counter': [99, 100]},
                    'FT': {'age.to_modify': 98, 'age.to_counter': [50, 97]},
                    'FF': {'age.to_modify': 98, 'age.to_counter': [58, 97]}
                }
            ),
            (
                estime2.Age(99), True, {
                    'TT': {'age.to_modify': 99, 'age.to_counter': [100, 100]},
                    'TF': {'age.to_modify': 99, 'age.to_counter': [100, 100]},
                    'FT': {'age.to_modify': 99, 'age.to_counter': [50, 98]},
                    'FF': {'age.to_modify': 99, 'age.to_counter': [59, 98]}
                }
            ),
            (
                estime2.Age(97), False, {
                    'TT': {'age.to_modify': 96, 'age.to_counter': [97, 100]},
                    'TF': {'age.to_modify': 96, 'age.to_counter': [97, 100]},
                    'FT': {'age.to_modify': 96, 'age.to_counter': [50, 95]},
                    'FF': {'age.to_modify': 96, 'age.to_counter': [56, 95]}
                }
            ),
            (
                estime2.Age(97), True, {
                    'TT': {'age.to_modify': 97, 'age.to_counter': [98, 100]},
                    'TF': {'age.to_modify': 97, 'age.to_counter': [98, 100]},
                    'FT': {'age.to_modify': 97, 'age.to_counter': [50, 96]},
                    'FF': {'age.to_modify': 97, 'age.to_counter': [57, 96]}
                }
            ),
            (
                estime2.Age(55), False, {
                    'TT': {'age.to_modify': 54, 'age.to_counter': [55, 94]},
                    'TF': {'age.to_modify': 54, 'age.to_counter': [55, 94]},
                    'FT': {'age.to_modify': 54, 'age.to_counter': [14, 53]},
                    'FF': {'age.to_modify': 54, 'age.to_counter': [14, 53]}
                }
            ),
            (
                estime2.Age(55), True, {
                    'TT': {'age.to_modify': 55, 'age.to_counter': [56, 95]},
                    'TF': {'age.to_modify': 55, 'age.to_counter': [56, 95]},
                    'FT': {'age.to_modify': 55, 'age.to_counter': [15, 54]},
                    'FF': {'age.to_modify': 55, 'age.to_counter': [15, 54]}
                }
            ),
            (
                estime2.Age(45), False, {
                    'TT': {'age.to_modify': 44, 'age.to_counter': [45, 84]},
                    'TF': {'age.to_modify': 44, 'age.to_counter': [45, 84]},
                    'FT': {'age.to_modify': 44, 'age.to_counter': [4, 43]},
                    'FF': {'age.to_modify': 44, 'age.to_counter': [4, 43]}
                }
            ),
            (
                estime2.Age(45), True, {
                    'TT': {'age.to_modify': 45, 'age.to_counter': [46, 85]},
                    'TF': {'age.to_modify': 45, 'age.to_counter': [46, 85]},
                    'FT': {'age.to_modify': 45, 'age.to_counter': [5, 44]},
                    'FF': {'age.to_modify': 45, 'age.to_counter': [5, 44]}
                }
            ),
            (
                estime2.Age(7), False, {
                    'TT': {'age.to_modify': 6, 'age.to_counter': [7, 50]},
                    'TF': {'age.to_modify': 6, 'age.to_counter': [7, 46]},
                    'FT': {'age.to_modify': 6, 'age.to_counter': [-1, 5]},
                    'FF': {'age.to_modify': 6, 'age.to_counter': [-1, 5]}
                }
            ),
            (
                estime2.Age(7), True, {
                    'TT': {'age.to_modify': 7, 'age.to_counter': [8, 50]},
                    'TF': {'age.to_modify': 7, 'age.to_counter': [8, 47]},
                    'FT': {'age.to_modify': 7, 'age.to_counter': [0, 6]},
                    'FF': {'age.to_modify': 7, 'age.to_counter': [0, 6]}
                }
            ),
            (
                estime2.Age(1), False, {
                'TT': {'age.to_modify': 0, 'age.to_counter': [1, 50]},
                'TF': {'age.to_modify': 0, 'age.to_counter': [1, 40]},
                'FT': {'age.to_modify': 0, 'age.to_counter': [-1, -1]},
                'FF': {'age.to_modify': 0, 'age.to_counter': [-1, -1]}
                }
            ),
            (
                estime2.Age(1), True, {
                'TT': {'age.to_modify': 1, 'age.to_counter': [2, 50]},
                'TF': {'age.to_modify': 1, 'age.to_counter': [2, 41]},
                'FT': {'age.to_modify': 1, 'age.to_counter': [0, 0]},
                'FF': {'age.to_modify': 1, 'age.to_counter': [0, 0]}
                }
            ),
            (
                estime2.Age(0), False, {
                'TT': {'age.to_modify': -1, 'age.to_counter': [0, 50]},
                'TF': {'age.to_modify': -1, 'age.to_counter': [0, 39]},
                'FT': {'age.to_modify': -1, 'age.to_counter': [0, 50]},
                'FF': {'age.to_modify': -1, 'age.to_counter': [0, 39]}
                }
            ),
            (
                estime2.Age(0), True, {
                'TT': {'age.to_modify': 0, 'age.to_counter': [1, 50]},
                'TF': {'age.to_modify': 0, 'age.to_counter': [1, 40]},
                'FT': {'age.to_modify': 0, 'age.to_counter': [1, 50]},
                'FF': {'age.to_modify': 0, 'age.to_counter': [1, 40]}
                }
            )
        ]
    )
    def test_ages_int(
        self, problematic_age, comp_in_comp_end, expecteds
    ):
        '''
        Test if the function correctly calculates modification age and
        neighbouring ages of ages depending on comp_in_comp_end, and the 
        following global options:

            + `method_use.old_neigh` == True or False
            + `method_use.age_floor` == True or False
            + `age.floor` == 50
            + `age.down_to` == 40
            + `age.max` == 99

        In case where the problematic age is either 0 or 100+, test if the
        function overrides the predefined `method_use.old_neigh` option and
        applies an appropriate approach:

            + If the age is 0, then the function behaves as if 
                `method_use.old_neigh` is True REGARDLESS of the original
                global option value;
            + If the age is 100+, then the function behaves as if
                `method_use.old_neigh` is False REGARDLESS of the original
                global option value
        '''

        keys = ['TT', 'TF', 'FT', 'FF']
        bool_selected = [False, True]
        for ii in keys:
            estime2.set_option(
                'method_use.old_neigh', bool_selected[ii[0] == 'T'],
                'method_use.age_floor', bool_selected[ii[1] == 'T']
            )
            result = estime2.poptable.calculate_ages_to_modify_and_counter(
                problematic_age, 
                comp_in_comp_end
            )
            assert expecteds[ii] == result
