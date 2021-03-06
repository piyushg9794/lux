#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pandas as pd
import lux
import pytest


def test_case1():
    ldf = pd.read_csv("lux/data/car.csv")
    ldf.set_intent(["Horsepower"])
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == "Horsepower"


def test_case2():
    ldf = pd.read_csv("lux/data/car.csv")
    ldf.set_intent(["Horsepower", lux.Clause("MilesPerGal", channel="x")])
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == "Horsepower"
    assert type(ldf._intent[1]) is lux.Clause
    assert ldf._intent[1].attribute == "MilesPerGal"


def test_case3():
    ldf = pd.read_csv("lux/data/car.csv")
    ldf.set_intent(["Horsepower", "Origin=USA"])
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == "Horsepower"
    assert type(ldf._intent[1]) is lux.Clause
    assert ldf._intent[1].attribute == "Origin"
    assert ldf._intent[1].value == "USA"


def test_case4():
    ldf = pd.read_csv("lux/data/car.csv")
    ldf.set_intent(["Horsepower", "Origin=USA|Japan"])
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == "Horsepower"
    assert type(ldf._intent[1]) is lux.Clause
    assert ldf._intent[1].attribute == "Origin"
    assert ldf._intent[1].value == ["USA", "Japan"]


def test_case5():
    ldf = pd.read_csv("lux/data/car.csv")
    ldf.set_intent([["Horsepower", "MilesPerGal", "Weight"], "Origin=USA"])
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == ["Horsepower", "MilesPerGal", "Weight"]
    assert type(ldf._intent[1]) is lux.Clause
    assert ldf._intent[1].attribute == "Origin"
    assert ldf._intent[1].value == "USA"

    ldf.set_intent(["Horsepower|MilesPerGal|Weight", "Origin=USA"])
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == ["Horsepower", "MilesPerGal", "Weight"]
    assert type(ldf._intent[1]) is lux.Clause
    assert ldf._intent[1].attribute == "Origin"
    assert ldf._intent[1].value == "USA"


def test_case6():
    ldf = pd.read_csv("lux/data/car.csv")
    ldf.set_intent(["Horsepower", "Origin=?"])
    ldf._repr_html_()
    assert type(ldf._intent[0]) is lux.Clause
    assert ldf._intent[0].attribute == "Horsepower"
    assert type(ldf._intent[1]) is lux.Clause
    assert ldf._intent[1].attribute == "Origin"
    assert ldf._intent[1].value == ["USA", "Japan", "Europe"]


def test_case7():
    df = pd.read_csv("lux/data/car.csv")
    df.intent = [["Horsepower", "MilesPerGal", "Acceleration"], "Origin"]
    df._repr_html_()
    assert len(df.current_vis) == 3


def test_validator_invalid_value():
    df = pd.read_csv("lux/data/college.csv")
    with pytest.warns(
        UserWarning,
        match="The input value 'bob' does not exist for the attribute 'Region' for the DataFrame.",
    ):
        df.intent = ["Region=bob"]


def test_validator_invalid_filter():
    df = pd.read_csv("lux/data/college.csv")

    with pytest.raises(KeyError, match="'New England'"):
        with pytest.warns(
            UserWarning,
            match="The input 'New England' looks like a value that belongs to the 'Region' attribute.",
        ):
            df.intent = ["New England", "Southeast", "Far West"]


def test_validator_invalid_attribute():
    df = pd.read_csv("lux/data/college.csv")
    with pytest.raises(KeyError, match="'blah'"):
        with pytest.warns(
            UserWarning, match="The input attribute 'blah' does not exist in the DataFrame."
        ):
            df.intent = ["blah"]
