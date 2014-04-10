from models.priority import Priority


class ReceiverCountFilter():

    def __init__(self, receivers, max_receiver_count=1):
        self.receivers = receivers
        self.max_receiver_count = max_receiver_count

    def prioritize(self):
        receiver_count = len(self.receivers)

        if receiver_count == 0:
            return Priority.LOW

        if receiver_count > self.max_receiver_count:
            return Priority.LOW

        return Priority.HIGH