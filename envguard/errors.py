class EnvError(Exception):
    """Base error for envguard."""

class ValidationError(EnvError):
    """Raised when env validation fails."""

    def __init__(self, messages: list[str]) -> None:
        self.messages = messages
        super().__init__(self._format())

    def _format(self) -> str:
        lines = ["❌ Configuration error:\n"]
        for msg in self.messages:
            lines.append(f"- {msg}")
        return "\n".join(lines)