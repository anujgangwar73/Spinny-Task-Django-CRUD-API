# Spinny-Task-Django-CRUD-API

Title:

API Service for CRUD



Description

Consider a store which has an inventory of boxes which are all cuboid(which have length, breadth and height). Each Cuboid has been added by a store employee who is associated as the creator of the box even if it is updated by any user later on.



Tasks:

0. Data Modelling

   Build minimal Models required for the such a store. You can use contrib modules for necessary models(for eg: users)



Build api for the following specifications:

1. Add Api:

   Adding a box with given dimensions(length breadth and height).

   Adding user should be automatically associated with the box and shall not be overridden

   Permissions:

         User should be logged in and should be staff to add the box



2. Update Api:

   Update dimensions of a box with a given id:

   Permissions:

         Any Staff user should be able to update any box. but shall not be able to update the creator or creation date



3. List all Api

   List all boxes available:

   Data For each box Required:

           1. Length

           2. width

           3. Height

           4. Area

           5. Volume

           6. Created By :  (This Key shall only be available if requesting user is staff)

           7. Last Updated :  (This Key shall only be available if requesting user is staff)

   Permissions:

           Any user shall be able to see boxes in the store

   Filters:

           1. Boxes with length_more_than or length_less_than

           2. Boxes with breadth_more_than or breadth_less_than

           3. Boxes with height_more_than or height_less_than

           4. Boxes with area_more_than or area_less_than

           5. Boxes with volume_more_than or volume_less_than

           6. Boxes created by a specific user by username

           7. Boxes created before or after a given date

4. List my boxes:

   List all boxes available created by me:

   Data For each box Required:

           1. Length

           2. width

           3. Height

           4. Area

           5. Volume

           6. Created By

           7. Last Updated

   Permissions:

           Only Staff user shall be able to see his/her created boxes in the store

   Filters:

           1. Boxes with length_more_than or length_less_than

           2. Boxes with breadth_more_than or breadth_less_than

           3. Boxes with height_more_than or height_less_than

           4. Boxes with area_more_than or area_less_than

           5. Boxes with volume_more_than or volume_less_than



4. Delete Api:

   Delete a box with a given id:

   Permissions:

        Only the creater of the box shall be able to delete the box.



Conditions to be fulfilled on each add/update/delete:

Average area of all added boxes should not exceed A1

Average volume of all boxes added by the current user shall not exceed V1

Total Boxes added in a week cannot be more than L1

Total Boxes added in a week by a user cannot be more than L2

Values A1, V1, L1 and L2 shall be configured externally. You can choose 100, 1000, 100, and 50 as their respective default values.
