import pandas as pd

traffic_df = pd.read_csv('./data/road/road_combined_data.csv')
pd.set_option('display.max_columns', None)

traffic_df['date_time'] = pd.to_datetime(traffic_df['date'] + ' ' + traffic_df['time'])
traffic_df = traffic_df.drop(columns=['date', 'time', 'roadname', 'fromnode', 'tonode'])
traffic_df = traffic_df.sort_values(by=['date_time', 'id'], ascending=True)

desired = ['date_time', 'id', 'len', 'maxSpeed', 'speed', 'ttime', 'traffic']
traffic_df = traffic_df[desired]

print(traffic_df.head(20))
traffic_df.to_csv('./data/road/processed_road_data.csv', index=False)
print("💾 데이터 저장 완료!")
