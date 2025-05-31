#!/usr/bin/env python3

from app.lib import Models
import app.tui as tui

Models.models_requirement()
tui.AIChatApp().run()