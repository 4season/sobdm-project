import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

pd.set_option('display.max_columns', None)
bus_df = pd.read_csv('./data/bus/processed_bus_data.csv')
road_df = pd.read_csv('./data/road/processed_road_data.csv')
weather_df = pd.read_csv('./data/weather/processed_weather_data.csv')

# 문자열을 날짜(datetime) 형식으로 변환하기
bus_df['arrivalDate'] = pd.to_datetime(bus_df['arrivalDate'])
weather_df['date_weather'] = pd.to_datetime(weather_df['date_weather'])
road_df['date_time'] = pd.to_datetime(road_df['date_time'])

# 날짜 기준으로 정렬하기 (merge_asof 필수 조건)
bus_df = bus_df.sort_values('arrivalDate')
weather_df = weather_df.sort_values('date_weather')

# 날씨 데이터와 결합
merge_weather_df = pd.merge_asof(
    bus_df,
    weather_df,
    left_on='arrivalDate',
    right_on='date_weather',
    direction='backward'
)

# 결합 데이터 10분으로 반올림
merge_weather_df['rounded_time'] = merge_weather_df['arrivalDate'].dt.round('10min')

# 도로 교통량 데이터와 결합
final_df = pd.merge(
    merge_weather_df,
    road_df,
    left_on=['rounded_time', 'road_id'],
    right_on=['date_time', 'id'],
    how='left'
)

# 결측치 처리 (예시: 앞의 값으로 채우기)
final_df = final_df.ffill().bfill()

# 시간 데이터 주기적 변환 (Time -> Sin/Cos)
final_df['hour_sin'] = np.sin(2 * np.pi * final_df['hour'] / 24)
final_df['hour_cos'] = np.cos(2 * np.pi * final_df['hour'] / 24)
final_df['minute_sin'] = np.sin(2 * np.pi * final_df['minute'] / 60)
final_df['minute_cos'] = np.cos(2 * np.pi * final_df['minute'] / 60)
final_df['day_sin'] = np.sin(2 * np.pi * final_df['day_of_week'] / 7)
final_df['day_cos'] = np.cos(2 * np.pi * final_df['day_of_week'] / 7)

# 도착 시간 변환
final_df['arrivalMinute'] = final_df['arrivalDate'].dt.minute
final_df['arrival_min_sin'] = np.sin(2 * np.pi * final_df['arrivalMinute'] / 60)
final_df['arrival_min_cos'] = np.cos(2 * np.pi * final_df['arrivalMinute'] / 60)

# 도로 주기 지정
final_df['station_sin'] = np.sin(2 * np.pi * final_df['station'] / 21)
final_df['station_cos'] = np.cos(2 * np.pi * final_df['station'] / 21)
final_df['road_sin'] = np.sin(2 * np.pi * final_df['road_id'] / 6)
final_df['road_cos'] = np.cos(2 * np.pi * final_df['road_id'] / 6)

scale_features = [
    'len', 'maxSpeed', 'speed', 'ttime',
    'traffic', 'temp', 'rain', 'humidity'
]

no_scale_features = [
    'day_sin', 'day_cos', 'hour_sin', 'hour_cos',
    'minute_sin', 'minute_cos', 'is_weekend', 'is_commute',
    'bus_line', 'road_sin', 'road_cos', 'station_sin', 'station_cos',
    'arrival_min_sin', 'arrival_min_cos'
]

scaler = MinMaxScaler()
df_scaled_part = pd.DataFrame(
    scaler.fit_transform(final_df[scale_features]),
    columns=scale_features
)
df_no_scaled_part = final_df[no_scale_features].reset_index(drop=True)
X = pd.concat([df_scaled_part, df_no_scaled_part], axis=1)

desired_order = [
    # [1] 시간 관련 (순환 데이터)
    'day_sin', 'day_cos', 'hour_sin', 'hour_cos', 'minute_sin', 'minute_cos', 'arrival_min_sin', 'arrival_min_cos',
    # [2] 상황 여부 (0 또는 1)
    'is_weekend', 'is_commute',
    # [3] 도로 및 교통 정보 (순환 데이터 또는 스케일링 된 것)
    'road_sin', 'road_cos', 'station_sin', 'station_cos', 'bus_line', 'len', 'maxSpeed', 'speed', 'traffic',
    # [4] 날씨 정보 (스케일링 된 것)
    'temp', 'rain', 'humidity'
]
X = X[desired_order]

print("🎉 학습 준비 완료! 데이터 형태:", X.shape)
#print(X.head(20))
X.to_pickle('./data/processed/processed_data.pkl')
X.to_csv('./data/processed/processed_data.csv', index=False)
print("💾 데이터 저장 완료!")