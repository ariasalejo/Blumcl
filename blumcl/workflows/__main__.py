"""Permite ejecutar: python -m blumcl.workflows"""
from blumcl.workflows import __init__ as _w
if hasattr(_w, "menu"):
    _w.menu()
