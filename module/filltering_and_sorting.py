import pandas as pd

def reconstruct_independent_of_trip_id(df):
    # 정렬: 차량별로, 시간 순서대로 정렬
    sorted_df = df.sort_values(by=['vehicle', 'arrivalDate'])

    cleaned_rows = []
    new_trip_counter = 0

    # 차량별로 반복
    for vehicle_id, group in sorted_df.groupby('vehicle'):
        current_buffer = []
        next_expected_station = 1

        for _, row in group.iterrows():
            current_station = row['station']

            if current_station == next_expected_station:
                current_buffer.append(row)
                next_expected_station += 1

                if next_expected_station > 21:
                    generated_id = f"gen_{vehicle_id}_{new_trip_counter}"

                    for buffer_row in current_buffer:
                        row_dict = buffer_row.to_dict()
                        row_dict['generated_trip_id'] = generated_id
                        cleaned_rows.append(row_dict)

                    new_trip_counter += 1
                    current_buffer = []
                    next_expected_station = 1

            elif current_station == 1:
                current_buffer = [row]
                next_expected_station = 2

    return pd.DataFrame(cleaned_rows)

# 시간 차이 계산
# if not cleaned_df.empty:
#    cleaned_df['arrivalDate'] = pd.to_datetime(cleaned_df['arrivalDate'])
#    cleaned_df['next_arrival_time'] = cleaned_df.groupby('generated_trip_id')['arrivalDate'].shift(-1)
#    cleaned_df['travel_time_sec'] = (cleaned_df['next_arrival_time'] - cleaned_df['arrivalDate']).dt.total_seconds()

# 결과 출력
# print("찾아낸 완벽한 운행 횟수:", cleaned_df['generated_trip_id'].nunique())
# print(cleaned_df[['generated_trip_id', 'vehicle', 'station', 'travel_time_sec']].head(22))