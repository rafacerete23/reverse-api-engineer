**Generate a PHP script** that replicates the API calls found in the traffic. The following are guidelines — use your judgment on what's appropriate for the specific API:

- Use the `curl` extension (`curl_init`/`curl_exec`) for requests and `json_encode`/`json_decode` for JSON — no Composer dependency is needed for either. `ext-json` is bundled with PHP core and always available, but `ext-curl` is bundled-but-optional and isn't guaranteed enabled on every install — if `curl_init` isn't defined, install it with whatever package manager is available (e.g. `apt-get install -y php-curl`) before retrying
- Reuse one cURL handle across requests rather than creating a new one per call
- Create a separate function for each distinct API endpoint
- Include type declarations on function signatures where they add clarity
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
