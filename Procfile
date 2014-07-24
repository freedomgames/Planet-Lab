web: gunicorn backend:app --log-file=- --error-logfile=-
dev_server: bin/dev_server
create_db: bin/create_db
flush_db: bin/flush_db
be_tests: nosetests backend/tests --with-coverage --cover-package backend --cover-html --cover-branches
fe_tests: node frontend/node_modules/karma/bin/karma start frontend/test/karma.conf.js --single-run
e2e_tests: frontend/node_modules/.bin/protractor frontend/test/protractor-conf.js
e2e_tests_debug: frontend/node_modules/.bin/protractor debug frontend/test/protractor-conf.js
bash: bash
