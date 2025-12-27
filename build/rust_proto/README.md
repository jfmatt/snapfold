# Rust Protobuf Edition 2024 Transformation

This directory contains a Bazel macro that enables building Rust protobuf code from edition 2024 proto files, working around prost's current lack of edition support ([tokio-rs/prost#1031](https://github.com/tokio-rs/prost/issues/1031)).

## The Problem

- Your proto files use `edition = "2024"` (the modern protobuf standard)
- Prost (the standard Rust protobuf library) doesn't support protobuf editions yet
- Prost will panic if you try to build edition 2024 protos directly

## The Solution

The `rust_proto3_library` macro transforms edition 2024 proto files to proto3 syntax at build time:

1. **Transform**: Replaces `edition = "2024";` with `syntax = "proto3";`
2. **Clean**: Removes edition-specific imports and options (like `go_features.proto`)
3. **Build**: Creates a `rust_prost_library` from the transformed proto

## Usage

### In your BUILD.bazel

```starlark
load("@rules_proto//proto:defs.bzl", "proto_library")
load("//build/rust_proto:defs.bzl", "rust_proto3_library")

# Original edition 2024 proto_library (for Go and other languages that support editions)
proto_library(
    name = "myproto_proto",
    srcs = ["my.proto"],
    deps = ["@googleapis//google/type:money_proto"],
)

# Transformed proto3 library for Rust
rust_proto3_library(
    name = "myproto_rust_proto",
    srcs = ["my.proto"],  # Same source files as above
    deps = ["@googleapis//google/type:money_proto"],
    visibility = ["//visibility:public"],
)
```

### In your Rust code

The generated crate name is derived from the proto_library and ends with `_proto3`:

```rust
// If your rust_proto3_library target is named "myproto_rust_proto",
// the crate will be named "myproto_proto3"
use myproto_proto3::your::package::name::*;

fn example() {
    let msg = MyMessage {
        field: "value".to_string(),
        ..Default::default()
    };
    println!("{:?}", msg);
}
```

## Example

See `gamedef/BUILD.bazel` for a real example:

```starlark
rust_proto3_library(
    name = "gamedef_rust_proto",
    srcs = ["game.proto"],
    deps = [
        "@googleapis//google/type:money_proto",
    ],
    visibility = ["//visibility:public"],
)
```

And `rustlib/src/lib.rs` for usage:

```rust
pub use gamedef_proto3::snapfold::gamedef::*;

pub fn create_sample_game() -> GameStructure {
    GameStructure {
        id: "test-game".to_string(),
        name: "Test Texas Hold'em".to_string(),
        // ... rest of the proto message
    }
}
```

## What Gets Transformed

The transformation removes edition-specific features that prost doesn't support:

### Before (edition 2024):
```protobuf
edition = "2024";

package snapfold.gamedef;

import "google/protobuf/go_features.proto";
option features.(pb.go).strip_enum_prefix = STRIP_ENUM_PREFIX_STRIP;

message MyMessage {
    // ...
}
```

### After (proto3):
```protobuf
syntax = "proto3";

package snapfold.gamedef;


message MyMessage {
    // ...
}
```

## Important Notes

1. **Source files remain edition 2024**: This only affects the Rust build. Your original `.proto` files stay in edition 2024 for Go and other languages.

2. **Crate naming**: The generated Rust crate name is `<target_name_without_suffixes>_proto3`. For example:
   - Target `gamedef_rust_proto` → crate `gamedef_proto3`
   - Target `mylib_proto` → crate `mylib_proto3`

3. **Dependencies**: Proto dependencies should reference the base `proto_library` targets, not transformed ones.

4. **Go-specific features removed**: Edition-specific imports like `go_features.proto` and options like `features.(pb.go).*` are automatically removed during transformation since they're not relevant for Rust code generation.

## Future Migration

When prost adds edition support (see [tokio-rs/prost#1031](https://github.com/tokio-rs/prost/issues/1031)):

1. Replace `rust_proto3_library` with `rust_prost_library`
2. Update imports from `<name>_proto3::` to the actual crate name
3. Remove this transformation infrastructure

## Implementation Details

The macro creates three internal targets:

1. `_<name>_transformed_srcs`: Genrule that transforms the proto files
2. `<name_cleaned>_proto3`: proto_library from transformed sources
3. `<name>`: rust_prost_library (your public target)

The transformation uses `sed` to perform the syntax replacements. See `defs.bzl` for details.

## Testing

See `rustlib:rustlib_test` for an example test that instantiates and validates proto messages.
