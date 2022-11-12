"""Manage your daily journals"""
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "0.0.0"  # fallback if package hasn't been `pip install`ed
