"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['voicecode.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'applogo.icns',
    'argv_emulation': True,
    'packages': ['pyaudio', 'speech_recognition', 'pyperclip', 'pyautogui'],
    'includes': ['pyaudio', 'speech_recognition', 'pyperclip', 'pyautogui']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)