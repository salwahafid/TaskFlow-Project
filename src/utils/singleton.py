class ServiceNotification:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceNotification, cls).__new__(cls)
        return cls._instance

    def envoyer_notification(self, message):
        print(f"Notification : {message}")


notif1 = ServiceNotification()
notif2 = ServiceNotification()

notif1.envoyer_notification("Tâche assignée")
print(notif1 is notif2)