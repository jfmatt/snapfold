/// A simple greeting function from the shared Rust library
pub fn get_greeting(name: &str) -> String {
    if name.is_empty() {
        "Hello from the Rust library!".to_string()
    } else {
        format!("Hello, {}! (from Rust library)", name)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_greeting() {
        assert_eq!(get_greeting(""), "Hello from the Rust library!");
        assert_eq!(get_greeting("World"), "Hello, World! (from Rust library)");
    }
}
