#End 2 End Testing (Protractor)
To run the end-2-end tests against the application you use [Protractor](https://github.com/angular/protractor).

## Starting the Web Server
You will need a web server running the application locally for these tests.
Follow the instructions found in backend/README.md to set up the web server
for local development.

Once configured, you can start the server by running:
```
source venv/bin/activate && foreman start dev_server -e .test_env
```
or alternatively from the frontend directory:
```
npm run test-server
```
which is an alias for the above command.

The application should now be available at `http://localhost:5000`

## Testing with Protractor

As a one-time setup, download webdriver.
```
npm run update-webdriver
```

Start the Protractor test runner using the e2e configuration:

```
npm run protractor
```
