# Claude Models Overview

## Overview

Claude is a family of state-of-the-art large language models developed
by Anthropic.

This document covers:

-   The current Claude model lineup described in the source
    documentation.
-   Recommended use cases for each model.
-   Comparative latency and pricing.
-   Thinking behavior and default effort.
-   Context-window and output limits.
-   Reliable-knowledge and training-data cutoffs.
-   Retirement timelines.
-   Model identifiers across supported platforms.
-   Programmatic model discovery through the Models API.
-   General prompt and output performance characteristics.

Each model's dedicated documentation page contains its full
specifications and available resources.

------------------------------------------------------------------------

# Current Claude Model Lineup

The source documentation recommends starting with **Claude Opus 5.5**
for most workloads.

Use **Claude Fable 5.1** when:

-   The workload requires demanding reasoning.
-   The workload involves long-horizon agentic work.
-   Evaluations on Claude Opus 5.5 still fall short even when using
    higher effort.

All current models described in this lineup support:

-   Text input.
-   Image input.
-   Text output.
-   Multilingual capabilities.
-   Vision.
-   Tool use.

The platforms on which a model is available are listed on that model's
dedicated documentation page.

------------------------------------------------------------------------

# Model Comparison

  ---------------------------------------------------------------------------
  Feature        Claude Fable   Claude Opus    Claude Sonnet  Claude Haiku
                 5.1            5.5            5.5            4.5
  -------------- -------------- -------------- -------------- ---------------
  Primary        Demanding      Long-running   Best           Fastest model
  positioning    reasoning and  agentic coding combination of with
                 long-horizon   and knowledge  speed and      near-frontier
                 agentic work   work           intelligence   intelligence

  Comparative    Slower         Moderate       Fast           Fastest
  latency                                                     

  Input pricing  \$10 / input   \$4 / input    \$2 / input    \$1 / input
                 MTok           MTok           MTok           MTok

  Output pricing \$50 / output  \$20 / output  \$10 / output  \$5 / output
                 MTok           MTok           MTok           MTok

  Claude API ID  Not specified  Not specified  Not specified  Not specified
                 in supplied    in supplied    in supplied    in supplied
                 source         source         source         source

  Capabilities   Not specified  Not specified  Not specified  Not specified
                 in supplied    in supplied    in supplied    in supplied
                 comparison     comparison     comparison     comparison
                 table          table          table          table

  Thinking       Adaptive       Adaptive       Adaptive       Extended
                 (always on)    (always on)                   

  Default effort `high`         `medium`       `high`         Not supported

  Context window 1M tokens      1M tokens      1M tokens      200K tokens

  Maximum output 128K tokens    128K tokens    128K tokens    64K tokens

  Reliable       Jun 2026       Jun 2026       Jun 2026       Feb 2025
  knowledge                                                   
  cutoff                                                      

  Training data  Jun 2026       Jun 2026       Jun 2026       Jul 2025
  cutoff                                                      

  Retirement     Not sooner     Not sooner     Not sooner     Not sooner than
                 than September than September than September October 15,
                 1, 2027        22, 2027       28, 2027       2026
  ---------------------------------------------------------------------------

> **Source-data limitation:** The supplied comparison table contains
> blank values for the Claude API ID, generic capabilities field, model
> IDs, and platform-specific IDs. These values are intentionally not
> inferred or fabricated in this document.

------------------------------------------------------------------------

# Model Selection Guidance

## Claude Opus 5.5

Recommended starting point for **most workloads**.

Positioning:

-   Long-running agentic coding.
-   Knowledge work.
-   General-purpose high-quality workloads.

Key characteristics:

-   Moderate comparative latency.
-   \$4 per input MTok.
-   \$20 per output MTok.
-   Adaptive thinking is always on.
-   Default effort: `medium`.
-   Context window: 1M tokens.
-   Maximum output: 128K tokens.
-   Reliable knowledge cutoff: Jun 2026.
-   Training data cutoff: Jun 2026.
-   Retirement: not sooner than September 22, 2027.

## Claude Fable 5.1

Use for workloads that require **demanding reasoning** or **long-horizon
agentic work**.

It is also the recommended choice when evaluations on Claude Opus 5.5
remain insufficient even when Opus 5.5 is run at higher effort.

Key characteristics:

-   Slower comparative latency.
-   \$10 per input MTok.
-   \$50 per output MTok.
-   Adaptive thinking is always on.
-   Default effort: `high`.
-   Context window: 1M tokens.
-   Maximum output: 128K tokens.
-   Reliable knowledge cutoff: Jun 2026.
-   Training data cutoff: Jun 2026.
-   Retirement: not sooner than September 1, 2027.

