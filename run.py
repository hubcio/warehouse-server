# -*- encoding: utf-8 -*-

import os
from WarehouseServer import app, com, db, User

# ----------------------------------------
# launch
# ----------------------------------------


if __name__ == '__main__':
    com.start()
    if not os.path.exists('db.sqlite'):
        db.create_all()
        User.add_super_admin()
    app.run(debug=True, host='0.0.0.0', threaded=True)

