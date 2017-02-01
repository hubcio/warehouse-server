# -*- encoding: utf-8 -*-

import os
from WarehouseServer import app, com, db, User

# ----------------------------------------
# launch
# ----------------------------------------


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
        User.add_super_admin()
    #com.run(port='COM3')
    app.run(debug=True, host='0.0.0.0')


