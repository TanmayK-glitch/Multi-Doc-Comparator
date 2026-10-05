# Claude API Rate Limits

## Overview

To mitigate misuse and manage capacity on the API, Anthropic places limits on how much an organization can use the Claude API.

### Claude Platform on AWS

The rate limits described on this page also apply to Claude Platform on AWS, but billing and limit management differ:

- Billing is through AWS Marketplace rather than Anthropic credit purchases.
- Organizations on Claude Platform on AWS are placed on the **Start** tier.
- Organizations can move to a higher tier automatically as they build a history of paid AWS Marketplace invoices.
- To request higher limits, contact an Anthropic account representative or [Anthropic Support](https://support.claude.com/).
- The **Request rate limit increase** flow is not available for Claude Platform on AWS.
- Per-workspace rate-limit configuration is not available on Claude Platform on AWS.
- Fast mode is not available on Claude Platform on AWS.
- See [Rate limits and quotas on Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas) for platform-specific details.

## Types of Limits

There are two primary types of API usage limits:

1. **Spend limits** — set a maximum monthly cost an organization can incur for API usage.
2. **Rate limits** — set the maximum number of API requests and tokens an organization can use over a defined period.

The API enforces service-configured limits at the organization level. Organizations can also configure lower limits for individual workspaces.

---

# About Rate Limits

- Limits are designed to prevent API abuse while minimizing impact on common customer usage patterns.
- Limits are defined by **usage tier**.
- Organizations are automatically placed into a tier based on usage history and account standing.
- Organizations can move to higher tiers over time as they use the API.
- New organizations and organizations with limited usage history may initially be placed in the **Evaluation** tier.
- Evaluation-tier limits can be lower than the standard limits shown on this page while account history is established.
- These initial limits help Anthropic prevent fraud and abuse and increase automatically as the organization builds usage history.
- Organization tier and current limits can be viewed on the [Rate limits](https://platform.claude.com/settings/limits) page in the [Claude Console](https://platform.claude.com/).
- Limits can be enforced over shorter time intervals than the displayed per-minute rate. For example, a limit of 60 RPM may effectively be enforced as approximately 1 request per second. Short bursts can therefore exceed the effective rate and trigger rate-limit errors.
- The limits documented here are standard limits for each tier. Higher limits can be requested where supported.
- The API uses the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket) for rate limiting.
  - Capacity is continuously replenished up to the maximum limit.
  - Limits are not reset only at fixed time boundaries.
- Rate limits represent **maximum allowed usage**, not guaranteed minimum capacity.
- These limits help reduce unintentional overspend and promote fair distribution of resources among users.

---

# Spend Limits

### Claude Platform on AWS

The same monthly spend caps apply to Claude Platform on AWS, and API requests stop when the cap is reached. Billing and tier increases work differently on AWS. See [Spend limits on Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#spend-limits).

Each of the Start, Build, and Scale tiers has a monthly spend cap. This is the maximum amount an organization can spend on the API during a calendar month.

The organization's monthly spend cap and configurable spend limit can be viewed on the [Billing](https://platform.claude.com/settings/billing) page.

| Usage tier | Monthly spend cap |
|---|---:|
| Start | $500 USD |
| Build | $1,000 USD |
| Scale | $200,000 USD |
| Custom | No monthly spend cap; limits are arranged with the account team |

## Reaching the Spend Cap

Once an organization reaches its tier's spend cap:

- API usage pauses until **00:00 UTC on the first day of the next month**, unless a higher limit is requested sooner.
- API requests made while usage is paused return **HTTP 429**.
- The error type is `rate_limit_error`.
- The response does **not** include a `retry-after` header.
- Retrying the request, including automatic SDK retries, fails until API access resumes.
- On the Messages API, `error.details.error_code` is `enforced_spend_limit_reached`.
- This error code distinguishes a spend-cap response from an ordinary rate-limit response.
- Moving to a higher usage tier restores access.

### Example Spend-Cap Error

```json
{
  "type": "error",
  "error": {
    "type": "rate_limit_error",
    "message": "You have reached your API usage limits: your organization has crossed its monthly API usage threshold, set based on your organization's API tier. You will regain access on 2026-09-01 at 00:00 UTC.",
    "details": { "error_code": "enforced_spend_limit_reached" }
  },
  "request_id": "req_018EeWyXxfu5pfWkrYcMdjWG"
}
```

See [Requesting higher limits](https://platform.claude.com/docs/en/api/rate-limits#requesting-higher-limits) for ways to restore access sooner.

## Setting a Custom Spend Limit

Organizations can set their own spend limit below the tier's maximum cap to control costs.

### Step 1: Navigate to Billing

Go to **Settings > Billing** in the Claude Console:

[Billing](https://platform.claude.com/settings/billing)

### Step 2: Open the Spend Limit Editor

In the **Spend limits** section, select:

- **Adjust limit**, or
- **Set limit** if no limit is currently configured.

### Step 3: Adjust the Spend Limit

Enter the desired value.

The configured spend limit cannot exceed the organization's current tier cap.

### Behavior When a Configured Spend Limit Is Reached

When usage reaches a custom organization or workspace spend limit:

- Requests return **HTTP 400**.
- The error type is `invalid_request_error`.
- For an organization limit, the message begins with:
  - `You have reached your specified API usage limits`
- For a workspace limit, the message begins with:
  - `You have reached your specified workspace API usage limits`
- The response states when access resumes.
- Raising or removing the configured limit can restore access sooner.

### Claude Code Workspace Exception

Limits on the [Claude Code workspace](https://platform.claude.com/docs/en/manage-claude/workspaces#claude-code-workspace) are checked separately.

Claude Code requests that exceed that workspace's limit can instead receive:

- HTTP `429`
- A `retry-after` header

---

# Rate Limits

The Messages API rate limits are measured separately for each model class using:

- **RPM** — requests per minute
- **ITPM** — input tokens per minute
- **OTPM** — output tokens per minute

If any rate limit is exceeded:

- The API returns **HTTP 429**.
- The response identifies the rate limit that was exceeded.
- The response includes a `retry-after` header indicating how long to wait before retrying.

## Acceleration Limits

Organizations may also encounter HTTP 429 errors because of **acceleration limits**.

These can occur when API usage increases sharply.

To reduce the likelihood of acceleration-limit errors:

- Ramp traffic up gradually.
- Maintain consistent usage patterns.
- Avoid sudden large increases in request volume.

---

# Cache-Aware ITPM

Many API providers use a combined tokens-per-minute limit that counts cached and uncached input and output tokens.

For **most Claude models**, only **uncached input tokens** count toward the ITPM rate limit.

This makes effective throughput substantially higher when prompt caching is used.

## What Counts Toward ITPM

| Token field | Description | Counts toward ITPM? |
|---|---|---|
| `input_tokens` | Tokens after the last cache breakpoint | Yes |
| `cache_creation_input_tokens` | Tokens being written to cache | Yes |
| `cache_read_input_tokens` | Tokens read from cache | No, for most models |

ITPM limits are estimated at the beginning of a request and adjusted during the request to reflect actual input-token usage.

## Understanding `input_tokens`

The `input_tokens` field does **not** represent all input tokens in the request.

It represents only tokens appearing **after the last cache breakpoint**.

Total input tokens can be calculated as:

```text
total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens
```

### Example

Suppose a request contains:

- A 200,000-token cached document.
- A 50-token user question.

The response may show:

```text
input_tokens: 50
```

even though the total input is:

```text
200,050 tokens
```

For rate-limit purposes on most models, only the uncached portions count:

```text
ITPM usage = input_tokens + cache_creation_input_tokens
```

Cached-read tokens do not count toward ITPM for most models.

## Effective Throughput Example

Suppose an organization has:

```text
ITPM limit = 2,000,000 tokens/minute
Cache hit rate = 80%
```

The organization could effectively process approximately:

```text
10,000,000 total input tokens/minute
```

This consists of:

- 2,000,000 uncached tokens that count toward the limit.
- 8,000,000 cached tokens that do not count toward the limit.

Therefore, prompt caching can substantially increase effective throughput without increasing the configured ITPM limit.

## Haiku 3.5 Exception

**Claude Haiku 3.5** is an exception.

For Haiku 3.5:

- `cache_read_input_tokens` also count toward ITPM.
- This is indicated by footnote 4 in the rate-limit table.

For other models, cached input tokens do not count toward rate limits and are billed at the cache-read rate.

## Recommended Caching Strategy

To maximize effective rate-limit capacity, cache repeated content such as:

- System instructions.
- Repeated prompts.
- Large context documents.
- Tool definitions.
- Conversation history.

See [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) for implementation guidance.

Organizations can monitor cache hit rates on the [Usage page](https://platform.claude.com/usage) and use that information to optimize caching.

---

# Output Token Rate Limits

OTPM rate limits are evaluated in real time as output tokens are generated.

Only the **actual tokens generated** count toward OTPM.

The `max_tokens` parameter does **not** factor into OTPM rate-limit calculations.

Therefore:

- Setting a higher `max_tokens` value does not itself consume additional OTPM capacity.
- Only tokens actually generated count toward the output-token limit.

---

# Model-Specific Rate Limits

Rate limits are applied separately for each model.

This means an organization can use different models simultaneously, with each model drawing from its respective rate limit.

Current rate limits can be viewed on the [Rate limits](https://platform.claude.com/settings/limits) page in the Claude Console.

Configured limits can also be retrieved programmatically through the [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api).

## `inference_geo` and Rate Limits

Rate limits are currently shared across all `inference_geo` values.

Requests using:

```json
"inference_geo": "us"
```

and:

```json
"inference_geo": "global"
```

draw from the same rate-limit pool.

## Standard Messages API Rate Limits

| Model | Maximum RPM | Maximum ITPM | Maximum OTPM |
|---|---:|---:|---:|
| Claude Fable 5.x¹ | 1,000 | 500,000 | 100,000 |
| Claude Opus 5.5 | 1,000 | 2,000,000 | 400,000 |
| Claude Opus 5 | 1,000 | 2,000,000 | 400,000 |
| Claude Opus 4.x² | 1,000 | 2,000,000 | 400,000 |
| Claude Sonnet 5.5 | 1,000 | 2,000,000 | 400,000 |
| Claude Sonnet 5 | 1,000 | 2,000,000 | 400,000 |
| Claude Sonnet 4.x³ | 1,000 | 2,000,000 | 400,000 |
| Claude Haiku 4.5 | 1,000 | 2,000,000 | 400,000 |
| Claude Haiku 3.5⁴ (retired, except on Bedrock and Google Cloud) | 1,000 | 100,000 | 20,000 |

### Rate-Limit Footnotes

**¹ Fable rate limit**

The Fable rate limit is a combined limit covering traffic across:

- Claude Fable 5.1
- Claude Fable 5

Claude Mythos 5.1 and Claude Mythos 5 have a separate combined limit under the same terms.

**² Opus 4.x rate limit**

The Opus 4.x rate limit is a combined limit covering:

- Claude Opus 4.8
- Claude Opus 4.7
- Claude Opus 4.6
- Claude Opus 4.5

Claude Opus 5.5 and Claude Opus 5 each have separate rate limits and are not part of this combined bucket.

**³ Sonnet 4.x rate limit**

The Sonnet 4.x rate limit is a combined limit covering:

- Claude Sonnet 4.6
- Claude Sonnet 4.5

Claude Sonnet 5.5 and Claude Sonnet 5 each have separate rate limits and are not part of this combined bucket.

**⁴ Haiku 3.5 ITPM**

For Haiku 3.5, `cache_read_input_tokens` count toward ITPM usage.

---

# Message Batches API Rate Limits

The Message Batches API has separate rate limits shared across all models.

These limits include:

- Requests per minute across API endpoints.
- Maximum number of batch requests simultaneously in the processing queue.
- Maximum number of requests contained in a single batch.

A **batch request** means an individual request that is part of a Message Batch.

A single Message Batch can contain thousands of batch requests. Each individual batch request counts toward the processing-queue limit while it has not yet been successfully processed by the model.

| Maximum RPM | Maximum batch requests in processing queue | Maximum batch requests per batch |
|---:|---:|---:|
| 1,000 | 200,000 | 100,000 |

---

# Managed Agents Rate Limits

[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) endpoints are rate-limited per organization.

These limits are separate from the Messages API limits.

| Operation | Limit |
|---|---:|
| Create endpoints, such as agents, sessions, and environments | 300 requests/minute |
| Read endpoints, such as retrieve, list, and stream | 1,200 requests/minute |

---

# Files API Rate Limits

The [Files API](https://platform.claude.com/docs/en/build-with-claude/files) has its own per-organization rate limit.

The limit is:

- Shared across upload, list, retrieve, download, and delete operations.
- Separate from the Messages API rate limits.

See [Files API rate limits](https://platform.claude.com/docs/en/build-with-claude/files#rate-limits) for the current value.

---

# Fast Mode Rate Limits

Fast mode is a **research preview** with dedicated rate limits.

When using:

```json
"speed": "fast"
```

with:

- Claude Opus 5.5
- Claude Opus 5
- Claude Opus 4.8

dedicated fast-mode rate limits apply.

These limits are separate from standard Opus rate limits.

## Fast Mode Rate-Limit Behavior

When fast-mode limits are exceeded:

- The API returns HTTP `429`.
- The response includes a `retry-after` header.
- The response includes `anthropic-fast-*` headers showing fast-mode rate-limit status.

See [Fast mode rate limits](https://platform.claude.com/docs/en/build-with-claude/fast-mode#rate-limits).

## Model Availability

### Claude Opus 4.7

Fast mode is **not available**.

Requests using fast mode with Opus 4.7 return an error.

### Claude Opus 4.6

Requests to `claude-opus-4-6` with:

```json
"speed": "fast"
```

run at **standard speed** rather than fast mode.

See [Fast mode supported models](https://platform.claude.com/docs/en/build-with-claude/fast-mode#supported-models).

---

# Monitoring Rate Limits in the Claude Console

Rate-limit usage can be monitored on the [Usage](https://platform.claude.com/usage) page of the [Claude Console](https://platform.claude.com/).

The Usage page provides:

- Token usage charts.
- Request usage charts.
- Rate-limit charts.
- Visibility into available headroom.
- Information that can help identify peak usage.
- Information useful when determining which limits to request.
- Information useful for improving cache rates.

## Rate Limit - Input Tokens Chart

The input-token rate-limit chart includes:

- Hourly maximum uncached input tokens per minute.
- Current input tokens per minute rate limit.
- Cache rate for input tokens, representing the percentage of input tokens read from cache.

## Rate Limit - Output Tokens Chart

The output-token rate-limit chart includes:

- Hourly maximum output tokens per minute.
- Current output tokens per minute rate limit.

---

# Requesting Higher Limits

For the standard Claude API:

- Higher rate limits can be requested from the **Rate limits** page in the Claude Console.
- Higher monthly spend caps can also be requested.
- Use **Request rate limit increase** on the [Rate limits](https://platform.claude.com/settings/limits) page.
- Anthropic Support can also raise limits.
- For urgent requests, contact [Anthropic Support](https://support.claude.com/).

## Claude Platform on AWS

The **Request rate limit increase** flow is not available for Claude Platform on AWS.

Instead:

- Contact an Anthropic account representative, or
- Contact [Anthropic Support](https://support.claude.com/).

When requesting higher AWS limits, include:

- The models requiring increased limits.
- Peak input tokens per minute for each model.
- Peak output tokens per minute for each model.
- Approximate percentage/share of input that is cached or repeated context.

See [Rate limits and quotas on Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas).

---

# Workspace Rate Limits

Organizations can configure lower spend and rate limits for individual workspaces.

Workspace limits can protect one workspace from excessive usage and preserve capacity for other workspaces.

## Example

Suppose an organization has:

```text
Organization ITPM = 40,000 tokens/minute
Organization OTPM = 8,000 tokens/minute
```

The organization could configure one workspace with:

```text
Workspace ITPM = 30,000 tokens/minute
```

This prevents that workspace from consuming the entire organization's input-token allowance.

Unused capacity can remain available to other workspaces.

## Workspace Limit Rules

- Limits cannot be set on the **default Workspace**.
- If a workspace limit is not configured, the workspace uses the organization's limit.
- Workspace limits are configured independently for each limiter type, such as:
  - Requests per minute.
  - Input tokens per minute.
  - Output tokens per minute.
- Organization-wide limits always apply.
- Workspace limits do not increase the organization's total capacity.
- Even if workspace limits add up to more than the organization's limit, the organization-wide limit remains the effective upper bound.

Current organization and workspace rate limits can be read programmatically through the [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api).

For general workspace information, see [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces).

---

# Response Headers

Claude API responses include headers describing:

- The rate limit currently enforced.
- Current remaining capacity.
- When the limit will be replenished.
- Priority Tier capacity where applicable.

## Rate-Limit Response Headers

| Header | Description |
|---|---|
| `retry-after` | Number of seconds to wait before retrying. Earlier retries will fail. This header is not sent with a spend-cap 429. |
| `anthropic-ratelimit-requests-limit` | Maximum number of requests allowed within the applicable rate-limit period. |
| `anthropic-ratelimit-requests-remaining` | Number of requests remaining before rate limiting occurs. |
| `anthropic-ratelimit-requests-reset` | Time when the request rate limit will be fully replenished, in RFC 3339 format. |
| `anthropic-ratelimit-tokens-limit` | Maximum number of tokens allowed within the applicable rate-limit period. |
| `anthropic-ratelimit-tokens-remaining` | Number of tokens remaining before rate limiting, rounded to the nearest thousand. |
| `anthropic-ratelimit-tokens-reset` | Time when the token rate limit will be fully replenished, in RFC 3339 format. |
| `anthropic-ratelimit-input-tokens-limit` | Maximum number of input tokens allowed within the applicable rate-limit period. |
| `anthropic-ratelimit-input-tokens-remaining` | Number of input tokens remaining before rate limiting, rounded to the nearest thousand. |
| `anthropic-ratelimit-input-tokens-reset` | Time when the input-token rate limit will be fully replenished, in RFC 3339 format. |
| `anthropic-ratelimit-output-tokens-limit` | Maximum number of output tokens allowed within the applicable rate-limit period. |
| `anthropic-ratelimit-output-tokens-remaining` | Number of output tokens remaining before rate limiting, rounded to the nearest thousand. |
| `anthropic-ratelimit-output-tokens-reset` | Time when the output-token rate limit will be fully replenished, in RFC 3339 format. |
| `anthropic-priority-input-tokens-limit` | Maximum number of Priority Tier input tokens allowed within the applicable rate-limit period. Priority Tier only. |
| `anthropic-priority-input-tokens-remaining` | Number of Priority Tier input tokens remaining before rate limiting, rounded to the nearest thousand. Priority Tier only. |
| `anthropic-priority-input-tokens-reset` | Time when the Priority Tier input-token rate limit will be fully replenished, in RFC 3339 format. Priority Tier only. |
| `anthropic-priority-output-tokens-limit` | Maximum number of Priority Tier output tokens allowed within the applicable rate-limit period. Priority Tier only. |
| `anthropic-priority-output-tokens-remaining` | Number of Priority Tier output tokens remaining before rate limiting, rounded to the nearest thousand. Priority Tier only. |
| `anthropic-priority-output-tokens-reset` | Time when the Priority Tier output-token rate limit will be fully replenished, in RFC 3339 format. Priority Tier only. |
| `anthropic-priority-output-tokens-reset` | Time when the Priority Tier output-token rate limit will be fully replenished, in RFC 3339 format. Priority Tier only. |

## Most Restrictive Token Limit

The `anthropic-ratelimit-tokens-*` headers show values for the **most restrictive token limit currently in effect**.

For example:

- If a workspace per-minute token limit is the current constraint, these headers show the workspace's per-minute token-rate-limit values.
- If workspace limits do not apply, the headers show the total tokens remaining.
- Total tokens means the combined input and output token capacity.

This behavior ensures that response headers expose the most relevant constraint affecting the current request.

## Identifying the Workspace

To determine which workspace a request was counted against, inspect the:

```text
anthropic-workspace-id
```

response header.

This header contains the ID of the workspace to which the API key or access token resolved.

See the [API response headers documentation](https://platform.claude.com/docs/en/api/overview#response-headers).

---

# Rate-Limit Error Handling Summary

| Situation | HTTP status | Error type / indicator | `retry-after` |
|---|---:|---|---|
| Standard rate limit exceeded | 429 | `rate_limit_error` | Yes |
| Acceleration limit exceeded | 429 | Rate-limit response | Yes |
| Monthly tier spend cap reached | 429 | `rate_limit_error` + `enforced_spend_limit_reached` | No |
| Custom organization/workspace spend limit reached | 400 | `invalid_request_error` | Not applicable |
| Fast mode rate limit exceeded | 429 | Fast-mode rate-limit response | Yes |

---

# Key Concepts for Implementations

When implementing a Claude API client, gateway, or middleware, the following distinctions are important:

1. **Do not treat every 429 identically.**
   - Standard rate-limit 429s include `retry-after`.
   - Spend-cap 429s do not include `retry-after` and contain `enforced_spend_limit_reached`.

2. **Respect `retry-after`.**
   - Retrying before the indicated time can fail again.

3. **Account for acceleration limits.**
   - Even when the nominal RPM/ITPM/OTPM limit appears sufficient, sudden traffic increases can cause 429 responses.

4. **Prompt caching can increase effective throughput.**
   - For most models, cached-read tokens do not count toward ITPM.
   - Cache repeated system instructions, documents, tools, and conversation context when appropriate.

5. **Model limits are independent.**
   - Separate models can be used concurrently within their respective limits.

6. **Workspace limits are lower bounds on allocation, not additional capacity.**
   - Organization-wide limits always remain effective.

7. **`max_tokens` does not consume OTPM merely by being set higher.**
   - OTPM is based on actual generated output tokens.

8. **`inference_geo` does not create separate rate-limit pools.**
   - `us` and `global` requests share the same rate-limit pool.

9. **Use response headers for runtime rate-limit state.**
   - Remaining capacity and reset timestamps can be used for adaptive client behavior.

10. **Use the Rate Limits API for programmatic configuration inspection.**
    - This allows applications and administrative tooling to inspect organization/workspace limits.

---

# Related Documentation

- [Rate Limits](https://platform.claude.com/docs/en/api/rate-limits)
- [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api)
- [Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws)
- [Rate Limits and Quotas on Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#rate-limits-and-quotas)
- [Fast Mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode)
- [Fast Mode Rate Limits](https://platform.claude.com/docs/en/build-with-claude/fast-mode#rate-limits)
- [Files API](https://platform.claude.com/docs/en/build-with-claude/files)
- [Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
- [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces)
- [Claude Console Rate Limits](https://platform.claude.com/settings/limits)
- [Claude Console Usage](https://platform.claude.com/usage)
- [Claude Console Billing](https://platform.claude.com/settings/billing)
- [Anthropic Support](https://support.claude.com/)
