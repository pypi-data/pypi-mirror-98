# -*- coding = UTF-8 -*-
# Author   :buxiubuzhi
# File     : case.py
# project  : UIAutoProject
# time     : 2020/12/4 18:05
# Describe : 
# ---------------------------------------
import pytest


class TestCase:

    @pytest.fixture(scope="function")
    def setUp(self, getdriver): ...
