use std::env;
use std::fs::File;
use std::path::PathBuf;

pub fn create_file() -> File {
    let mut path: PathBuf = PathBuf::from(env::current_exe().unwrap());
    path.pop();
    path.push("data.json");
    let path_str: &str = path.to_str().unwrap();
    let mut options: std::fs::OpenOptions = std::fs::OpenOptions::new();
    options.write(true).create(true);
    options.open(path_str).expect("Couldn't create the file")
}
