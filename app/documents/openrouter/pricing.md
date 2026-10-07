# OpenRouter Provider Pricing

## Overview

OpenRouter provider model documents describe pricing for inference using structured `pricing` arrays.

Pricing is attached to the **modality that owns the billable usage**:

* Input modality pricing belongs inside an input modality.
* Output modality pricing belongs inside an output modality.
* Request-scoped pricing belongs in the root `pricing` array.

This structure allows a provider to describe different prices for text, images, video, audio, cached prompts, generated outputs, and request-level operations.

All `cost_usd` values must be represented as **strings** to avoid floating-point precision issues.

Example:

```json
{
  "pricing": [
    {
      "type": "web_search",
      "unit": "search",
      "cost_usd": "0.01"
    }
  ]
}
```

---

## 1. Pricing Structure

A pricing entry contains:

```json
{
  "type": "prompt",
  "unit": "token",
  "cost_usd": "0.000008"
}
```

| Field      | Description                                     |
| ---------- | ----------------------------------------------- |
| `type`     | Billing category                                |
| `unit`     | Unit used for billing                           |
| `cost_usd` | Price per billing unit, represented as a string |

Pricing is scoped according to where the `pricing` array appears.

### Input pricing

Input modality pricing is used for costs associated with input data.

Examples:

* Prompt tokens
* Cached prompt tokens
* Cache writes
* Images
* Video
* Audio
* Characters

### Output pricing

Output modality pricing is used for generated output.

Examples:

* Completion tokens
* Internal reasoning tokens
* Generated images
* Generated audio
* Generated video
* Generated speech

### Root pricing

Root-level pricing is reserved for **request-scoped charges**.

Examples:

* Per-request charges
* Web-search charges

---

## 2. Supported Pricing Types

### Input pricing types

| Type            | Meaning                               |
| --------------- | ------------------------------------- |
| `prompt`        | Cost per unit of input consumed       |
| `cached_prompt` | Cost per unit read from prompt cache  |
| `cache_write`   | Cost per unit written to prompt cache |

Example:

```json
{
  "type": "prompt",
  "unit": "token",
  "cost_usd": "0.000008"
}
```

### Output pricing types

| Type                 | Meaning                           |
| -------------------- | --------------------------------- |
| `completion`         | Cost per unit of generated output |
| `internal_reasoning` | Cost per internal reasoning token |

Example:

```json
{
  "type": "completion",
  "unit": "token",
  "cost_usd": "0.000024"
}
```

### Root pricing types

| Type         | Meaning               |
| ------------ | --------------------- |
| `request`    | Flat cost per request |
| `web_search` | Cost per web search   |

Example:

```json
{
  "pricing": [
    {
      "type": "request",
      "unit": "request",
      "cost_usd": "0.001"
    },
    {
      "type": "web_search",
      "unit": "search",
      "cost_usd": "0.01"
    }
  ]
}
```

---

## 3. Supported Pricing Units

Input and output pricing can use units appropriate to the modality.

Common units include:

* `token`
* `image`
* `megapixel`
* `second`
* `character`
* `request`
* `search`

The allowed combinations depend on the pricing scope.

For example:

```json
{
  "type": "prompt",
  "unit": "token",
  "cost_usd": "0.000008"
}
```

represents a price per input token.

An image output can instead use:

```json
{
  "type": "completion",
  "unit": "image",
  "cost_usd": "0.05"
}
```

---

## 4. Token Pricing

Token-based pricing is commonly used for text inference.

For example:

```json
{
  "type": "prompt",
  "unit": "token",
  "cost_usd": "0.000008"
}
```

means the provider charges `$0.000008` per input token.

An output price can be represented as:

```json
{
  "type": "completion",
  "unit": "token",
  "cost_usd": "0.000024"
}
```

If a model charges separately for internal reasoning tokens, the provider can declare:

```json
{
  "type": "internal_reasoning",
  "unit": "token",
  "cost_usd": "0.000024"
}
```

---

## 5. Cached Prompt Pricing

Prompt caching is represented through pricing entries on the **input modality**.

The main cache-related pricing types are:

* `cached_prompt` — tokens read from the prompt cache.
* `cache_write` — tokens written to the prompt cache.

Example:

```json
{
  "type": "text",
  "pricing": [
    {
      "type": "prompt",
      "unit": "token",
      "cost_usd": "0.000008"
    },
    {
      "type": "cached_prompt",
      "unit": "token",
      "cost_usd": "0.000001"
    },
    {
      "type": "cache_write",
      "unit": "token",
      "cost_usd": "0.00001"
    }
  ]
}
```

Cache pricing is **input-side pricing**. Cache entries should not be placed on output modalities.

---

## 6. Cache TTL and Cache SKUs

Different cache lifetimes can be represented as separate pricing entries using `ttl_seconds`.

Example:

```json
{
  "type": "cache_write",
  "unit": "token",
  "ttl_seconds": 300,
  "cost_usd": "0.00001"
}
```

A provider can expose multiple cache-write prices:

