# 🚌 SOBDM Project
### Seongnam-si 109 Bus Delay Prediction Model using Multilayer Perceptron (MLP)

**성남시 109번 버스 지연 시간 예측 모델**을 구축하는 프로젝트입니다. 머신러닝 기반 딥러닝 모델을 활용하여 버스 도착 시간을 정확하게 예측합니다.

---

## 📋 프로젝트 개요

### 목표
- 버스의 예상 도착 시간을 정확하게 예측
- 도로 교통량, 날씨, 시간대 등 다양한 요소를 종합적으로 분석
- 탑승객 편의성 증대 및 교통 서비스 개선

### 주요 특징
- **딥러닝 모델**: Multilayer Perceptron (MLP) 기반 신경망
- **다중 데이터 소스**: 버스 데이터, 도로 교통량, 날씨 정보 통합
- **시계열 분석**: 시간대별 패턴 분석을 통한 정확한 예측
- **주기적 데이터 변환**: Sin/Cos 변환을 이용한 순환 데이터 처리

---

## 📊 프로젝트 구조

```
sobdm-project/
├── data/                           # 데이터 저장소
│   ├── bus/                        # 버스 관련 데이터
│   ├── road/                       # 도로 교통량 데이터
│   ├── weather/                    # 날씨 데이터
│   └── processed/                  # 전처리된 데이터
├── module/                         # 유틸리티 모듈
│   ├── analyze_worst.py           # 오차 분석 모듈
│   ├── filltering_and_sorting.py  # 데이터 필터링 및 정렬
│   ├── plt_mode.py                # 시각화 모듈
│   └── road_dataframe.py          # 도로 데이터 처리
├── gragh/                          # 분석 그래프 및 시각화
│   ├── HeatMap.png                # 요일별 시간대 교통량 히트맵
│   ├── StackedBar.png             # 교통 상태 비율 분석
│   └── road_traffic_analysis.R    # R 기반 교통 분석 스크립트
├── bus_recorded_data/             # 버스 기록 데이터
├── main.py                         # 모델 학습 및 평가 메인 스크립트
├── preprocess_data.py             # 데이터 전처리 스크립트
├── best_bus_model.keras           # 학습된 최고 성능 모델
├── bus_model.png                  # 모델 구조 다이어그램
├── LICENSE                        # MIT License
└── README.md                      # 프로젝트 문서

```

---

## 🛠️ 기술 스택

### 언어 및 라이브러리
- **Python** (62.8%)
  - TensorFlow/Keras: 딥러닝 모델 구축
  - Pandas, NumPy: 데이터 처리 및 분석
  - Scikit-learn: 전처리, 모델 평가
  - Matplotlib, Seaborn: 데이터 시각화

- **Rust** (32.8%): 고성능 데이터 처리 지원
- **R** (4.4%): 통계 분석 및 시각화

---

## 🚀 시작하기

### 필수 요구사항
```bash
# Python 3.8 이상
python --version

# 필요 라이브러리 설치
pip install -r requirements.txt
```

### 주요 라이브러리
- TensorFlow 2.x
- Keras
- Pandas, NumPy
- Scikit-learn
- Matplotlib

### 설치 방법
```bash
# 저장소 복제
git clone https://github.com/4season/sobdm-project.git
cd sobdm-project

# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 필수 패키지 설치
pip install tensorflow keras pandas numpy scikit-learn matplotlib
```

---

## 📈 데이터 처리 파이프라인

### 1. 데이터 전처리 (`preprocess_data.py`)
- **버스 데이터**: 도착 시간, 정거장, 노선 정보
- **도로 교통량 데이터**: 시간별 교통 상태, 속도 정보
- **날씨 데이터**: 기온, 강수량, 습도

#### 주요 처리 과정
```python
# 1. 데이터 병합 (Merge)
- 버스 데이터 ← 날씨 데이터 ← 도로 교통량 데이터

# 2. 주기적 데이터 변환 (Cyclic Encoding)
- hour → (hour_sin, hour_cos)
- minute → (minute_sin, minute_cos)
- day_of_week → (day_sin, day_cos)

# 3. 특성 스케일링
- MinMaxScaler: 수치 데이터 정규화
- 순환 데이터는 스케일링하지 않음
```

### 2. 모델 학습 (`main.py`)

#### 모델 구조
```
Input Layer (15 features)
    ↓
Dense(128) → BatchNorm → Swish + Dropout(0.3)
    ↓
Dense(64) → BatchNorm → Swish + Dropout(0.3)
    ↓
Dense(32) → Swish
    ↓
Output Layer (2 units) → [arrival_min_sin, arrival_min_cos]
```

