# Anthropic Pricing

## Overview

Anthropic pricing covers:

-   Claude model token pricing.
-   Prompt caching.
-   Cloud platform pricing.
-   Claude Platform on AWS.
-   Claude in Microsoft Foundry.
-   Data residency.
-   Fast mode.
-   Batch processing.
-   Long-context usage.
-   Tool use and tool-specific overhead.
-   Claude Managed Agents.
-   Rate limits.
-   Volume and enterprise discounts.
-   Billing and payment.

All prices in this document are in **USD** unless otherwise stated.

For the most current pricing information, use the official Anthropic
pricing page:

`https://claude.com/pricing`

------------------------------------------------------------------------

# 1. Model Pricing

Model pricing is based primarily on:

-   Input tokens.
-   Output tokens.
-   Prompt-cache writes.
-   Prompt-cache reads/hits and refreshes.

Pricing is expressed per **MTok**, meaning one million tokens.

## Standard Model Pricing

  --------------------------------------------------------------------------
  Model            Input       Output     5-minute 1-hour cache Cache hits /
                                       cache write        write    refreshes
  --------- ------------ ------------ ------------ ------------ ------------
  Claude     \$10 / MTok  \$50 / MTok    \$12.50 /  \$20 / MTok     \$0.25 /
  Fable 5.1                                   MTok                      MTok

  Claude      \$4 / MTok  \$20 / MTok   \$5 / MTok   \$8 / MTok     \$0.20 /
  Opus 5.5                                                              MTok

  Claude      \$2 / MTok  \$10 / MTok     \$2.50 /   \$4 / MTok     \$0.20 /
  Sonnet                                      MTok                      MTok
  5.5                                                           

  Claude      \$1 / MTok   \$5 / MTok     \$1.25 /   \$2 / MTok     \$0.10 /
  Haiku 4.5                                   MTok                      MTok

  Claude     \$10 / MTok  \$50 / MTok    \$12.50 /  \$20 / MTok     \$0.25 /
  Mythos                                      MTok                      MTok
  5.1                                                           

  Claude     \$10 / MTok  \$50 / MTok    \$12.50 /  \$20 / MTok   \$1 / MTok
  Fable 5                                     MTok              

  Claude     \$10 / MTok  \$50 / MTok    \$12.50 /  \$20 / MTok   \$1 / MTok
  Mythos 5                                    MTok              

  Claude      \$5 / MTok  \$25 / MTok     \$6.25 /  \$10 / MTok     \$0.50 /
  Opus 5                                      MTok                      MTok

  Claude      \$5 / MTok  \$25 / MTok     \$6.25 /  \$10 / MTok     \$0.50 /
  Opus 4.8                                    MTok                      MTok

  Claude      \$5 / MTok  \$25 / MTok     \$6.25 /  \$10 / MTok     \$0.50 /
  Opus 4.7                                    MTok                      MTok

  Claude      \$5 / MTok  \$25 / MTok     \$6.25 /  \$10 / MTok     \$0.50 /
  Opus 4.6                                    MTok                      MTok

  Claude      \$5 / MTok  \$25 / MTok     \$6.25 /  \$10 / MTok     \$0.50 /
  Opus 4.5                                    MTok                      MTok

  Claude     \$15 / MTok  \$75 / MTok    \$18.75 /  \$30 / MTok     \$1.50 /
  Opus 4.1                                    MTok                      MTok

  Claude     \$15 / MTok  \$75 / MTok    \$18.75 /  \$30 / MTok     \$1.50 /
  Opus 4                                      MTok                      MTok

  Claude      \$2 / MTok  \$10 / MTok     \$2.50 /   \$4 / MTok     \$0.20 /
  Sonnet 5                                    MTok                      MTok

  Claude      \$3 / MTok  \$15 / MTok     \$3.75 /   \$6 / MTok     \$0.30 /
  Sonnet                                      MTok                      MTok
  4.6                                                           

  Claude      \$3 / MTok  \$15 / MTok     \$3.75 /   \$6 / MTok     \$0.30 /
  Sonnet                                      MTok                      MTok
  4.5                                                           

  Claude      \$3 / MTok  \$15 / MTok     \$3.75 /   \$6 / MTok     \$0.30 /
  Sonnet 4                                    MTok                      MTok

  Claude        \$0.80 /   \$4 / MTok   \$1 / MTok     \$1.60 /     \$0.08 /
  Haiku 3.5         MTok                                   MTok         MTok
  --------------------------------------------------------------------------

## Model Pricing Modifiers

All other models use the standard **0.1x multiplier** for the applicable
pricing modifier unless a model-specific exception is documented.

### Tokenizer change

Claude 4.7 and later models, plus Claude Mythos Preview, use a newer
tokenizer.

The newer tokenizer:

-   Contributes to improved performance across a wide range of tasks.
-   Produces approximately **30% more tokens for the same text**.
-   Does not guarantee exactly 30% more tokens for every workload; the
    actual increase depends on content and workload shape.

