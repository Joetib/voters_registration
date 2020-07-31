This is a project to learn more about web development with django. Just a little actually.



# Endpoints

Note that:
`<int:id>` means an integer that represents an id

- `admin/`      This is not a rest endpoint
- `user/`       Returns the details of the user

    methods allowed:
    * GET

- `user/profile/`

    methods allowed:
    * GET 
    * PUT



- `regions/` returns a list of all regions and their details
    
    methods allowed:
    * GET
- `regions/<int:region_id>/districts/` returns a list of all districts
    
    methods allowed:
    * GET

- `district/<int:district_id>/registration-centers/` returns a list of all registration centers and their details in a district
    
    methods allowed:
    * GET

- `registration-center/<int:registration_center_id>/available-days/` Returns the available Days that a particular registration center will work.
    
    methods allowed:
    * GET

- `registration-center/<int:registration_center_id>/day/<int:day_id>/slots/available/` Returns the available slots in a particular day at a registration center.
    
    methods allowed:
    * GET

- `appointment/create/` Books an appointment
    
    methods allowed:
    * POST (The posted data should include the appointment_slot as an id)

- `appointment/` Gets and edits details of an appointment of the current user
    
    methods allowed:
    * GET
    * PUT

- `rest-auth/password/reset/`
- `rest-auth/password/reset/confirm/`  
- `rest-auth/login/`  
- `rest-auth/logout/`  
- `rest-auth/user/`  
- `rest-auth/password/change/` 