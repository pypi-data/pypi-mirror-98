from actionpack.procedure import Procedure

from multiprocessing import ProcessPoolExecutor
from typing import List


class Plan:

    def __init__(self, *procedures: List[Procedure]):
        self.procedures = procedures

    def execute(self):
        pass
