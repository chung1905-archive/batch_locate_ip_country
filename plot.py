import pandas as pd
import matplotlib.pyplot as plt

from typing import Dict


def show(data: Dict[str, int]):
    df = pd.DataFrame.from_dict(data, orient='index', columns=["Hackers"])
    df = df.sort_values("Hackers", ascending=False)
    print(df)

    others_df: pd.DataFrame = df.query("`Hackers` < 10")
    others_sum: pd.Series = others_df.sum()
    df2 = pd.DataFrame.from_dict({'Others': others_sum}, orient='index', columns=["Hackers"])
    df = pd.concat([df, df2])

    drop_dict: dict = others_df.to_dict(orient='index')
    drop_list: list = list(drop_dict.keys())

    df = df.drop(axis='row', index=drop_list)
    df.plot(kind="bar")
    plt.show()
