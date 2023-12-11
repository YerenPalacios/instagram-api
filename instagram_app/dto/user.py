from dataclasses import dataclass

@dataclass
class UserDTO:
    id: int
    name: str
    username: str
    email: str
    phone: str
    image: str
    is_active: bool
    is_staff: bool
    description: str
    color: str
    is_following: bool | None
