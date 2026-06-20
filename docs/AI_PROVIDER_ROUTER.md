# AI Provider Router

Phase 4 makes provider routing operational instead of a simple mock.

## Provider order

1. Groq
2. NVIDIA NIM
3. OpenRouter
4. Local Qwen
5. Local Llama

## Runtime behavior

- Providers are sorted by priority and cost weight.
- Quota exhaustion removes a provider from consideration.
- Rate limiting is tracked per provider over a one-minute window.
- Circuit breaker state opens after repeated failures and cools down before retry.
- Usage events record provider, task, token counts, estimated cost, latency, success, and errors.
- The transport layer is injectable so production can use real HTTP clients while tests use deterministic local transports.

## Production integration path

The current `SimulatedProviderTransport` should be replaced by provider-specific transports for Groq, NVIDIA NIM, OpenRouter, and local OpenAI-compatible inference servers. The router contract remains the same: `generate(prompt, task)` returns provider, model, text, token counts, and estimated cost.
