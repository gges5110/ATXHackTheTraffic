# ATXHackTheTraffic

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4a7ff1eb19fa47ec98984815942a20c0)](https://www.codacy.com/app/gges5110/ATXHackTheTraffic?utm_source=github.com&utm_medium=referral&utm_content=gges5110/ATXHackTheTraffic&utm_campaign=badger)

This is a project for travel time prediction in Austin, TX using the dataset provided by the City of Austin.

# Server Routes
They are stored inside [views](https://github.com/gges5110/ATXHackTheTraffic/tree/master/views) folder. To add a new route, 
  1. Add a new .py file in views/ 
  2. Import it into run.py
  3. Register the blueprint to our app.

The new .py file should have a format like this:
```python
from flask import Blueprint

routeName = Blueprint('routeName', __name__)

@routeName.route("/routeName", methods=['GET'])
def routeName_function():
    return "The new route page."
```

# Tests
Tests are put in [tests](https://github.com/gges5110/ATXHackTheTraffic/tree/master/tests) folder. 
If you want to import something from the top level module, add it to [context.py](https://github.com/gges5110/ATXHackTheTraffic/blob/master/tests/context.py)
and then import to your test file.
