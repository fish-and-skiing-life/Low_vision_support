import numpy as np


def calc_exponential_moving_average(x):
    """指数移動平均を計算する

    Parameters
    ----------
    x : numpy.array
        時系列データ

    Returns
    -------
    float
        指数移動平均
    """
    alpha = 2 / (len(x) + 1)
    return alpha * np.sum([signal * (1.0 - alpha) ** i for i, signal in enumerate(x[::-1])])


def calc_moving_average_convergence_divergence(x, recent_span=7):
    """移動平均収束拡散法を計算する

    Parameters
    ----------
    x : numpy.array
        時系列データ
    recent_span : int, default 7
        直近 recent_span 点までを短期トレンドとする

    Returns
    -------
    float
        移動平均収束拡散法
    """
    return calc_exponential_moving_average(x[-recent_span:]) - calc_exponential_moving_average(x)


def calc_trend_score(x, recent_span=7):
    """GoogleTrendスコアから修正トレンドスコアを計算する．
    スコア計算には移動平均収束拡散法(MACD)を利用．
    MACDの値が負になる場合はスコアは0とする．
    スコアの値域は [0, 1]

    Parameters
    ----------
    x : list[float]
        GoogleTrendScoreの系列データ
    recent_span : int, default 7
        直近 recent_span 点までを短期トレンドとする
    
    Returns
    -------
    float
        修正トレンドスコア
    """
    macd_score = calc_moving_average_convergence_divergence(x, recent_span)
    
    if macd_score < 0:
        return 0.0
    
    return macd_score / 100
