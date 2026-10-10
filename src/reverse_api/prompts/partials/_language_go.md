**Generate a Go program** that replicates the API calls found in the traffic. The following are guidelines — use your judgment on what's appropriate for the specific API:

- Prefer the standard library (`net/http`, `encoding/json`) — a single-file program with no external dependencies is the default; only introduce a module and third-party packages if the API genuinely needs something the standard library doesn't provide (e.g. a specific auth scheme's signing library)
- Reuse one `*http.Client` (with cookie jar if the API relies on cookies) across requests rather than creating a new one per call
- Create a separate function for each distinct API endpoint, with a typed struct for its response shape
- Return errors rather than panicking; wrap them with context (`fmt.Errorf("...: %w", err)`)
- Include a `main` function with example usage

**Authentication & credentials:**
- Treat cookies, bearer tokens, session IDs, API keys, and CSRF values from captured traffic as secrets. Never copy their literal values into generated source, documentation, examples, command output, or logs.
- Preserve the observed authentication scheme, but read each required value from a clearly named environment variable using the language's standard library (for example, `RAE_AUTHORIZATION`, `RAE_SESSION_COOKIE`, or `RAE_API_KEY`). Do not add a dotenv/config dependency just for this.
- If a required variable is missing, fail with a concise message naming the variable, without printing its value. Document the required variable names and how to set them in the generated README; use placeholders only.
- Keep unauthenticated clients zero-configuration. Use the language's cookie jar/session where appropriate, but do not persist captured cookie values. Implement token refresh only when the captured traffic shows a supported refresh flow.

**Testing:**
- If a module was initialized, first run: `go mod tidy`
- Format the code with: `gofmt -w {client_filename}`
- Run with: `{run_command}`
- You have up to 5 attempts to fix issues

Save the program to: `{scripts_dir}/{client_filename}`
Save documentation to: `{scripts_dir}/README.md`
If external dependencies are used, save the module files: `{scripts_dir}/go.mod` and `{scripts_dir}/go.sum`
