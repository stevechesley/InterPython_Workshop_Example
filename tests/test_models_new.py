"""Tests for statistics functions within the Model layer."""

import pandas as pd
import pandas.testing as pdt
import pytest

def test_calc_stat():
    # Test it...

    from lcanalyzer.models import calc_stats
    test_cols = list("abc")
    test_dict = {}
    test_dict["df0"] = pd.DataFrame(
        data=[[8, 8, 0], 
            [0, 1, 1], 
            [2, 3, 1], 
            [7, 9, 7]], columns=test_cols
    )
    test_dict["df1"] = pd.DataFrame(
        data=[[3, 8, 2], 
            [3, 8, 0], 
            [3, 9, 8], 
            [8, 2, 5]], columns=test_cols
    )
    test_dict["df2"] = pd.DataFrame(
        data=[[8, 4, 3], 
            [7, 6, 3], 
            [4, 2, 9], 
            [6, 4, 0]], columns=test_cols
    )
    test_output = pd.DataFrame(
        data=[[9,9,6],[5.25,6.75,4.],[1,2,2]],
        columns=['df0','df1','df2'],
        index=['max','mean','min']
    )
    
#   assert calc_stats(test_dict, test_dict.keys(), 'b') == test_output
    pdt.assert_frame_equal(calc_stats(test_dict, test_dict.keys(), 'b'),
       test_output,
       check_exact=False,
       atol=0.01)


# Parametrization for normalize_lc function testing with ValueError
@pytest.mark.parametrize(
    "test_input_df, test_input_colname, expected, expected_raises",
    [
        (pd.DataFrame(data=[[8, 9, 1], 
                            [1, 4, 1], 
                            [1, 2, 4], 
                            [1, 4, 1]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[1,0.285,0,0.285]),
        None),
        (pd.DataFrame(data=[[1, 1, 1], 
                            [1, 1, 1], 
                            [1, 1, 1], 
                            [1, 1, 1]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[0.,0.,0.,0.]),
        None),
        (pd.DataFrame(data=[[0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[0.,0.,0.,0.]),
        None),
        (pd.DataFrame(data=[[8, 9, 1], 
                            [1, -99.9, 1], 
                            [1, 2, 4], 
                            [1, 4, 1]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[1,0.285,0,0.285]),
        ValueError),
    ])
def test_normalize_lc(test_input_df, test_input_colname, expected,expected_raises):
    """Test how normalize_lc function works for arrays of positive integers."""
    from lcanalyzer.models import normalize_lc
    import pandas.testing as pdt
    if expected_raises is not None:
        with pytest.raises(expected_raises):
            pdt.assert_series_equal(
                normalize_lc(test_input_df,test_input_colname),
                expected,
                check_exact=False,
                atol=0.01,
                check_names=False
            )
    else:
        pdt.assert_series_equal(
            normalize_lc(test_input_df,test_input_colname),
            expected,
            check_exact=False,
            atol=0.01,
            check_names=False
        )
