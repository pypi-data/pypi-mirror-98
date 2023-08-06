class GetSignalUniverses:
    def get_signal_universes(self):
        """
        Function to retrieve the signal universes.

        Returns:
            JSON list of universe objects.
        """
        request_params = {"method": "get", "path": "/api/signals/universes"}

        response = self._request(**request_params)

        return response
