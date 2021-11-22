use jsonschema::{JSONSchema, CompilationOptions};
use argparse::{ArgumentParser, Store};
use serde_json::Value;

fn configure_validator_options(directory: &str) -> CompilationOptions {
    let mut options = JSONSchema::options();
    for entry in std::fs::read_dir(&directory).unwrap_or_else(|_| panic!("Failed to read from {}", &directory)) {
        let file = entry.unwrap();
        let schema_str = std::fs::read_to_string(&file.path()).unwrap();
        let schema: Value = serde_json::from_str(&schema_str)
            .unwrap_or_else(|err| panic!("Failed to parse {}: {}", file.path().to_str().unwrap(), err.to_string()));
        if let Value::Object(root) = &schema {
            if let Some(id_value) = root.get("$id") {
                if let Some(id) = id_value.as_str() {
                    options.with_document(id.to_string(), schema.clone());
                    continue;
                }
            }
        }

        // If the loop makes it here, then it failed to find an ID for this schema
        panic!("Missing id property for {}", file.path().to_str().unwrap());
    }

    return options;
}

fn attempt_compile(directory: &str, options: CompilationOptions) -> bool {
    let mut error_found = false;
    for entry in std::fs::read_dir(&directory).unwrap() {
        let file = entry.unwrap();
        let schema_str = std::fs::read_to_string(&file.path()).unwrap();
        let schema: Value = serde_json::from_str(&schema_str).unwrap();
        if let Err(err) = options.compile(&schema) {
            println!("Error in {}: {}", file.path().to_str().unwrap(), err.to_string());
            error_found = true;
        }
    }

    return error_found;
}

fn main() {
    let mut directory = String::new();
    {
        let mut parser = ArgumentParser::new();
        parser.refer(&mut directory)
            .add_argument("schema-directory", Store, "Specify the directory of schemas to check");

        parser.parse_args_or_exit();
    }

    let validator_options = configure_validator_options(&directory);
    if !attempt_compile(&directory, validator_options) {
        println!("Congratulations! No errors were found!");
    }
}
