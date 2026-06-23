# Runa Import System — Status & Plan

> **Honesty note (2026-06-23):** This file previously contained aspirational marketing
> copy ("most advanced import system ever created") with **fabricated benchmarks**
> (e.g. "8× faster than Rust", "95% cache hit ratio") describing features that are not
> implemented or not wired into the compiler. That content has been removed. This document
> now states what is **actually built and on the live compile path**, what exists as
> **unwired/partial source**, and the **committed plan** to complete the system to zero
> technical debt. No performance number appears here unless it was measured; none have been
> measured yet, so none are stated.

---

## 1. What actually works today (verified, on the live compile path)

The compiler's real import path is `compiler/driver/compiler_driver.runa`:
`process_imports` → `process_imports_into`. For each `Import "<path>" as <Alias>` it:

1. Resolves the path to a local source file.
2. Reads the file (`read_file_internal` → `runtime_read_file`).
3. Parses it.
4. Recursively **merges** the imported module's declarations into the root program under a
   flat namespace, with a visited-set for cycle detection / de-duplication and a
   platform-skip gate for per-arch sources.

This local-file, flat-merge resolver is what all 150 compiler modules use, and it works.
Module-qualified references (`Module.fn(args)`, `name from Module`) are carried as the plain
name plus a module-alias tag and resolved at the mangling/resolution stage.

**That is the entirety of the functional import system right now.** It is enough to compile
the compiler itself and local Runa projects.

## 2. What exists as source but is NOT functional / NOT wired in

These files exist and (mostly) compile, but the live driver does **not** call them, and
several are blocked on missing dependencies:

| Area | File(s) | Real status |
|------|---------|-------------|
| Remote fetch (HTTP/HTTPS) | `import_system/remote.runa` | HTTP-over-TCP partially coded; **HTTPS returns 0 — "BLOCKED on TLS implementation"** |
| Git / registry imports | `remote.runa`, `analytics.runa` | URL-shape detection only; no working fetch (needs TLS) |
| Parallel import workers | `driver/import_driver.runa` | Field plumbing exists; **not invoked by the live driver**; unverified |
| Caching / hot reload | `import_driver.runa` | Field plumbing exists; not invoked; unverified |
| Security validation | `import_system/security.runa` | Not on live path; unverified end-to-end |
| Analytics / profiling | `import_system/analytics.runa` | Not on live path; unverified |
| PQ / classical crypto | `import_system/crypto/**` | **Real and compiling** (sha2/sha3, x25519/x448, ml_kem, ml_dsa, slh_dsa, falcon, x509, trust_store) — these are the building blocks TLS will consume |

The headline dependency: **there is no TLS stack.** The crypto *primitives* are built, but the
TLS record layer, 1.3 handshake state machine, and certificate-chain verification (wired to
`trust_store`) do not exist. Until they do, no secure remote/git/registry import can function.

## 3. The committed target (zero technical debt)

The import system **will** deliver the full feature set — universal resolution (local /
package / URL / git / registry), parallel processing, caching, hot reload, security
validation, and analytics — done completely and verified end-to-end. This is a committed
0.0.8.5-era workstream, sequenced after the modular compiler self-hosts and the memory model
(Arena/Shared/ARC) is completed. Definition of done:

1. **Mechanism complete in the driver:** resolve the `import_driver` vs `process_imports`
   fork — one canonical, fully-wired live path; no dead/parallel import driver.
2. **TLS built** (on the existing crypto): record layer + TLS 1.3 handshake + X.509 chain
   verification against `trust_store`. Security-critical → gets a dedicated design review
   before implementation.
3. **Remote / git / registry fetch** working over TLS, signature-verified, proven by a real
   test that imports a remote module end-to-end (fetch → verify → compile → run).
4. **Parallel / cache / hot-reload / security / analytics** each implemented, wired into the
   live path, and covered by functional tests.
5. **This document rewritten** to describe shipped behavior, with **measured** benchmarks
   (real comparisons or none).

Tracking: see `docs/dev/DEVELOPMENT_ROADMAP.md` and the corresponding `RUNA-DECISIONS.md`
entry for the phased breakdown and ordering.

---

**Copyright 2025 Sybertnetics Artificial Intelligence Solutions. All rights reserved.**
