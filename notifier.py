from abc import ABC, abstractmethod

from win10toast import ToastNotifier


class Notifier(ABC):
  @abstractmethod
  def notify(self, message: str, body: str, duration: int) -> None:
    pass


class WindowsNotifier(Notifier):
  def notify(self, message: str, body: str, duration: int = 20) -> None:
    """
    Args:
      message: The title of the notification.
      body: The body text of the notification.
      duration: The duration (in seconds) to display the notification (defaults to 20).
    """

    toast = ToastNotifier()
    toast.show_toast(message, body, duration=duration, threaded= True)

