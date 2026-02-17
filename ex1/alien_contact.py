from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional, Annotated
from typing_extensions import Self
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


ALIEN_CONTACT = [
    {
        'contact_id': 'AC_2024_001',
        'timestamp': '2024-01-20T00:00:00',
        'location': 'Atacama Desert, Chile',
        'contact_type': ContactType.PHYSICAL.value,
        'signal_strength': 9.6,
        'duration_minutes': 99,
        'witness_count': 11,
        'message_received': 'Greetings from Zeta Reticuli',
        'is_verified': True
    },
    {
        'contact_id': 'AC_2024_002',
        'timestamp': '2024-08-20T00:00:00',
        'location': 'Mauna Kea Observatory, Hawaii',
        'contact_type': ContactType.RADIO.value,
        'signal_strength': 5.6,
        'duration_minutes': 152,
        'witness_count': 6,
        'message_received': None,
        'is_verified': False
    },
    {
        "contact_id": "WRONG_FORMAT",
        "timestamp": "2024-01-15T14:30:00",
        "location": "Area 51",
        "contact_type": ContactType.RADIO.value,
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": None,
        "is_verified": False
    },
    {
        "contact_id": "AC_2024_003",
        "timestamp": "2024-01-16T09:15:00",
        "location": "Roswell",
        "contact_type": ContactType.TELEPATHIC.value,
        "signal_strength": 6.2,
        "duration_minutes": 30,
        "witness_count": 1,
        "message_received": None,
        "is_verified": False
    },
    {
        "contact_id": "AC_2024_004",
        "timestamp": "2024-01-15T14:30:00",
        "location": "Area 51",
        "contact_type": ContactType.RADIO.value,
        "signal_strength": 8,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": None,
        "is_verified": False
    }
]


class AlienContact(BaseModel):
    contact_id: Annotated[str, Field(strict=True, min_length=5, max_length=15)]
    timestamp: datetime
    location: Annotated[str, Field(strict=True, min_length=3, max_length=100)]
    contact_type: ContactType
    signal_strength: Annotated[float, Field(strict=True, ge=0.0, le=10.0)]
    duration_minutes: Annotated[int, Field(strict=True, ge=1, le=1440)]
    witness_count: Annotated[int, Field(strict=True, ge=1, le=100)]
    message_received: Optional[Annotated[str,
                                         Field(strict=True, max_length=500)]]
    is_verified: bool = False

    @model_validator(mode='after')
    def verif_ID(self) -> Self:
        if (self.contact_id[:2] != "AC"):
            raise ValueError("contact_id must begin with 'AC'")
        return self

    @model_validator(mode='after')
    def verif_physical_contact(self) -> Self:
        if (self.contact_type.value == ContactType.PHYSICAL.value
           and self.is_verified is False):
            raise ValueError("physical contact must be verified")
        return self

    @model_validator(mode='after')
    def verif_telepathic(self) -> Self:
        if (self.contact_type.value == ContactType.TELEPATHIC.value
           and self.witness_count < 3):
            raise ValueError("telepathic contact \
requires at least 3 witnesses")
        return self

    @model_validator(mode='after')
    def verif_signal(self) -> Self:
        if (self.signal_strength > 7.0 and self.message_received is None):
            raise ValueError("strong signals should include received messages")
        return self


def print_infos(contact: AlienContact):
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    if (contact.message_received is not None):
        print(f"Message '{contact.message_received}'")
    print()


def main() -> None:
    print("==========================================")
    try:
        contact1 = AlienContact(**ALIEN_CONTACT[0])
        print_infos(contact1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()

    print("==========================================")
    try:
        contact1 = AlienContact(**ALIEN_CONTACT[1])
        print_infos(contact1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()

    print("==========================================")
    try:
        contact1 = AlienContact(**ALIEN_CONTACT[2])
        print_infos(contact1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()

    print("==========================================")
    try:
        contact1 = AlienContact(**ALIEN_CONTACT[3])
        print_infos(contact1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()

    print("==========================================")
    try:
        contact1 = AlienContact(**ALIEN_CONTACT[4])
        print_infos(contact1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()


if (__name__ == "__main__"):
    main()
