<p align="center">
  <img src="https://raw.githubusercontent.com/AciDCooL/hacs-trappers/main/custom_components/trappers/brand/icon.png" alt="HACS Trappers Logo" width="150">
</p>

# Trappers for Home Assistant

A custom component integration that connects Home Assistant to the [Trappers API](https://api.trappers.net/) and [Trappers Shop](https://trappersshop.fiscfree.nl/#/user/login).

[![Hassfest Status](https://github.com/AciDCooL/hacs-trappers/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/AciDCooL/hacs-trappers/actions/workflows/hassfest.yaml)

## Features
- UI Configuration (No YAML required!)
- Automatically creates all Trappers sensors

## Installation via HACS
1. Open HACS in Home Assistant.
2. Click on Integrations.
3. Click the 3 dots in the top right corner and select **Custom repositories**.
4. Add the URL of this repository *AciDCooL/hacs-trappers* and select **Integration** as the category.
5. Click **Add** and then install the **Trappers** integration.
6. Restart Home Assistant.

## Setup
1. Go to **Settings > Devices & Services** in Home Assistant.
2. Click **Add Integration** in the bottom right corner.
3. Search for **Trappers**.
4. Enter your email and password when prompted.
5. Enjoy your fully integrated cycling dashboard!

## Example Dashboard:
![screenshot](images/example_dashboard.png)

### Dashboard Code (YAML)
You can copy and paste these cards directly into your Home Assistant dashboard!

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: >-
      ## 🚲 Trappers Progress

      You have registered **{{ states('sensor.trappers_days_this_week') }} / 5** days this week.

      💸 So far, you've earned **€{{ states('sensor.trappers_euro_earned_this_week') }}** this week! Keep it up!
  - type: grid
    columns: 2
    square: false
    cards:
      - type: tile
        entity: sensor.trappers_balance
      - type: tile
        entity: sensor.trappers_euro_value
      - type: tile
        entity: sensor.trappers_last_registration
      - type: tile
        entity: sensor.total_trappers_trips
  - type: custom:apexcharts-card
    header:
      show: true
      title: Trappers Balance (Last 30 Days)
      show_states: true
      colorize_states: true
    graph_span: 30d
    series:
      - entity: sensor.trappers_balance
        name: Balance
        type: area
        color: "#3498db"
        opacity: 0.3
        stroke_width: 2
        fill_raw: last
        statistics:
          type: state
          period: day
          align: end
  - type: grid
    columns: 2
    square: false
    cards:
      - type: gauge
        entity: sensor.trappers_days_this_week
        min: 0
        max: 5
        name: Days (This Week)
        needle: true
        severity:
          green: 4
          yellow: 2
          red: 0
      - type: gauge
        entity: sensor.trappers_euro_earned_this_week
        min: 0
        max: 7.34
        name: Earned (This Week)
        needle: true
        severity:
          green: 5.86
          yellow: 2.93
          red: 0
  - type: gauge
    entity: sensor.trappers_next_payout_progress
    name: Progress to Next €100 Giftcard
    needle: true
    min: 0
    max: 100
    severity:
      green: 80
      yellow: 50
      red: 0
```
