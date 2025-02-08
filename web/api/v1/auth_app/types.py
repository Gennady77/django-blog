from typing import NamedTuple

class PasswordResetDTO(NamedTuple):
	uid: str
	token: str