Claude Sonnet 4.6 and earlier models use the previous tokenizer.

This tokenizer difference matters when comparing token-based costs
across model generations.

------------------------------------------------------------------------

# 2. Cloud Platform Pricing

Claude is available through partner-operated cloud platforms where the
cloud provider invoices the customer.

Supported partner-operated platforms include:

-   Amazon Bedrock.
-   Google Cloud.

For Anthropic-operated cloud platforms billed through a marketplace, use
the separate pricing sections for:

-   Claude Platform on AWS.
-   Claude in Microsoft Foundry.

## Amazon Bedrock

Official pricing is provided by AWS:

`https://aws.amazon.com/bedrock/pricing/`

Claude models are available through Amazon Bedrock.

## Google Cloud

Official pricing is provided by Google Cloud:

`https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models`

Claude models are available through Google Cloud.

------------------------------------------------------------------------

# 3. Regional and Multi-Region Endpoint Pricing

Starting with:

-   Claude Sonnet 4.5.
-   Claude Haiku 4.5.
-   Claude Opus 4.5.

cloud platforms provide different endpoint-routing options.

## Amazon Bedrock endpoint types

Bedrock provides:

### Global endpoints

-   Use dynamic routing.
-   Optimize for maximum availability.

### Regional endpoints

-   Guarantee data routing through specified geographic regions.

## Google Cloud endpoint types

Google Cloud provides:

### Global endpoints

Global routing.

### Multi-region endpoints

Dynamic routing within a geographic area.

### Regional endpoints

Routing through a specific region.

## Regional pricing premium

Regional and multi-region endpoints have a **10% premium over global
endpoints**.

This means the effective multiplier is:

``` text
1.1x global endpoint pricing
```

The first-party Claude API is global by default.

For first-party data-residency options and pricing, use the Data
Residency Pricing section.

## Scope of regional/multi-region pricing

This pricing structure applies to:

-   Claude Sonnet 4.5.
-   Claude Haiku 4.5.
-   Claude Opus 4.5.
-   All future models.

Earlier models, including Claude Opus 4.1 and earlier releases, retain
their existing pricing.

------------------------------------------------------------------------

# 4. Claude Platform on AWS Pricing

Claude Platform on AWS is billed through **AWS Marketplace** using
**Claude Consumption Units (CCUs)**.

## Billing model

Anthropic:

1.  Rates token usage in USD using standard per-model and per-feature
    pricing.
2.  Applies any negotiated discount.
3.  Converts the resulting USD amount into CCUs.
4.  Uses a fixed conversion of **\$0.01 per CCU**.
5.  Reports CCU usage to AWS Marketplace hourly.

The AWS bill shows a single CCU line item.

## Claude Platform on AWS pricing structure

  -----------------------------------------------------------------------
  Concept                             Details
  ----------------------------------- -----------------------------------
  Billing unit                        Claude Consumption Unit (CCU)

  CCU price                           \$0.01 per CCU

  Conversion                          Standard model/feature token
                                      pricing is calculated in USD, then
                                      converted to CCUs at \$0.01 per CCU

  Billing cadence                     Hourly metering to AWS Marketplace;
                                      monthly invoices

  Payment model                       Arrears/postpaid only; no prepaid
                                      credits

  Discounts                           Applied as fewer CCUs metered

  Tax                                 Pre-tax metering; AWS Marketplace
                                      handles tax

  Cost visibility                     Real-time breakdown in Claude
                                      Console through AWS Console; AWS
                                      Cost Explorer shows aggregated CCUs
  -----------------------------------------------------------------------

The **\$0.01 CCU price is fixed**. Negotiated discounts affect the
token-to-CCU conversion rather than changing the CCU price itself.

## Inference geography on Claude Platform on AWS

For Claude 4.6 and later models:

``` text
inference_geo = "us"
```

applies a **1.1x pricing multiplier**.

The default:

``` text
inference_geo = "global"
```

uses standard pricing.

See Anthropic's Data Residency documentation for details.

## Private offers

When signing up through the AWS Console's Claude Platform on AWS service
page:

1.  AWS looks up private offers associated with the account.
2.  AWS prompts the customer to accept the applicable offer in AWS
    Marketplace.

Contact the Anthropic account representative for private-offer terms.

If an existing Amazon Bedrock private offer exists, contact Anthropic or
AWS before starting with Claude Platform on AWS so that discounts are
applied correctly.

**Discounts cannot be applied retroactively to usage incurred before the
private offer is accepted.**

------------------------------------------------------------------------

# 5. Claude in Microsoft Foundry Pricing

Claude in Microsoft Foundry is billed through the **Azure Marketplace**
using Claude Consumption Units (CCUs).

The billing model is similar to Claude Platform on AWS.

## Billing model

Anthropic:

1.  Rates token usage in USD using standard per-model and per-feature
    pricing.
2.  Applies negotiated discounts.
3.  Converts the resulting amount into CCUs.
4.  Uses **\$0.01 per CCU**.
5.  Reports CCUs to Azure Marketplace hourly.

