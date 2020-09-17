import source.controllers.api as web_interface

# from ..source.ui.web.controllers import api as web_interface


print("about to start the flask app...")
web_interface.app.run(host="127.0.0.1", port=5001)
