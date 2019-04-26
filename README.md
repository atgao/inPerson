# inPerson
Capstone project for COS333 Spring 2019
Team Members: Alice Gao, Anna Qin, Michael Peng, Ioana Teodorescu
Website: nperson.herokuapp.com

To run the project initially locally run in the base folder:

    npm install
    pip install -r requirements.txt
    ./runserver.sh

## Frontend TODOS (for Ioana)
1. ~Search bar~
    * ~UI - popup~
    * ~request - search~
    * ~UI - follow button~
    * ~request - follow user~
    * ~-> Later: follow request already sent/ following~

2. ~Follow Requests menu~
    * ~request - get follow requests~
    * ~UI - accept, ignore~
    * ~request - accept follow request~
    * ~request - delete follow request~ 
    * ~request - ignore follow request~

3. Account menu
    * ~UI - display name~
    * ->-> Later Later: UI - display blocked users
    * ->-> Later Later: request - get blocked users

4. ~Followers/Following menu~
    * ~request - remove follower~ 
    * ~request - remove following~  
    * ~UI - add buttons with requests to UI~

5. Display Schedules
    * request - get followers schedule
    * UI - display schedule

6. Classes menu
    * ~request - search for classes~
    * ~UI - add in sidebar classes menu~        --> not tested
        * ~search bar~
        * ~display list results~ 
    * ->-> Later Later: advanced search

7. ~All the things marked with /Later/~
    * ~follow request already sent/ following~

8. Handle errors             -> <3 Alice working on it

9. Testing

10. ~Deploy~

11. Later Later -- in order: 
    * classes advanced search
    * request - block users
    * request - get blocked user
    * UI - display blocked users

## UI -- B I G problems (how did it even end up like this wtfff)
* Navbar: Make *Follow requests* (and Account Menu) displayed vertically not horizontally
* Calendar form display weirddd
* Content shift on opening menu
* Make it not look horrendous on mobile (will prob just make an app for it tho over the summer)