The Azure bill shows a single CCU line item.

## Claude in Microsoft Foundry pricing structure

  -----------------------------------------------------------------------
  Concept                             Details
  ----------------------------------- -----------------------------------
  Billing unit                        Claude Consumption Unit (CCU)

  CCU price                           \$0.01 per CCU

  Conversion                          Standard model/feature token
                                      pricing in USD, converted to CCUs
                                      at \$0.01 per CCU

  Billing cadence                     Hourly metering to Azure
                                      Marketplace; monthly invoices

  Payment model                       Arrears/postpaid only; no prepaid
                                      credits

  Discounts                           Applied as fewer CCUs metered

  Tax                                 Pre-tax metering; Azure Marketplace
                                      handles tax

  Cost visibility                     Azure Cost Management shows
                                      aggregated CCUs
  -----------------------------------------------------------------------

## Inference geography in Microsoft Foundry

Azure deployments can use the **US Data Zone Standard** deployment type.

This:

-   Keeps inference within the United States.
-   Is equivalent to:

``` text
inference_geo = "us"
```

on the Claude API. - Applies the same **1.1x pricing multiplier**.

See the Data Residency documentation for details.

------------------------------------------------------------------------

# 6. Prompt Caching Pricing

Prompt caching reduces cost and latency by reusing previously processed
portions of prompts across API calls.

Useful cached content can include:

-   Large system prompts.
-   Documents.
-   Conversation history.
-   Other repeated context.

Instead of processing the same content repeatedly at the standard input
rate, subsequent requests can read it from cache at a reduced price.

## Prompt caching methods

There are two ways to enable prompt caching.

### Automatic caching

Add a single:

``` text
cache_control
```

field at the top level of the request.

The system automatically manages cache breakpoints as the conversation
grows.

This is the recommended starting point for most use cases.

### Explicit cache breakpoints

Place:

``` text
cache_control
```

directly on individual content blocks.

This provides fine-grained control over exactly what is cached.

## Prompt caching multipliers

  ------------------------------------------------------------------------
  Cache operation                 Pricing multiplier Cache duration
  --------------------- ---------------------------- ---------------------
  5-minute cache write        1.25x base input price 5 minutes

  1-hour cache write             2x base input price 1 hour

  Cache read / hit          0.1x base input price by Same duration as
                                             default preceding write
  ------------------------------------------------------------------------

### Model-specific cache-read pricing

Some models have lower cache-read multipliers:

  Model                          Cache read multiplier             Example price
  ---------------------------- ----------------------- -------------------------
  Claude Fable 5.1                              0.025x             \$0.25 / MTok
  Claude Mythos 5.1                             0.025x             \$0.25 / MTok
  Claude Opus 5.5                                0.05x             \$0.20 / MTok
  Standard applicable models                      0.1x   10% of base input price

## How cache charges work

Cache write tokens are charged when content is first stored.

Cache read tokens are charged when a later request retrieves the cached
content.

Under the standard 0.1x cache-read multiplier:

-   A 5-minute cache write costs 1.25x.
-   One cache read costs 0.1x.
-   Therefore the initial write plus one read totals 1.35x, making
    repeated use increasingly beneficial as the cache is reused.
-   A 1-hour cache write costs 2x.
-   Two cache reads add 0.2x, for a total of 2.2x before further reads.

For the model-specific 0.025x and 0.05x cache-read rates, cache reads
are even cheaper.

> The source documentation describes the 5-minute write as paying off
> after one cache read and the 1-hour write after two cache reads. When
> doing exact cost analysis, calculate the full write-plus-read sequence
> rather than treating the read price alone as the break-even condition.

## Pricing modifier stacking

Prompt-caching multipliers stack with other pricing modifiers,
including:

-   Batch API discounts.
-   Data-residency multipliers.

Implementation details, supported models, and code examples are covered
in Anthropic's Prompt Caching documentation.

------------------------------------------------------------------------

# 7. Data Residency Pricing

For Claude 4.6 and later models, specifying US-only inference using:

``` text
inference_geo = "us"
```

applies a **1.1x multiplier** to all token pricing categories.

The multiplier applies to:

-   Input tokens.
-   Output tokens.
-   Cache writes.
-   Cache reads.

Global routing:

``` text
inference_geo = "global"
```

is the default and uses standard pricing.

## Platforms affected

The 1.1x first-party data-residency multiplier applies to:

-   Claude API.
-   Claude Platform on AWS.

For Microsoft Foundry:

-   US Data Zone Standard is equivalent to US-only inference.
-   It uses the same 1.1x multiplier.

For partner-operated platforms:

-   Amazon Bedrock has its own regional pricing.
-   Google Cloud has its own regional and multi-region pricing.

Consult their official pricing pages for those platform-specific prices.

## Earlier models

Earlier models do not support the `inference_geo` parameter.

If the parameter is included for a model that does not support it, the
API returns:

``` text
HTTP 400
```

