from dotenv import load_dotenv
import os


class Config:

    def __init__(self):
        load_dotenv()
        self.allowed_users = self._get_allowed_users()
        self.bot_token = os.getenv("BOT_TOKEN")
        self.theneo_api_key = os.getenv("THENEO_API_KEY")

    def _get_allowed_users(self) -> list[str]:
        return [username.replace("@", "") for username in os.getenv("ALLOWED_USERS").split(",")]

config = Config()