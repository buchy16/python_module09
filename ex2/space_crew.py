from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Optional, Annotated, List
from typing_extensions import Self
from enum import Enum


SPACE_MISSIONS = [
    {
        'mission_id': 'M2024_TITAN',
        'mission_name': 'Solar Observatory Research Mission',
        'destination': 'Solar Observatory',
        'launch_date': '2024-03-30T00:00:00',
        'duration_days': 451,
        'crew': [
            {
                'member_id': 'CM001',
                'name': 'Sarah Williams',
                'rank': 'captain',
                'age': 43,
                'specialization': 'Mission Command',
                'years_experience': 19,
                'is_active': True
            },
            {
                'member_id': 'CM002',
                'name': 'James Hernandez',
                'rank': 'captain',
                'age': 43,
                'specialization': 'Pilot',
                'years_experience': 30,
                'is_active': True
            },
            {
                'member_id': 'CM003',
                'name': 'Anna Jones',
                'rank': 'cadet',
                'age': 35,
                'specialization': 'Communications',
                'years_experience': 15,
                'is_active': True
            },
            {
                'member_id': 'CM004',
                'name': 'David Smith',
                'rank': 'commander',
                'age': 27,
                'specialization': 'Security',
                'years_experience': 15,
                'is_active': True
            },
            {
                'member_id': 'CM005',
                'name': 'Maria Jones',
                'rank': 'cadet',
                'age': 55,
                'specialization': 'Research',
                'years_experience': 30,
                'is_active': True
            }
        ],
        'mission_status': 'planned',
        'budget_millions': 2208.1
    },
    {
        'mission_id': 'M2024_MARS',
        'mission_name': 'Jupiter Orbit Colony Mission',
        'destination': 'Jupiter Orbit',
        'launch_date': '2024-10-01T00:00:00',
        'duration_days': 1065,
        'crew': [
            {
                'member_id': 'CM011',
                'name': 'Emma Brown',
                'rank': 'officier',
                'age': 49,
                'specialization': 'Mission Command',
                'years_experience': 27,
                'is_active': True
            },
            {
                'member_id': 'CM012',
                'name': 'John Hernandez',
                'rank': 'lieutenant',
                'age': 36,
                'specialization': 'Science Officer',
                'years_experience': 22,
                'is_active': True
            },
            {
                'member_id': 'CM013',
                'name': 'Sofia Rodriguez',
                'rank': 'officier',
                'age': 29,
                'specialization': 'Life Support',
                'years_experience': 20,
                'is_active': True
            },
            {
                'member_id': 'CM014',
                'name': 'Sofia Lopez',
                'rank': 'lieutenant',
                'age': 44,
                'specialization': 'Systems Analysis',
                'years_experience': 25,
                'is_active': True
            }
        ],
        'mission_status': 'planned',
        'budget_millions': 4626.0
    },
    {
        'mission_id': 'M2024_EUROPA',
        'mission_name': 'Europa Colony Mission',
        'destination': 'Europa',
        'launch_date': '2024-02-07T00:00:00',
        'duration_days': 666,
        'crew': [
            {
                'member_id': 'CM021',
                'name': 'Lisa Garcia',
                'rank': 'captain',
                'age': 36,
                'specialization': 'Medical Officer',
                'years_experience': 2,
                'is_active': True
            },
            {
                'member_id': 'CM022',
                'name': 'John Garcia',
                'rank': 'cadet',
                'age': 46,
                'specialization': 'Security',
                'years_experience': 3,
                'is_active': True
            },
            {
                'member_id': 'CM023',
                'name': 'Michael Johnson',
                'rank': 'officer',
                'age': 54,
                'specialization': 'Research',
                'years_experience': 30,
                'is_active': True
            },
            {
                'member_id': 'CM024',
                'name': 'Sarah Rodriguez',
                'rank': 'lieutenant',
                'age': 54,
                'specialization': 'Research',
                'years_experience': 30,
                'is_active': True
            },
            {
                'member_id': 'CM025',
                'name': 'Maria Smith',
                'rank': 'cadet',
                'age': 38,
                'specialization': 'Communications',
                'years_experience': 4,
                'is_active': True
            }
        ],
        'mission_status': 'planned',
        'budget_millions': 4976.0
    }
]


class Rank(Enum):
    CADET = "cadet"
    OFFICIER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMenber(BaseModel):
    member_id: Annotated[str, Field(strict=True, min_length=3, max_length=10)]
    name: Annotated[str, Field(strict=True, min_length=2, max_length=50)]
    rank: Rank
    age: Annotated[int, Field(strict=True, ge=18, le=80)]
    specialization: Annotated[str, Field(strict=True, min_length=3, max_length=30)]
    years_experience: Annotated[int, Field(strict=True, ge=0, le=50)]
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: Annotated[str, Field(strict=True, min_length=5, max_length=15)]
    mission_name: Annotated[str, Field(strict=True, min_length=3, max_length=100)]
    destination: Annotated[str, Field(strict=True, min_length=3, max_length=50)]
    launch_date: datetime
    duration_days: Annotated[int, Field(strict=True, ge=1, le=3650)]
    crew: Annotated[List[CrewMenber], Field(strict=True, min_length=1, max_length=12)]
    mission_status: str = "planned"
    budget_millions: Annotated[float, Field(strict=True, ge=1.0, le=10000.0)]

    @model_validator(mode='after')
    def verif_ID(self) -> Self:
        if (self.mission_id[0] != "M"):
            raise ValueError("Mission ID must start with 'M'")
        return self

    @model_validator(mode='after')
    def check_for_capt_or_com(self) -> Self:
        for crew in self.crew:
            if ((crew.rank.value == Rank.CAPTAIN.value) or (crew.rank.value == Rank.COMMANDER.value)):
                return self
        raise ValueError("Must have at least one Commander or Captain")

    @model_validator(mode='after')
    def check_experience(self) -> Self:
        experienced_crew = 0
        for crew in self.crew:
            if (crew.years_experience > 5):
                experienced_crew += 1
        percentage = round((100 * experienced_crew) / len(self.crew))
        if (percentage < 50 and self.duration_days > 365):
            raise ValueError("Long missions need 50% experienced crew")
        return self

    @model_validator(mode='after')
    def check_activity(self):
        for crew in self.crew:
            if (crew.is_active is False):
                raise ValueError("All crew members must be active")
        return self


def print_infos(mission: SpaceMission):
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    for crew in mission.crew:
        print(f"- {crew.name} ({crew.rank.value}) - {crew.specialization}")
    print()


def main() -> None:
    print("====================================")
    try:
        mission1 = SpaceMission(**SPACE_MISSIONS[0])
        print_infos(mission1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()

    print("====================================")
    try:
        mission1 = SpaceMission(**SPACE_MISSIONS[1])
        print_infos(mission1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()

    print("====================================")
    try:
        mission1 = SpaceMission(**SPACE_MISSIONS[2])
        print_infos(mission1)
    except (ValidationError, ValueError) as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])
        print()


if (__name__ == "__main__"):
    main()
