'''
@author Alessia Bussard
@description Handler for heart rate data from clients
'''


class HeartRateHandler:
    """Handler for heart rate requests from clients"""

    _game_handler = None

    def __init__(self, game_handler):
        self._game_handler = game_handler

    def handle(self, request, player_id):
        try:
            # Extract heart rate from request
            heart_rate = request.get_heart_rate()

            # Add detailed debug logging
            print("=========== HEART RATE DATA RECEIVED ===========")
            print(f"Received heart rate request from player: {player_id}")
            print(f"Heart rate value: {heart_rate:.1f} BPM")
            print("================================================")

            # Get the game object
            game = self._game_handler.get_game()
            if not game:
                # Create response
                from commands.responses.HeartRateResponse import HeartRateResponse
                return HeartRateResponse(False, "Game not initialized")

            # Get player from game
            player = game.get_player(player_id)
            if not player:
                # Create response
                from commands.responses.HeartRateResponse import HeartRateResponse
                return HeartRateResponse(False, f"Player {player_id} not found")

            # Store heart rate in player
            player.set_heart_rate(heart_rate)

            # Log heart rate
            print(f"Received heart rate: {heart_rate:.1f} BPM from player {player_id}")

            # Create success response
            from commands.responses.HeartRateResponse import HeartRateResponse
            return HeartRateResponse(True, "Heart rate data processed successfully")

        except Exception as e:
            print(f"Error processing heart rate data: {e}")
            # Create error response
            from commands.responses.HeartRateResponse import HeartRateResponse
            return HeartRateResponse(False, f"Error processing heart rate data: {str(e)}")

