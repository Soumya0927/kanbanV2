# Local Setup
- Make sure you have the necessary requirements installed and updated, mentioned in the requirements.txt file

# Local Development Run
- Simply run app.py present in backend folder , it will initiate the flask app in development. 
- Then run frontend folder by using `npm run serve` command , it will initiate the vue app in development. 
- For `Mailhog`, `Celery`, `Celery beat` run their respective commands in separate terminals to initiate them. 


# Folder Structure

- `database.sqlite3` has the sqlite3 DB.
- `app.py` is where our application code is
 - `frontend-components` - contains all the vue component files
 - `assets` contains imgs used in app

"mad2"
    ├── readme.md
    ├── projectreport.pdf
    ├──`backend Folder`
            ├── app.py
            └── database.sqlite3
            └── api
                ├──api.py
            ├── data_access.py
            └── flask_cache.py
            └── flask_celery1.py
            └── gen_email.py
            └── models.py
            └── report.html

    ├──`frontend Folder`
            ├── public
                    ├── index.html
            ├── src
                ├── assets
                └── components
                        └── createCard.vue
                        └── createList.vue
                        ├── editCard.vue
                        └── editList.vue
                        └── HelloWorld.vue
                        └── LoginUser.vue
                        └── NavBar.vue
                        └── NavBardash.vue
                        └── SignupUser.vue
                        └── summary.vue
                ├── router
                        ├──index.js
                └── store
                └── views
                        ├── AboutView.vue
                        └── HomeView.vue
                ├── App.vue
                └── main.js


  
   
