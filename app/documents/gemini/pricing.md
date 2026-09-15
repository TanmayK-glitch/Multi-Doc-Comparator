# Gemini Developer API Pricing

## Overview

Gemini API pricing is divided into three tiers:

- **Free** — For developers and small projects getting started with the Gemini API.
- **Paid** — For production applications requiring higher volumes and advanced features.
- **Enterprise** — For enterprise deployments powered by Gemini Enterprise Agent Platform.

### Free Tier

- Limited access to certain models
- Free input and output tokens
- Google AI Studio access
- Content may be used to improve Google's products

### Paid Tier

- Higher rate limits for production deployments
- Access to context caching
- Batch API with 50% cost reduction
- Access to Google's most advanced models
- Content is not used to improve Google's products

### Enterprise

Includes all Paid features, with optional access to:

- Dedicated support channels
- Advanced security and compliance
- Provisioned throughput
- Volume-based discounts
- ML Ops, model garden, and other enterprise capabilities

---

# Model Pricing

## Gemini 3.8 Flash

Model: `gemini-3.8-flash`

Description: Google's most intelligent Flash model, designed for long-horizon software engineering, autonomous agents, and complex enterprise workflows.

### Standard Pricing

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $0.75 / 1M tokens through Dec 31, 2026; $1.50 from Jan 1, 2027 |
| Output | Free | $3.75 / 1M tokens through Dec 31, 2026; $7.50 from Jan 1, 2027 |
| Context caching | Free | $0.075 / 1M tokens through Dec 31, 2026; $0.15 from Jan 1, 2027 |
| Context storage | Free | $0.50 / 1M tokens/hour through Dec 31, 2026; $1.00 from Jan 1, 2027 |
| Google Search grounding | Not available | 5,000 free requests/month, then $14 / 1,000 requests |
| Google Maps grounding | Not available | 5,000 free prompts/month, then $14 / 1,000 queries |

---

## Gemini 3.7 Flash

Model: `gemini-3.7-flash`

Description: High-speed Flash model designed for everyday coding, agentic tool use, and reliable multi-step execution.

### Standard Pricing

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $0.75 / 1M tokens through Dec 31, 2026; $1.50 from Jan 1, 2027 |
| Output | Free | $3.75 / 1M tokens through Dec 31, 2026; $7.50 from Jan 1, 2027 |
| Context caching | Free | $0.075 / 1M tokens through Dec 31, 2026; $0.15 from Jan 1, 2027 |
| Context storage | Free | $0.50 / 1M tokens/hour through Dec 31, 2026; $1.00 from Jan 1, 2027 |
| Google Search grounding | Not available | 5,000 free requests/month, then $14 / 1,000 requests |
| Google Maps grounding | Not available | 5,000 free prompts/month, then $14 / 1,000 queries |

---

## Gemini 3.6 Flash

Model: `gemini-3.6-flash`

Description: Previous-generation Flash model balancing speed and multimodal capabilities across general agentic and everyday tasks.

### Standard Pricing

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $0.75 / 1M tokens through Dec 31, 2026; $1.50 from Jan 1, 2027 |
| Output | Free | $3.75 / 1M tokens through Dec 31, 2026; $7.50 from Jan 1, 2027 |
| Context caching | Free | $0.075 / 1M tokens through Dec 31, 2026; $0.15 from Jan 1, 2027 |
| Context storage | Free | $0.50 / 1M tokens/hour through Dec 31, 2026; $1.00 from Jan 1, 2027 |
| Google Search grounding | Not available* | 5,000 free requests/month, then $14 / 1,000 requests |
| Google Maps grounding | Not available* | 5,000 free prompts/month, then $14 / 1,000 queries |

\* Can be tested in Google AI Studio.

---

## Gemini 3.5 Flash

Model: `gemini-3.5-flash`

Description: Earlier Flash model optimized for speed and foundational performance across routine, high-throughput workloads.

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $1.50 / 1M tokens |
| Output | Free | $9.00 / 1M tokens |
| Context caching | Free | $0.15 / 1M tokens |
| Context storage | Free | $1.00 / 1M tokens/hour |
| Google Search grounding | Not available* | 5,000 free requests/month, then $14 / 1,000 requests |
| Google Maps grounding | Not available* | 5,000 free prompts/month, then $14 / 1,000 queries |

---

## Gemini 3.5 Live Translate

Model: `gemini-3.5-live-translate-preview`

