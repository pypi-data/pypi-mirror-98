from dataclasses import dataclass
from .models import Preferences


@dataclass(frozen=True)
class Credentials:
    public_key: str
    private_key: str
    project_id: int



def get_tilda_credentials() -> Credentials:
    preferences = Preferences.get_solo()

    return Credentials(
        public_key=preferences.public_key,
        private_key=preferences.private_key,
        project_id=preferences.project_id
    )
