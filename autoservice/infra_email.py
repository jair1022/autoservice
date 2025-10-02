from .interfaces import EmailService

class ConsoleEmail(EmailService):
    def send(self, to: str, subject: str, body: str) -> None:
        print(f"[EMAIL] to={to} subject={subject}\n{body}")