------------------------------------------------------------------------

# 8. Fast Mode Pricing

Fast mode is a **research preview** feature that provides significantly
faster output at premium pricing.

It is available for:

-   Claude Opus 5.5.
-   Claude Opus 5.
-   Claude Opus 4.8.

Fast mode pricing applies across the **full context window**, including
requests with more than 200K input tokens.

## Fast mode pricing

  Model                     Input        Output
  ----------------- ------------- -------------
  Claude Opus 5.5      \$8 / MTok   \$40 / MTok
  Claude Opus 5       \$10 / MTok   \$50 / MTok
  Claude Opus 4.8     \$10 / MTok   \$50 / MTok

## Fast mode availability

Fast mode is available only on the **first-party Claude API**.

It is not available on:

-   Claude Platform on AWS.
-   Partner-operated cloud platforms.

## Unsupported or special model behavior

### Claude Opus 4.7

Fast mode is not available.

A request with:

``` text
speed = "fast"
```

returns an error.

### Claude Opus 4.6

Fast mode is not available.

Requests run at standard speed and are billed at standard rates.

## Fast mode modifier stacking

Fast mode pricing stacks with:

-   Prompt caching multipliers.
-   Data-residency multipliers.

Fast mode cannot be combined with the **Batch API**.

------------------------------------------------------------------------

# 9. Batch Processing Pricing

The Batch API provides asynchronous processing for large volumes of
requests.

It provides a **50% discount on both input and output tokens**.

## Batch pricing

  Model                   Batch input     Batch output
  ------------------- --------------- ----------------
  Claude Fable 5.1         \$5 / MTok      \$25 / MTok
  Claude Opus 5.5          \$2 / MTok      \$10 / MTok
  Claude Sonnet 5.5        \$1 / MTok       \$5 / MTok
  Claude Haiku 4.5      \$0.50 / MTok    \$2.50 / MTok
  Claude Mythos 5.1        \$5 / MTok      \$25 / MTok
  Claude Fable 5           \$5 / MTok      \$25 / MTok
  Claude Mythos 5          \$5 / MTok      \$25 / MTok
  Claude Opus 5         \$2.50 / MTok   \$12.50 / MTok
  Claude Opus 4.8       \$2.50 / MTok   \$12.50 / MTok
  Claude Opus 4.7       \$2.50 / MTok   \$12.50 / MTok
  Claude Opus 4.6       \$2.50 / MTok   \$12.50 / MTok
  Claude Opus 4.5       \$2.50 / MTok   \$12.50 / MTok
  Claude Opus 4.1       \$7.50 / MTok   \$37.50 / MTok
  Claude Opus 4         \$7.50 / MTok   \$37.50 / MTok
  Claude Sonnet 5          \$1 / MTok       \$5 / MTok
  Claude Sonnet 4.6     \$1.50 / MTok    \$7.50 / MTok
  Claude Sonnet 4.5     \$1.50 / MTok    \$7.50 / MTok
  Claude Sonnet 4       \$1.50 / MTok    \$7.50 / MTok
  Claude Haiku 3.5      \$0.40 / MTok       \$2 / MTok

Batch processing is intended for workloads where asynchronous execution
is acceptable.

Fast mode is **not available** with the Batch API.

------------------------------------------------------------------------

# 10. Long-Context Pricing

Claude 4.6 and later models, plus Claude Mythos Preview, include the
full **1M-token context window at standard pricing**.

A long-context request is not automatically charged a higher per-token
rate.

For example:

-   A 9K-token request and a 900K-token request use the same per-token
    pricing rate for the same model and pricing configuration.

Prompt caching and batch-processing discounts apply at their standard
rates across the full context window.

------------------------------------------------------------------------

# 11. Tool Use Pricing

Tool-use requests are priced based on:

1.  Total input tokens sent to the model, including the `tools`
    parameter.
2.  Total output tokens generated.
3.  Additional usage-based charges for server-side tools where
    applicable.

Examples of server-side tool charges can include web-search charges per
search.

## Client-side versus server-side tools

### Client-side tools

Client-side tools are priced like normal Claude API requests.

Their additional token usage contributes to normal input/output token
costs.

### Server-side tools

Server-side tools can incur additional charges based on their specific
usage.

## Sources of additional tool-use tokens

Tool use can add tokens through:

-   The `tools` parameter.
    -   Tool names.
    -   Tool descriptions.
    -   Tool schemas.
-   `tool_use` content blocks.
-   `tool_result` content blocks.

When tools are included, the API also automatically adds a special
system prompt that enables tool use.

## Tool-use system prompt overhead

The following table gives the additional system-prompt tokens for
requests with tools.

The table assumes **at least one tool is provided**.

If no tools are provided and the tool choice is:

``` text
none
```

