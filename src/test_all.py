#!/usr/bin/env python3

from test_ports import test_all as ports_test_all
from test_ula import test_all as ula_test_all
from test_sequencial import test_all as sequencial_test_all

if __name__ == "__main__":
    ports_test_all()
    ula_test_all()
#   sequencial_test_all()
