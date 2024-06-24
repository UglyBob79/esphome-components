# `ESPHome` components

A collection of my ESPHome external components.

Please ⭐️ this repo if you find it useful.

To use this repository you should configure it inside your yaml-configuration:
```yaml
external_components:
  - source: github://UglyBob79/esphome-components
```

## [Tasker](components/tasker)
The Tasker component allows you to run automations by making schedules with weekdays and time values.

**Features:**
- Schedule by weekdays, for example  `MON-FRI` or special days like `ODD`, `EVEN` and `EOD` (every other day). Ranges can be used, as well as multiple items comma separated
- Schedule by time values with minute precision, for example `18:00` or `3:45` (max 5 time values per schedule). Multiple values should be comma separated
- Schedule values will be exposes as text fields, which can be edited for instance from [Home Assistant](https://www.home-assistant.io/)
- Schedule values are saved on flash for persitence
- Supports multiple schedules

**Requirements:**
- [ESPHome](https://esphome.io) version **2024.4.2** or later (earlier probably works, but haven't tested yet)
- [ESPHOME Time Component](https://esphome.io/components/time/index.html) needs to be configured as a time source

#### ESPHome configuration example
Note: This example use sets up two schedules with text components that can be edited for instance from Home Assistant.
```yaml
tasker:
  schedules:
    - id: schedule_1
      days_of_week:
        name: Schedule 1 Days
        id: schedule_days_1
      times:
        name: Schedule 1 Times
        id: schedule_times_1
      on_time:
        then:
          - logger.log: "Schedule 1 triggered"
    - id: schedule_2
      days_of_week:
        name: Schedule 2 Days
        id: schedule_days_2
      times:
        name: Schedule 2 Times
        id: schedule_times_2
      on_time:
        then:
          - logger.log: "Schedule 2 triggered"
```

#### Supported text formats

**Time values:**
- HH:MM or H:MM format
- Multiple values comma separated, i.e. 10:00,15:30,16:45
- Max 5 time values per schedule, any more will be ignored

**Days of week values:**
- Days can be specified with values `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT` or `SUN`
- Ranges can be used, i.e. `MON-FRI`
- Multiple values comma separated, i.e. `MON-THU,SUN`
- Special day values `ODD` or `EVEN` can be used to trigger on odd or even weekdays. Monday is considered the first even day of the week
- Special day `EOD` can be used to trigger every other day
- Special day value `ALL` can be used to match every day of the week

#### Limitations
Currently doesn't take daylight saving switches into consideration. This means a schedule could trigger twice or not at all, if the time value occurs during the switch.