then the additional tool-use system-prompt cost is **0 tokens**.

  Model                 `auto` / `none`   `any` / `tool`
  ------------------- ----------------- ----------------
  Claude Opus 5.5                   286              588
  Claude Sonnet 5.5                 286              588
  Claude Haiku 4.5                  496              588
  Claude Opus 5                     286              406
  Claude Opus 4.8                   290              410
  Claude Opus 4.7                   675              804
  Claude Opus 4.6                   497              589
  Claude Opus 4.5                   496              588
  Claude Opus 4.1                   313              315
  Claude Opus 4                     313              315
  Claude Sonnet 5                   354              474
  Claude Sonnet 4.6                 497              589
  Claude Sonnet 4.5                 496              588
  Claude Sonnet 4                   313              315
  Claude Haiku 3.5                  264              355

These tokens are added to normal input and output token usage when
calculating the total cost of a request.

------------------------------------------------------------------------

# 12. Specific Tool Pricing

## Bash Tool

The Bash tool definition adds additional input tokens.

  Model                                               Additional input tokens
  ------------------------------------------------- -------------------------
  Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7                         325
  Claude Opus 4.6, Claude Sonnet 4.6, and earlier                         244

These tokens are in addition to the model's normal tool-use
system-prompt overhead.

Additional tokens can also be consumed by:

-   Command output (`stdout` / `stderr`).
-   Error messages.
-   Large file contents.

Therefore, Bash usage can increase costs beyond the static
tool-definition overhead.

------------------------------------------------------------------------

# 13. Code Execution Tool Pricing

Code execution has two different pricing behaviors depending on whether
web search/web fetch is also used.

## Code execution with web search or web fetch

Code execution is **free** when used with:

-   `web_search_20260209` or later.
-   `web_fetch_20260209` or later.

There are no additional code-execution charges beyond standard input and
output token costs.

## Code execution without web search/web fetch

When used without those tools, code execution is billed by execution
time.

Rules:

-   Minimum execution time: **5 minutes**.
-   Each organization receives **1,550 free hours per month**.
-   Additional usage beyond 1,550 hours costs **\$0.05 per hour per
    container**.
-   If files are included in a request, execution time is billed even
    when the code execution tool is not called because files are
    preloaded onto the container.

## Usage reporting

Code execution usage is represented in the response, for example:

``` json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 239,
    "server_tool_use": {
      "code_execution_requests": 1
    }
  }
}
```

------------------------------------------------------------------------

# 14. Text Editor Tool Pricing

The text editor tool follows the same general pricing structure as other
Claude tools.

Normal model input and output tokens are charged according to the
selected Claude model.

The `text_editor_20250429` tool version used with Claude 4.x adds:

``` text
700 additional input tokens
```

This is in addition to normal token usage.

------------------------------------------------------------------------

# 15. Web Search Tool Pricing

Web search is charged separately from standard token usage.

Example usage reporting:

``` json
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 6039,
    "cache_read_input_tokens": 7123,
    "cache_creation_input_tokens": 7345,
    "server_tool_use": {
      "web_search_requests": 1
    }
  }
}
```

## Web search price

Claude API web search costs:

``` text
$10 per 1,000 searches
```

This is **in addition to standard token costs** for search-generated
content.

## How searches are counted

Each web search counts as **one use**, regardless of how many results it
returns.

Search results retrieved throughout a conversation count as input
tokens:

-   During search iterations within a turn.
-   In subsequent conversation turns when the retrieved results remain
    in context.

If a web-search request errors, the web search is **not billed**.

------------------------------------------------------------------------

# 16. Web Fetch Tool Pricing

Web fetch has **no additional tool charge** beyond standard token costs.

Example usage reporting:

``` json
{
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  }
}
```

The customer pays standard token costs for fetched content that becomes
part of the conversation context.

## Controlling web-fetch cost

Use:

``` text
max_content_tokens
```

to limit the amount of fetched content included in context.

This helps prevent unexpectedly large token consumption.

Approximate token counts from the source:

  Content                              Approximate tokens
  ---------------------------------- --------------------
  Average web page, 10 kB                         \~2,500
  Large documentation page, 100 kB               \~25,000
  Research paper PDF, 500 kB                    \~125,000

------------------------------------------------------------------------

# 17. Computer Use Tool Pricing

Computer use follows standard Claude tool-use pricing.

## Current computer toolset overhead

Declaring:

``` text
computer_toolset_20260801
```

with its default members adds approximately **4,500 input tokens**.

Approximate overhead by model group:

-   About 4,520 tokens on Claude Fable 5, Claude Mythos 5, Claude Opus
    5, and Claude Opus 4.8.
-   About 4,590 tokens on Claude Sonnet 5.

This overhead covers:

-   Member tool definitions.
-   Tool-use system prompt.

Disabling `zoom` through `configs` removes approximately **410 tokens**.

The exact count for a request is reported in the response's `usage`
object.

The overhead can be estimated in advance using the token-counting
endpoint.

## Earlier computer tool versions

The following figures apply to:

-   `computer_20251124`
-   `computer_20250124`

They do not apply to `computer_toolset_20260801`.

Earlier tool overhead:

