**Generate a Java program** that replicates the API calls found in the traffic. The following are guidelines — use your judgment on what's appropriate for the specific API:

- Use `java.net.http.HttpClient` (built into the JDK since 11) for requests — no HTTP library dependency needed
- Use Gson for JSON parsing/serialization — the one dependency this needs, since the JDK has no built-in JSON support
- Create a minimal Maven project (`pom.xml`) with the Gson dependency and the `exec-maven-plugin`, so the client runs with a single command and no extra flags. A conventional Maven layout only compiles `src/main/java`, but `{client_filename}` is saved at the project root (see below) — override the build's `<sourceDirectory>` to `.` (project root) in the POM so `mvn compile` actually finds and compiles it
- Configure `exec-maven-plugin` for the `exec:exec` goal with exactly this configuration — do not use the `exec:java` goal or `<mainClass>`: `exec:java` invokes `main` reflectively in-process, which fails on the package-private `ApiClient` class described below ("symbolic reference class is not accessible"), while `exec:exec` spawns a real `java` process, and its `<classpath/>` element expands to the full dependency classpath with the correct platform-specific separator (`:` on macOS/Linux, `;` on Windows):

  ```xml
  <plugin>
      <groupId>org.codehaus.mojo</groupId>
      <artifactId>exec-maven-plugin</artifactId>
      <version>3.1.0</version>
      <configuration>
          <executable>java</executable>
          <arguments>
              <argument>-classpath</argument>
              <classpath/>
              <argument>ApiClient</argument>
          </arguments>
      </configuration>
  </plugin>
  ```
- Create a separate method for each distinct API endpoint, with a small class for its response shape
- Reuse one `HttpClient` instance across requests rather than creating a new one per call
- Include a `main` method with example usage
- The output file is named `{client_filename}` (lowercase with underscores), so name the top-level class holding `main` exactly `ApiClient`, declared package-private, *without* the `public` modifier — a `public` class's filename must exactly match its class name, and this generator's file naming convention doesn't follow Java's usual PascalCase file naming. A package-private top-level class compiles and runs identically; it just isn't visible from other packages, which this single-file client has no need for.

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
Save the Maven project file to: `{scripts_dir}/pom.xml`