## Claude Sonnet 5.5

Positioned as the **best combination of speed and intelligence**.

Key characteristics:

-   Fast comparative latency.
-   \$2 per input MTok.
-   \$10 per output MTok.
-   Adaptive thinking.
-   Default effort: `high`.
-   Context window: 1M tokens.
-   Maximum output: 128K tokens.
-   Reliable knowledge cutoff: Jun 2026.
-   Training data cutoff: Jun 2026.
-   Retirement: not sooner than September 28, 2027.

## Claude Haiku 4.5

Positioned as the **fastest model with near-frontier intelligence**.

Key characteristics:

-   Fastest comparative latency.
-   \$1 per input MTok.
-   \$5 per output MTok.
-   Extended thinking.
-   Default effort is not supported.
-   Context window: 200K tokens.
-   Maximum output: 64K tokens.
-   Reliable knowledge cutoff: Feb 2025.
-   Training data cutoff: Jul 2025.
-   Retirement: not sooner than October 15, 2026.

------------------------------------------------------------------------

# Model Identifiers and Platform Availability

The documentation describes model identifiers across multiple platforms.

The supplied comparison table contains fields for:

-   Model IDs.
-   Claude API alias.
-   Amazon Bedrock ID.
-   Google Cloud ID.
-   Microsoft Foundry ID.
-   Claude Platform on AWS ID.

However, the supplied source does not contain values for these fields.

Therefore, the following identifiers should be retrieved from the
authoritative model-specific documentation rather than inferred:

  -----------------------------------------------------------------------------
  Model      Model ID   Claude API Amazon     Google     Microsoft   Claude
                        alias      Bedrock ID Cloud ID   Foundry ID  Platform
                                                                     on AWS ID
  ---------- ---------- ---------- ---------- ---------- ----------- ----------
  Claude     Not        Not        Not        Not        Not         Not
  Fable 5.1  provided   provided   provided   provided   provided    provided

  Claude     Not        Not        Not        Not        Not         Not
  Opus 5.5   provided   provided   provided   provided   provided    provided

  Claude     Not        Not        Not        Not        Not         Not
  Sonnet 5.5 provided   provided   provided   provided   provided    provided

  Claude     Not        Not        Not        Not        Not         Not
  Haiku 4.5  provided   provided   provided   provided   provided    provided
  -----------------------------------------------------------------------------

Each model's documentation page specifies the platforms where that model
is available.

------------------------------------------------------------------------

# Model IDs, Aliases, and Versioning

Model selection should distinguish between:

-   Model IDs.
-   Aliases.
-   Snapshots.

The source documentation points to **Model IDs and versioning** for
understanding how these identifiers and versions work.

When building integrations, do not assume that a model's human-readable
name alone is equivalent to its API model ID.

------------------------------------------------------------------------

# Using the Models API

Claude provides a **Models API** that allows applications to query
available model information programmatically.

The Models API response includes model information such as:

-   `max_input_tokens`
-   `max_tokens`
-   `capabilities`

Example conceptual response fields:

``` text
max_input_tokens
max_tokens
capabilities
line
```

## The `line` field

Each model returned by the Models API also contains a `line` field.

The `line` field identifies the model line to which the model belongs.

For example:

-   Claude Opus 4.5 reports `line = "opus"`.
-   Claude Opus 4.6 reports `line = "opus"`.

### Why use `line`

Use `line` when grouping models, such as when implementing:

-   A model picker.
-   Model-family filters.
-   Model-line selection.
-   UI grouping of related models.

Do **not** infer the model line from the model's `id`.

### `line` may be null

The `line` field is:

``` text
null
```

when a model does not belong to a model line.

### Do not assume the set of model lines is fixed

Anthropic may add additional model lines in the future.

Therefore:

-   Treat `line` as a dynamic field.
-   Do not hard-code the current set of possible values.
-   Read the `line` value returned by the Models API.

------------------------------------------------------------------------

# Model Capabilities and Performance

Current Claude models are described as particularly strong in several
areas.

## Reasoning

Claude models provide top-tier reasoning performance.

Model choice should depend on the reasoning requirements of the
workload, with Fable 5.1 specifically positioned for demanding reasoning
and long-horizon agentic work.

## Coding

Claude models are designed for strong coding performance.

Opus 5.5 is specifically positioned for:

-   Long-running agentic coding.
-   Knowledge work.

## Multilingual tasks