-   System prompt overhead: approximately 466--499 tokens.
-   Tool definition: approximately 735 input tokens per tool definition,
    measured with `computer_20250124`.

## Additional computer-use token consumption

Computer use can also consume tokens through:

-   Screenshots returned in tool results.
-   Zoom images returned in tool results.
-   Tool execution results returned to Claude.

Screenshot and zoom images are billed as image input.

If Bash or text editor tools are also used, their own token costs apply
separately.

------------------------------------------------------------------------

# 18. Browser Use Tool Pricing

Browser use also follows standard Claude tool-use pricing.

## Current browser toolset overhead

Declaring:

``` text
browser_toolset_20260801
```

with default members adds approximately **6,600 input tokens**.

Approximate overhead by model group:

-   About 6,610 tokens on Claude Fable 5, Claude Mythos 5, Claude Opus
    5, and Claude Opus 4.8.
-   About 6,670 tokens on Claude Sonnet 5.

This includes:

-   Default member tool definitions.
-   Tool-use system prompt.

Enabling all four optional members adds approximately **880 tokens**.

Disabling members with `configs` reduces the overhead.

The exact request-specific count is available in the response `usage`
object.

The overhead can be estimated in advance with the token-counting
endpoint.

## Additional browser-use token consumption

Browser use can consume additional tokens through:

-   Screenshots and zoom images.
-   Text tool results such as accessibility trees.
-   Page text.
-   Console entries.
-   Network entries.

Images are billed as image input.

If computer use, Bash, text editor, or custom tools are used alongside
browser use, those tools have separate token costs.

------------------------------------------------------------------------

# 19. Claude Managed Agents Pricing

Claude Managed Agents is billed on two dimensions:

1.  Tokens.
2.  Session runtime.

## Managed Agent token pricing

All tokens consumed during a Claude Managed Agents session are billed
using the rates from standard Model Pricing.

Prompt caching multipliers apply in the same way.

Web search inside a session incurs the standard:

``` text
$10 per 1,000 searches
```

price.

On Claude Platform on AWS, session token and runtime charges are
converted to Claude Consumption Units at the standard rate.

Fast mode premium pricing applies when:

``` text
model.speed = "fast"
```

## Managed Agent data residency pricing

The data-residency multiplier also applies.

When:

``` text
model.inference_geo = "us"
```

sessions use the **1.1x standard pricing multiplier**.

This is the same multiplier used for US-only inference on the Messages
API.

## Messages API modifiers that do not apply

The following modifiers do not apply to Claude Managed Agents sessions:

  -----------------------------------------------------------------------
  Modifier                            Why it does not apply
  ----------------------------------- -----------------------------------
  Batch API discount                  Sessions are stateful and
                                      interactive; there is no batch mode

  Cloud platform pricing              Managed Agents are not available on
                                      partner-operated cloud platforms
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 20. Managed Agent Session Runtime

Managed Agents additionally charge for session runtime.

  ------------------------------------------------------------------------
  SKU                                           Rate Metering
  --------------------- ---------------------------- ---------------------
  Session runtime            \$0.08 per session-hour Duration in `running`
                                                     status

  ------------------------------------------------------------------------

Runtime is measured to the millisecond.

Runtime accrues only while the session status is:

``` text
running
```

The following states do **not** count toward runtime:

-   `idle`
-   `rescheduling`
-   `terminated`

Session runtime replaces the code-execution container-hour billing model
when using Claude Managed Agents.

You are **not separately billed for container hours** on top of session
runtime.

------------------------------------------------------------------------

# 21. Managed Agent Worked Example

Consider a one-hour coding session using Claude Opus 5 with:

-   50,000 input tokens.
-   15,000 output tokens.
-   1 hour of running session time.

Pricing:

  Line item         Calculation                          Cost
  ----------------- --------------------------- -------------
  Input tokens      50,000 × \$5 / 1,000,000           \$0.25
  Output tokens     15,000 × \$25 / 1,000,000         \$0.375
  Session runtime   1.0 × \$0.08                       \$0.08
  **Total**                                       **\$0.705**

## Managed Agent example with prompt caching

If 40,000 of the input tokens are cache reads:

  Line item               Calculation                               Cost
  ----------------------- -------------------------------- -------------
  Uncached input tokens   10,000 × \$5 / 1,000,000                \$0.05
  Cache-read tokens       40,000 × \$5 × 0.1 / 1,000,000          \$0.02
  Output tokens           15,000 × \$25 / 1,000,000              \$0.375
  Session runtime         1.0 × \$0.08                            \$0.08
  **Total**                                                  **\$0.525**

The example demonstrates that prompt caching can reduce the token
portion of Managed Agent costs while session runtime remains separately
metered.

------------------------------------------------------------------------

# 22. High-Volume Example

The source provides an example for processing **10,000 support
tickets**:

-   Average conversation size: approximately 3,700 tokens.
-   Model: Claude Haiku 4.5.
-   Input price: \$1 / MTok.
-   Output price: \$5 / MTok.
-   Estimated total cost: approximately **\$37.00 per 10,000 tickets**.

