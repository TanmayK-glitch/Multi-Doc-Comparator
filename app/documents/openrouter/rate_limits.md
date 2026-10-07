---

title: OpenRouter Rate Limits
topic: Rate Limits
provider: OpenRouter
scope: API request rate limits, free-model quotas, provider throttling, and 429 handling
----------------------------------------------------------------------------------------

# OpenRouter Rate Limits

## Overview

OpenRouter enforces limits that control how many requests an account can make.

There are two main categories of limits:

| Limit type    | What it controls                                                                                     | Error when exceeded          | Where to check                                        |
| ------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------- |
| Credit limits | How much can be spent, including account balance, per-key credit caps, and in-flight spending budget | HTTP `402 Payment Required`  | `GET /api/v1/key` and `error.metadata.limit_source`   |
| Rate limits   | How many requests can be made, including free-model request caps and DDoS protection                 | HTTP `429 Too Many Requests` | `X-RateLimit-*` headers on applicable error responses |

This document focuses on **rate limits**. Credit limits are separate from request-rate limits.

---

## Checking Rate-Limit Information

OpenRouter provides API-key information through:

```http
GET https://openrouter.ai/api/v1/key
```

The response includes information about free-model daily request usage:

```typescript
type Key = {
  data: {
    free_model_daily_requests: {
      used: number;
      limit: number;
      remaining: number;
    };
  };
};
```

### `free_model_daily_requests`

| Field       | Meaning                                                            |
| ----------- | ------------------------------------------------------------------ |
| `used`      | Number of free-model requests recorded during the current UTC day  |
| `limit`     | Number of free-model requests allowed during the current UTC day   |
| `remaining` | Number of free-model requests remaining during the current UTC day |

The daily counter is useful for monitoring free-model usage before requests begin failing.

The per-minute free-model limit is not reported in this response.

---

# Free-Model Rate Limits

OpenRouter applies specific request limits to **free model variants**.

A free model variant is identified by a model ID ending in:

```text
:free
```

The documented free-model limits are:

| All-time credits purchased | Requests per minute | Requests per day |
| -------------------------- | ------------------: | ---------------: |
| Less than 10 credits       |              20 RPM |           50 RPD |
| At least 10 credits        |              20 RPM |        1,000 RPD |

Where:

* **RPM** = requests per minute
* **RPD** = requests per day
* The daily limit is measured using the current **UTC day**.

### Free-model limit behavior

The `free_model_daily_requests` object returned by `GET /api/v1/key` reports the daily counter and ceiling when these limits apply.

Some accounts, endpoints, and BYOK requests may be exempt from free-model limits. In those cases, the reported `remaining` value reflects the applicable tier policy rather than necessarily representing an enforced request ceiling.

The per-minute limit is not included in the `GET /api/v1/key` response.

---

## Free-Model Credit Threshold

The free-model daily tier is based on **all-time credits purchased**.

The documented threshold is:

```text
10 credits
```

The higher daily limit is associated with accounts that have purchased at least the required amount of credits.

OpenRouter also notes that rounding and top-up fees can affect the reported tier around the threshold.

---

# DDoS Protection

OpenRouter also uses DDoS protection to prevent abusive or unreasonable request volumes.

Cloudflare's DDoS protection may block requests that **dramatically exceed reasonable usage**.

This can result in an HTTP:

```text
429 Too Many Requests
```

response.

DDoS protection is separate from the normal free-model request quotas.

---

# HTTP 429 Too Many Requests

A rate-limited request normally returns:

```json
{
  "error": {
    "code": 429,
    "message": "Rate limit exceeded",
    "metadata": {
      "error_type": "rate_limit_exceeded"
    }
  }
}
```

HTTP `429` indicates that the request was rate limited.

A `429` can originate from two different sources:

1. **OpenRouter platform limits**
2. **The upstream model provider**

---

## OpenRouter-Side Rate Limits

OpenRouter itself may return `429` when the request exceeds a platform-level limit, such as:

* Free-model requests per minute
* Free-model requests per day
* DDoS protection thresholds

When OpenRouter itself applies the rate limit, the response can include:

```text
X-RateLimit-Limit
X-RateLimit-Remaining
X-RateLimit-Reset
```

These headers describe the platform limit that was reached.

---

## Upstream Provider Rate Limits

The model provider serving the request may also return a rate-limit error.

This can happen when the upstream provider:

* Is rate limiting the client
* Has reached its own capacity
* Cannot currently accept additional requests

When the `429` originates from an upstream provider, the response may contain:

```text
error.metadata.provider_code
```

This field carries the provider's original error code when available.

OpenRouter can use provider fallback routing to retry another eligible provider serving the same model before returning the error to the client.

Fallback models can also be configured to try another model if all providers for the original model are exhausted.

---

# Rate-Limit Headers

When OpenRouter itself returns a `429` for a platform-level rate limit, the error response can contain:

| Header                  | Meaning                                 |
| ----------------------- | --------------------------------------- |
| `X-RateLimit-Limit`     | The applicable request limit            |
| `X-RateLimit-Remaining` | Remaining requests under that limit     |
| `X-RateLimit-Reset`     | Information about when the limit resets |

