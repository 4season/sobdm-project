use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct DATA {
    pub url: String,
    #[serde(rename = "BBOX")]
    pub bbox: String,
    #[serde(rename = "WIDTH")]
    pub width: u16,
    #[serde(rename = "HEIGHT")]
    pub height: u16,
    #[serde(rename = "SHAPE_LAYER")]
    pub shape_layer: String,
    #[serde(rename = "X")]
    pub x: u16,
    #[serde(rename = "Y")]
    pub y: u16,
}