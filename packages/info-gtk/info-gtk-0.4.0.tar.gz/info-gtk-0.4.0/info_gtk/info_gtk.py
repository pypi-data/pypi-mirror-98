#!/usr/bin/env python

import attr
import logging
import json
from bs4 import BeautifulSoup
from requests import Session
from typing import List, Optional

from . import DataIndividu
from . import StatusNuptk
from . import KelulusanSertifikasi
from . import RombonganBelajar
from .table_data import TableData


@attr.dataclass(slots=True)
class LoginData:
    userid: str
    password: str
    submit: str = "Login"
    mod: str = "cek_guru"
    metode: str = "Account"
    s: str = "990"


@attr.dataclass
class InfoGtk:
    email: str
    password: str
    dashboard: str = ""
    is_login: bool = False
    base_url: str = "https://info.gtk.kemdikbud.go.id/"

    def __attrs_post_init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._session = Session()
        self._soup: Optional[BeautifulSoup] = None
        self._data_individu: Optional[DataIndividu] = None
        self._status_nuptk: Optional[StatusNuptk] = None
        self._kelulusan_sertifikasi: Optional[KelulusanSertifikasi] = None
        self._rombongan_belajar: List[RombonganBelajar] = list()
        self._verify = False
        if not self.is_login and not self.dashboard:
            self.login()
        if not self.dashboard:
            self.dashboard = self.get_dashboard()

    @property
    def soup(self) -> BeautifulSoup:
        if self._soup:
            return self._soup
        self._soup = BeautifulSoup(self.dashboard, "html.parser")
        return self._soup

    @property
    def data_individu(self) -> DataIndividu:
        if self._data_individu:
            return self._data_individu
        table_data = TableData.makes(
            data=self.dashboard,
            locate="/*individu*/",
            offset=1,
            lstrip="try {var tabledata = ",
            rstrip=';putTable("#fit_individu",tabledata);} catch(err) {  };',
        )
        self._data_individu = DataIndividu.from_table_data(table_data)
        return self._data_individu

    @property
    def status_nuptk(self) -> StatusNuptk:
        if self._status_nuptk:
            return self._status_nuptk
        table_data = TableData.makes(
            data=self.dashboard,
            locate="/*arsip NUPTK*/",
            offset=1,
            lstrip="try { var tabledata = ",
            rstrip=';putTable("#fit_ArsipNuptk",tabledata);} catch(err) {  };',
        )
        self._status_nuptk = StatusNuptk.from_table_data(table_data)
        return self._status_nuptk

    @property
    def kelulusan_sertifikasi(self) -> KelulusanSertifikasi:
        if self._kelulusan_sertifikasi:
            return self._kelulusan_sertifikasi
        table_data = TableData.makes(
            data=self.dashboard,
            locate="/*arsip kelulusan*/",
            offset=1,
            lstrip="try {var tabledata = ",
            rstrip=';putTable("#fit_Kelulusan",tabledata);} catch(err) {  };',
        )
        self._kelulusan_sertifikasi = KelulusanSertifikasi.from_table_data(table_data)
        return self._kelulusan_sertifikasi

    @property
    def rombongan_belajar(self) -> List[RombonganBelajar]:
        if self._rombongan_belajar:
            return self._rombongan_belajar
        rombel_text = TableData.clean(
            data=self.dashboard,
            locate="/*Rombongan Belajar*/",
            offset=1,
            lstrip="try {var tabledata = ",
            rstrip=";putTabelRombonganBelajar(tabledata);} catch(err) {  };",
        )
        if rombel_text.endswith(",]"):
            rombel_text = rombel_text.rstrip(",]") + "]"
        rombel_data = json.loads(rombel_text)
        self._rombongan_belajar = RombonganBelajar.from_list(rombel_data)
        return self._rombongan_belajar

    def login(self, email: str = None, password: str = None, retry=0) -> bool:
        email = email or self.email
        password = password or self.password
        if self.is_login:
            self.logout()
        self._logger.debug("Getting login page")
        res = self._session.get(self.base_url + "/?s=999&pesan=", verify=self._verify)
        if not res.ok:
            self._logger.debug("Getting login page failed")
            if retry > 0:
                return self.login(email, password, retry)
            return False
        # Capthca
        data = LoginData(userid=email, password=password)
        headers = {"Referer": res.url}
        self._logger.debug("Trying to login")
        res = self._session.post(
            self.base_url,
            data=attr.asdict(data),
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
        self.is_login = res.status_code == 302
        return self.is_login

    def get_dashboard(self) -> str:
        res = self._session.get(self.base_url + "dashboard", verify=self._verify)
        if res.status_code != 404 or not res.text:
            return ""
        return res.text

    def logout(self) -> bool:
        res = self._session.get(self.base_url + "auth/logout", verify=self._verify)
        return res.ok
