#[derive(Debug, serde::Deserialize)]
pub struct BusParams {
    #[serde(rename = "serviceKey")]
    pub service_key: String,
    #[serde(rename = "routeId")]
    pub route_id: String,
    pub format: String
}

#[derive(Debug, serde::Deserialize)]
pub struct BusPastParams {
    #[serde(rename = "serviceKey")]
    pub service_key: String,
    #[serde(rename = "sDay")]
    pub s_day: String,
    #[serde(rename = "routeId")]
    pub route_id: String,
    #[serde(rename = "stationId")]
    pub station_id: String,
    #[serde(rename = "staOrder")]
    pub sta_order: String
}

/*
#[derive(Debug, serde::Deserialize)]
pub struct TMapParams {
    #[serde(rename = "appKey")]
    pub app_key: String,
    pub version: u8,
    #[serde(rename = "trafficType")]
    pub traffic_type: String,
    #[serde(rename = "zoomLevel")]
    pub zoom_level: String,
    pub radius: u8,
    #[serde(rename = "centerLat")]
    pub center_lat: String,
    #[serde(rename = "centerLon")]
    pub center_lon: String,
    #[serde(rename = "reqCoordType")]
    pub req_coord_type: String,
    #[serde(rename = "respCoordType")]
    pub resp_coord_type: String,
    pub sort: String,
    pub format: String
}
 */