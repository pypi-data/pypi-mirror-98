#!/bin/bash
export PATH=$PATH:/tmp/clang/bin
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_CC=/tmp/clang/bin/clang
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_TOOLCHAIN_PREFIX=/tmp/cctools/bin
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_AR=/tmp/cctools/bin/x86_64-apple-darwin-ar
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_RANLIB=/tmp/cctools/bin/x86_64-apple-darwin-ranlib
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_LD_LIBRARY_PATH=/tmp/clang/lib
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_RUSTFLAGS="-C linker=/tmp/clang/bin/clang -C link-arg=-B -C link-arg=/tmp/cctools/bin -C link-arg=-target -C link-arg=x86_64-apple-darwin -C link-arg=-isysroot -C link-arg=/tmp/MacOSX10.12.sdk -C link-arg=-Wl,-syslibroot,/tmp/MacOSX10.12.sdk -C link-arg=-Wl,-dead_strip"
# For ring's use of `cc`.
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_APPLE_DARWIN_CFLAGS_x86_64_apple_darwin="-B /tmp/cctools/bin -target x86_64-apple-darwin -isysroot /tmp/MacOSX10.12.sdk -Wl,-syslibroot,/tmp/MacOSX10.12.sdk -Wl,-dead_strip"
# The wrong linker gets used otherwise: https://github.com/rust-lang/rust/issues/33465.
export ORG_GRADLE_PROJECT_RUST_ANDROID_GRADLE_TARGET_X86_64_PC_WINDOWS_GNU_RUSTFLAGS="-C linker=x86_64-w64-mingw32-gcc"

# Ensure we're compiling dependencies in non-debug mode.
# This is required for rkv/lmdb to work correctly on Android targets and not link to unavailable symbols.
export TARGET_CFLAGS="-DNDEBUG"

# Install clang, a port of cctools, and the macOS SDK into /tmp. This
# is all cribbed from mozilla-central; start at
# https://searchfox.org/mozilla-central/rev/39cb1e96cf97713c444c5a0404d4f84627aee85d/build/macosx/cross-mozconfig.common.

pushd /tmp || exit

tooltool.py \
  --url=http://taskcluster/tooltool.mozilla-releng.net/ \
  --manifest="/builds/worker/checkouts/src/taskcluster/scripts/macos-cc-tools.manifest" \
  fetch

curl -sfSL --retry 5 --retry-delay 10 https://firefox-ci-tc.services.mozilla.com/api/queue/v1/task/NcaljhkvQOSKxGlBSWJl_w/runs/0/artifacts/public/build/cctools.tar.xz > cctools.tar.xz
tar -xf cctools.tar.xz
ls -l /tmp/cctools
curl -sfSL --retry 5 --retry-delay 10 https://firefox-ci-tc.services.mozilla.com/api/queue/v1/task/eJJotfnPSt2weVG0sZlfeQ/runs/0/artifacts/public/build/clang.tar.zst > clang.tar.zst
tar -I zstd -xf clang.tar.zst
ls -l /tmp/clang
ls -l /tmp/clang/bin

rustup target add x86_64-apple-darwin
rustup target add x86_64-pc-windows-gnu

popd || exit
