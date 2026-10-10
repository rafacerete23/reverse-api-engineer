**Generate a Python script** using `requests` that replicates the API calls found in the traffic. The following are guidelines — use your judgment on what's appropriate for the specific API:

- Prefer `requests` with a `Session` for connection reuse and cookie persistence
- Create separate functions for each distinct API endpoint
- Include type hints, docstrings, and error handling where they add clarity
- Include a `main` section with example usage

**Authentication & credentials:**
- Treat cookies, bearer tokens, session IDs, API keys, and CSRF values from captured traffic as secrets. Never copy their literal values into generated source, documentation, examples, command output, or logs.
- Preserve the observed authentication scheme, but read each required value from a clearly named environment variable using the language's standard library (for example, `RAE_AUTHORIZATION`, `RAE_SESSION_COOKIE`, or `RAE_API_KEY`). Do not add a dotenv/config dependency just for this.
- If a required variable is missing, fail with a concise message naming the variable, without printing its value. Document the required variable names and how to set them in the generated README; use placeholders only.
- Keep unauthenticated clients zero-configuration. Use the language's cookie jar/session where appropriate, but do not persist captured cookie values. Implement token refresh only when the captured traffic shows a supported refresh flow.

**Bot detection:**
- If you encounter bot detection or anti-scraping measures, first try `httpcloak` to cloak your HTTP fingerprint (TLS, HTTP/2, header order)
- If `httpcloak` cannot bypass the protection, fall back to making fetch requests through the browser via Playwright CDP
- As a last resort, use full Playwright browser automation

**Testing:**
- After generating the code, test it: `{run_command}`
- You have up to 5 attempts to fix issues

Save the script to: `{scripts_dir}/{client_filename}`
Save documentation to: `{scripts_dir}/README.md`
