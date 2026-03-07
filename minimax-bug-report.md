### Bug Report: MiniMax Integration Fails Due to Hardcoded `-chat` Suffix in `openai-completions` Adapter

**System Information:**
- **OpenClaw Version:** (Please insert version if known)
- **Host OS:** macOS 25.3.0 (arm64)
- **Provider:** MiniMax (`https://api.minimax.io/v1`)

**Describe the Bug:**
When configuring MiniMax as a custom OpenAI-compatible provider (`api: "openai-completions"`), the adapter appears to incorrectly append a `-chat` suffix to the model ID, causing valid model names to be rejected by the API.

**Steps to Reproduce:**

1.  **Configure Custom Provider:**
    Set up a custom provider in `openclaw.json` as follows:
    ```json
    "minimax-custom": {
      "baseUrl": "https://api.minimax.io/v1",
      "apiKey": "YOUR_MINIMAX_API_KEY",
      "api": "openai-completions",
      "models": [
        {
          "id": "abab6.5", 
          "name": "MiniMax abab 6.5 (Custom)"
        }
      ]
    }
    ```

2.  **Verify API Connectivity:**
    A direct `curl` request to the MiniMax API (e.g., for model listing, which fails with 404, or a direct chat completion) confirms that the `baseUrl` and API key are correct and the service is reachable.

3.  **Spawn Sub-Agent (Attempt 1):**
    Attempt to spawn a sub-agent using a model name known to be incorrect according to the API, but which matches the pattern OpenClaw seems to enforce:
    - **Command:** `sessions_spawn(model="minimax-custom/abab6.5-chat", ...)`
    - **Result:** `HTTP 400: invalid params, unknown model 'abab6.5-chat'`

4.  **Spawn Sub-Agent (Attempt 2):**
    Attempt to spawn a sub-agent using the *correct* model name (`abab6.5`):
    - **Command:** `sessions_spawn(model="minimax-custom/abab6.5", ...)`
    - **Result:** `HTTP 400: invalid params, unknown model 'abab6.5-chat'`. 

**Expected Behavior:**
The second spawn attempt should succeed, as it uses the correct model ID (`abab6.5`).

**Actual Behavior:**
The system fails with the same error in both cases, indicating that even when `abab6.5` is provided, the adapter internally modifies it to `abab6.5-chat` before sending the request to the MiniMax API, which then correctly rejects the unknown model name.

**Conclusion:**
This appears to be a bug in the `openai-completions` adapter where it incorrectly assumes all models should have a `-chat` suffix, making it impossible to use providers like MiniMax that do not follow this naming convention.
