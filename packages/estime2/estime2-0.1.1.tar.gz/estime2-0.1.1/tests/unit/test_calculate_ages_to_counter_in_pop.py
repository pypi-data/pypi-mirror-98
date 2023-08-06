
import estime2
import pytest



class TestCalculateAgesToCounterInPop:
    '''
    Test behaviours of `estime2.poptable.calculate_ages_to_counter_in_pop`
    function.
    '''

    @pytest.mark.parametrize(
        "to_counter_age, comp_in_comp_end, expected", 
        [
            ([50, 98], False, [51, 99]),    # problematic_age == 100+
            ([50, 99], True, [50, 99]),     #     "
            ([99, 100], False, [100, 100]), # problematic_age == 99
            ([100, 100], True, [100, 100]), # problematic_age == 99
            ([-1, 5], False, [0, 6]),       # problematic_age == 7
            ([0, 0], True, [0, 0])          # problematic_age == 1
        ]
    )
    def test_ages_for_pop(
        self, to_counter_age, comp_in_comp_end, expected
    ):
        '''
        Test if the function returns the correct minimum and maximum ages 
        to be counter-adjusted depending on the arguments: 
        `to_counter_age`, `comp_in_comp_end`.
        '''

        result = estime2.poptable.calculate_ages_to_counter_in_pop(
            to_counter_age, 
            comp_in_comp_end
        )
        assert expected == result
