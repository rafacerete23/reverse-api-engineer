**Generate a Ruby script** that replicates the API calls found in the traffic. The following are guidelines — use your judgment on what's appropriate for the specific API:

- Use `net/http` and `json` for requests and JSON — both are part of Ruby's standard library, so no gem/Bundler dependency is needed
- Reuse persistent connections (`Net::HTTP.start` held open across calls) rather than opening a new connection per request — use a separate connection per distinct scheme/host/port, since one is bound to a single origin and captured traffic may span several (e.g. separate login, API, and upload hosts)
- Create a separate method for each distinct API endpoint
- Include example usage at the bottom of the script

**Authentication & credentials:**
- Treat cookies, bearer tokens, session IDs, API keys, and CSRF values from captured traffic as secrets. Never copy their literal values into generated source, documentation, examples, command output, or logs.
- Preserve the observed authentication scheme, but read each required value from a clearly named environment variable using the language's standard library (for example, `RAE_AUTHORIZATION`, `RAE_SESSION_COOKIE`, or `RAE_API_KEY`). Do not add a dotenv/config dependency just for this.
- If a required variable is missing, fail with a concise message naming the variable, without printing its value. Document the required variable names and how to set them in the generated README; use placeholders only.
- Keep unauthenticated clients zero-configuration. Use the language's cookie jar/session where appropriate, but do not persist captured cookie values. Implement token refresh only when the captured traffic shows a supported refresh flow.

**Testing:**
- Run: `{run_command}`
- You have up to 5 attempts to fix issues

Save the script to: `{scripts_dir}/{client_filename}`
Save documentation to: `{scripts_dir}/README.md`
