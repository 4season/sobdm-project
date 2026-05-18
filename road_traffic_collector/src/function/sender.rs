use std::sync::Arc;
use tokio::sync::Mutex;
use std::error::Error;
use crate::constant::{link, params};
use crate::function::output_stream;
use crate::list::road;
use crate::model::{request, response};

pub async fn send_requests(client: reqwest::Client, file_lock: Arc<Mutex<()>>) -> Result<(), Box<dyn Error>> {
    let mut handles = vec![];

    for i in 0..road::X_LIST.len() {
        let client_clone = client.clone();
        let lock_clone = file_lock.clone();

        let handle = tokio::spawn(async move {
            let param = request::DATA {
                url: params::URL.to_string(),
                bbox: params::BBOX.to_string(),
                width: params::WIDTH,
                height: params::HEIGHT,
                shape_layer: params::SHAPE_LAYER.to_string(),
                x: road::X_LIST[i],
                y: road::Y_LIST[i] };

            let res = client_clone.get(link::POLICE)
                .query(&param)
                .send()
                .await;

            match res {
                Ok(response) => {
                    println!("✅ [{}번째 요청 성공: 상태 코드 {}", i+1, response.status());
                    match response.text().await {
                        Ok(text) => {
                            //println!("📝 서버로부터 받은 실제 데이터: {}", text);
                            match serde_json::from_str::<response::DATA>(&text) {
                                Ok(data) => {
                                    println!("🚓 [{}번째] 경찰청 교통정보: {:?}", i+1, data);
                                    if let Err(e) = output_stream::save_to_csv(&data, i, &lock_clone).await {
                                        eprintln!("❌ [{}번째] CSV 저장 오류: {}", i+1, e);
                                    }
                                },
                                Err(e) => {
                                    eprintln!("❌ [{}번째] JSON 파싱 오류: {}", i+1, e);
                                }
                            }
                        },
                        Err(e) => {
                            eprintln!("❌ [{}번째] 응답 본문 읽기 오류: {}", i+1, e);
                        }
                    }
                },
                Err(e) => {
                    eprintln!("❌ [{}번째] 요청 오류: {}", i+1, e);
                }
            }
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.await?;
    }

    println!("✅ 모든 요청 처리가 완료되었습니다.");
    Ok(())
}