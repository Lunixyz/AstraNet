use serde_json::{json, Value};

pub fn create_changenumber_diff_json(latest_data: &Value, old_data: &Value) -> serde_json::Value {
    let latest_changenumber = latest_data["changenumber"].as_i64().unwrap();
    let old_changenumber = old_data["changenumber"].as_i64().unwrap();
    let has_difference = latest_changenumber != old_changenumber;
    json!({
        "latest_changenumber": latest_changenumber,
        "old_changenumber": old_changenumber,
        "has_difference": has_difference,
    })
}
