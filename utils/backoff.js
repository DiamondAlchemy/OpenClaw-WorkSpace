/**
 * Executes an async function with exponential backoff for rate limit errors (429).
 *
 * @param {Function} fn - The async function to execute.
 * @param {number} [maxRetries=5] - Maximum number of retry attempts.
 * @returns {Promise<any>} - The result of the function execution.
 * @throws {Error} - Re-throws error if retries exhausted or error is not rate-limit related.
 */
async function callWithBackoff(fn, maxRetries = 5) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i < maxRetries - 1 && /rate.limit|429/i.test(e.message)) {
        const wait = Math.pow(2, i) * 1000 + Math.random() * 1000;
        console.log(`Rate limited. Waiting ${(wait / 1000).toFixed(1)}s...`);
        await new Promise((r) => setTimeout(r, wait));
      } else {
        throw e;
      }
    }
  }
}

module.exports = { callWithBackoff };
