mod models;
mod constant;

use tokio::time::{self, Duration};
use reqwest;
use serde::Deserialize;
use models::*;
use constant::*;
use std::env;
use dotenv::dotenv;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {

    dotenv().ok();
    let api_key_live = env::var("API_KEY_LIVE").expect("API_KEY가 .env 파일에 설정되어 있어야 합니다.");
    let api_key_past = env::var("API_KEY_PAST").expect("API_KEY가 .env 파일에 설정되어 있어야 합니다.");

    let mut interval = time::interval(Duration::from_secs(60));

    loop {
        interval.tick().await;

        let client = reqwest::Client::new();
        let params = request::BusParams {
            service_key: "".parse().unwrap(),
            route_id: "".parse().unwrap(),
            format: "json".parse().unwrap()
        };

        match reqwest::get().await {
            Ok(response) => {
                match response.json::<response::BusLiveData>().await {
                    Ok(data) => println!("성공적으로 데이터를 파싱했습니다: {:?}", data),
                    Err(error) => eprintln!("JSON 파싱 에러: {}", error),
                }
            }
            Err(error) => eprintln!("요청 에러: {}", error),
        }
    }
}