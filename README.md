# scroll_me
Python bot that scrolls

# Dependencies
Run `python3 -m pip install requirements.pip` from project folder

# Usage
Start the program
`python3 scroll_me.py`

Default shortcut to start scrolling `ctrl + shift + < + >`

Shortcut to terminate program `ctrl + shift + k + l`

Scrolling can be stop by moving the mouse any time.

# Config
Following properties could be specified in config (default config attached)

```
{
  "HOT_KEYS": {
    "START_SCROLLING": "ctrl + shift + < + >",
    "TERMINATE_PROGRAM": "ctrl + shift + k + l"
  }
  "SLEEP_TIME_BETWEEN_SCROLLS": 1.5,
  "CLICKS_TO_SCROLL": 3
}