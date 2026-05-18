mod constant;
mod model;
mod function;
mod list;

use model::*;
use function::*;
use clokwerk::{AsyncScheduler, TimeUnits};
use chrono::{Timelike, Utc};
use chrono_tz::Tz;
use std::time::Duration;
use std::sync::Arc;
use tokio::sync::Mutex;

#[tokio::main]
async fn main() {
    let client = reqwest::Client::new();
    let file_lock = Arc::new(Mutex::new(()));
    
    let mut scheduler = AsyncScheduler::with_tz(Tz::Asia__Seoul)
    ;

    scheduler.every(10.minutes()).run(move || {
        let client_clone = client.clone();
        let lock_clone = file_lock.clone();

        async move {
            let now_seoul = Utc::now().with_timezone(&Tz::Asia__Seoul);
            let current_hour = now_seoul.hour();
            
            if current_hour >= 6 && current_hour < 23 {
                println!("✅ 현재 시간({}시)은 실행 창구입니다. 11개의 요청을 보냅니다.", current_hour);
                if let Err(e) = sender::send_requests(client_clone, lock_clone).await {
                    eprintln!("❌ 요청 처리 중 에러 발생: {}", e);
                }
            } else {
                println!("🌙 현재 시간({}시)은 실행 창구가 아닙니다. 작업을 건너뜁니다.", current_hour);
            }
        }
    });

    loop {
        scheduler.run_pending().await;
        tokio::time::sleep(Duration::from_millis(500)).await;
    }
}