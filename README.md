# Trappers for Home Assistant

A custom component integration that connects Home Assistant to the [Trappers API](https://api.trappers.net/) and [Trappers Shop](https://trappersshop.fiscfree.nl/#/user/login).

## Features
- UI Configuration (No YAML required!)
- Automatically creates all Trappers sensors
- Safe asynchronous backend (`aiohttp`) prevents startup delays
- Tracks your lifetime balance, total trips, and weekly gamification stats.

## Installation via HACS
1. Open HACS in Home Assistant.
2. Click on Integrations.
3. Click the 3 dots in the top right corner and select **Custom repositories**.
4. Add the URL of this repository and select **Integration** as the category.
5. Click **Add** and then install the **Trappers** integration.
6. Restart Home Assistant.

## Setup
1. Go to **Settings > Devices & Services** in Home Assistant.
2. Click **Add Integration** in the bottom right corner.
3. Search for **Trappers**.
4. Enter your email and password when prompted.
5. Enjoy your fully integrated gamified cycling dashboard!

## Example Dashboard:
![screenshot](images/example_dashboard.png)
