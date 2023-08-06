import os

from kloppy import OptaSerializer
from kloppy.domain import (
    AttackingDirection,
    Period,
    Orientation,
    Provider,
    Player,
    Position,
    Ground,
)
from kloppy.domain.models.common import DatasetType


class TestOpta:
    def test_correct_deserialization(self):
        base_dir = os.path.dirname(__file__)

        serializer = OptaSerializer()

        with open(f"{base_dir}/files/opta_f24.xml", "rb") as f24_data, open(
            f"{base_dir}/files/opta_f7.xml", "rb"
        ) as f7_data:

            dataset = serializer.deserialize(
                inputs={"f24_data": f24_data, "f7_data": f7_data}
            )
        assert dataset.metadata.provider == Provider.OPTA
        assert dataset.dataset_type == DatasetType.EVENT
        assert len(dataset.events) == 17
        assert len(dataset.metadata.periods) == 2
        assert dataset.events[10].ball_owning_team == dataset.metadata.teams[1]
        assert dataset.events[15].ball_owning_team == dataset.metadata.teams[0]
        assert (
            dataset.metadata.orientation == Orientation.ACTION_EXECUTING_TEAM
        )
        assert dataset.metadata.teams[0].name == "FC København"
        assert dataset.metadata.teams[0].ground == Ground.HOME
        assert dataset.metadata.teams[1].name == "FC Nordsjælland"
        assert dataset.metadata.teams[1].ground == Ground.AWAY

        player = dataset.metadata.teams[0].players[0]
        assert player.player_id == "111319"
        assert player.jersey_no == 21
        assert str(player) == "Jesse Joronen"
        assert player.position.position_id == "1"
        assert player.position.name == "Goalkeeper"

        assert dataset.metadata.periods[0] == Period(
            id=1,
            start_timestamp=1537714933.608,
            end_timestamp=1537717701.222,
            attacking_direction=AttackingDirection.NOT_SET,
        )
        assert dataset.metadata.periods[1] == Period(
            id=2,
            start_timestamp=1537718728.873,
            end_timestamp=1537721737.788,
            attacking_direction=AttackingDirection.NOT_SET,
        )
