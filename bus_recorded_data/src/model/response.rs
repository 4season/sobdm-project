#[derive(Debug, serde::Deserialize)]
pub struct BusLiveData {
    #[serde(rename = "queryTime")]
    pub query_time: String, // api 요청 시간
    #[serde(rename = "plateNo")]
    pub plate_no: String, // 차량번호
    #[serde(rename = "stationId")]
    pub station_id: String, // 정류소 ID
    #[serde(rename = "stationSeq")]
    pub station_seq: String, // 현재 정류소 순번
    #[serde(rename = "stateCd")]
    pub state_cd: String, // 운행 상태 코드 (1: 주행 중 | 2: 정류소 도착)
    pub crowded: String, // 버스 안 혼잡도
}

#[derive(Debug, serde::Deserialize)]
pub struct BusPastData {
    pub infortm: String, // 정보 생성 날짜
    pub staOrder: String, // 정류소 순번
    pub stationId: String, // 정류소 ID
    pub depatureDate: String, // 출발 예정 시간
    pub arrivalDate: String, // 도착 예정 시간
    pub RArrivalDate: String, // 실시간 도착 시간
    pub routeSeq: String, // 노선 순번 (1: 상행 | 2: 하행)
    pub runSeq: String, // 운행 순번
    pub vehId: String, // 차량 ID
}

/*
#[derive(Debug, serde::Deserialize)]
pub struct TMapData {
    pub updateTime: String, // 마지막 데이터 업데이트 시간
    pub linkId: String, // 도로 링크 ID
    pub description: String, // 도로 상황 Text
    pub congestion: u8, // 도로 혼잡도 (0: 정보없음 | 1: 원할 | 2: 서행 | 3: 지체 | 4: 정체)
    pub roadType: String, // 도로 타입 (001: 고속도로 | 002: 도시고속도로 | 004: 주요도로 | 005: 터널 | 006: 한강교량 | 007: 한강주변도로 | 013: 수도권 주요국도)
    pub startNodName: String, // 시작 도로 노드
    pub endNodName: String, // 끝 도로 노드
    pub distance: u32, // 구간 거리
    pub travalTime: u32, // 구간 통행 시간s
    pub travalSpeed: u8 // 구간 통행 속도
}
 */