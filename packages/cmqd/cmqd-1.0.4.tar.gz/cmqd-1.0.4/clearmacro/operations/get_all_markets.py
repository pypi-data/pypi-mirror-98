class GetAllMarkets:
    def get_all_markets(self):
        """
        Function to retrieve the list of all markets.

        Returns:
            JSON list of market objects.
        """
        request_params = {"method": "get", "path": "/api/signals/markets"}

        response = self._request(**request_params)

        return response
