use serde::{Deserialize, Serialize};
#[derive(Serialize, Deserialize, Debug)]
pub struct DATA {
    pub roadname: String,
    pub fromnode: String,
    pub tonode: String,
    pub len: String,
    #[serde(rename = "maxSpeed")]
    pub max_speed: String,
    pub speed: String,
    pub ttime: String,
}