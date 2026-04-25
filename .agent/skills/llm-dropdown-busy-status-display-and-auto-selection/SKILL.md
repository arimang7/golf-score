---
name: LLM Dropdown - Busy Status Display and Auto-selection
description: This skill enables health status badges (Busy/Fast/Normal) in the LLM model selection dropdown for AI reports and implements auto-selection for the most responsive and latest model.
---

# LLM Dropdown - Busy Status Display and Auto-selection

## Overview

In the `AI In-depth Analysis Report` section, the LLM model selection dropdown:

- Measures real-time response latency (Busy status) for each model and displays it via badges.
- Automatically selects the most responsive and latest model upon page load.

## Architecture

```
[Browser Load]
    │
    ▼
GET /api/model-health
    │
    ├── Parallel Ping (Minimal prompt "hi", maxOutputTokens: 1)
    │   ├── gemini-3.1-flash-lite
    │   ├── gemini-3-flash
    │   ├── gemini-3.1-pro
    │   ├── gemini-2.5-flash
    │   └── gemini-2.5-flash-lite
    │
    ▼
Response: { models: [...], recommended: "modelID" }
    │
    ▼
UI Dropdown: Display badges + Automatically set selectedModel
```

## Implementation Structure

| Component       | Description                                  |
| --------------- | -------------------------------------------- |
| **Backend API** | Endpoint for measuring model health (Ping)   |
| **Frontend UI** | Dropdown component with auto-selection logic |

## Health Status Criteria

| Response Time    | Status | Badge     | Color  |
| ---------------- | ------ | --------- | ------ |
| < 3000ms         | fast   | 🟢 Fast   | Green  |
| 3000~8000ms      | normal | 🟡 Normal | Yellow |
| > 8000ms / Error | busy   | 🔴 Busy   | Red    |

## Model Priorities (Lower priority value = Higher precedence)

| Priority | Model ID                        | Characteristics      |
| -------- | ------------------------------- | -------------------- |
| 1        | `gemini-3.1-flash-lite` | Newest + Lightweight |
| 2        | `gemini-3-flash`        | Newest               |
| 3        | `gemini-3.1-pro`          | Flagship Reasoning   |
| 4        | `gemini-2.5-flash`      | Stable               |
| 5        | `gemini-2.5-flash-lite` | Ultra Lightweight    |

## Auto-selection Algorithm

```typescript
// Find the first "fast" model by priority order.
// If none, find "normal". Fallback to the first model in the list.
const best =
  results.find((r) => r.status === "fast") ||
  results.find((r) => r.status === "normal") ||
  results[0];
```

## UI States

| Scenario                 | State                                                 |
| ------------------------ | ----------------------------------------------------- |
| Health Check in Progress | Dropdown disabled + "⏳ Checking model status..."     |
| Load Complete            | Badges and latency (ms) displayed next to each option |
| AI Analysis in Progress  | Dropdown disabled to prevent mid-analysis changes     |

## API Example: /api/model-health

```json
{
  "models": [
    {
      "id": "gemini-3.1-flash-lite",
      "label": "🔬 gemini-3.1-flash-lite",
      "priority": 1,
      "latency": 1234,
      "status": "fast"
    }
  ],
  "recommended": "gemini-3.1-flash-lite"
}
```

- When adding or removing models, update the model configuration in both the backend API and the frontend UI.
- Ping requests use `maxOutputTokens: 1` to minimize costs and latency.
- Measurements are parallelized via `Promise.all`; total check time ≈ latency of the slowest model.
