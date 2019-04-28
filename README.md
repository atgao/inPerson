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

3. ~Account menu~
    * ~UI - display name~
    * ~UI - Logout~
    * ~redirect - Logout~

4. ~Followers/Following menu~
    * ~request - remove follower~ 
    * ~request - remove following~  
    * ~UI - add buttons with requests to UI~

5. Display Schedules
    * ~request - get followers schedule~
    * ~UI - display schedule~
    * actual schedule displaying (with overlaying and everything)
        * ~display own schedule~
        * display others' schedules
        * UI - display/ remove following's schedule

6. Classes menu
    * ~request - search for classes~
    * ~UI - add in sidebar classes menu~ 
        * ~search bar~
        * ~display list results~ 
    * ->-> Later Later: advanced search

7. ~All the things marked with /Later/~
    * ~follow request already sent/ following~

8. Handle errors             -> <3 Alice working on it

9. Testing

10. ~Deploy~

## Others - not urgent, probably not in MVP
11. Later Later -- in order:
    * classes advanced search

12. Not as important imo but can do:
    * request - block users
    * request - get blocked user
    * UI - display blocked users

13. After one time events are implemented on backend:
    * add custom one time events (remove part where i remove the option in Calendar.js)
    * import google cal

## ~UI -- B I G problems (how did it even end up like this wtfff)~ ->  nvm we GUCCI
* ~Navbar: Make *Follow requests* (and Account Menu) displayed vertically not horizontally~
* ~Calendar form display weirddd~
* ~Content shift on opening menu~
* ~Make it not look horrendous on mobile (will prob just make an app for it tho over the summer)~

