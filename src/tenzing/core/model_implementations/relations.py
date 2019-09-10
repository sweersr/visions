from pathlib import Path
from urllib.parse import urlparse

from tenzing.core.model_implementations.types.tenzing_bool import tenzing_bool
from tenzing.core.model_implementations.types.tenzing_float import tenzing_float
from tenzing.core.model_implementations.types.tenzing_geometry import tenzing_geometry
from tenzing.core.model_implementations.types.tenzing_object import tenzing_object
from tenzing.core.model_implementations.types.tenzing_path import tenzing_path
from tenzing.core.model_implementations.types.tenzing_string import tenzing_string
from tenzing.core.model_implementations.types.tenzing_integer import tenzing_integer
from tenzing.core.model_implementations.types.tenzing_timestamp import tenzing_timestamp
from tenzing.core.model_implementations.types.tenzing_url import tenzing_url
from tenzing.core.models import model_relation
from tenzing.utils import test_utils
import logging
import pandas as pd


def register_integer_relations():
    relations = [
        model_relation(tenzing_integer, tenzing_float,
                       test_utils.coercion_equality_test(lambda s: s.astype(int))),
        model_relation(tenzing_integer, tenzing_string,
                       test_utils.coercion_test(lambda s: s.astype(int))),
    ]
    for relation in relations:
        tenzing_integer.register_relation(relation)


def register_float_relations():
    def test_string_is_float(series):
        coerced_series = test_utils.option_coercion_evaluator(tenzing_float.cast)(series)
        if coerced_series is None:
            return False
        else:
            return True
    relations = [
        model_relation(tenzing_float, tenzing_string, test_string_is_float),
    ]
    for relation in relations:
        tenzing_float.register_relation(relation)


def register_string_relations():
    relations = [
        model_relation(tenzing_string, tenzing_object),
    ]
    for relation in relations:
        tenzing_string.register_relation(relation)


def register_url_relations():
    relations = [
        model_relation(tenzing_url, tenzing_string,
                       test_utils.coercion_test(lambda s: all(k in ['netloc', 'scheme'] for k in urlparse(s)._asdict())))
    ]
    for relation in relations:
        tenzing_url.register_relation(relation)


def register_path_relations():
    relations = [
        model_relation(tenzing_path, tenzing_string,
                       test_utils.coercion_test(lambda s: Path(s)))
    ]
    for relation in relations:
        tenzing_path.register_relation(relation)


def register_timestamp_relations():
    relations = [
        model_relation(tenzing_timestamp, tenzing_string,
                       test_utils.coercion_test(lambda s: pd.to_datetime(s))),
        model_relation(tenzing_timestamp, tenzing_object)
    ]
    for relation in relations:
        tenzing_timestamp.register_relation(relation)


def register_geometry_relations():
    def string_is_geometry(series):
        """
            Shapely logs failures at a silly severity, just trying to suppress it's output on failures.
        """
        from shapely import wkt
        logging.disable()
        try:
            result = all(wkt.loads(value) for value in series)
        except Exception:
            result = False
        finally:
            logging.disable(logging.NOTSET)

        return result

    relations = [
        model_relation(tenzing_geometry, tenzing_string, string_is_geometry),
        model_relation(tenzing_geometry, tenzing_object, transformer=lambda series: series)
    ]
    for relation in relations:
        tenzing_geometry.register_relation(relation)


class string_bool_relation:
    # TODO: extend with Y/N
    _boolean_maps = {'true': True,
                     'false': False}

    # _boolean_maps = {'y': True,
    #                  'n': False}
    # _boolean_maps = {'yes': True,
    #                  'no': False}

    # TODO: ensure that series.str.lower() has no side effects
    def string_is_bool(self, series):
        return series.apply(type).eq(str).all() and series.str.lower().isin(self._boolean_maps.keys()).all()

    def map_string_to_bool(self, series):
        return series.str.lower().map(self._boolean_maps)


def register_bool_relations():
    sb_relation = string_bool_relation()
    relations = [
        model_relation(tenzing_bool, tenzing_string,
                       sb_relation.string_is_bool, sb_relation.map_string_to_bool)
    ]
    for relation in relations:
        tenzing_bool.register_relation(relation)


register_integer_relations()
register_float_relations()
register_string_relations()
register_timestamp_relations()
register_bool_relations()
register_geometry_relations()
register_url_relations()
register_path_relations()