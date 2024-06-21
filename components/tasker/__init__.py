import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text, switch
from esphome import core
from esphome import automation
from esphome.components import time
from esphome.const import (
    CONF_ID,
    CONF_TIME_ID,
    CONF_TIMES, 
    CONF_DAYS_OF_WEEK,
    CONF_MODE,
    CONF_ON_TIME,
    CONF_TRIGGER_ID,
)

# Additional config options
CONF_SCHEDULES = "schedules"
CONF_ENABLE = "enable"

# Automatically load components if the user hasn’t added them manually
AUTO_LOAD = [ "switch", "text", "time" ]

tasker_ns = cg.esphome_ns.namespace('tasker')
Tasker = tasker_ns.class_('Tasker')
Schedule = tasker_ns.class_('Schedule', cg.Component)
TaskerText = tasker_ns.class_("TaskerText", text.Text, cg.Component)
TaskerSwitch = tasker_ns.class_("TaskerSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Tasker),
        cv.GenerateID(CONF_TIME_ID): cv.use_id(time.RealTimeClock),
        cv.Required(CONF_SCHEDULES): cv.ensure_list({
            cv.Required(CONF_ID): cv.declare_id(Schedule),
            cv.Optional(CONF_ENABLE): switch.SWITCH_SCHEMA.extend(
                {
                    cv.GenerateID(): cv.declare_id(TaskerSwitch),
                }
            ),
            cv.Optional(CONF_DAYS_OF_WEEK): text.TEXT_SCHEMA.extend(
                {
                    cv.GenerateID(): cv.declare_id(TaskerText),
                    cv.Optional(CONF_MODE, default="TEXT"): cv.enum(text.TEXT_MODES, upper=True),
                }
            ),
            cv.Required(CONF_TIMES): text.TEXT_SCHEMA.extend(
                {
                    cv.GenerateID(): cv.declare_id(TaskerText),
                    cv.Optional(CONF_MODE, default="TEXT"): cv.enum(text.TEXT_MODES, upper=True),
                }
            ),
            cv.Optional(CONF_ON_TIME): automation.validate_automation(  
                single=True
            ),
        }),
    },
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    time_ = await cg.get_variable(config[CONF_TIME_ID])
    cg.add(var.set_time(time_))

    for schedule_conf in config.get(CONF_SCHEDULES, []):
        schedule = cg.new_Pvariable(schedule_conf[CONF_ID])
        await cg.register_component(schedule, schedule_conf)
        await cg.register_parented(schedule, var)

        if CONF_ENABLE in schedule_conf:
            enable_switch = await switch.new_switch(schedule_conf.get(CONF_ENABLE))
            await cg.register_component(enable_switch, schedule_conf.get(CONF_ENABLE))
            cg.add(schedule.set_enable_switch(enable_switch))

        if CONF_DAYS_OF_WEEK in schedule_conf:
            days_of_week_text = await text.new_text(schedule_conf.get(CONF_DAYS_OF_WEEK))
            await cg.register_component(days_of_week_text, schedule_conf.get(CONF_DAYS_OF_WEEK))
            cg.add(schedule.set_days_of_week_text(days_of_week_text))

        times_text = await text.new_text(schedule_conf.get(CONF_TIMES))
        await cg.register_component(times_text, schedule_conf.get(CONF_TIMES))
        cg.add(schedule.set_times_text(times_text))

        if (CONF_ON_TIME in schedule_conf):
            await automation.build_automation(
                schedule.get_trigger(), [], schedule_conf[CONF_ON_TIME]
            )
