# -*- encoding: utf-8 -*-

import os
from WarehouseServer import app, ser, db, User

# ----------------------------------------
# launch
# ----------------------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    ser.run(port='COM1')
    if not os.path.exists('db.sqlite'):
        db.create_all()
        User.add_super_admin()
