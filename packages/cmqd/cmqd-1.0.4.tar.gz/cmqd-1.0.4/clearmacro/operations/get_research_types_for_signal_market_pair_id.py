class GetResearchTypesForSignalMarketPairId:
    def get_research_types_for_signal_market_pair_id(self, signal_id: int, market_id: int):
        """
        Function to retrieve the list of research types corresponding to the passed signal id and market id.

        Args:
            signal_id (int): One of the signals. Available options are the "signalId" fields from the list of signal objects obtained by calling the get_signals_catalogue method.
            market_id (int): One of the valid markets for the above signal. Available options are the "classId" fields from the list of market objects obtained by calling the get_markets_for_signal_id(signal_id) method.

        Returns:
            JSON list of research type objects.
        """
        request_params = {
            "method": "get",
            "path": f"/api/signals/{signal_id}/markets/{market_id}/researchtypes",
        }

        response = self._request(**request_params)

        return response
