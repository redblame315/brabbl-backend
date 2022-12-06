# brabbl

## Development

* Go to project folder
* create virtual env: `virtualenv -p /usr/bin/python3 env` (first time only)
* `. env/bin/activate`
* make sure postgresql is locally installed and running:
  `pg_ctl -D /usr/local/var/postgres status`
  (start with `pg_ctl -D /usr/local/var/postgres start`)


make sure database „brabbl“ exists
  `psql -l`lists all databases
  - create new empty database with `createdb brabbl`
  or even better:
  - restore the development dummy database with: `psql brabbl < dev_db.sql`

* `pip install -e .`
* `pip install -r requirements/dev.txt`
* `cd brabbl`
* `python manage.py migrate`

To access the django admin, you might want to add your own staff superuser with:
`python manage.py createsuperuser`

Start local server with
* `python manage.py runserver`

CSS files for Welcome page are got from the frontend application considering selected theme. Please run `npm run build_new_staging` to generate theme files.
Also don't forget to run `python manage.py collectstatic`


## Deployment:

Before deployment: Check if staging or production server has latest translations (e.g. using `git status`).

Copy .po file(s) to your local machine using `scp` if need. For example:

`scp brabbl-new_staging@staging.brabbl.com://home/brabbl-new_staging/src/brabbl/brabbl/locale/de/LC_MESSAGES/django.po ./Python/brabbl/django.po`

If translations aren't up to date just revert changes using `git checkout <path to file>`

Run deploying script

* `fab new_staging deploy` or `fab production deploy`

For provisioning of server, check the `deployment/` subdirectory.

Be sure that your host is added into `ALLOWED_HOSTS`. Fill in `SITE_DOMAIN` on your settings.

Note that `SESSION_COOKIE_SECURE` defaults to `True`. So if you don't use SSL on staging you should set it to `False` for staging.


## Server Setup

Before provisioning: please make sure config files in deployment folder are up to date:
- hosts
- provision.yaml
- files/authorized_keys
- files/ntp.conf ?? (handled  by Ansible, but where do these values come from?)

Check Ansible inventory (host configuration) with:
`ansible-inventory -i hosts.yaml --list -y`

Server setup is done with Ansible by running (in your 'env' environment):
./provision [environment]
(e.g.: ./provision production)

Running server is controlled/managed by 'Supervisor' 
Note: currently after running 'provision' command, it's necessary to update supervisor manually on the server (as root user):
(root@server) supervisorctl update

Note: after provisioning, but before Deployment (via fab) works, it's necessary to add the server's public ssh key to Github


## API Docs

The current API is documented (as API Blueprint) in the docs folder.
Use `npm install` and `gulp` in the docs folder to build a html version of the docs.


## Coding Style

Make sure your editor of choice supports EditorConfig [http://editorconfig.org] so the
styles defined in `.editorconfig` are picked up and respected.

PEP8 conformity is checked as part of the test suite.


## Testing

Use `py.test brabbl` from the project root to run the tests.


## Embedding options

brabbl API can be integrated as a 'list' (listing all discussions for
a specific customer) or on a detail page (hosting the actual discussions).


## Snippet

```
<div id="brabbl-widget"></div>
<script>
(function() {
  window.brabbl = {
    customerId: "brabbl-test",
    /* articleID is just another name for 'externalID'. e.g. a context var hardcoded by the customer or something like `window.location.pathname`  */
    articleId: "XYZ",
    defaultTags: ["foo", "bar"], // this tags will be added automatically on "Create discussion form"
    view: "list" // only for embedding option 'list', omit for embedding option 'discussion'
  },
  script = document.createElement('script'),
  entry = document.getElementsByTagName('script')[0];
  script.src = "https://staging.brabbl.com/embed/brabbl.js";
  script.async = true;
  entry.parentNode.insertBefore(script, entry);
})();
</script>
```

## Glossary

* Customer - one "integration environment". All users are specific to
  one customer (although usernames must be unique through all customers).
  Integrations are limited to certain domains per customer.

* Discussion - Discussions can have _one_ statement
  attached (for integration options 1-3) or _multiple_ statements (for 4 and 5).

* Statement - parent for all arguments. 


## i18n and 'Wordings'

* Rosetta - translations can be added also by non-developers via Django tool 'Rosetta' either on production or on staging server. Login as a 'staff' user at [api.server.url]/admin and go to [api.server.url]/Rosetta to modify translations (.po files) on that server.

* We have a lot of 'Wordings' that can be set individually per customer and aren't affected by .po files / translations. These are stored as data in our brabbl database. If you want to add a new language, we also have to add new wordings for it and select them to be used by that customer. We have
  - Wordings (for 'discussion' terms, e.g. barometer values, pro-contra terminology, etc.)
  - Notification Wordings (for text on login screen, notifications, error messages, etc. )
  - Email Group (for text in Emails)

* The development / deployment workflow for adding strings that need i18n is like this:
  1) developer adds a new feature that includes a new user facing string
  2) developer updates src/utils/language_utils.py to include the new key
  3) developer downloads the latest translations (.po files) from staging.brabbl.com to make sure local ‘staging’ branch is up to date (see above in 'deployment')
  4) developer runs python manage.py makemessages -a  (in local project folder: backend/deployment)
  5) developer commits and pushes changes and merge into ‘staging’
  6) developer deploys to staging.brabbl.com
  7) translators add translations via staging.brabbl.com/rosetta
  8) when translations are done: repeat steps 3+5 to have the repo up to date with all translations
  9) after deploying updated translations to a server (e.g. to ‘production’, it’s necessary to login to Django Admin / Rosetta and klick ‘save’ for each and every language that has been updated. (If you forget to do this, the new translations files will not be used!!)


