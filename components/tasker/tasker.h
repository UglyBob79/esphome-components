/****
Copyright (c) 2024 Mattias Månsson

This library is free software; you can redistribute it and/or modify it 
under the terms of the GNU Lesser GeneralPublic License as published by the Free Software Foundation; 
either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; 
without even the impliedwarranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU Lesser General Public License for more details. 
You should have received a copy of the GNU Lesser General Public License along with this library; 
if not, write tothe Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA, 
or connect to: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
****/

#pragma once

#include "esphome/core/component.h"
#include "esphome/core/preferences.h"
#include "esphome/core/helpers.h"
#include "esphome/core/time.h"
#include "esphome/core/automation.h"

#include "esphome/components/text/text.h"
#include "esphome/components/time/real_time_clock.h"

namespace esphome {
namespace tasker {

using namespace text;

#define TASKER_MAX_TEXT_LEN 32
#define TASKER_MAX_TIMES_CNT 5

struct Time {
    uint8_t hour;
    uint8_t minute;

    Time() : hour(0), minute(0) {}
    Time(const uint8_t hour, const uint8_t minute)
        : hour(hour), minute(minute) {}
} __attribute__((packed));

class Tasker {
 public:
    static const char *TAG;
    
    /// Set the real time clock
    void set_time(time::RealTimeClock *time) { time_ = time; }

    /// Get the real time clock
    time::RealTimeClock *get_time() const { return time_; }
    

    time::RealTimeClock *time_;
};

class Schedule : public Component, public Parented<Tasker> {
// TODO Organize public/protected and later move out data to struct
public:
    static const char *TAG;

    Text* days_of_week_text;
    Text* times_text;

    // TODO Optimize to keep odd/even inside the same storage byte as days
    bool odd : 1;
    bool even : 1;
    union {
        struct {
            bool mon : 1;
            bool tue : 1;
            bool wed : 1;
            bool thu : 1;
            bool fri : 1;
            bool sat : 1;
            bool sun : 1;
        } day;
        uint8_t raw;
    } days;
    Time time[TASKER_MAX_TIMES_CNT];
    uint8_t time_cnt;

    Schedule() : time_cnt(0) {
        days.raw = 0;
    }

    float get_setup_priority() const override { return setup_priority::DATA; }
    void setup() override;
    void loop() override;
    void dump_config() override;

    void dump() const;

    /// Sets the days of week text component from yaml
    void set_days_of_week_text(Text* days_of_week_text);

    /// Sets the times text component from yaml
    void set_times_text(Text* times_text);

    /// Gets the trigger to connect it to yaml
    Trigger<> *get_trigger() const { return this->trigger_; }

protected:
    time_t last_sec_;

    void on_days_of_week_state_changed(const std::string& days_of_week);
    void on_times_state_changed(const std::string& times);
    void check_trigger(int day_of_week, uint8_t hour, uint8_t minute);
    bool check_day_of_week_match(int day_of_week);
    bool check_time_match(uint8_t hour, uint8_t minute);

    Trigger<> *trigger_ = new Trigger<>();
};

class TaskerText : public Component, public text::Text {
public:
    void setup() override;
    void control(const std::string& state);

protected:
    ESPPreferenceObject pref_;
};

}  // namespace tasker
}  // namespace esphome