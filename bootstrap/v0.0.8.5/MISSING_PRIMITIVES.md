# Missing Primitives Report

Files imported by the compiler but not yet implemented. Generated during v0.0.8.5 compilation cleanup.

Summary:
- **12 truly missing files** (needs implementation or import removal)
- **7 internal/compiler files** need these to compile

## Priority 1: Heavily used, well-defined APIs

### `compiler/frontend/primitives/core/syscall_core.runa`
**Used by 7 files** (all compiler/internal utilities)
Required procs:
- `proc syscall_1 from Syscall`
- `proc syscall_2 from Syscall`
- `proc syscall_3 from Syscall`
- `proc syscall_4 from Syscall`
- `proc syscall_6 from Syscall`

Importers:
- `compiler/internal/arena_utils.runa`
- `compiler/internal/buffer_utils.runa`
- `compiler/internal/file_utils.runa`
- `compiler/internal/hash_utils.runa`
- `compiler/internal/memory_debug.runa`
- `compiler/internal/owned_utils.runa`
- `compiler/internal/time_utils.runa`

Note: Platform-specific syscall files already exist at `compiler/frontend/primitives/platform/<platform>/syscall.runa` and `compiler/frontend/primitives/assembly/syscall.runa`. This module may be a thin dispatcher, or these callers should import the platform one directly.

---

### `compiler/frontend/primitives/io/file_io.runa`
**Used by 6 files** (import system + one backend)
Required procs:
- `proc read_file from FileIO`
- `proc write_file from FileIO`
- `proc write_string_to_file from FileIO`
- `proc copy_file from FileIO`
- `proc copy_directory from FileIO`
- `proc create_directory_recursive from FileIO`
- `proc delete_file from FileIO`
- `proc delete_directory from FileIO`
- `proc directory_exists from FileIO`
- `proc get_temp_dir from FileIO`

Importers:
- `compiler/frontend/import_system/cache.runa`
- `compiler/frontend/import_system/hot_reload.runa`
- `compiler/frontend/import_system/parallel.runa`
- `compiler/frontend/import_system/remote.runa`
- `compiler/frontend/import_system/resolution.runa`
- `compiler/middle/gungnir/hir/translation/backends/fsharp/hir_to_fsharp.runa`

Note: See `compiler/frontend/primitives/io/io_core.runa`, `file_metadata.runa` — these may already have some of these procs. Check if `FileIO` alias should point at `io_core.runa`.

---

### `compiler/frontend/primitives/io/file.runa`
**Used by 8 test files** (translation test harnesses)
Required procs:
- `proc read_file from File`

Importers: `compiler/middle/gungnir/hir/translation/tests/csharp/*`, `css/*`, `html/*`, `jsx/*`, `mongodb/*`

Note: Could be a thin wrapper over `io_core.runa` or a redirect. Single function is trivial.

---

## Priority 2: Specialized primitives

### `compiler/frontend/primitives/threading/posix_threads.runa`
**Used by 1 file:** `compiler/frontend/import_system/parallel.runa`
Required procs (extensive POSIX thread + atomic API):
- `proc pthread_cond_create from PThreads`
- `proc pthread_cond_destroy from PThreads`
- `proc pthread_cond_signal from PThreads`
- `proc pthread_cond_broadcast from PThreads`
- `proc atomic_counter_create from PThreads`
- `proc atomic_get from PThreads`
- `proc atomic_increment from PThreads`
- `proc get_nproc from PThreads`
- (probably more: pthread_create/join/mutex — search the file)

Note: Existing `compiler/frontend/primitives/threading/thread_core.runa` and `sync_core.runa` may already implement some of these. Consider renaming to match or creating a posix-specific wrapper.

---

### `compiler/frontend/primitives/process/threading.runa`
**Used by 1 file:** `compiler/frontend/import_system/hot_reload.runa`
Required procs:
- `proc pthread_create from PThreads`
- `proc pthread_join from PThreads`

Note: Overlaps with `posix_threads.runa` above. May consolidate into one module.

---

### `compiler/frontend/primitives/network/tcp_sockets.runa`
**Used by 1 file:** `compiler/frontend/import_system/remote.runa`
Required procs:
- `proc tcp_connect from TCP`
- `proc tcp_send from TCP`
- `proc tcp_receive_all from TCP`
- `proc tcp_close from TCP`

Note: Network primitives module needs to be designed. Minimal surface for `remote.runa` to pull packages over the wire.

---

### `compiler/frontend/primitives/process/process.runa`
**Used by 2 files:** analytics, hot_reload
Required procs:
- `proc syscall2 from ProcessModule`
- `proc sleep_milliseconds from ProcessModule`

### `compiler/frontend/primitives/system/process.runa`
**Used by 1 file:** remote.runa
Required procs:
- `proc execute_command from ProcessModule`
- `proc sleep_milliseconds from ProcessModule`

Note: These two overlap. Could be one `process_primitives.runa` module.

---

### `compiler/frontend/primitives/char_core.runa`
**Used by 2 files:** dockerfile_lexer, lua_lexer
Usage:
- Imported `as CharCore` but no `proc X from CharCore` calls found in grep — may be accessed via `CharCore.CONSTANT` style (constant table).

Note: Possibly a redirect to `compiler/frontend/primitives/types/ascii_conversion.runa` or a character-classification helper. Check importer files to confirm what they expect.

---

## Priority 3: Low-use or unclear

### `compiler/frontend/primitives/testing/test_framework.runa`
**Used by 1 file:** `compiler/middle/gungnir/hir/translation/tests/fsharp_tests.runa`
Usage: No `proc X from TestFramework` calls grep'd — may use `TestFramework.CONSTANT` or not use at all.
Note: If the import is unused, it can be deleted. If actually used, needs a minimal test framework.

---

### `compiler/internal/unicode_tables.runa`
**Used by 1 file:** `compiler/internal/string_utils.runa`
Usage: No grep'd calls — may be used as data tables (constants) by string_utils for character classification.
Note: Could be a large data file (Unicode category tables). Implementation is mostly tables, not logic.

---

### `../emitter_common.runa` (relative path, unresolvable)
**Used by 1 file:** `compiler/middle/gungnir/hir/translation/backends/julia/hir_to_julia.runa`
The path resolves to `compiler/middle/gungnir/hir/translation/backends/emitter_common.runa` which doesn't exist.
Note: Could be a common utility shared across all backends. If so, creating it would also benefit other backends (currently each emitter has its own utilities).

---

## Recommendations

**Quick path to full compilation (in priority order):**

1. **Resolve `file_io.runa`** — Point all `as FileIO` imports to existing `io_core.runa` if it already has these procs, else extend `io_core.runa`. Big impact: 6 files.
2. **Resolve `syscall_core.runa`** — Point all `as Syscall` imports to `assembly/syscall.runa` or platform-specific. Big impact: 7 files.
3. **Create `file.runa`** — Trivial wrapper for `read_file`. Unblocks 8 test files.
4. **Decide on `char_core.runa`** — Either redirect to existing `ascii_conversion.runa` or create minimal char-class module.
5. **Remove unused imports** — `testing/test_framework.runa` and `unicode_tables.runa` appear unused; verify and delete the imports.
6. **Networking/process/threading** — These are larger design decisions. Consider whether v0.0.8.5 needs them or if the files importing them can be disabled temporarily.
