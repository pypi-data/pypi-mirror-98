class GetSignalsForMarketId:
    def get_signals_for_market_id(self, class_id: int):
        """
        Function to retrieve the list of signals available for the given market.

        Args:
            class_id (int): One of the valid markets. Available options are the "classId" fields from the list of market objects obtained by calling the get_all_markets method.

        Returns:
            JSON list of signal objects.
        """
        request_params = {"method": "get", "path": f"/api/signals/markets/{class_id}"}

        response = self._request(**request_params)

        return response
