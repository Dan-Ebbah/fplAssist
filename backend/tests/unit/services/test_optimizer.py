import unittest
from unittest import mock
import pulp
from app.services.optimizer import optimize_xi, FORMATIONS, POS_ORDER

class TestOptimizer(unittest.TestCase):
    def setUp(self):
        """Set up test data that can be reused across tests."""
        # Create a simple test dataset of player projections
        self.test_projections = [
            {
                "player": {
                    "id": 1,
                    "name": "Test GK 1",
                    "position": "GK",
                    "price": 5.0,
                    "club_id": 1
                },
                "xpts_mean": 4.5
            },
            {
                "player": {
                    "id": 2,
                    "name": "Test GK 2",
                    "position": "GK",
                    "price": 4.5,
                    "club_id": 2
                },
                "xpts_mean": 3.5
            },
            # Defenders
            {
                "player": {
                    "id": 3,
                    "name": "Test DEF 1",
                    "position": "DEF",
                    "price": 6.0,
                    "club_id": 3
                },
                "xpts_mean": 5.0
            },
            {
                "player": {
                    "id": 4,
                    "name": "Test DEF 2",
                    "position": "DEF",
                    "price": 5.5,
                    "club_id": 4
                },
                "xpts_mean": 4.8
            },
            {
                "player": {
                    "id": 5,
                    "name": "Test DEF 3",
                    "position": "DEF",
                    "price": 5.0,
                    "club_id": 5
                },
                "xpts_mean": 4.2
            },
            {
                "player": {
                    "id": 6,
                    "name": "Test DEF 4",
                    "position": "DEF",
                    "price": 4.0,
                    "club_id": 6
                },
                "xpts_mean": 3.8
            },
            {
                "player": {
                    "id": 7,
                    "name": "Test DEF 5",
                    "position": "DEF",
                    "price": 4.0,
                    "club_id": 7
                },
                "xpts_mean": 3.5
            },
            # Midfielders
            {
                "player": {
                    "id": 8,
                    "name": "Test MID 1",
                    "position": "MID",
                    "price": 10.0,
                    "club_id": 8
                },
                "xpts_mean": 8.0
            },
            {
                "player": {
                    "id": 9,
                    "name": "Test MID 2",
                    "position": "MID",
                    "price": 9.5,
                    "club_id": 9
                },
                "xpts_mean": 7.5
            },
            {
                "player": {
                    "id": 10,
                    "name": "Test MID 3",
                    "position": "MID",
                    "price": 8.0,
                    "club_id": 10
                },
                "xpts_mean": 7.0
            },
            {
                "player": {
                    "id": 11,
                    "name": "Test MID 4",
                    "position": "MID",
                    "price": 7.5,
                    "club_id": 11
                },
                "xpts_mean": 6.5
            },
            {
                "player": {
                    "id": 12,
                    "name": "Test MID 5",
                    "position": "MID",
                    "price": 6.5,
                    "club_id": 12
                },
                "xpts_mean": 5.5
            },
            # Forwards
            {
                "player": {
                    "id": 13,
                    "name": "Test FWD 1",
                    "position": "FWD",
                    "price": 11.0,
                    "club_id": 13
                },
                "xpts_mean": 9.0
            },
            {
                "player": {
                    "id": 14,
                    "name": "Test FWD 2",
                    "position": "FWD",
                    "price": 10.0,
                    "club_id": 14
                },
                "xpts_mean": 8.5
            },
            {
                "player": {
                    "id": 15,
                    "name": "Test FWD 3",
                    "position": "FWD",
                    "price": 9.0,
                    "club_id": 15
                },
                "xpts_mean": 7.8
            },
        ]

    @mock.patch('pulp.LpProblem.solve')
    @mock.patch('pulp.value')
    def test_optimize_xi_formation(self, mock_pulp_value, mock_solve):
        """Test if the optimizer respects the selected formation."""
        # Mock pulp.value to return 1 (selected) for certain players based on a 3-4-3 formation
        def side_effect(var):
            # GK
            if var == 1: return 1  # GK1 selected
            # DEF - 3 selected
            elif var in [3, 4, 5]: return 1
            elif var in [6, 7]: return 0
            # MID - 4 selected
            elif var in [8, 9, 10, 11]: return 1
            elif var == 12: return 0
            # FWD - 3 selected
            elif var in [13, 14, 15]: return 1
            # Captain selection
            elif var == 13: return 1  # FWD1 as captain
            else: return 0
        
        mock_pulp_value.side_effect = side_effect
        
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=100.0, formation="3-4-3"
        )
        
        # Check correct number of players selected
        self.assertEqual(len(xi), 11)
        
        # Verify formation constraints are respected
        positions = [player["player"]["position"] for player in xi]
        self.assertEqual(positions.count("GK"), 1)
        self.assertEqual(positions.count("DEF"), 3)
        self.assertEqual(positions.count("MID"), 4)
        self.assertEqual(positions.count("FWD"), 3)
        
        # Check captain selection
        self.assertEqual(cap_id, 13)
        
        # Check if bench has exactly 4 players
        self.assertEqual(len(bench), 4)

    def test_optimize_xi_integration(self):
        """Real integration test with actual optimization."""
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=100.0, formation="3-4-3"
        )
        
        # Check if we get 11 players in the starting XI
        self.assertEqual(len(xi), 11)
        
        # Check if we get 4 players on the bench
        self.assertEqual(len(bench), 4)
        
        # Check if total cost is under or equal to budget
        self.assertLessEqual(total_cost, 100.0)
        
        # Ensure formation constraints are respected
        positions = [player["player"]["position"] for player in xi]
        self.assertEqual(positions.count("GK"), 1)
        self.assertEqual(positions.count("DEF"), 3)
        self.assertEqual(positions.count("MID"), 4)
        self.assertEqual(positions.count("FWD"), 3)
    
    def test_player_locks_and_excludes(self):
        """Test if player lock and exclude constraints work properly."""
        # Lock player ID 2 (backup GK)
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=100.0, formation="3-4-3", 
            lock_player_ids=[2]
        )
        
        # Ensure locked player is in the XI
        locked_player_in_xi = any(p["player"]["id"] == 2 for p in xi)
        self.assertTrue(locked_player_in_xi)
        
        # Exclude player ID 8 (highest scoring midfielder)
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=100.0, formation="3-4-3", 
            exclude_player_ids=[8]
        )
        
        # Ensure excluded player is not in the XI
        excluded_player_in_xi = any(p["player"]["id"] == 8 for p in xi)
        self.assertFalse(excluded_player_in_xi)
    
    def test_different_formations(self):
        """Test if different formations work correctly."""
        # Test 3-5-2 formation
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=100.0, formation="3-5-2"
        )
        
        # Check formation constraints
        positions = [player["player"]["position"] for player in xi]
        self.assertEqual(positions.count("GK"), 1)
        self.assertEqual(positions.count("DEF"), 3)
        self.assertEqual(positions.count("MID"), 5)
        self.assertEqual(positions.count("FWD"), 2)
        
        # Test 4-4-2 formation
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=100.0, formation="4-4-2"
        )
        
        # Check formation constraints
        positions = [player["player"]["position"] for player in xi]
        self.assertEqual(positions.count("GK"), 1)
        self.assertEqual(positions.count("DEF"), 4)
        self.assertEqual(positions.count("MID"), 4)
        self.assertEqual(positions.count("FWD"), 2)
    
    def test_budget_constraint(self):
        """Test if the budget constraint is respected."""
        # Set a very low budget to force cheaper selections
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            self.test_projections, budget=60.0, formation="3-4-3"
        )
        
        # Check if total cost is under or equal to budget
        self.assertLessEqual(total_cost, 60.0)
        
        # Set normal budget
        xi_normal, bench_normal, cap_id_normal, total_cost_normal, exp_pts_normal = optimize_xi(
            self.test_projections, budget=100.0, formation="3-4-3"
        )
        
        # Expected points should be higher with more budget
        self.assertGreaterEqual(exp_pts_normal, exp_pts)
    
    def test_club_constraint(self):
        """Test if the club constraint (max 3 players per club) is respected."""
        # Create test data with multiple players from the same club
        club_test_data = self.test_projections.copy()
        
        # Add 4 players from club 1 with good points
        for i in range(16, 20):
            club_test_data.append({
                "player": {
                    "id": i,
                    "name": f"Club 1 Player {i}",
                    "position": "DEF" if i < 18 else "MID",
                    "price": 5.0,
                    "club_id": 1
                },
                "xpts_mean": 7.0  # High points to encourage selection
            })
            
        xi, bench, cap_id, total_cost, exp_pts = optimize_xi(
            club_test_data, budget=100.0, formation="3-4-3"
        )
        
        # Count players from club 1
        club_1_players = sum(1 for p in xi if p["player"]["club_id"] == 1)
        
        # Check club constraint is respected
        self.assertLessEqual(club_1_players, 3)

if __name__ == "__main__":
    unittest.main()
