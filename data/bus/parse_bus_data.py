import json
import time

import pandas as pd
import requests

SERVICE_KEY = '1234567890'
YEAR = 2025
MONTH = 11
ROUTE_ID = '241219001'
STATION_IDS = [
    '206000908',
    '206000304',
    '206000303',
    '206000808',
    '206000810',
    '206000812',
    '206000814',
    '206000815',
    '206000816',
    '206000045',
    '206000044',
    '206000672',
    '206000770',
    '206000326',
    '206000817',
    '206000463',
    '206000906',
    '206000813',
    '206000811',
    '206000809',
    '206000908'
]
OUTPUT_CSV_FILE = 'bus_arrivals_1115-1130.csv'

all_arrivals_list = []

for day in range(15, 31):
    sDay = f"{YEAR}-{str(MONTH).zfill(2)}-{str(day).zfill(2)}"

    for index, station_id in enumerate(STATION_IDS, start=1):
        api_url = f"https://api.gbis.go.kr/ws/rest/pastarrivalservice/json?serviceKey={SERVICE_KEY}&sDay={sDay}&routeId={ROUTE_ID}&stationId={station_id}&staOrder={index}"
        print(api_url)
        print(f"🔄 {sDay} 날짜, {station_id} 정류장 데이터 요청 중...")

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and data.get("response", {}).get("msgBody") and data["response"]["msgBody"].get("pastArrivalList"):
                past_arrivals = data["response"]["msgBody"]["pastArrivalList"]
                for arrival_info in past_arrivals:
                    arrival_info['searchDate'] = sDay
                    arrival_info['queriedStationId'] = station_id
                all_arrivals_list.extend(past_arrivals)
                print(f"✅ {len(past_arrivals)}개의 도착 정보를 추가했습니다.")
            else:
                result_message = data.get("response", {}).get("msgHeader", {}).get("resultMessage", "데이터 없음")
                print(f"⚠️ {sDay} / {station_id}: {result_message}")

        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 중 오류 발생: {sDay} / {station_id} ({e})")
        except json.JSONDecodeError:
            print(f"❌ JSON 파싱 오류: {sDay} / {station_id} (서버 응답 확인 필요)")
        time.sleep(0.2)

        # CSV 파일로 저장
        if all_arrivals_list:
            print("\n⏳ 모든 데이터를 CSV 파일로 변환 중입니다...")
            df = pd.DataFrame(all_arrivals_list)

            columns_to_keep = [
                'searchDate',
                'queriedStationId',
                'arrivalDate',
                'depatureDate',
                'routeId',
                'vehId',
                'stationId'
            ]

            existing_columns = [col for col in columns_to_keep if col in df.columns]
            df_final = df[existing_columns]

            df_final.to_csv(OUTPUT_CSV_FILE, index=False, encoding='utf-8-sig')
            print(f"\n🎉 성공! '{OUTPUT_CSV_FILE}' 파일이 생성되었습니다.")
        else:
            print("\n🤷 수집된 데이터가 없어 파일을 생성하지 않았습니다.")