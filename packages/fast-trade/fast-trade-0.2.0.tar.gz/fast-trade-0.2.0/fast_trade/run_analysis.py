import pandas as pd
from datetime import timedelta


def analyze_df(df: pd.DataFrame, backtest: dict):
    """Analyzes the dataframe and runs sort of a market simulation, entering and exiting positions

    Parameters
    ----------
        df, dataframe from process_dataframe after the actions have been added
        backtest: dict, contains instructions on when to enter/exit trades

    Returns
    -------
        df, returns a dataframe with the new rows processed
    """
    in_trade = False
    last_base = float(backtest["base_balance"])
    comission = float(backtest["comission"])
    last_aux = 0.0
    new_total_value = last_base

    aux_list = []
    base_list = []
    total_value_list = []
    in_trade_list = []
    fee_list = []

    for row in df.itertuples():
        close = row.close
        curr_action = row.action
        fee = 0

        if curr_action in ["e", "ae"] and not in_trade:
            # this means we should enter the trade
            last_aux = convert_base_to_aux(last_base, close)
            fee = calculate_fee(last_aux, comission)

            last_aux = last_aux - fee
            new_total_value = convert_aux_to_base(last_aux, close)

            # should be extremely close to 0
            last_base = round(last_base - new_total_value, 8)
            in_trade = True
            fee = convert_aux_to_base(fee, close)

        if curr_action in ["x", "ax", "tsl"] and in_trade:
            # this means we should EXIT the trade
            last_base = convert_aux_to_base(last_aux, close)
            fee = calculate_fee(last_base, comission)
            last_base = last_base - fee
            last_aux = convert_base_to_aux(last_base, close)

            new_total_value = last_base

            in_trade = False

        aux_list.append(last_aux)
        base_list.append(last_base)
        total_value_list.append(new_total_value)
        in_trade_list.append(in_trade)
        fee_list.append(fee)

    if backtest.get("exit_on_end") and in_trade:
        last_base = convert_aux_to_base(last_aux, close)
        last_aux = convert_base_to_aux(last_base, close)
        new_date = df.index[-1] + timedelta(minutes=1)

        df = df.append(pd.DataFrame(index=[new_date]))

        aux_list.append(last_aux)
        base_list.append(last_base)
        total_value_list.append(new_total_value)
        in_trade_list.append(in_trade)
        fee_list.append(False)

    df["aux"] = aux_list
    df["base"] = base_list
    df["total_value"] = total_value_list
    df["in_trade"] = in_trade_list
    df["fee"] = fee_list

    return df


def convert_base_to_aux(last_base: float, close: float):
    """converts the base coin to the aux coin
    Parameters
    ----------
        last_base, the last amount maintained by the backtest
        close, the closing price of the coin

    Returns
    -------
        float, amount of the last base divided by the closing price
    """
    if last_base:
        return round(last_base / close, 8)
    return 0.0


def convert_aux_to_base(last_aux: float, close: float):
    """converts the aux coin to the base coin
    Parameters
    ----------
        last_base, the last amount maintained by the backtest
        close, the closing price of the coin
    Returns
    -------
        float, amount of the last aux divided by the closing price
    """
    if last_aux:
        return round(last_aux * close, 8)
    return 0.0


def calculate_fee(price: float, comission: float):
    """calculates the trading fees from the exchange
    Parameters
    ----------
        price, amount of the coin after the transaction
        comission, percentage of the transaction
    """
    if comission:
        return round((price / 100) * comission, 8)

    return 0.0