Description: Low-latency, real-time speech-to-speech translation model supporting 70+ languages.

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $3.50 / 1M tokens or $0.0053/min audio |
| Output | Free | $21.00 / 1M tokens or $0.0315/min audio |

---

## Gemini 3.5 Transcribe Live

Model: `gemini-3.5-transcribe-live`

Description: Low-latency, real-time speech-to-text model for bidirectional streaming audio transcription over WebSockets.

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $3.50 / 1M tokens or $0.005/min audio |
| Output | Free | $21.00 / 1M tokens or $0.004/min text |

---

## Gemini 3.5 Transcribe

Model: `gemini-3.5-transcribe`

Description: Speech-to-text model supporting automatic language detection, speaker diarization, word-level timestamps, and custom vocabulary biasing.

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $2.00 / 1M tokens or $0.003/min audio |
| Output | Free | $12.00 / 1M tokens or $0.002/min text |

---

## Gemini 3.5 Flash-Lite

Model: `gemini-3.5-flash-lite`

Description: Cost-efficient model optimized for high-volume agentic tasks, translation, and simple data processing.

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input | Free | $0.30 / 1M tokens |
| Output | Free | $2.50 / 1M tokens |
| Context caching | Not available | $0.03 / 1M tokens |
| Context storage | Not available | $1.00 / 1M tokens/hour |

---

## Gemini 3.1 Flash-Lite

Model: `gemini-3.1-flash-lite`

Description: Cost-efficient model optimized for high-volume agentic tasks, translation, and simple data processing.

| Metric | Free Tier | Paid Tier |
|---|---:|---:|
| Input — text/image/video | Free | $0.25 / 1M tokens |
| Input — audio | Free | $0.50 / 1M tokens |
| Output | Free | $1.50 / 1M tokens |
| Context caching — text/image/video | Not available | $0.025 / 1M tokens |
| Context caching — audio | Not available | $0.05 / 1M tokens |
| Context storage | Not available | $1.00 / 1M tokens/hour |

---

# Tool Pricing

Tools have their own pricing, which is applied on top of the selected model's pricing.

## Google Search

- Gemini 2.5 models: 1,500 RPD free, then $35 / 1,000 grounded prompts.
- Gemini 3 models: 5,000 free search requests/month, then $14 / 1,000 requests.

## Google Maps

- Free tier: 500 RPD for supported models.
- Paid tier: 1,500 RPD free for supported Flash models.
- Pro models: up to 10,000 RPD free.
- Additional usage: $25 / 1,000 grounded prompts.

## Code Execution

- Free of charge on the Free Tier.
- On Paid Tier, code execution is billed according to the selected model's standard token rates.
- Generated code and execution results are billed as output tokens.
- Results used by the model during iterative reasoning are billed as input tokens.

## URL Context

- Free on the Free Tier.
- On the Paid Tier, retrieved content is charged as input tokens according to the selected model's pricing.

## File Search

- Free on the Free Tier.
- Paid usage charges embeddings at $0.15 / 1M tokens.
- Retrieved document tokens are charged according to the selected model's normal token rates.

---

# Agent Pricing

Agent usage is calculated from the underlying model token consumption and tool usage.

## Gemini Deep Research Agent

- Model inference is charged at standard Gemini list rates.
- Input, output, and intermediate reasoning tokens are billed.
- Tool usage fees apply according to the relevant tool's pricing.

## Managed Agents

- Model inference is charged at standard Gemini list rates.
- Environment compute such as CPU, memory, and sandbox execution is not billed during the preview period.

## Antigravity Agent

- Model inference is charged at standard Gemini list rates.
- Tool usage is billed according to the existing pricing structure.

---

# Embeddings

## Gemini Embedding 2

Model: `gemini-embedding-2`

Description: Multimodal embedding model mapping text, images, video, audio, and PDFs into a unified embedding space.

| Input Type | Free Tier | Paid Tier |
|---|---:|---:|
| Text | Free | $0.20 / 1M tokens |
| Image | Free | $0.45 / 1M tokens |
| Audio | Free | $6.50 / 1M tokens |
| Video | Free | $12.00 / 1M tokens |

---

# Important Notes

- A single Gemini request may result in multiple Google Search queries.
- Customers are charged for each individual search query performed.
- Google AI Studio usage is free of charge in available regions.
- Prices may differ on Gemini Enterprise Agent Platform.
- Rate limits are subject to change.
- Document tokens for the `DOCUMENT` modality, such as PDFs, are billed at the image-token rate.
- Dynamic retrieval can reduce grounding costs because only requests containing at least one grounding support URL from the web are charged for Google Search grounding.