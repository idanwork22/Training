"""
    This python file will be for all the
    needed indicators
"""


def SMA(*args):
    """
    function to calculate SMA
    This is a dynamic function
    the first args variable is the DataFrame
    and all the rest are the number of the moving avg
    """

    df = args[0].copy()
    for i in range(1, len(args)):
        print(args[i])
        df["SMA(" + str(args[i]) + ")"] = df["Close"].rolling(int(args[i])).mean()

    df.dropna(inplace=True)
    return df
