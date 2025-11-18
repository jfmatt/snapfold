use rustlib;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Hello from the Rust CLI!");
    println!("Built with Bazel");
    println!("{}", rustlib::get_greeting("Rust CLI"));

    // Simple example showing reqwest is available
    let url = "https://httpbin.org/get";
    println!("\nMaking a GET request to {}...", url);

    let response = reqwest::get(url).await?;
    let status = response.status();

    println!("Response status: {}", status);

    if status.is_success() {
        println!("Request successful!");
    }

    Ok(())
}
