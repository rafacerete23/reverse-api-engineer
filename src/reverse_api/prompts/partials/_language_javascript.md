**Generate a JavaScript module** that replicates the API calls found in the traffic. The following are guidelines — use your judgment:

- Use modern JavaScript (ES2022+) with ESM modules
- Prefer native `fetch` (Node.js 18+); use `axios` only if you need retries or interceptors
- Create separate async functions for each endpoint
- Add JSDoc comments and error handling where they add clarity
- Include example usage in a main section
- If using external deps, generate a `package.json` with `"type": "module"`

**Authentication & credentials:**
- Treat cookies, bearer tokens, session IDs, API keys, and CSRF values from captured traffic as secrets. Never copy their literal values into generated source, documentation, examples, command output, or logs.
- Preserve the observed authentication scheme, but read each required value from a clearly named environment variable using the language's standard library (for example, `RAE_AUTHORIZATION`, `RAE_SESSION_COOKIE`, or `RAE_API_KEY`). Do not add a dotenv/config dependency just for this.
- If a required variable is missing, fail with a concise message naming the variable, without printing its value. Document the required variable names and how to set them in the generated README; use placeholders only.
- Keep unauthenticated clients zero-configuration. Use the language's cookie jar/session where appropriate, but do not persist captured cookie values. Implement token refresh only when the captured traffic shows a supported refresh flow.

**Testing:**
- If `package.json` was generated, first run: `npm install`
- Run with: `{run_command}`
- You have up to 5 attempts to fix issues

Save the module to: `{scripts_dir}/{client_filename}`
Save documentation to: `{scripts_dir}/README.md`
If external dependencies are used, save: `{scripts_dir}/package.json`