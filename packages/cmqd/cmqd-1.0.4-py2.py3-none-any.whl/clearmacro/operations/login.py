class Login:
    def _login(self, username, password):
        data = {
            "email": username,
            "password": password,
        }

        request_params = {
            "method": "post",
            "path": "/api/auth/login",
            "json": data,
        }

        self.configuration.logger.debug("Executing operation login: %s", request_params)

        self._emit('operation:login', request_params)

        response = self._request(**request_params)

        return response
