# C / C++ (placeholder track)

Last reviewed: not yet (placeholder). Before building it, research current courses and versions
with `dojo-new-track`.

Not built yet, and not part of any plan unless a learner chooses it in their roadmap
(`docs/ROADMAP.md`). When a plan reaches it, the tutor agrees the toolchain with the learner,
writes `track.json` (`docs/TRACKS.md`) and generates the first module only.

## Prerequisites

- Fluent in one language first (its track's first milestone, such as Python M1), so C++ is a
  second language and not two new things at once.
- Comfortable in a terminal; basic git.

## Theory (offered just in time, per module)

- Memory: stack and heap, addresses and pointers, object lifetime (before C basics).
- Compilation and linking: source, object files, headers, the linker (before multi-file builds).
- Undefined behaviour and why it does not always crash (before debugging with sanitizers).
- Value, reference and move semantics (before modern C++).

## Outline

1. C basics: types, pointers, arrays, strings, structs, `malloc`/`free`, undefined behaviour,
   `gdb`, `valgrind`.
2. Modern C++ (17/20): references, RAII, classes, the STL, smart pointers, move semantics,
   templates basics.
3. Tooling: CMake, GoogleTest (`ctest` as the track's test command), sanitizers, clang-format.

## Toolchain

A compiler, CMake and GoogleTest. A container keeps the host clean and is the suggested default;
the test command in `track.json` can call it.

## Bridges from Python

Each lesson names the Python equivalent first: a list and `std::vector`, a dict and
`std::unordered_map`, a `with` block and RAII, exceptions in both, and where they differ (fixed
types, manual lifetimes, compile errors before running).
