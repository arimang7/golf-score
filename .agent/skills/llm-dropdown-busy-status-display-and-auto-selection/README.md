# LLM Dropdown Busy Status & Auto-selection (Gemini)

This skill provides a feature that visually displays the real-time response status of each Gemini model when generating AI analysis reports and automatically suggests the most efficient model.

## Overview

The Google Gemini API does not provide an official service status (Busy/Health) API. This system implements a unique health-check mechanism that measures response latency by sending minimal pings to each model through a backend proxy.

## Key Features

1. **Real-time Status Measurement**: Measures response speeds for all Gemini models in parallel upon page load.
2. **Visual Status Badges**: Displays 🟢 Fast, 🟡 Normal, and 🔴 Busy badges along with the actual latency.
3. **Intelligent Auto-selection**: Automatically selects the most optimized model based on responsiveness (Fast > Normal) and version priority.
4. **Custom Dropdown UI**: Provides a rich UI including status badges, going beyond the limitations of the standard HTML `<select>` tag.

## Usage

### 1. Configuration

- Manage target models and priorities in your backend API configuration.
- Update the configuration when adding or removing AI models.

### 2. UI Verification

- The dropdown should be integrated into your application's analysis report or settings section.
- A health check starts automatically upon component mounting, displaying a "Checking model status..." message until completion.

### 3. Status Criteria

- **Fast (< 3s)**: Ready for immediate response.
- **Normal (3-8s)**: Available, but with slight delay.
- **Busy (> 8s)**: High service load or connection error.

## Technical Considerations

- **Cost Optimization**: Uses `maxOutputTokens: 1` during pings to minimize token consumption.
- **User Experience (UX)**: Waiting time is minimized via parallel measurement using `Promise.all`. It includes outside-click detection for an intuitive dropdown experience.
