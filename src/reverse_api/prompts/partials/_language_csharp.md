**Generate a C# program** that replicates the API calls found in the traffic. The following are guidelines — use your judgment on what's appropriate for the specific API:

- Use `System.Net.Http.HttpClient` and `System.Text.Json` — both are part of the .NET base class library (available since .NET Core 3.0), so no external NuGet package is needed for HTTP or JSON
- Create a minimal project file (`.csproj`) so the program can be run with a single command. Target `net8.0` by default, but this only works if that SDK/runtime is actually installed — if `dotnet run` reports the target framework isn't supported or the required runtime isn't installed, change `<TargetFramework>` to match what's actually there (check `dotnet --version`; a machine with only a newer SDK needs a higher target like `net10.0`, an older one a lower target like `net6.0`) and retry; both libraries above work fine on any of these versions, only the project file's stated target needs to match the installed SDK
- Create a separate method for each distinct API endpoint, with a small record or class for its response shape
- Reuse one `HttpClient` instance across requests rather than creating a new one per call
- Include a `Main` method with example usage

**Authentication & credentials:**
- Treat cookies, bearer tokens, session IDs, API keys, and CSRF values from captured traffic as secrets. Never copy their literal values into generated source, documentation, examples, command output, or logs.
- Preserve the observed authentication scheme, but read each required value from a clearly named environment variable using the language's standard library (for example, `RAE_AUTHORIZATION`, `RAE_SESSION_COOKIE`, or `RAE_API_KEY`). Do not add a dotenv/config dependency just for this.
- If a required variable is missing, fail with a concise message naming the variable, without printing its value. Document the required variable names and how to set them in the generated README; use placeholders only.
- Keep unauthenticated clients zero-configuration. Use the language's cookie jar/session where appropriate, but do not persist captured cookie values. Implement token refresh only when the captured traffic shows a supported refresh flow.

**Testing:**
- Run: `{run_command}`
- You have up to 5 attempts to fix issues

Save the program to: `{scripts_dir}/{client_filename}`
Save documentation to: `{scripts_dir}/README.md`
Save the project file to: `{scripts_dir}/ApiClient.csproj`
