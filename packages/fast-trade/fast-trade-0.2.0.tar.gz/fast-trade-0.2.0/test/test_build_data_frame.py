import pytest
import pandas as pd
import datetime

from fast_trade.build_data_frame import (
    detect_time_unit,
    load_basic_df_from_csv,
    apply_transformers_to_dataframe,
    apply_charting_to_df,
)


def test_detect_time_unit_s():
    mock_timestring = 1595115901734
    result = detect_time_unit(mock_timestring)

    assert result == "ms"


def test_detect_time_unit_ms():
    mock_timestring = 1595115901
    result = detect_time_unit(mock_timestring)

    assert result == "s"


def test_load_basic_df_from_csv_str_1():
    mock_ohlcv_path = "./test/ohlcv_data.csv.txt"

    result_df = load_basic_df_from_csv(mock_ohlcv_path)
    header = list(result_df.head())
    assert "close" in header
    assert "open" in header
    assert "high" in header
    assert "low" in header
    assert "volume" in header

    assert result_df.index.name == "date"


def test_load_basic_df_from_csv_list_1():
    mock_ohlcv_path = "./test/ohlcv_data.csv.txt"

    result_df = load_basic_df_from_csv(mock_ohlcv_path)

    expected_line = [0.01404, 0.01, 0.025, 0.01, 3117.0]

    assert list(result_df.iloc[1]) == expected_line


def test_load_basic_df_from_csv_str_error_1():
    mock_ohlcv_path = "./test/SomeFakeNews.csv.txt"

    with pytest.raises(Exception, match=r"File not found:*"):
        load_basic_df_from_csv(mock_ohlcv_path)


def test_apply_transformers_to_dataframe_1_ind():
    mock_df = pd.read_csv("./test/ohlcv_data.csv.txt")
    mock_transformers = [
        {"transformer": "sma", "name": "example_transformer_name", "args": [3]}
    ]

    result_df = apply_transformers_to_dataframe(mock_df, mock_transformers)

    header = list(result_df.head())

    assert "example_transformer_name" in header
    assert "FAKE_transformer_name" not in header


def test_apply_transformers_to_dataframe_no_args():
    mock_df = pd.read_csv("./test/ohlcv_data.csv.txt")
    mock_transformers = [{"transformer": "rsi", "name": "rsi", "args": []}]

    result_df = apply_transformers_to_dataframe(mock_df, mock_transformers)

    assert "rsi" in list(result_df.columns)


def test_apply_charting_to_df_1():
    mock_df = pd.read_csv("./test/ohlcv_data.csv.txt", index_col="date")
    # mock_df.set_index(["date"], inplace=True)
    mock_df.index = pd.to_datetime(mock_df.index, unit="s")
    mock_chart_period = "2Min"
    mock_start_time = "2018-04-17"
    mock_stop_time = ""

    result_df = apply_charting_to_df(
        mock_df, mock_chart_period, mock_start_time, mock_stop_time
    )

    assert (result_df.iloc[2].name - result_df.iloc[1].name).total_seconds() == 120
    assert (result_df.iloc[4].name - result_df.iloc[1].name).total_seconds() == 360


def test_apply_charting_to_df_2():
    mock_df = pd.read_csv("./test/ohlcv_data.csv.txt")
    mock_df.set_index(["date"], inplace=True)
    mock_df.index = pd.to_datetime(mock_df.index, unit="s")
    mock_chart_period = "1Min"
    mock_start_time = "2018-04-17 04:00:00"
    mock_stop_time = "2018-04-17 04:10:00"

    past_stop_time = datetime.datetime.strptime(
        "2018-04-17 04:11:00", "%Y-%m-%d %H:%M:%S"
    )
    result_df = apply_charting_to_df(
        mock_df, mock_chart_period, mock_start_time, mock_stop_time
    )

    assert result_df.iloc[-1].name < past_stop_time


def test_apply_charting_to_df_3():
    mock_df = pd.read_csv("./test/ohlcv_data.csv.txt")
    mock_df.set_index(["date"], inplace=True)
    mock_df.index = pd.to_datetime(mock_df.index, unit="s")
    mock_chart_period = "1Min"
    mock_start_time = ""
    mock_stop_time = "2018-04-17 04:10:00"

    past_stop_time = "2018-04-17 04:11:00"

    result_df = apply_charting_to_df(
        mock_df, mock_chart_period, mock_start_time, mock_stop_time
    )

    past_stop_time = datetime.datetime.strptime(
        "2018-04-17 04:11:00", "%Y-%m-%d %H:%M:%S"
    )
    result_df = apply_charting_to_df(
        mock_df, mock_chart_period, mock_start_time, mock_stop_time
    )

    assert result_df.index[0] < past_stop_time
