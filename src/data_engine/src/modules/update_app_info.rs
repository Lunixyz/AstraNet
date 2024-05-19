use serde_json::{json, Map, Value};
use std::collections::HashMap;

pub fn update_app_info(
    app: &mut HashMap<String, Value>,
    appid: String,
    latest_data: Map<String, Value>,
    changenumber_diff: Value,
) {
    let mut new_json: Map<String, Value> = Map::new();
    new_json.insert("old_data".to_string(), json!(latest_data.clone()));
    new_json.insert("latest_data".to_string(), json!(latest_data));
    new_json.insert("changenumber_diff".to_string(), changenumber_diff);
    app.insert(appid, json!(new_json));
}
