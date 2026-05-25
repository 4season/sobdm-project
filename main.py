import pandas as pd
import numpy as np
from tensorflow.keras import Input
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Activation
from tensorflow.keras.optimizers import AdamW
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from module.plt_mode import plt_hist_restored, plt_time_restored
from module.analyze_worst import analyze_worst_cases
from sklearn.metrics import r2_score

df = pd.read_pickle('./data/processed/processed_data.pkl')
pd.set_option('display.max_columns', None)

target_col = ['arrival_min_sin', 'arrival_min_cos']
drop_col = ['minute_sin', 'minute_cos']
#    'day_sin', 'day_cos', 'hour_sin', 'hour_cos', 'minute_sin', 'minute_cos',
#    'is_weekend', 'is_commute',
#    'road_sin', 'road_cos', 'station_sin', 'station_cos', 'bus_line', target_col, 'len', 'maxSpeed', 'speed', 'traffic',
#    'temp', 'rain', 'humidity'
#]
X = df.drop(columns=target_col + drop_col)
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential([
    Input(shape=X_train.shape[1:]),

    Dense(128),
    BatchNormalization(),
    Activation('swish'),
    Dropout(0.3),

    Dense(64),
    BatchNormalization(),
    Activation('swish'),
    Dropout(0.3),

    Dense(32),
    Activation('swish'),

    Dense(2)
])

optimizer = AdamW(learning_rate=0.001, weight_decay=0.004)
model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])

callbacks = [
    EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
    ModelCheckpoint('best_bus_model.keras', monitor='val_loss', save_best_only=True),
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6, verbose=1)
]

print("🚌 Bus Arrival Time Prediction Training is Activation now.")
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=callbacks,
    verbose=1
)

loss, mae = model.evaluate(X_test, y_test)
mae_sec = (mae * (60 / (2 * np.pi))) * 60
print(f"\n평균 오차(MAE): {mae:.4f} | 평균 오차(Sec): {mae_sec:.2f}")

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"모델의 점수(R2 Score): {r2:.4f}")

plt_hist_restored(history, cycle=60)
plt_time_restored(y_test, y_pred, 50)

#print("가장 많이 틀린 데이터 TOP 10")
#worst_df = analyze_worst_cases(y_test, y_pred, X_test, cycle=60, top_n=10)

# 결과 출력
#pd.set_option('display.max_columns', None)  # 모든 컬럼 보기
#print(worst_df[['Actual(Min)', 'Predicted(Min)', 'Error(Sec)']])
#print('\n전체 보기: ')
#print(worst_df)

#print('\nsin값과 상관관계가 지나치게 높은(0.9 이상) 변수가 있는지 확인')
#corr_matrix = df.corr()
#print(corr_matrix['arrival_min_sin'].sort_values(ascending=False))