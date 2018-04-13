# -*- encoding: utf-8 -*-

import os
from WarehouseServer import app, com, db, User, servo, path

# ----------------------------------------
# launch
# ----------------------------------------


if __name__ == '__main__':
    com.start()  # TODO comment this if running on local pc
    print "com started"
    servo.start()
    print "servo started"
    path.start()
    print "path started"

    if not os.path.exists('db.sqlite'):
        db.create_all()
        User.add_super_admin()
    app.run(debug=True, host='192.168.1.122', use_reloader=False, threaded=True)
    print "flask started"







