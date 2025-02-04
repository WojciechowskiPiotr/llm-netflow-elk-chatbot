# --- Debugging ---
class DebugFlags:
    def __init__(self) -> None:
        self.flag_debugging_messages = 0
        self.flag_override_dsl = 0

    def set_debugging_flag(self):
        self.flag_debugging_messages = 1

    def set_override_dsl_flag(self):
        self.flag_override_dsl = 1

    def get_debbugging_flag(self):
        return self.flag_debugging_messages

    def get_override_dsl_flag(self):
        return self.flag_override_dsl


debugflags: DebugFlags = DebugFlags()