Current models support multilingual capabilities and are described as
performing strongly on multilingual tasks.

## Long-context workloads

Current models support long-context processing.

The models in the supplied lineup provide:

-   1M-token context windows for Fable 5.1, Opus 5.5, and Sonnet 5.5.
-   200K-token context window for Haiku 4.5.

## Vision and image processing

All current models in the supplied lineup support:

-   Image input.
-   Vision.

The documentation describes Claude models as strong in image processing.

## Tool use

All current models in the supplied lineup support tool use.

This makes them suitable for applications involving:

-   Agentic workflows.
-   Tool-calling.
-   External actions.
-   Long-running autonomous tasks.

## Honesty

The documentation also identifies honesty as an area where current
Claude models perform strongly.

------------------------------------------------------------------------

# Prompt and Output Performance

## General performance

Claude models are described as providing top-tier results in:

-   Reasoning.
-   Coding.
-   Multilingual tasks.
-   Long-context handling.
-   Honesty.
-   Image processing.

For general and model-specific prompting guidance, use Anthropic's
prompt engineering documentation.

## Response style and engagement

Claude models are intended for applications requiring rich, human-like
interactions.

If an application requires shorter or more concise responses, prompt the
model explicitly to control the desired output length.

Prompt engineering guidance should be used to tune:

-   Response length.
-   Output style.
-   Task-specific behavior.
-   Model-specific prompting strategies.

## Model migration

When migrating from an earlier Claude model generation, users may see
significant improvements in overall performance.

For workloads currently using Claude Opus 5 or earlier, the source
documentation recommends consulting the **Migrating to Claude Opus 5.5**
migration guide.

------------------------------------------------------------------------

# Model Cutoff Terminology

Claude model documentation distinguishes between two types of
knowledge/data cutoffs.

## Reliable knowledge cutoff

The reliable knowledge cutoff indicates the point through which the
model's knowledge is considered reliable according to Anthropic's
published model information.

For the supplied lineup:

  Model               Reliable knowledge cutoff
  ------------------- ---------------------------
  Claude Fable 5.1    Jun 2026
  Claude Opus 5.5     Jun 2026
  Claude Sonnet 5.5   Jun 2026
  Claude Haiku 4.5    Feb 2025

## Training data cutoff

The training data cutoff describes the cutoff associated with the
model's training data.

For the supplied lineup:

  Model               Training data cutoff
  ------------------- ----------------------
  Claude Fable 5.1    Jun 2026
  Claude Opus 5.5     Jun 2026
  Claude Sonnet 5.5   Jun 2026
  Claude Haiku 4.5    Jul 2025

These two cutoff concepts should not be treated as interchangeable.

For detailed cutoff information, use Anthropic's Transparency Hub.

------------------------------------------------------------------------

# Context Window and Maximum Output

  Model                 Context window   Maximum output
  ------------------- ---------------- ----------------
  Claude Fable 5.1           1M tokens      128K tokens
  Claude Opus 5.5            1M tokens      128K tokens
  Claude Sonnet 5.5          1M tokens      128K tokens
  Claude Haiku 4.5         200K tokens       64K tokens

The **context window** describes how much context the model can process.

The **maximum output** describes the maximum number of output tokens the
model can generate.

These are separate limits.

------------------------------------------------------------------------

# Thinking and Effort

The supplied lineup uses different thinking configurations.

  Model               Thinking               Default effort
  ------------------- ---------------------- ----------------
  Claude Fable 5.1    Adaptive (always on)   `high`
  Claude Opus 5.5     Adaptive (always on)   `medium`
  Claude Sonnet 5.5   Adaptive               `high`
  Claude Haiku 4.5    Extended               Not supported

Important distinctions:

-   **Adaptive thinking** means the model can adapt its reasoning
    behavior to the task.
-   Fable 5.1 and Opus 5.5 have adaptive thinking described as **always
    on**.
-   Sonnet 5.5 uses adaptive thinking.
-   Haiku 4.5 uses extended thinking.
-   Haiku 4.5 does not support a default effort setting.

------------------------------------------------------------------------

# Pricing

Pricing in the supplied documentation is expressed per million tokens
(MTok).

  Model                 Input price   Output price
  ------------------- ------------- --------------
  Claude Fable 5.1      \$10 / MTok    \$50 / MTok
  Claude Opus 5.5        \$4 / MTok    \$20 / MTok
  Claude Sonnet 5.5      \$2 / MTok    \$10 / MTok
  Claude Haiku 4.5       \$1 / MTok     \$5 / MTok

