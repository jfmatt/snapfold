# Snapfold - Multi-Language Bazel Project

Demonstrates Go and Rust in a single Bazel monorepo using Bzlmod.

## Project Structure

```
snapfold/
├── lib/greeting/       # Go library package
├── gocli/cmd/cli/      # Go CLI binary
├── rustlib/            # Rust library (Bazel-native)
├── rustcli/            # Rust CLI binary (Bazel-native)
├── go.mod              # Go module for entire repo
├── Cargo.toml          # External Rust dependencies
├── MODULE.bazel        # Bazel module configuration
└── .bazelrc            # Build configuration
```

## Build Playbooks

### Go (Bazel)
```bash
bazel build //<path/to/package>:<target>
bazel run //<path/to/package>:<target>
bazel run //<path/to/package>:<target> -- <args>
```

### Go (Native)
```bash
go build -o <output> ./<path/to/package>
./<output> <args>
```

### Rust (Bazel)
```bash
bazel build //<path/to/package>:<target>
bazel run //<path/to/package>:<target>
bazel test //<path/to/package>:<test_target>
```

## Dependency Management

### Go Dependencies

**Repo-level operation:**
```bash
# Add or update dependency
bazel run @rules_go//go get <module>@<version>

# Regenerate BUILD files for all Go packages
bazel run //:gazelle

# Verify builds
bazel build //<path/to/package>:<target>

# If warned about missing use_repo, add it:
bazel run @buildozer -- 'use_repo_add @gazelle//:extensions.bzl go_deps <repo_name>' //MODULE.bazel:all
```

**Update all Go dependencies:**
```bash
bazel run @rules_go//go get -u ./...
bazel run //:gazelle
```

### Rust Dependencies

**For external crates (from crates.io):**

#### Add a new external crate
```bash
# 1. Edit Cargo.toml and add dependency under [dependencies]
# 2. Regenerate lockfile
cargo generate-lockfile

# 3. Update Bazel's crate repository
CARGO_BAZEL_REPIN=1 bazel sync --only=crates

# 4. Edit the BUILD.bazel file for your Rust target
#    Add @crates//:<crate_name> to the deps list

# 5. Verify build
bazel build //<path/to/package>:<target>
```

#### Update all external Rust dependencies
```bash
cargo update
CARGO_BAZEL_REPIN=1 bazel sync --only=crates
```

#### For internal Rust crates

Per-module operation - just edit BUILD.bazel:
```bash
# Add //<path/to/library>:<library_name> to deps in BUILD.bazel
bazel build //<path/to/package>:<target>
```

## Toolchain Configuration

### Go SDK Selection

```bash
# Use host-local Go installation (default)
bazel build --config=go_host //<path/to/package>:<target>

# Use Bazel-downloaded Go
bazel build --config=hermetic //<path/to/package>:<target>
```

## Maintenance

```bash
# Clean build cache
bazel clean

# Clean everything including external dependencies
bazel clean --expunge
```

## Architecture

**Go:**
- Single module at repo root (go.mod)
- Internal packages reference each other via import paths
- BUILD files auto-generated via Gazelle
- Compatible with both Bazel and native Go tooling

**Rust:**
- Bazel-native with manually written BUILD files
- Internal crates reference each other via Bazel labels
- External dependencies managed via root Cargo.toml + crate_universe
- Hermetic builds with all dependencies fetched by Bazel
