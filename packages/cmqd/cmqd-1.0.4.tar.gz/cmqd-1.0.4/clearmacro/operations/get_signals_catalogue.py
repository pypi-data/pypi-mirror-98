class GetSignalsCatalogue:
    def get_signals_catalogue(self):
        """
        Function to retrieve the list of all signals.

        Returns:
            JSON list of signal objects.
        """
        request_params = {"method": "get", "path": "/api/signals/catalogue"}

        response = self._request(**request_params)

        return response
