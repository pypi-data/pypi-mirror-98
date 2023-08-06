# -*- encoding: utf-8 -*-
#
# (c) 2021 David Garcia (@dgarcia360)
# This code is licensed under MIT license (see LICENSE.md for details)

def split_list_by_commas(a):
    return [s.strip() for s in (a or "").split(",") if s.strip()]
