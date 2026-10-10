**Generate a TypeScript module** that replicates the API calls found in the traffic. The following are guidelines — use your judgment:

- Use strict typing with interfaces for request/response types
- Use ESM modules and native `fetch` (Node.js 18+); use `axios` only if needed
- Create separate async functions for each endpoint
- Export a class-based API client with proper encapsulation
- Include example usage in a main section
- Generate a `package.json` with `"type": "module"`, `tsx`, `typescript`, `@types/node`

**Authentication & credentials:**
- Treat cookies, bearer tokens, session IDs, API keys, and CSRF values from captured traffic as secrets. Never copy their literal values into generated source, documentation, examples, command output, or logs.
- Preserve the observed authentication scheme, but read each required value from a clearly named environment variable using the language's standard library (for example, `RAE_AUTHORIZATION`, `RAE_SESSION_COOKIE`, or `RAE_API_KEY`). Do not add a dotenv/config dependency just for this.
- If a required variable is missing, fail with a concise message naming the variable, without printing its value. Document the required variable names and how to set them in the generated README; use placeholders only.
- Keep unauthenticated clients zero-configuration. Use the language's cookie jar/session where appropriate, but do not persist captured cookie values. Implement token refresh only when the captured traffic shows a supported refresh flow.

**Testing:**
- Run: `npm install && {run_command}`
- You have up to 5 attempts to fix issues

Save the module to: `{scripts_dir}/{client_filename}`
Save documentation to: `{scripts_dir}/README.md`
Save the package.json to: `{scripts_dir}/package.json`