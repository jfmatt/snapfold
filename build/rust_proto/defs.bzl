"""Rust protobuf rules with edition → proto3 transformation.

This module provides a workaround for prost's lack of edition support by transforming
edition 2024 proto files to proto3 syntax at build time.

When prost adds edition support (https://github.com/tokio-rs/prost/issues/1031),
this transformation can be removed and rust_prost_library can be used directly.
"""

load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_rust_prost//:defs.bzl", "rust_prost_library")

def _transform_proto_impl(ctx):
    """Transforms edition 2024 proto files to proto3 syntax."""
    outputs = []

    for src in ctx.files.srcs:
        # Create output file with same name
        out = ctx.actions.declare_file(
            ctx.label.name + "/" + src.basename,
        )
        outputs.append(out)

        # Transform the proto file
        ctx.actions.run_shell(
            inputs = [src],
            outputs = [out],
            command = """
                # Read the input file and transform it
                sed -e 's/^edition = "2024";$/syntax = "proto3";/' \
                    -e '/^import "google\\/protobuf\\/go_features\\.proto";$/d' \
                    -e '/^option features\\..*$/d' \
                    "$1" > "$2"
            """,
            arguments = [src.path, out.path],
            mnemonic = "TransformProtoEdition",
            progress_message = "Transforming %s from edition 2024 to proto3" % src.short_path,
        )

    return [DefaultInfo(files = depset(outputs))]

_transform_proto = rule(
    implementation = _transform_proto_impl,
    attrs = {
        "srcs": attr.label_list(
            allow_files = [".proto"],
            mandatory = True,
            doc = "Proto source files to transform",
        ),
    },
    doc = "Transforms edition 2024 proto files to proto3 syntax for prost compatibility",
)

def rust_proto3_library(
        name,
        srcs,
        deps = [],
        visibility = None,
        **kwargs):
    """Creates a rust_prost_library from edition 2024 proto files.

    This macro works around prost's lack of edition support by:
    1. Transforming edition → proto3 syntax
    2. Creating a new proto_library from transformed sources
    3. Generating rust_prost_library from the transformed proto_library

    Args:
        name: Name of the rust_prost_library target
        srcs: List of .proto source files (edition 2024)
        deps: List of proto_library dependencies (use transformed versions if they use editions)
        visibility: Visibility for the rust_prost_library target
        **kwargs: Additional arguments passed to rust_prost_library

    Example:
        # In your BUILD.bazel:
        load("@rules_proto//proto:defs.bzl", "proto_library")
        load("//build/rust_proto:defs.bzl", "rust_proto3_library")

        # Original edition 2024 proto_library (for Go and other languages)
        proto_library(
            name = "myproto_proto",
            srcs = ["my.proto"],
            deps = ["@googleapis//google/type:money_proto"],
        )

        # Transformed proto3 library for Rust
        rust_proto3_library(
            name = "myproto_rust_proto",
            srcs = ["my.proto"],  # Same source files
            deps = ["@googleapis//google/type:money_proto"],
            visibility = ["//visibility:public"],
        )
    """

    # Generate transformed proto files
    transform_name = "_%s_transformed_srcs" % name
    _transform_proto(
        name = transform_name,
        srcs = srcs,
        tags = ["manual"],
    )

    # Create proto_library from transformed sources
    # Use the target name directly (without underscore prefix) so the generated
    # Rust crate gets a clean name matching the rust_prost_library target
    proto3_name = "%s_proto3" % name.replace("_rust_proto", "").replace("_proto", "")
    proto_library(
        name = proto3_name,
        srcs = [":%s" % transform_name],
        deps = deps,
        tags = ["manual"],
    )

    # Generate Rust code from transformed proto_library
    # The crate name will be derived from the proto_library name above
    rust_prost_library(
        name = name,
        proto = ":%s" % proto3_name,
        visibility = visibility,
        **kwargs
    )
