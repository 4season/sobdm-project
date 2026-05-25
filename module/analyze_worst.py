import numpy as np
import pandas as pd


def analyze_worst_cases(y_test, y_pred, X_test, cycle=60, top_n=10):

    # 실제값(Actual) 시간으로 복원
    actual_angle = np.arctan2(y_test.iloc[:, 0], y_test.iloc[:, 1])
    actual_angle = np.where(actual_angle < 0, actual_angle + 2 * np.pi, actual_angle)
    actual_min = actual_angle * (cycle / (2 * np.pi))

    # 예측값(Predicted) 시간으로 복원
    pred_angle = np.arctan2(y_pred[:, 0], y_pred[:, 1])
    pred_angle = np.where(pred_angle < 0, pred_angle + 2 * np.pi, pred_angle)
    pred_min = pred_angle * (cycle / (2 * np.pi))

    # 오차 계산 (초 단위)
    diff = np.abs(actual_min - pred_min)
    diff = np.minimum(diff, cycle - diff)  # 원형 데이터의 특성 고려
    error_sec = diff * 60

    # 데이터프레임
    results = pd.DataFrame({
        'Actual(Min)': actual_min,
        'Predicted(Min)': pred_min,
        'Error(Sec)': error_sec
    }, index=y_test.index)

    # 오차가 큰 순서대로 정렬
    worst_cases = results.sort_values(by='Error(Sec)', ascending=False).head(top_n)

    # 원본 데이터(X_test)의 정보도 같이 붙여서 원인 분석하기
    # X_test가 있다면 해당 인덱스의 정보(날씨, 시간대 등)를 가져옵니다.
    if X_test is not None:
        worst_cases = worst_cases.join(X_test)

    return worst_cases
