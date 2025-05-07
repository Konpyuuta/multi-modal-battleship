'''
@author Alessia Bussard
@description Server-side response for heart rate requests
'''

# Use the correct import path for your server-side Response base class
from commands.responses.Response import Response
# Use the correct import path for your server-side RequestTypes
from commands.requests.RequestTypes import RequestTypes


class HeartRateResponse(Response):
    """Response for heart rate requests"""

    def __init__(self, success=True, message="Heart rate data received"):
        """
        Initialize a heart rate response

        Args:
            success (bool): Whether the heart rate data was successfully processed
            message (str): Response message
        """
        # Adapt this constructor to match your server's Response class structure
        super().__init__(RequestTypes.HEART_RATE)
        self._success = success
        self._message = message

    # Include any other methods required by your server's Response interface