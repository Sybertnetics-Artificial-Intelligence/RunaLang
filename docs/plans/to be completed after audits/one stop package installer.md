### **The Solution: A Unified Installer Script with Platform Detection**

We will not offer different `.exe`, `.dmg`, or `.deb` files directly on your main download page. Instead, we will provide a single, simple, and memorable command that users can paste into their terminal. This is the modern standard for developer tools (used by Rust, Deno, Homebrew, and countless others).

#### **The User Experience**

A user goes to our website, `runalang.org`, and clicks "Install." They are presented with a single, copy-pasteable command:

```bash
# For Linux and macOS
curl --proto '=https' --tlsv1.2 -sSf https://install.runalang.org | sh

# For Windows (PowerShell)
irm https://install.runalang.org -useb | iex
```

That's it. The user doesn't need to know their OS, their CPU architecture, or anything else. The script handles everything.

---

### **How It Works Under the Hood**

The `install.runalang.org` URL doesn't point to a file. It points to a small, intelligent **installer script** that runs on your server. This script's job is to be a "smart dispatcher."

Here's the step-by-step process:

1.  **User Runs the Command:** The user's terminal contacts `install.runalang.org`.
2.  **Server-Side Platform Detection:** Your server inspects the incoming HTTP request headers. The `User-Agent` header contains information about the user's operating system (Linux, macOS, Windows) and CPU architecture (x86_64, arm64/aarch64 for Apple Silicon, etc.).
3.  **The "Dispatcher" Script:** Based on this detected information, your server dynamically does the following:
    *   **If it detects macOS on an Apple Silicon (arm64) Mac:** It serves a shell script that knows to download the `runa-aarch64-apple-darwin.tar.gz` package.
    *   **If it detects Linux on a standard Intel/AMD (x86_64) machine:** It serves a shell script that downloads the `runa-x86_64-unknown-linux-gnu.tar.gz` package.
    *   **If it detects a request from Windows PowerShell:** It serves a PowerShell script (`.ps1`) that downloads the `runa-x86_64-pc-windows-msvc.zip` package.
4.  **The Client-Side Installation:** The script that gets downloaded to the user's machine is now platform-specific. Its job is to:
    *   Download the correct, pre-compiled binary package for their exact system.
    *   Unzip/untar the package into a standard location (e.g., `~/.runa/`).
    *   Update the user's system `PATH` environment variable so they can immediately type `runa` in their terminal from any directory.
    *   Run a final `runa --version` command to verify that the installation was successful.

### **The Required Build Artifacts**

To make this work, our CI/CD (Continuous Integration/Continuous Deployment) pipeline needs to produce a pre-compiled, self-contained binary package for every supported platform and architecture. These are the "different packages" we asked about, but they are an implementation detail hidden from the user.

Our CI pipeline (e.g., using GitHub Actions) will have a build matrix that looks something like this:

| Operating System | CPU Architecture | Package Name                             |
| :--------------- | :--------------- | :--------------------------------------- |
| `ubuntu-latest`  | `x86_64`         | `runa-x86_64-unknown-linux-gnu.tar.gz`   |
| `macos-latest`   | `x86_64`         | `runa-x86_64-apple-darwin.tar.gz`        |
| `macos-latest`   | `arm64`          | `runa-aarch64-apple-darwin.tar.gz`       |
| `windows-latest` | `x86_64`         | `runa-x86_64-pc-windows-msvc.zip`        |

Each of these packages will be uploaded to a central location (like a cloud storage bucket or your GitHub Releases page) where the installer script can find them.

---

### **Runa's Own Toolchain Manager**

This initial installation is just the beginning. The `runa` executable itself should come with a built-in toolchain manager to handle updates.

*   `runa upgrade`: This command will automatically check for a new version of Runa, download the correct package for the user's platform, and replace the current installation.
*   `runa toolchain install <version>`: This allows advanced users to install and switch between different versions of the Runa compiler (e.g., the stable, beta, and nightly channels).

This is exactly how Rust's `rustup` works, and it is the gold standard for developer-focused language distribution.

**Conclusion:**

We are correct that we need **different packages** for different platforms. However, we should **not** expose this complexity to the user.

The solution is a **single, unified installation command** that points to a smart, server-side script. This script detects the user's platform and delivers the correct binary package, providing a seamless and professional installation experience that works identically for everyone, everywhere.