When comparing model costs, consider both:

-   Input token volume.
-   Output token volume.

A model with a lower input price can still become more expensive if its
workload generates substantially more output tokens.

------------------------------------------------------------------------

# Retirement Timelines

The supplied documentation gives minimum retirement dates.

  Model               Retirement
  ------------------- ------------------------------------
  Claude Fable 5.1    Not sooner than September 1, 2027
  Claude Opus 5.5     Not sooner than September 22, 2027
  Claude Sonnet 5.5   Not sooner than September 28, 2027
  Claude Haiku 4.5    Not sooner than October 15, 2026

The phrase **"not sooner than"** indicates a minimum retirement date
rather than a guaranteed retirement date.

Applications should not treat the listed date as an exact guaranteed
shutdown date unless Anthropic explicitly confirms one.

------------------------------------------------------------------------

# Quick Model Selection Matrix

  -----------------------------------------------------------------------
  Requirement                         Suggested model
  ----------------------------------- -----------------------------------
  General-purpose starting point      Claude Opus 5.5

  Long-running agentic coding         Claude Opus 5.5

  Knowledge work                      Claude Opus 5.5

  Demanding reasoning                 Claude Fable 5.1

  Long-horizon agentic work           Claude Fable 5.1

  Opus 5.5 remains insufficient even  Claude Fable 5.1
  at higher effort                    

  Best speed/intelligence balance     Claude Sonnet 5.5

  Fastest model                       Claude Haiku 4.5

  Near-frontier intelligence with     Claude Haiku 4.5
  lowest listed price                 

  Large context requirements          Fable 5.1, Opus 5.5, or Sonnet 5.5

  Lower-cost high-throughput          Haiku 4.5
  workloads                           
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# Getting Started

After selecting a model, the next step is to make the first Claude API
call.

Relevant resources include:

-   **Claude API getting started guide** --- for making the first API
    request.
-   **Model IDs and versioning** --- for understanding model IDs,
    aliases, and snapshots.
-   **Anthropic Transparency Hub** --- for reliable-knowledge and
    training-data cutoff information.
-   **Models API** --- for programmatically discovering available
    models, token limits, capabilities, and model lines.
-   **Prompting best practices** --- for general and model-specific
    prompting guidance.
-   **Prompt engineering guides** --- for controlling model behavior and
    output.
-   **Claude Opus 5.5 migration guide** --- for migrating workloads from
    Claude Opus 5 or earlier.

------------------------------------------------------------------------

# Source References

The supplied source references the following Anthropic documentation
resources:

-   Claude Fable 5.1 overview:
    `https://platform.claude.com/docs/en/models/fable-5-1/overview`
-   Claude Opus 5.5 overview:
    `https://platform.claude.com/docs/en/models/opus-5-5/overview`
-   Claude Sonnet 5.5 overview:
    `https://platform.claude.com/docs/en/models/sonnet-5-5/overview`
-   Claude Haiku 4.5 overview:
    `https://platform.claude.com/docs/en/models/haiku-4-5/overview`
-   Getting started: `https://platform.claude.com/docs/en/get-started`
-   Model IDs and versioning:
    `https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions`
-   Anthropic Transparency Hub: `https://www.anthropic.com/transparency`
-   Models API: `https://platform.claude.com/docs/en/api/models/list`
-   Prompting best practices:
    `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`
-   Prompt engineering:
    `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering`
-   Migrating to Claude Opus 5.5:
    `https://platform.claude.com/docs/en/models/opus-5-5/migration-guide`

------------------------------------------------------------------------

# RAG Retrieval Notes

This document intentionally keeps several concepts separate because they
represent different retrieval targets:

-   **Model selection** → which Claude model should be used for a
    workload.
-   **Model IDs** → identifiers used to invoke models on specific
    platforms.
-   **Aliases and snapshots** → versioning concepts.
-   **Thinking and effort** → reasoning configuration.
-   **Context window** → maximum context capacity.
-   **Maximum output** → maximum generated output.
-   **Reliable knowledge cutoff** → reliability-oriented knowledge
    boundary.
-   **Training data cutoff** → training-data boundary.
-   **Retirement** → minimum stated model retirement timeline.
-   **`line`** → API-provided model-family grouping field.
-   **Capabilities** → programmatically discoverable model capabilities.
-   **Pricing** → input and output token costs.

Do not infer missing model IDs or platform identifiers from model names.
The supplied source leaves those fields blank, so authoritative
model-specific documentation should be used when exact identifiers are
required.
