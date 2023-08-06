class GetMarketsForSignalId:
    def get_markets_for_signal_id(self, signal_id: int):
        """
        Function to retrieve the list of markets corresponding to the passed signal id.

        Args:
            signal_id (int): One of the signals. Available options are the "signalId" fields from the list of signals objects obtained by calling the get_signals_catalogue method.

        Returns:
            JSON list of market objects.
        """
        request_params = {"method": "get", "path": f"/api/signals/{signal_id}/markets"}

        response = self._request(**request_params)

        return response
