mod modules;
use serde_json::from_str;
use std::io;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut input: String = String::new();
    println!("What AppId should I analyze? ");
    io::stdin()
        .read_line(&mut input)
        .expect("failed to readline");
    println!("Ok, running app_write...");
    let _ = modules::wjson::a_writer(from_str(&input).unwrap_or(0)).await?;
    Ok(())
}
