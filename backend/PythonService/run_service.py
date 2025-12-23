#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import uvicorn
from main import app

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
