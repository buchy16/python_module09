from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional, Annotated

SPACE_STATIONS = [
    {
        'station_id': 'LGW125',
        'name': 'Titan Mining Outpost',
        'crew_size': 6,
        'power_level': 76.4,
        'oxygen_level': 95.5,
        'last_maintenance': '2023-07-11T00:00:00',
        'is_operational': True,
        'notes': None
    },
    {
        'station_id': 'QCH189',
        'name': 'Deep Space Observatory',
        'crew_size': 50,
        'power_level': 70.8,
        'oxygen_level': 88.1,
        'last_maintenance': '2023-08-24T00:00:00',
        'is_operational': False,
        'notes': 'We are deep deep, Jhony Deep, deeper stop deeping, \
ping pang pong, ping pong, pingnata'
    }
]


class SpaceStation(BaseModel):
    station_id: Annotated[str, Field(strict=True, min_length=3, max_length=10)]
    name: Annotated[str, Field(strict=True, min_length=1, max_length=50)]
    crew_size: Annotated[int, Field(strict=True, ge=0, le=20)]
    power_level: Annotated[float, Field(strict=True, ge=0.0, le=100.0)]
    oxygen_level: Annotated[float, Field(strict=True, ge=0.0, le=100.0)]
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[Annotated[str, Field(strict=True, max_length=200)]]


def main() -> None:
    print("============================================================")
    try:
        station1 = SpaceStation(**SPACE_STATIONS[0])
        print("Valid station created:")
        print(f"ID: {station1.station_id}")
        print(f"Name: {station1.name}")
        print(f"Crew: {station1.crew_size} people")
        print(f"Power: {station1.power_level}%")
        print(f"Oxygen: {station1.oxygen_level}%")
        print(f"Status: \
{'Operationel' if station1.is_operational is True else 'Not Operational'}")
        if (station1.notes is not None):
            print(f"Note: {station1.notes}")
        print()
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])

    print("============================================================")
    try:
        station2 = SpaceStation(**SPACE_STATIONS[1])
        print("Valid station created:")
        print(f"ID: {station2.station_id}")
        print(f"Name: {station2.name} people")
        print(f"Crew: {station2.crew_size}%")
        print(f"Power: {station2.power_level}%")
        print(f"Oxygen: {station2.oxygen_level}")
        print(f"Status: \
{'Operationel' if station2.is_operational is True else 'Not Operational'}")
        if (station2.notes is not None):
            print(f"Note: {station2.notes}")
        print()
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])


if (__name__ == "__main__"):
    main()
