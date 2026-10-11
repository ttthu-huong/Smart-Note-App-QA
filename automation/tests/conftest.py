"""Shared pytest configuration and fixtures for Smart Note App QA.

Centralizes test fixtures, device driver lifecycle, and screen precondition fixtures
following IEEE 829 & ISTQB standards to eliminate duplication across test suites.
"""
import sys
import pytest
from automation.core.device import SmartNoteDriver
from automation import config

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


@pytest.fixture(scope="session")
def driver():
    """Shared session-level SmartNoteDriver instance.
    
    Initializes device connection, ensures device wakefulness,
    and shares connection across all tests in the session.
    """
    drv = SmartNoteDriver()
    drv.ensure_device_ready()
    return drv


@pytest.fixture(scope="session")
def device(driver):
    """Direct access to uiautomator2 Device instance."""
    return driver.device


@pytest.fixture(scope="function")
def ensure_home(driver):
    """Function-level fixture ensuring the app is at HomeScreen before a test."""
    driver.ensure_home_screen()
    return driver


@pytest.fixture(scope="function")
def ensure_login(driver):
    """Function-level fixture ensuring the app is at LoginScreen before a test."""
    driver.ensure_login_screen()
    return driver