```json
{
  "pricing": [
    {
      "type": "cache_write",
      "unit": "token",
      "ttl_seconds": 300,
      "cost_usd": "0.00001"
    },
    {
      "type": "cache_write",
      "unit": "token",
      "ttl_seconds": 3600,
      "cost_usd": "0.00002"
    }
  ]
}
```

`ttl_seconds` is a qualifier of the pricing entry rather than part of the `type`.

The effective identity of a cache SKU includes its qualifiers. Two pricing entries with the same effective identity are invalid.

---

## 7. Conditional Pricing with `overrides`

Providers can define conditional pricing when the price depends on request parameters or request-derived quantities.

Conditional pricing uses the `overrides` array attached to the pricing entry it modifies.

Example:

```json
{
  "type": "prompt",
  "unit": "token",
  "cost_usd": "0.000002",
  "overrides": [
    {
      "when": {
        "prompt_tokens": {
          "gte": 200001
        }
      },
      "cost_usd": "0.000004"
    }
  ]
}
```

In this example:

* The base price is `$0.000002` per token.
* When `prompt_tokens >= 200001`, the price becomes `$0.000004`.

---

## 8. Pricing Override Conditions

Override predicates support:

* `equals`
* `gte`
* `lte`
* `min_items`

Example:

```json
{
  "when": {
    "resolution": {
      "equals": "4K"
    }
  },
  "cost_usd": "0.09"
}
```

Multiple conditions in a plain map are treated as an **AND** condition.

Example:

```json
{
  "when": {
    "resolution": {
      "equals": "4K"
    },
    "steps": {
      "gte": 30
    }
  },
  "cost_usd": "0.12"
}
```

This applies when both conditions are true.

More complex conditions can use:

* `allOf`
* `anyOf`
* `not`

These operators can be nested.

---

## 9. Override Evaluation Order

Override entries are evaluated in order.

When multiple predicates match, the **later matching entry wins**.

Therefore, the order of entries matters when creating a pricing matrix.

Example:

```json
{
  "type": "completion",
  "unit": "image",
  "cost_usd": "0.03",
  "overrides": [
    {
      "when": {
        "resolution": {
          "equals": "2K"
        }
      },
      "cost_usd": "0.05"
    },
    {
      "when": {
        "resolution": {
          "equals": "4K"
        }
      },
      "cost_usd": "0.09"
    }
  ]
}
```

---

## 10. Parameter-Based Pricing

Override predicates are based on request parameters or request-derived quantities.

For example, pricing can vary according to:

* Prompt token count
* Image resolution
* Generation steps
* Other supported parameters

Time itself is **not** a request parameter and therefore should not be represented using `overrides`.

Time-dependent pricing uses the dedicated time-of-day pricing mechanism instead.

---

## 11. Megapixel Pricing

The `megapixel` unit is used for resolution-scaled media.

A price declared as:

```json
{
  "type": "completion",
  "unit": "megapixel",
  "cost_usd": "0.015"
}
```

represents a rate of `$0.015` per megapixel.

One megapixel equals **1,000,000 pixels**.

The total cost scales with the pixel dimensions of the media.

---

## 12. Time-of-Day Pricing

Time-dependent pricing can be represented using:

* `utc_start`
* `utc_end`

These values use `HHMM` format in UTC.

Example:

```json
{
  "type": "prompt",
  "unit": "token",
  "cost_usd": "0.000008"
}
```

Base price:

```text
$0.000008 per token
```

Peak price:

```json
{
  "type": "prompt",
  "unit": "token",
  "utc_start": 800,
  "utc_end": 1630,
  "cost_usd": "0.000008"
}
```

The time window is **half-open**:

```text
utc_start <= time < utc_end
```

The window may also wrap across midnight.

`utc_start` and `utc_end` must be provided together and must be different.

---

## 13. Weekly Time-Based Pricing

Time-dependent pricing can optionally use `utc_days`.

Example:

```json
{
  "type": "prompt",
  "unit": "token",
  "utc_days": [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday"
  ],
  "utc_start": 800,
  "utc_end": 1630,
  "cost_usd": "0.000008"
}
```

The price applies only during the specified UTC days and time window.

Valid day names are:

```text
monday
tuesday
wednesday
thursday
friday
saturday
sunday
```

---

## 14. Time-Based Pricing Limitations

The documented pricing system has several limitations:

* Up to 2 time windows per model.
* All windowed entries must share the same non-base prices.
* All windowed entries must use the same `utc_days` set, or none.
* Certain unsupported schedule declarations may be accepted by the schema but produce translation warnings and are not billed.
* The base pricing should be the cheapest/off-peak rate.

Using the cheapest rate as the base ensures that unsupported schedule declarations do not cause users to be overcharged.

---

## 15. Pricing and Free Models

A provider can mark a model variant as free using:

```json
{
  "id": "your-org/your-model",
  "is_free": true
}
```

When `is_free` is `true`:

* The endpoint is treated as a free endpoint.
* Any pricing supplied alongside it is ignored.
* The endpoint always has zero cost.

A provider can publish both free and paid variants of the same model. The free variant must explicitly use:

```json
"is_free": true
```

---

## 16. Service-Tier Pricing

Providers can publish different pricing for different service tiers.

Example:

