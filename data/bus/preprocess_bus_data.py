import pandas as pd
import module.road_dataframe as rd

pd.set_option('display.max_columns', None)

# 데이터 로드 및 병합
df0 = pd.read_csv('./data/bus/bus_arrivals_1101-1114.csv')
df1 = pd.read_csv('./data/bus/bus_arrivals_1115-1130.csv')
concat_df = pd.concat([df0, df1])

# 로드 데이터 매핑 준비
mapping_df = pd.DataFrame(rd.road_mapping_data)
mapping_df = mapping_df.drop(columns=['ROAD_NAME', 'CROSS_ROAD'])

# 날짜 결측치 처리
concat_df['arrivalDate'] = pd.to_datetime(concat_df['arrivalDate'])
# 원본 데이터 컬럼명 오타(depatureDate) 반영 확인
concat_df['depatureDate'] = pd.to_datetime(concat_df['depatureDate'])
concat_df['arrivalDate'] = concat_df['arrivalDate'].fillna(concat_df['depatureDate'])

# 정타(departureDate) 컬럼 처리
if 'departureDate' in concat_df.columns:
     concat_df['departureDate'] = pd.to_datetime(concat_df['departureDate'])
     concat_df['arrivalDate'] = concat_df['arrivalDate'].fillna(concat_df['departureDate'])

# 불필요 컬럼 삭제
columns_to_drop = ['searchDate', 'queriedStationId', 'depatureDate', 'departureDate', 'routeId']
columns_to_drop = [col for col in columns_to_drop if col in concat_df.columns]
concat_df = concat_df.drop(columns=columns_to_drop)

# 파생 변수 생성 (요일, 출퇴근 등)
concat_df['hour'] = concat_df['arrivalDate'].dt.hour
concat_df['minute'] = concat_df['arrivalDate'].dt.minute
concat_df['day_of_week'] = concat_df['arrivalDate'].dt.dayofweek
concat_df['is_weekend'] = (concat_df['day_of_week'] >= 5).astype(int)
is_weekday = (concat_df['is_weekend'] == 0)
is_morning_rush = (concat_df['hour'] >= 6) & (concat_df['hour'] <= 9)
is_evening_rush = (concat_df['hour'] >= 17) & (concat_df['hour'] <= 20)
concat_df['is_commute'] = (is_weekday & is_morning_rush).astype(int) | (is_weekday & is_evening_rush).astype(int)

# 정렬 및 중복 제거
concat_df = concat_df.sort_values(by=['vehId', 'arrivalDate'], ascending=True)
concat_df = concat_df.drop_duplicates(subset=['vehId', 'stationId','arrivalDate'], keep='first')
concat_df['vehicle'] = concat_df['vehId'].astype('category').cat.codes

# Merge 수행
merge_df = pd.merge(concat_df, mapping_df, left_on=['stationId'], right_on=['STATION_ID'], how='left')

# 단일 필터링 로직 적용
merge_df = merge_df.sort_values(by=['vehId', 'arrivalDate', 'STATION_NUM'])

merge_df['next_station'] = merge_df.groupby('vehId')['STATION_NUM'].shift(-1)
merge_df['prev_station'] = merge_df.groupby('vehId')['STATION_NUM'].shift(1)

# 1. 1번 정류장이 원래 있었는지 확인
print("1번 정류장 개수:", len(merge_df[merge_df['STATION_NUM'] == 1]))

# 2. 1번 정류장 바로 뒤에 무엇이 있었길래 지워졌는지 확인 (샘플 10개)
check_logic = merge_df[merge_df['STATION_NUM'] == 1][['STATION_NUM', 'next_station']].head(10)
check_logic2 = merge_df[merge_df['STATION_NUM'] == 1][['STATION_NUM', 'prev_station']].head(10)

print("\n[1번 정류장과 그 다음 정류장 확인]")
print(check_logic)
print("\n[1번 정류장과 그 이전 정류장 확인]")
print(check_logic2)

# 필터링 조건 설정
mask_fake_21 = (merge_df['STATION_NUM'] == 21) & (merge_df['next_station'] == 2) & (merge_df['prev_station'] == 1)
mask_fake_1 = (merge_df['STATION_NUM'] == 1) & ~(merge_df['next_station'] == 2)

# 필터링 적용
clean_df = merge_df[~mask_fake_21& ~mask_fake_1].copy()

# Trip ID 생성
df = clean_df
df['station'] = df['STATION_NUM']
df['prev_station'] = df.groupby('vehicle')['station'].shift(1)
is_start_of_trip = (df['station'] == 1) | \
                   ((df['station'] < 5) & (df['prev_station'] > 15))
df['trip_id'] = is_start_of_trip.astype(int).groupby(df['vehicle']).cumsum()

# 마무리 정리
clean_df = df.drop(columns=['prev_station', 'next_station', 'prev_station'])
clean_df = clean_df.sort_values(by=['vehicle', 'arrivalDate'])
clean_df = clean_df.reset_index(drop=True)

clean_df = clean_df.rename(columns={'ROAD_ID': 'road_id', 'LINE': 'bus_line'})
desired = ['arrivalDate', 'day_of_week', 'is_weekend', 'is_commute', 'hour', 'minute', 'trip_id', 'vehicle', 'station', 'road_id', 'bus_line']
clean_df = clean_df[desired]

# 결과 출력
print(clean_df.head(50))
clean_df.to_csv('./data/bus/processed_bus_data.csv', index=False)
print("💾 데이터 저장 완료!")