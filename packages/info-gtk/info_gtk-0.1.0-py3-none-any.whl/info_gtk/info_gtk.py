#!/usr/bin/env python

import logging
from requests import Session


class InfoGtk:
    BASE_URL: str = "https://info.gtk.kemdikbud.go.id/"

    def __init__(self, email: str, password: str):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._email = email
        self._password = password
        self._session = Session()
        self._dashboard = ""
        self._verify = False
        self.is_login = False
        if not self.is_login:
            self.is_login = self.login(email, password)
        if not self._dashboard:
            self._dashboard = self.get_dashboard()

    @property
    def dashboard(self) -> str:
        if not self._dashboard:
            self._dashboard = self.get_dashboard()
        return self._dashboard

    def login(self, email: str = None, password: str = None, retry=0) -> bool:
        email = email or self._email
        password = password or self._password
        if self.is_login:
            self.logout()
        self._logger.debug("Getting login page")
        res = self._session.get(self.BASE_URL + "/?s=999&pesan=", verify=self._verify)
        if not res.ok:
            self._logger.debug("Getting login page failed")
            if retry > 0:
                return self.login(email, password, retry)
            return False
        # Capthca
        data = {
            "userid": self._email,
            "password": self._password,
            "submit": "Login",
            "mod": "cek_guru",
            "metode": "Account",
            "s": "990",
        }
        headers = {"Referer": res.url}
        self._logger.debug("Trying to login")
        res = self._session.post(
            self.BASE_URL,
            data=data,
            allow_redirects=False,
            headers=headers,
            verify=self._verify,
        )
        if not res.status_code == 302:
            self._logger.debug("Login failed")
            if retry > 0:
                return self.login(email, password, retry)
            return False
        self._logger.debug("Login success")
        return res.status_code == 302

    def get_dashboard(self) -> str:
        if self._dashboard:
            return self._dashboard
        res = self._session.get(self.BASE_URL + "dashboard", verify=self._verify)
        if res.status_code != 404 or not res.text:
            return ""
        self._dashboard = res.text
        return ""

    def logout(self) -> bool:
        res = self._session.get(self.BASE_URL + "auth/logout", verify=self._verify)
        return res.ok