The exact cost of a real workload depends on the actual input/output
token distribution.

------------------------------------------------------------------------

# 23. Cost Optimization Strategies

For agentic Claude applications, the source recommends:

## 1. Choose an appropriate model

General guidance:

-   **Haiku** for simple tasks.
-   **Sonnet** for most production workloads.
-   **Opus** for the most complex reasoning.

Model selection should be driven by actual workload requirements and
evaluation results rather than price alone.

## 2. Use prompt caching

Prompt caching can reduce cost when the same context is repeatedly
processed.

Good candidates include:

-   Large system prompts.
-   Long documents.
-   Repeated conversation history.
-   Reusable context.

## 3. Use batch processing

For non-time-sensitive work, the Batch API can provide a 50% discount on
input and output tokens.

## 4. Monitor usage

Track token consumption and workload patterns to identify optimization
opportunities.

## 5. Consider custom pricing at high volume

High-volume agent applications can contact Anthropic's enterprise sales
team for custom pricing arrangements.

------------------------------------------------------------------------

# 24. Rate Limits

Rate limits control how many requests an organization can make.

The source identifies three usage tiers:

  Tier    Purpose
  ------- --------------------------------------------------
  Start   Entry-level limits for getting started
  Build   Increased limits for growing applications
  Scale   Highest standard limits for production workloads

For detailed limits, consult Anthropic's Rate Limits documentation.

For requirements beyond the Scale tier or for custom pricing
arrangements, contact Anthropic sales.

------------------------------------------------------------------------

# 25. Volume Discounts

Volume discounts may be available for high-volume users.

They are negotiated **case by case**.

Standard usage tiers use the published Model Pricing.

Enterprise customers can contact Anthropic sales for custom pricing.

Academic and research discounts may also be available.

------------------------------------------------------------------------

# 26. Enterprise Pricing

Enterprise customers with specific requirements can negotiate:

-   Custom rate limits.
-   Volume discounts.
-   Dedicated support.
-   Custom commercial terms.

Enterprise pricing discussions can be initiated through:

-   Anthropic sales.
-   Claude Console.

------------------------------------------------------------------------

# 27. Billing and Payment

General billing rules described in the source:

-   Billing is based on actual monthly usage.
-   Prices are denominated in USD.
-   Credit cards are supported.
-   Invoicing is available.
-   Usage tracking is available in the Claude Console.

------------------------------------------------------------------------

# 28. Frequently Asked Questions

## How is token usage calculated?

Tokens are pieces of text processed by the model.

A rough English-language estimate is:

``` text
1 token ≈ 4 characters
1 token ≈ 0.75 words
```

These are approximations.

Actual token counts vary based on:

-   Language.
-   Content type.
-   Tokenizer.
-   Model generation.

The tokenizer differences described earlier can therefore materially
affect token counts and cost.

## Are there free tiers or trials?

New users receive a small amount of free credits for API testing.

Enterprise customers can contact sales about extended evaluation trials.

## How do discounts stack?

Batch API and prompt-caching discounts can be combined.

Pricing modifiers can therefore stack rather than being mutually
exclusive.

For exact combinations, calculate the applicable modifiers for the
relevant pricing category and consult the Prompt Caching and Batch
Processing documentation.

## What payment methods are accepted?

Standard accounts accept major credit cards.

Enterprise customers can arrange:

-   Invoicing.
-   Other negotiated payment methods.

------------------------------------------------------------------------

# 29. Pricing Modifier Interaction

Pricing should not be treated as a single flat model rate.

A request's effective cost can be affected by multiple dimensions.

Potential modifiers and cost sources include:

-   Base input price.
-   Base output price.
-   Prompt-cache write pricing.
-   Prompt-cache read pricing.
-   Batch API discount.
-   Data-residency multiplier.
-   Fast mode pricing.
-   Tool-use input overhead.
-   Server-side tool usage charges.
-   Managed Agent session runtime.
-   Cloud-platform endpoint premiums.
-   CCU conversion on marketplace-operated Anthropic platforms.

## Important stacking relationships

### Prompt caching

Prompt-caching multipliers can stack with:

-   Batch API pricing.
-   Data-residency pricing.

### Fast mode

Fast mode pricing can stack with:

-   Prompt caching.
-   Data residency.

Fast mode cannot be used with Batch API.

### Data residency

US-only inference applies a 1.1x multiplier to applicable token pricing
categories.

### Managed Agents

Managed Agents have both:

-   Token charges.
-   Session runtime charges.

Batch API and partner-cloud pricing modifiers do not apply to Managed
Agent sessions.

------------------------------------------------------------------------

# 30. Cost Calculation Framework

For a basic Claude API request without special modifiers:

``` text
Input cost =
input_tokens × input_price_per_token

Output cost =
output_tokens × output_price_per_token

Total =
input cost + output cost
```

For one million tokens:

``` text
1 MTok = 1,000,000 tokens
```

