#![warn(unused_imports)]
#![allow(warnings)]
use once_cell::sync::Lazy;
use reqwest::blocking::Client;
use reqwest::header::{HeaderMap, HeaderValue};
use serde::{Deserialize, Serialize};
use serde_json::json;
use serde_json::Value;
use std::collections::BTreeMap;
use std::collections::HashMap;
use std::fs::File;
use std::io::prelude::*;
use webbrowser;


fn main() -> std::io::Result<()> {
    let roles = vec![
        "rust engineer",
        "rust developer",
        "blockchain developer",
        "blockchain engineer",
    ];
    let db = match File::open("jobs.db.json") {
        Ok(mut file) => {
            let mut contents = String::new();
            file.read_to_string(&mut contents).unwrap();
            serde_json::from_str(&contents).unwrap()
        }
        Err(_) => {
            json!({});
        }
    };
    let notify = false;
    let url = "https://4cqmtmmk73-dsn.algolia.net/1/indexes/Post_production/query";
    let mut headers = HeaderMap::new();
    headers.insert("Origin", HeaderValue::from_static("https://startup.jobs"));
    headers.insert("User-Agent", HeaderValue::from_static("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"));
    headers.insert("Referer", HeaderValue::from_static("https://startup.jobs/"));
    headers.insert("Content-Type", HeaderValue::from_static("application/json"));
    let params = [
        (
            "x-algolia-agent",
            "Algolia for JavaScript (4.14.2); Browser (lite)",
        ),
        ("x-algolia-api-key", "17cd9f3c024650820efaa17c39ea2b1d"),
        ("x-algolia-application-id", "4CQMTMMK73"),
    ];
    let client = Client::new();
    for role in roles {
        let payload = json!({
            "query": role,
            "attributesToRetrieve": [
                "path",
                "company_slug",
                "company_logo_url",
                "title",
                "company_name",
                "_tags",
                "remote",
                "location",
                "location_html"
            ],
            "hitsPerPage": 25,
            "page": 0,
            "facets": [
                "commitment"
            ],
            "filters": "",
            "tagFilters": [
                ""
            ],
            "facetFilters": [
                [
                    "commitment:Full-Time",
                    "commitment:Part-Time",
                    "commitment:Internship",
                    "commitment:Contractor"
                ],
                "remote:true"
            ],
            "ruleContexts": [],
            "analyticsTags": [
                "frontend"
            ]
        });
        let payload_string = serde_json::to_string(&payload).unwrap();
        let response = client
            .post(url)
            .headers(headers.clone())
            .query(&params)
            .body(payload_string)
            .send()
            .unwrap();

        let json: Value = serde_json::from_str(&response.text().unwrap()).unwrap();
        if let Value::Object(map) = json {
            match map.get("hits").unwrap() {
                Value::Array(arr) => {
                    for i in (0..arr.len()) {
                        if let Value::Object(map) = &arr[i] {
                            let startup_link = "https://startup.jobs".to_string()
                                + &extract(map.get("path").unwrap());

                            let mut db = BTreeMap::new();
                            db.insert("path", startup_link);
                            db.insert("comapany-name", extract(map.get("company_name").unwrap()));
                            db.insert("title", extract(map.get("title").unwrap()));
                            db.insert("location", extract(map.get("location").unwrap()));
                            db.insert(
                                "remote",
                                extract_bool(map.get("remote").unwrap()).to_string(),
                            );
                            let mut file = File::create("jobs.db.json").unwrap();
                            serde_json::to_writer(&mut file, &db).unwrap();

                            // let v: Value = serde_json::from_str(db);
                            dbg!(json!(db));

                        }
                    }
                }
                _ => println!("{}", "I'm not working fam"),
            }
        }
    }
    Ok(())
}

fn extract(string: &Value) -> String {
    if let Value::String(str) = string {
        return str.to_string();
    } else {
        return String::new();
    }
}

fn extract_bool(bool: &Value) -> bool {
    if let Value::Bool(boolean) = bool {
        return *boolean;
    } else {
        return false;
    }
}
