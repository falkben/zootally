import pandas as pd
from django_mock_queries.query import MockModel, MockSet, MockField
from django.utils import timezone
import pytest
import datetime

from zoo_checks.helpers import qs_to_df, clean_df


class MockFieldIsRelation(MockField):
    def __init__(self, *args, **kwargs):
        self.is_relation = kwargs.pop("is_relation", False)
        super().__init__(*args, **kwargs)


def test_qs_to_df():
    # animal count
    test_data = {
        "id": 1637,
        "datecounted": datetime.datetime(2019, 9, 26, 13, 49, 28, 281415),
        "user_id": 4,
        "enclosure_id": 12,
        "condition": "SE",
        "animal_id": 29,
        "dateonlycounted": datetime.date(2019, 9, 26),
    }
    test_df = pd.DataFrame([test_data])
    qs = MockSet(MockModel(test_data))
    df = qs_to_df(qs, [MockFieldIsRelation(k) for k in list(test_data.keys())])
    assert pd.DataFrame.equals(df, test_df)

    # group count
    test_data = {
        "id": 6,
        "datecounted": datetime.datetime(2019, 9, 27, 3, 59, 59),
        "user_id": 1,
        "enclosure_id": 5,
        "count_male": 0,
        "count_female": 0,
        "count_unknown": 25,
        "group_id": 1,
        "dateonlycounted": datetime.date(2019, 9, 26),
    }
    test_df = pd.DataFrame([test_data])
    qs = MockSet(MockModel(test_data))
    df = qs_to_df(qs, [MockFieldIsRelation(k) for k in list(test_data.keys())])
    assert pd.DataFrame.equals(df, test_df)

    # species count
    test_data = {
        "id": 25,
        "datecounted": datetime.datetime(2019, 9, 27, 16, 10, 24, 504457),
        "user_id": 1,
        "enclosure_id": 5,
        "count": 3,
        "species_id": 10,
        "dateonlycounted": datetime.date(2019, 9, 27),
    }
    test_df = pd.DataFrame([test_data])
    qs = MockSet(MockModel(test_data))
    df = qs_to_df(qs, [MockFieldIsRelation(k) for k in list(test_data.keys())])
    assert pd.DataFrame.equals(df, test_df)


def test_clean_df():
    timestamp = timezone.localtime()
    test_data = [
        {
            "id": 1637,
            "datecounted": timestamp,
            "user__username": 4,
            "enclosure__name": "encl_test_name",
            "condition": "SE",
            "dateonlycounted": timestamp.date(),
        }
    ]
    test_df = pd.DataFrame(test_data)
    df_clean = clean_df(test_df)

    assert df_clean.loc[0]["date_counted"] == timestamp.replace(tzinfo=None).date()
    assert df_clean.loc[0]["time_counted"] == timestamp.replace(
        tzinfo=None
    ).time().strftime("%H:%M:%S")
