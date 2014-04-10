from models.priority import Priority


class RegistrationMessageFilter():

    def __init__(self, steps_cache, text):
        self.text = text
        self.steps_cache = steps_cache

    def prioritize(self):
        if self.steps_cache.has_text(self.text):
            return Priority.HIGH
        return Priority.LOW