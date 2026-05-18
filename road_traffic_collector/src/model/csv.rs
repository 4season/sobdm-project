use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct CsvRecord {
    pub date: String,
    pub time: String,
    pub id: String,
    pub roadname: String,
    pub fromnode: String,
    pub tonode: String,
    pub len: u16,
    #[serde(rename = "maxSpeed")]
    pub max_speed: u8,
    pub speed: u8,
    pub ttime: f32,
    pub traffic: u8,
}