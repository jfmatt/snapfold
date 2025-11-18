# Snapfold - Multi-Language Bazel Project

Multi-module Go workspace with Rust, built with Bazel and native tools.

## Project Structure

```
snapfold/
├── lib/                # Shared Go library module
├── gocli/cmd/cli/      # Go CLI application
├── rust/               # Rust CLI application
├── go.work             # Go workspace configuration
├── MODULE.bazel        # Bazel module (Bzlmod)
└── .bazelrc            # Bazel configuration
```

## Dependency Management

### Add Go Dependency
```bash
cd any/go/module/directory
go get github.com/example/package@v1.2.3
bazel run @rules_go//go -- mod tidy
popd
bazel run //:gazelle
bazel build :...
# If warned about missing use_repo:
bazel run @buildozer -- 'use_repo_add @gazelle//:extensions.bzl go_deps com_github_example_package' //MODULE.bazel:all
```

### Update All Go Dependencies
```bash
cd lib && go get -u ./... && cd ..
cd gocli && go get -u ./... && cd ..
cd lib && bazel run @rules_go//go -- mod tidy && cd ..
cd gocli && bazel run @rules_go//go -- mod tidy && cd ..
bazel run //:gazelle
```

### Add Rust Dependency
```bash
# Edit rust/Cargo.toml to add dependency
cd rust && cargo generate-lockfile && cd ..
mv rust/Cargo.lock .
CARGO_BAZEL_REPIN=1 bazel sync --only=crates
# Edit rust/BUILD.bazel to add to deps list
bazel build //rust:rustcli
```

### Update All Rust Dependencies
```bash
cd rust && cargo update && cd ..
mv rust/Cargo.lock .
CARGO_BAZEL_REPIN=1 bazel sync --only=crates
```

### Regenerate BUILD Files
```bash
bazel run //:gazelle
```

## SDK Selection

### Use Local Go (Default)
```bash
bazel build --config=go_host //gocli/cmd/cli:cli
```

### Use Downloaded Go 1.24.2
```bash
bazel build --config=hermetic //gocli/cmd/cli:cli
```

## Maintenance

### Clean Bazel Cache
```bash
bazel clean
```

### Clean Everything
```bash
bazel clean --expunge
```
