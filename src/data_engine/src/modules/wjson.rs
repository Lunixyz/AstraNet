use crate::modules::create_changenumber_diff_json::create_changenumber_diff_json;
use crate::modules::create_file::create_file;
use crate::modules::extract_data_from_value::extract_data_from_value;
use crate::modules::fetch_data_from_server::fetch_data_from_server;
use crate::modules::update_app_info::update_app_info;
use crate::modules::write_to_file::write_to_file;

use serde_json::{json, Value};
use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::path::PathBuf;

const DATA_FILE_NAME: &str = "data.json";
const APP_NOT_FOUND_MESSAGE: &str = "App not found";

pub async fn a_writer(appid: i32) -> Result<(), Box<dyn std::error::Error>> {
    let path: PathBuf = env::current_exe()?.parent().unwrap().join(DATA_FILE_NAME);
    let file: File = File::open(&path).unwrap_or_else(|_| create_file());

    let mut app: HashMap<String, Value> = serde_json::from_reader(file)?;

    let appinfo: Option<&mut Value> = app.get_mut(&appid.to_string());
    let (old_data, mut latest_data, _changenumber_diff) = match appinfo {
        Some(v) => extract_data_from_value(v),
        None => fetch_data_from_server(appid).await?,
    };

    let response: reqwest::Response =
        reqwest::get(format!("http://localhost:3000/app/{}/changelist", appid)).await?;
    let body: Value = response.json().await?;
    if body["data"].is_null() {
        println!("{}", APP_NOT_FOUND_MESSAGE);
        return Ok(());
    }

    let map = body["data"].as_object().unwrap().clone();

    let changenumber_diff: Value =
        create_changenumber_diff_json(&json!(&latest_data), &json!(&old_data));

    let new_data: HashMap<String, Value> = map
        .into_iter()
        .filter(|(key, value)| {
            if let Some(latest_value) = latest_data.get(key) {
                latest_value != value
            } else {
                true
            }
        })
        .collect();

    latest_data.extend(new_data);

    update_app_info(&mut app, appid.to_string(), latest_data, changenumber_diff);

    write_to_file(&json!(app))?;
    Ok(())
}
