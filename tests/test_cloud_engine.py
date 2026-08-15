import unittest
from unittest.mock import patch

from api import index as cloud


class CloudEngineTests(unittest.TestCase):
    def setUp(self):
        self.state = cloud.game.fresh_state()
        self.state["room"] = "ABCDE"

    def test_host_action_mutates_isolated_state(self):
        cloud.set_engine_state(self.state)
        cloud.game.handle_action({"type": "addTeam", "name": "Las Estrellas"})
        self.assertEqual(cloud.game.STATE["room"], "ABCDE")
        self.assertIn("Las Estrellas", [team["name"] for team in cloud.game.STATE["teams"]])

    def test_spectator_never_receives_secret_mime_prompt(self):
        self.state.update({
            "game": {"id": "mimica", "difficulty": "facil", "duration": 60, "rounds": 1},
            "status": "playing",
            "activePlayer": "player-one",
            "prompt": {"prompt": "Elefante", "category": "Animales"},
        })
        payload = cloud.public_payload(self.state, "__spectator__")
        self.assertEqual(payload["prompt"], "Contenido secreto en el celular del participante")

    def test_player_receives_only_own_who_am_i_assignment(self):
        self.state.update({
            "game": {"id": "quien_soy"},
            "whoAmIAssignments": {
                "player-one": {"prompt": "Batman"},
                "player-two": {"prompt": "Elsa"},
            },
        })
        payload = cloud.public_payload(self.state, "player-one")
        self.assertEqual(list(payload["whoAmIAssignments"]), ["player-one"])

    def test_only_room_owner_is_host(self):
        room = {"owner_id": "admin-one"}
        self.assertTrue(cloud.verify_host(room, {"id": "admin-one"}))
        self.assertFalse(cloud.verify_host(room, {"id": "admin-two"}))
        self.assertFalse(cloud.verify_host(room, None))

    @patch.object(cloud, "paged_rows")
    def test_statistics_are_grouped_by_game(self, rows):
        rows.return_value = [
            {"id": "1", "game": "trivia", "winner_team_id": "a"},
            {"id": "2", "game": "trivia", "winner_team_id": None},
            {"id": "3", "game": "mimica", "winner_team_id": "b"},
        ]
        stats = cloud.stats_for_user("admin-one")
        self.assertEqual(stats["totalGames"], 3)
        self.assertEqual(stats["gamesWithWinner"], 2)
        self.assertEqual(stats["byGame"]["trivia"], {"played": 2, "withWinner": 1})

    @patch.object(cloud, "db_request")
    def test_completed_game_is_saved_once_by_session_id(self, request):
        room = {"id": "room-id", "owner_id": "admin-id", "locale": "es"}
        state = {
            "status": "game_complete", "game": {"id": "trivia", "sessionId": "session-id", "rounds": 2},
            "winnerTeam": {"id": "sol", "name": "Equipo Sol"},
            "teams": [{"id": "sol", "name": "Equipo Sol", "score": 5}], "players": [{"id": "p1"}],
        }
        cloud.save_completed_session(room, state)
        payload = request.call_args.args[2]
        self.assertEqual(payload["id"], "session-id")
        self.assertEqual(payload["owner_id"], "admin-id")
        self.assertEqual(payload["winner_team_name"], "Equipo Sol")


if __name__ == "__main__":
    unittest.main()