For requests involving caching:

``` text
Total token cost =
uncached input cost
+ cache-write cost
+ cache-read cost
+ output cost
```

Then apply relevant pricing modifiers such as:

-   Batch processing.
-   Data residency.
-   Fast mode.

Tool usage may additionally increase input tokens and may introduce
separate server-side usage charges.

Managed Agents add:

``` text
session runtime =
running_duration × $0.08/hour
```

For marketplace-operated Anthropic platforms:

``` text
USD-rated usage
→ negotiated discount
→ USD amount after discount
→ CCU conversion at $0.01/CCU
→ marketplace billing
```

This layered model is important because the published model input/output
rate is not always the final effective cost.

------------------------------------------------------------------------

# 31. Key Pricing Terms

## MTok

One million tokens.

## Base input price

The standard price charged for input tokens before pricing modifiers.

## Base output price

The standard price charged for generated output tokens before pricing
modifiers.

## Prompt-cache write

A charge for storing input content in the prompt cache.

## Prompt-cache read / hit

A discounted charge when previously cached content is reused.

## Batch API

Asynchronous API processing that provides a 50% discount on input and
output token pricing.

## Data residency multiplier

A 1.1x multiplier for applicable US-only inference configurations.

## Fast mode

A research-preview mode providing faster output at premium model
pricing.

## CCU

Claude Consumption Unit.

Claude Platform on AWS and Claude in Microsoft Foundry use CCUs for
marketplace billing.

## Session runtime

The amount of time a Claude Managed Agents session remains in the
`running` state.

## Tool-use overhead

Additional input-token consumption caused by tool definitions, tool-use
system prompts, tool calls, results, and tool-specific payloads.

------------------------------------------------------------------------

# 32. Pricing References

The source references these Anthropic resources:

-   Main pricing page: `https://claude.com/pricing`
-   Model pricing:
    `https://platform.claude.com/docs/en/about-claude/pricing#model-pricing`
-   Claude Platform on AWS pricing:
    `https://platform.claude.com/docs/en/about-claude/pricing#claude-platform-on-aws-pricing`
-   Claude in Microsoft Foundry pricing:
    `https://platform.claude.com/docs/en/about-claude/pricing#claude-in-microsoft-foundry-pricing`
-   Prompt caching:
    `https://platform.claude.com/docs/en/build-with-claude/prompt-caching`
-   Data residency:
    `https://platform.claude.com/docs/en/manage-claude/data-residency`
-   Fast mode:
    `https://platform.claude.com/docs/en/build-with-claude/fast-mode`
-   Batch processing:
    `https://platform.claude.com/docs/en/build-with-claude/batch-processing`
-   Context windows:
    `https://platform.claude.com/docs/en/build-with-claude/context-windows`
-   Tool use:
    `https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview`
-   Token counting:
    `https://platform.claude.com/docs/en/build-with-claude/token-counting`
-   Rate limits: `https://platform.claude.com/docs/en/api/rate-limits`
-   Claude Managed Agents:
    `https://platform.claude.com/docs/en/managed-agents/overview`
-   Claude Platform on AWS:
    `https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws`
-   Claude in Microsoft Foundry:
    `https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry`
-   Amazon Bedrock pricing: `https://aws.amazon.com/bedrock/pricing/`
-   Google Cloud Claude pricing:
    `https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models`
-   Enterprise/contact sales: `https://claude.com/contact-sales`

------------------------------------------------------------------------

# 33. RAG Retrieval Notes

The pricing information is intentionally separated into distinct
retrieval concepts:

-   **Model pricing** → standard input/output and cache rates.
-   **Prompt caching** → cache write/read pricing and breakpoints.
-   **Cloud platform pricing** → Bedrock and Google Cloud.
-   **Marketplace billing** → CCUs for AWS and Microsoft Foundry.
-   **Data residency** → US-only inference and 1.1x pricing.
-   **Fast mode** → premium low-latency pricing and availability
    restrictions.
-   **Batch processing** → 50% input/output discount.
-   **Long context** → 1M-token context at standard pricing for
    applicable models.
-   **Tool use** → additional token overhead and server-side usage
    charges.
-   **Bash** → static definition overhead plus command-result tokens.
-   **Code execution** → free with supported web search/fetch versions,
    otherwise execution-time billing.
-   **Text editor** → additional tool-definition input tokens.
-   **Web search** → \$10 per 1,000 searches plus token costs.
-   **Web fetch** → no separate tool charge, but fetched content
    consumes normal input tokens.
-   **Computer use** → substantial toolset-definition and image/result
    token overhead.
-   **Browser use** → substantial toolset-definition and page/image
    result token overhead.
-   **Managed Agents** → model token pricing plus \$0.08/session-hour
    runtime.
-   **Cost optimization** → model selection, caching, batching, and
    monitoring.
-   **Billing** → monthly usage and supported payment methods.

When retrieving pricing information, distinguish between **base model
pricing** and **effective request pricing after modifiers and
tool-specific costs**.