```json
[
  {
    "id": "your-org/your-model",
    "pricing": [
      {
        "type": "prompt",
        "unit": "token",
        "cost_usd": "0.000008"
      }
    ]
  },
  {
    "id": "your-org/your-model",
    "service_tier": "flex",
    "pricing": [
      {
        "type": "prompt",
        "unit": "token",
        "cost_usd": "0.000004"
      }
    ]
  },
  {
    "id": "your-org/your-model",
    "service_tier": "priority",
    "pricing": [
      {
        "type": "prompt",
        "unit": "token",
        "cost_usd": "0.000012"
      }
    ]
  }
]
```

Supported service-tier values include:

* `flex`
* `priority`
* `fast`
* `ultrafast`

`fast` is an alias for `priority`. A provider should publish one or the other for a given model ID, not both.

The default tier is represented by omitting `service_tier`.

A free endpoint cannot be combined with `service_tier`.

---

## 17. User-Facing Discounts

Providers can use `discount_to_user` to reduce the price users see and pay.

The calculation is:

```text
user price = base price × (1 - discount_to_user)
```

Example:

```json
{
  "id": "your-org/your-model",
  "discount_to_user": 0.2
}
```

A value of `0.2` represents a **20% discount**.

For example:

```text
Base price = 0.000024
Discount = 20%

User price = 0.000024 × (1 - 0.2)
           = 0.0000192
```

The discount applies to every priced SKU, including:

* Prompt pricing
* Completion pricing
* Image pricing
* Cache reads
* Conditional overrides
* Time-windowed pricing

`discount_to_user` must be a number, not a string.

Valid behavior:

* `0` or omitted → no discount.
* `0.2` → 20% discount.
* Negative values → markup rather than discount.
* Values `>= 1` are invalid because they would result in free or negative pricing.

---

## 18. Pricing and Capacity Are Separate

Pricing and capacity are related but distinct.

A provider can declare:

```json
{
  "pricing": [
    {
      "type": "prompt",
      "unit": "token",
      "cost_usd": "0.000008"
    }
  ],
  "capacity": [
    {
      "type": "prompt",
      "unit": "token",
      "per": "minute",
      "value": 1000000
    }
  ]
}
```

The first describes **how much usage costs**.

The second describes **how much usage the provider can handle**.

A provider may declare pricing without declaring capacity, or capacity without pricing.

An absent `capacity` array means the limit is **undeclared**, not zero.

---

## 19. Important Pricing Rules

When creating a provider pricing document:

1. Put pricing on the modality that owns the billable usage.
2. Use root pricing only for request-scoped charges.
3. Represent every `cost_usd` as a string.
4. Do not add pricing entries for SKUs the provider does not bill.
5. Use `"0"` only for a genuinely free SKU that is exposed as a distinct billable line.
6. Use `overrides` for request-conditional pricing.
7. Use `utc_start` and `utc_end` for time-dependent pricing rather than `overrides`.
8. Put cache pricing on input modalities.
9. Use `discount_to_user` as a decimal fraction.
10. Keep base pricing as the cheapest rate when using time-dependent pricing.
11. Treat pricing and capacity as separate concepts.

---

## 20. Complete Pricing Example

The following example combines several pricing concepts:

```json
{
  "id": "your-org/your-model",

  "input_modalities": [
    {
      "type": "text",
      "pricing": [
        {
          "type": "prompt",
          "unit": "token",
          "cost_usd": "0.000008"
        },
        {
          "type": "cached_prompt",
          "unit": "token",
          "cost_usd": "0.000001"
        },
        {
          "type": "cache_write",
          "unit": "token",
          "ttl_seconds": 3600,
          "cost_usd": "0.00001"
        }
      ]
    }
  ],

  "output_modalities": [
    {
      "type": "text",
      "pricing": [
        {
          "type": "completion",
          "unit": "token",
          "cost_usd": "0.000024"
        },
        {
          "type": "internal_reasoning",
          "unit": "token",
          "cost_usd": "0.000024"
        }
      ]
    }
  ],

  "pricing": [
    {
      "type": "web_search",
      "unit": "search",
      "cost_usd": "0.01"
    }
  ],

  "discount_to_user": 0.1
}
```

This document describes:

* Input-token pricing.
* Cached-input pricing.
* Cache-write pricing.
* Output-token pricing.
* Internal-reasoning pricing.
* Request-level web-search pricing.
* A 10% user-facing discount.

---

## Key Takeaway

OpenRouter provider pricing is **not a single flat price field**.

Pricing is structured around the usage being billed:

```text
Input modality
    ├── prompt
    ├── cached_prompt
    └── cache_write

Output modality
    ├── completion
    └── internal_reasoning

Root
    ├── request
    └── web_search
```

Conditional pricing can be expressed with `overrides`, cache pricing can use cache-specific qualifiers such as `ttl_seconds`, time-dependent pricing can use UTC time windows, and user-facing discounts can be expressed with `discount_to_user`.

For a RAG system, these distinctions are important because queries about **token cost, cached-token cost, image pricing, conditional pricing, discounts, or provider pricing structure** should retrieve the correct pricing rules rather than unrelated provider-integration information.
