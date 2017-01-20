# Warehouse server API
## /api/device/state - GET - returns JSON - "admin","user"
Returns current state of device.

- x - current X position in mm
- y - current Y position in mm
- z - current Z  position in mm
- current_x - x axis current in mA
- current_y - y axis current in mA
- current_z - z axis current in mA

## /api/device/cells/<int:id> - GET - returns JSON - "admin","user"
Returns state of desired cell in JSON format.
Fields:
- id - cells id
- rfid - cells rfid
- owner - current cells owner
- x - position X
- y - position Y
- z - position Z
- sharedWith - array of usernames except owner
- lastAction - timestamp
- shortDescription - maximum 127 chars array
- longDescription - maximum 1023 chars array

## /api/device/cells/<int:id> - POST - "admin","user"
Used to get single cell from warehouse.
Fields:
- id - id of cell that user wants to get


.................................................................................
 
## /api/device/cells/all - GET - returns JSON - "admin","user"

Returns array of all cells owned by person performing request, formatted in /api/warehouse/state/<int:id> way.




# Warehouse users API
Each method returns JSON if was executed successfully. Every role (admin, user, etc.) can create new users that have role "user".

## /api/users/all - GET - JSON
Returns all users in JSON format. Requires ... role.
Fields:
- username

## /api/users/<int:id> - GET - JSON
Returns username of user 


#
