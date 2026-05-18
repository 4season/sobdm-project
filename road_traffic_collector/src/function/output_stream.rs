use crate::response;
use crate::identifier;
use crate::model::csv::CsvRecord;
use std::error::Error;
use std::fs::OpenOptions;
use std::sync::Arc;
use chrono::{Datelike, Local};
use tokio::sync::Mutex;

pub async fn save_to_csv(data: &response::DATA, i: usize, lock: &Arc<Mutex<()>>) -> Result<(), Box<dyn Error>> {
    let _guard = lock.lock().await;

    let record = CsvRecord {
        date: Local::now().format("%Y-%m-%d").to_string(),
        time: Local::now().format("%H:%M:%S").to_string(),
        id: (i+1).to_string(),
        roadname: data.roadname.clone(),
        fromnode: data.fromnode.clone(),
        tonode: data.tonode.clone(),
        len: data.len.parse().unwrap_or(0),
        max_speed: data.max_speed.parse().unwrap_or(0),
        speed: data.speed.parse().unwrap_or(0),
        ttime: data.ttime.parse().unwrap_or(0.00),
        traffic: identifier::traffic(
            data.max_speed.parse().unwrap_or(0),
            data.speed.parse().unwrap_or(0)),
    };

    let now = Local::now();
    let today = now.date_naive();
    let file_path = format!(
        "data/{}-{:02}-{:02}_traffic_data.csv",
        today.year(),
        today.month(),
        today.day()
    );

    let write_header = !std::path::Path::new(&file_path).exists();
    let file = OpenOptions::new()
        .append(true)
        .create(true)
        .append(true)
        .open(&file_path)?;

    let mut wtr = csv::WriterBuilder::new()
        .has_headers(write_header)
        .from_writer(file);

    wtr.serialize(record)?;
    wtr.flush()?;

    println!("✅ [{}번째] CSV 파일 저장 성공: {}", i+1, file_path);
    Ok(())
}