#### 학습 설정
- **옵티마이저**: AdamW (lr=0.001, weight_decay=0.004)
- **손실 함수**: Mean Squared Error (MSE)
- **평가 지표**: MAE (Mean Absolute Error), R² Score
- **콜백**:
  - EarlyStopping: 과적합 방지 (patience=15)
  - ModelCheckpoint: 최고 성능 모델 저장
  - ReduceLROnPlateau: 학습률 자동 조정

---

## 📊 분석 및 시각화

### 교통량 분석 (`gragh/road_traffic_analysis.R`)

#### 1. 히트맵 (HeatMap.png)
- 요일별 × 시간대별 평균 교통량
- 색상: 녹색(원활) → 노랑(서행) → 빨강(정체)
- 피크 시간대 및 요일 패턴 파악

#### 2. 스택 바 차트 (StackedBar.png)
- 요일별 시간대 교통 상태 비율
- 원활(1), 서행(2), 정체(3) 분포
- 요일별 변동성 분석

---

## 🎯 주요 기능

### 1. 데이터 분석 모듈 (`module/`)
- **analyze_worst.py**: 예측 오차가 큰 사례 분석
- **filltering_and_sorting.py**: 이상치 제거 및 데이터 정렬
- **plt_mode.py**: 모델 성능 시각화
- **road_dataframe.py**: 도로 데이터 전처리

### 2. 예측 성능 평가
```
평균 오차 (MAE): 초 단위로 표시
R² Score: 모델 설명력 (0~1, 높을수록 좋음)
최악 사례 분석: 오류가 큰 상황 파악
```

---

## 📝 사용 방법

### 1. 데이터 전처리
```bash
python preprocess_data.py
# 출력: 데이터 형태 및 저장 완료 메시지
```

### 2. 모델 학습 및 평가
```bash
python main.py
# 출력:
# - 학습 진행 상황
# - 평균 오차(MAE) 및 초 단위 오차
# - R² Score
# - 모델 성능 그래프
```

### 3. 학습된 모델 사용
```python
from tensorflow.keras.models import load_model

model = load_model('best_bus_model.keras')
predictions = model.predict(new_data)
```

---

## 📊 결과 및 성능

| 지표 | 설명 |
|------|------|
| **MAE** | Mean Absolute Error (분 단위) |
| **MAE(초)** | 평균 오차를 초 단위로 변환 |
| **R² Score** | 모델의 설명력 지수 |

### 모델 최적화 기법
- 배치 정규화 (Batch Normalization)
- 드롭아웃 (Dropout): 0.3
- 조기 종료 (Early Stopping)
- 학습률 감소 (ReduceLROnPlateau)

---

## 📚 관련 문서

- **109_DNN_발표자료.pdf**: 프로젝트 발표 자료
- **20213803_허준호_논문초안.pdf**: 논문 초안 및 상세 분석

---

## 🔍 특성 엔지니어링

### 입력 특성 (총 15개)
1. **시간 관련** (순환 데이터)
   - day_sin, day_cos (요일)
   - hour_sin, hour_cos (시간)
   - minute_sin, minute_cos (분)
   - arrival_min_sin, arrival_min_cos (도착 분)

2. **상황 여부**
   - is_weekend (주말 여부)
   - is_commute (통근 시간 여부)

3. **도로 및 교통 정보**
   - road_sin, road_cos (도로 ID)
   - station_sin, station_cos (정거장 ID)
   - bus_line (버스 노선)
   - len, maxSpeed, speed, traffic

4. **날씨 정보**
   - temp (기온)
   - rain (강수량)
   - humidity (습도)

### 출력 특성
- **arrival_min_sin, arrival_min_cos**: 도착 시간의 sin/cos 변환값
- 역변환으로 정확한 분 단위 도착 시간 복원

---

## 💡 주요 인사이트

1. **시간대 패턴**: 출퇴근 시간대(7-9시, 17-19시)에 버스 지연 증가
2. **요일 영향**: 평일과 주말의 교통 패턴 뚜렷한 차이
3. **날씨 요소**: 강수량과 습도가 버스 지연에 미치는 영향
4. **교통량 상관성**: 도로 교통량 증가 시 버스 지연 시간 급증

---

## 🤝 기여 가이드

버그 리포트, 기능 제안, Pull Request를 환영합니다!

---

## 📜 라이센스

이 프로젝트는 **MIT License** 하에 배포됩니다.  
자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.

---

## 👤 프로젝트 관리자

- **저자**: 4season
- **이메일**: [GitHub 프로필](https://github.com/4season)

---

## 📞 문의 및 지원

프로젝트에 대한 질문이나 제안사항이 있으신 경우:
- GitHub Issues를 통해 문제 제기
- Pull Request로 개선 제안
- 이메일을 통한 직접 연락

---

**Last Updated**: 2026-05-25  
**Version**: 1.0.0-beta