Successful inference responses do **not** include these `X-RateLimit-*` headers.

When every attempted provider returns a retry hint, the response can also contain:

```text
Retry-After
```

Clients should honor this header when present.

For proactive monitoring, use:

```http
GET https://openrouter.ai/api/v1/key
```

---

# Handling 429 Errors

The recommended response to rate limiting is to **retry with exponential backoff**.

### Recommended behavior

1. Detect HTTP `429`.
2. Check the error metadata to determine whether the limit originated from OpenRouter or an upstream provider.
3. If `Retry-After` is present, wait for the specified retry interval.
4. Otherwise, use exponential backoff before retrying.
5. For free-model limits, consider switching to a paid model variant or waiting for the quota to reset.
6. For provider-side limits, use fallback models or relax provider routing restrictions.

Do not immediately resend a rate-limited request in a tight loop.

---

## Handling Free-Model 429 Errors

If a free model reaches its platform request limit, possible solutions include:

* Wait for the applicable rate-limit window to reset.
* Purchase the required credits to increase the daily free-model allowance.
* Switch from the free model variant to the paid variant.

The documented free-model per-minute limit remains:

```text
20 requests per minute
```

The daily limit depends on the user's all-time purchased credits.

---

## Handling Provider-Side 429 Errors

If the upstream provider is rate limiting the request:

* Retry using exponential backoff.
* Honor `Retry-After` when provided.
* Configure fallback models when appropriate.
* Relax provider routing preferences so additional providers can serve the request.

OpenRouter may automatically retry other eligible providers for the same model through provider fallback routing.

---

# Mid-Stream Rate Limits

Rate-limit errors can also occur **after streaming has already started**.

In this situation, OpenRouter cannot return a new HTTP `429` status because the HTTP response has already begun with:

```text
HTTP 200 OK
```

Instead, the error is delivered as an **SSE event**.

The streamed response can contain:

```json
{
  "id": "cmpl-abc123",
  "object": "chat.completion.chunk",
  "created": 1234567890,
  "model": "openai/gpt-4o",
  "provider": "openai",
  "error": {
    "code": 429,
    "message": "Rate limit exceeded"
  },
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": ""
      },
      "finish_reason": "error"
    }
  ]
}
```

The important distinction is:

* **Rate limit before streaming starts:** HTTP `429 Too Many Requests`
* **Rate limit after streaming starts:** HTTP status remains `200 OK`, and the error is delivered as an SSE event with `finish_reason: "error"`

Applications using streaming responses should therefore handle rate-limit errors inside the SSE stream as well as handling normal HTTP `429` responses.

---

# Important Rate-Limit Concepts

## Rate Limits vs Credit Limits

These limits solve different problems.

### Rate limits

Control **how many requests** can be made.

Typical failure:

```text
429 Too Many Requests
```

Examples:

* Free-model requests per minute
* Free-model requests per day
* DDoS protection
* Upstream provider rate limits

### Credit limits

Control **how much can be spent**.

Typical failure:

```text
402 Payment Required
```

Examples:

* Account balance
* Per-key credit limit
* In-flight spending budget

A request can therefore fail because of a rate limit even when the account has sufficient credits, or because of a credit limit even when the request rate is low.

---

# Quick Reference

| Situation                                | Typical response        | Important information                             |
| ---------------------------------------- | ----------------------- | ------------------------------------------------- |
| Free model exceeds per-minute quota      | `429`                   | Free-model RPM limit                              |
| Free model exceeds daily quota           | `429`                   | `free_model_daily_requests`                       |
| DDoS protection triggered                | `429`                   | OpenRouter platform protection                    |
| Upstream provider rate limits request    | `429`                   | `error.metadata.provider_code` when available     |
| Platform rate limit reached              | `429`                   | `X-RateLimit-*` headers                           |
| Provider requests retry delay            | `429` or provider error | `Retry-After` when available                      |
| Rate limit occurs after streaming begins | HTTP remains `200`      | SSE event with error and `finish_reason: "error"` |
| Account spending limit reached           | `402`                   | Credit-limit handling, not a rate-limit problem   |

---

# Key Values

```text
Free-model requests per minute: 20 RPM

Free-model daily requests:
- Lower tier: 50 RPD
- Higher tier: 1,000 RPD

Higher daily free-model tier threshold:
10 all-time credits purchased

Rate-limit HTTP status:
429 Too Many Requests

Credit-limit HTTP status:
402 Payment Required
```

---

# RAG Retrieval Keywords

OpenRouter rate limits, OpenRouter API rate limit, OpenRouter 429, Too Many Requests, free model limits, free model RPM, free model RPD, requests per minute, requests per day, free_model_daily_requests, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, DDoS protection, provider rate limit, upstream provider throttling, provider_code, exponential backoff, streaming rate limit, SSE rate limit, mid-stream 429, fallback provider, fallback model, OpenRouter credit limits.
