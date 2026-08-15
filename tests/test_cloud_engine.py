import unittest

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


if __name__ == "__main__":
    unittest.main()
