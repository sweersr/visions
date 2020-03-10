from visions.core.model import VisionsBaseType, VisionsTypeset
from visions.core.implementations.types import visions_generic
from visions.core.model.relations import IdentityRelation
import pandas.api.types as pdt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class visions_statistical_set(VisionsTypeset):
    """Typeset that exclusively supports time related types

    Includes support for the following types:

    - visions_binary
    - visions_nominal
    - visions_ordinal
    - visions_interval
    - visions_ratio

    """

    def __init__(self):
        types = {
            visions_binary,
            visions_nominal,
            visions_ordinal,
            visions_interval,
            visions_ratio,
        }
        super().__init__(types)


class visions_binary(VisionsBaseType):

    @classmethod
    def get_relations(cls):
        return [IdentityRelation(visions_binary, visions_nominal)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_bool_dtype(series)


class visions_nominal(VisionsBaseType):

    @classmethod
    def get_relations(cls):
        return [IdentityRelation(visions_nominal, visions_generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return (pdt.is_categorical_dtype(series) and not series.cat.ordered) or pdt.is_bool_dtype(series)


class visions_ordinal(VisionsBaseType):

    @classmethod
    def get_relations(cls):
        return [IdentityRelation(visions_ordinal, visions_generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_categorical_dtype(series) and series.cat.ordered


class visions_interval(VisionsBaseType):
    """
    Aliases
    """
    @classmethod
    def get_relations(cls):
        return [IdentityRelation(visions_interval, visions_generic)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return pdt.is_numeric_dtype(series) and not pdt.is_bool_dtype(series)


class visions_ratio(VisionsBaseType):

    @classmethod
    def get_relations(cls):
        return [IdentityRelation(visions_ratio, visions_interval)]

    @classmethod
    def contains_op(cls, series: pd.Series) -> bool:
        return False


# TODO: make test cases
series_interval1 = pd.Series([2.4, 5.6, 3.5, 2.5, 4], name='interval 1')
series_interval3 = pd.Series([2, 5, 3, 2, 4, np.nan], dtype="Int64", name='interval 1')
series_interval2 = pd.Series([1, 5, 7, 9, 11], name='interval 2')
series_ratio1 = pd.Series([2.4, 5.6, 3.5, 2.5, 4], name='ratio 1')
series_ratio2 = pd.Series([2.3, 4, 2.3, 6.3, 7.8], name='ratio 2')
series_binary = pd.Series([True, True, False, True, False], dtype=bool, name='binary')
series_nominal1 = pd.Series(['kaas', 'yoghurt', 'kaas', 'melk', 'melk'], dtype='category', name='nominal 1')
series_nominal2 = pd.Series([1, 2, 3, 3, 1], dtype='category', name='nominal 2')
series_ordinal1 = pd.Series(pd.Categorical([1, 2, 3, 3, 1], categories=[1, 2, 3], ordered=True), name='ordinal 1')
series_ordinal2 = pd.Series(pd.Categorical([2, 2, 2, 3, 4], categories=[1, 2, 3, 4], ordered=True),
                            name='ordinal 2')
series_datetime = pd.to_datetime(
    pd.Series(['3/11/2000', '5/12/2008', '12/2/1993', '2/12/1993', '2/4/1923'], name='datetime'))
series_time_delta = pd.Series(
    [pd.Timedelta('1 days 00:03:43'), pd.Timedelta('5 days 12:33:57'), pd.Timedelta('0 days 01:25:07'),
     pd.Timedelta('-2 days 13:46:56'), pd.Timedelta('1 days 23:49:25')], name='time_delta')
# TODO: period dtype
# TODO: nullable integer
# TODO: interval dtype


if __name__ == "__main__":
    x = visions_statistical_set()
    x.plot_graph()
    plt.show()


    def check_all(series):
        print(series.name + ':')
        for i in [visions_nominal, visions_binary, visions_ordinal, visions_interval, visions_ratio]:
            print(str(i)+':', series in i)
        print('\n')

    for i in [series_interval1, series_interval2, series_ratio1, series_ratio2, series_binary, series_nominal1, series_nominal2, series_ordinal1, series_ordinal2, series_datetime, series_time_delta]:
        check_all(i)

