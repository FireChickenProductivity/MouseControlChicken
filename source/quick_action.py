from talon import Module, actions, settings

module = Module()

MOUSE_CONTROL_CHICKEN_QUICK_ACTION_SETTING_NAME = "mouse_control_chicken_quick_action"
MOUSE_CONTROL_CHICKEN_QUICK_ACTION_SETTING = 'user.' + MOUSE_CONTROL_CHICKEN_QUICK_ACTION_SETTING_NAME
module.setting(
    MOUSE_CONTROL_CHICKEN_QUICK_ACTION_SETTING_NAME,
    type = str,
    default = "",
    desc = "The mouse control chicken quick action to perform on dictating the main coordinates for a position on the active mouse control chicken coordinate system"
)

@module.action_class
class Actions:
    def mouse_control_chicken_perform_quick_action(coordinates: str):
        """Performs the mouse control chicken quick action on the specified coordinates"""
        action_description = settings.get(MOUSE_CONTROL_CHICKEN_QUICK_ACTION_SETTING)
        if not action_description:
            action_description = "user.mouse_control_chicken_click_position"
        action = getattr(actions, action_description)
        action(coordinates)