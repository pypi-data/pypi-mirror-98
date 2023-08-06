

def up_trend_ma(df):
    """ 如果ma线持续上升，给50分
    """
    if df is None or df.empty or len(df) < 60:
        return 0

    days = [1, 5, 10, 20, 60, 120]

    ma_list = []
    for x in days:
        if len(df) < x:
            break 
        ma_list.append(df[-x:]['close'].mean())

    # strong_up = df[-5:]['close'].mean() > df[-10:]['close'].mean() > df[-22:]['close'].mean(
    # ) > df[-50:]['close'].mean() > df[-60:]['close'].mean() > df[-120:]['close'].mean()

    for a, b in zip(ma_list[1:], ma_list[:-1]):
        if a > b:
            break 
    else:
        return 50
    return 0