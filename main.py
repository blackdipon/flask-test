#!/usr/bin/env python3.9

from website import creat_app

app = creat_app()

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=443, debug=False)
