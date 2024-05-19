use serde_json::{Map, Value};

pub fn extract_data_from_value(v: &Value) -> (Map<String, Value>, Map<String, Value>, Value) {
    let old_data: Map<String, Value> = v["old_data"].as_object().unwrap().clone();
    let latest_data: Map<String, Value> = v["latest_data"].as_object().unwrap().clone();
    let changenumber_diff: Value = v["changenumber_diff"].clone();
    (old_data, latest_data, changenumber_diff)
}
