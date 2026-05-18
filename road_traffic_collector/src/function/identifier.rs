pub fn traffic(road_type: i8, speed: u8) -> u8 { // 30이하: 어린이보호구역 | 70미만: 도시도로 | 70이상: 국도
    match road_type {
        70.. => traffic_national_road(speed),
        31..70 => traffic_city_road(speed),
        _ => traffic_school_zone(speed),
    }
}

fn traffic_national_road(speed: u8) -> u8 {
    match speed {
        0..30 => 3,
        30..=50 => 2,
        _ => 1,
    }
}

fn traffic_city_road(speed: u8) -> u8 {
    match speed {
        0..15 => 3,
        15..=25 => 2,
        _ => 1,
    }
}

fn traffic_school_zone(speed: u8) -> u8 {
    match speed {
        0..10 => 3,
        _ => 2,
    }
}