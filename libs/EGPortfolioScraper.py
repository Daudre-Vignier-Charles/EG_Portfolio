#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests

class Scraper:
    #URL_REQUEST = "https://estateguru.co/portal/portfolio/ajaxLoadInvestorPrimaryLoansTable?max=1000"
    URL_REQUEST = "https://estateguru.co/portal/portfolio/downloadInvestorFundedGroupLoans.excel?extension=xls&userId=78860&loanStatusFromTab=FUNDED_LOANS"
    URL_LOGIN = "https://estateguru.co/portal/login/authenticate"

    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        self._connect()

    def _connect(self):
        """Connect to EG using login and password"""
        self.session.post(Scraper.URL_LOGIN, data={"username" : self.username, "password" : self.password}, headers=dict(referer=Scraper.URL_LOGIN))

    def get_portfolio(self):
        """download page"""
        return self.session.get(self.URL_REQUEST).content
