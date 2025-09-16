from Reports import Reports
import os
from IPEDS import IPEDS

class IPEDS_Fall (IPEDS):
    def __init__(self):
        super().__init__(folder='IPEDS_Fall', report="2025-09-15-IPEDS Fall Survey")

