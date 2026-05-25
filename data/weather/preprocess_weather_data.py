import pandas as pd

weather_df = pd.read_csv('./data/weather/OBS_AWS_TIM_20251203000411.csv')
pd.set_option('display.max_columns', None)

# 날씨 데이터 열 이름 변경
weather_df = weather_df.rename(columns={
    '일시': 'date_weather',
    '기온(°C)': 'temp',
    '풍향(deg)': 'wind_dir',
    '풍속(m/s)': 'wind_speed',
    '강수량(mm)': 'rain',
    '습도(%)': 'humidity',
    '지점': 'spot_id',
    '지점명': 'spot_name'
})

weather_df['date_weather'] = pd.to_datetime(weather_df['date_weather'])
weather_df = weather_df.drop(columns=['wind_dir', 'wind_speed', 'spot_id', 'spot_name'])

desired = ['date_weather', 'temp', 'rain', 'humidity']
weather_df = weather_df[desired]
print(weather_df.head(20))

weather_df.to_csv('./data/weather/processed_weather_data.csv', index=False)
print("💾 데이터 저장 완료!")