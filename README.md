# AnotherLine: Your academic story

![Screenshot of AnotherLine homepage](http://www.clindgrencv.com/assets/img/outside/anotherline-readme.png "Screenshot of AnotherLine homepage")

## About

The AnotherLine app will offer scholars a way to add and update their CV/portfolio information online. From there, users can choose a CV template to showcase their work within the app, or, if the user has their own site hosted elsewhere, they can use their CV data via API endpoints to use with their own HTML/CSS/JS. Essentially, their data is open and can be exported and used as they so desire.

Additionally, scholars will be able to export their CV as a PDF. They will be able to export the entire CV or select desired elements to export as needed as a PDF.

## File Structure

<pre>anotherline-flask/
    .gitignore
    README.md
    config.py
    [your_config_var_name_file].py
    [your_sqlite_files].sqlite
    manage.py
    requirements.txt
    app/
        __init__.py
        decorators.py
        email.py
        models.py
        auth/
            __init__.py
            forms.py
            views.py
        main/
            __init__.py
            errors.py
            forms.py
            views.py
        static/
            assets/
                bootstrap/
                    ...
                css/
                    ...
                fonts/
                    ...
                img/
                    ...
                js/
                    ...
                lib/
                    ...
        templates/
            403.html
            404.html
            500.html
            _cvlist.html
            add_book.html
            base.html
            edit_book.html
            index.html
            login.html
            user.html
            __init__.py
            decorators.py
            email.y
            models.py
            auth/
                change_email.html
                change_password.html
                login.html
                register.html
                reset_password.html
                unconfirmed.html
                email/
                    [email templates]
            mail/
                new_user.html
                new_user.txt
    instance/
        ...
    migrations/
        ...
    tests/
        __init__.py
        test*.py
        test_basics.py
        test_user_model.py
    tmp/
        ...
    venv/
        ...
</pre>

## How to run and test on your machine

1. Install the Python [Flask](http://flask.pocoo.org/docs/0.10/installation/) web framework
2. In your terminal, navigate to app folder
3. \[ Need to provide additional steps to fully install AnotherLine \]
4. To start app in localhost, run <code>python manage.py runserver</code>
5. Navigate to http://localhost:5000/ in your browser.

## To-Dos

### Phase 1 - Develop database schema and templates, responsively.

The main goal of this first phase is to develop the schema and a few CV templates in tandem, as to revise either as necessary.

- Need to create diagram of database structure
- Need to create frontend wireframes

### Phase 2 - Build API

With the completion of semi-stable schema for the CV/Portfolio, we can now develop the API.

- build API for users to export and use their Cv data (JSON format)
- write the form templates for data input

## Other ways to contribute

- Create a new CV template.
- Open a new issue: [https://github.com/anotherline/anotherline/issues](https://github.com/anotherline/anotherline-flask/issues)
- Contact me with questions: chris.a.lindgren [at] gmail [dot] com.

## Contributors

* Chris Lindgren, [Writing Studies scholar](http://clindgrencv.com/) and web dev tinkerer 