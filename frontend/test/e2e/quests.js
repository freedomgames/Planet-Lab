'use strict';

var sh = require('execSync');


describe('Quest CRUD', function() {
    beforeEach(function() {
        // flush the database between tests
        var statusCode = sh.run([
            'cd .. &&',
            'source venv/bin/activate &&',
            'foreman run flush_db -e .dev_env'].join(' '));
        expect(statusCode).toBe(0);

        // the sign-in page is not angular, so we have to use the
        // driver directly to create and log in a user as it will
        // fail on non-angular pages otherwise
        browser.driver.get('http://localhost:5000/user/register');
        browser.driver.findElement(by.id('username')).sendKeys('testuser');
        browser.driver.findElement(by.id('password')).sendKeys('Snakes1');
        browser.driver.findElement(by.id('retype_password')).sendKeys('Snakes1');
        browser.driver.findElement(by.css('input[type="submit"]')).click()

        browser.driver.get('http://localhost:5000/user/sign-in');
        browser.driver.findElement(by.id('username')).sendKeys('testuser');
        browser.driver.findElement(by.id('password')).sendKeys('Snakes1');
        browser.driver.findElement(by.css('input[type="submit"]')).click()
    });

    it('should save name field', function() {
        // save a new quest
        browser.get('/app#/quests/new');
        element(by.binding('quest.name')).click();
        element(by.css('input[type="text"]')).sendKeys('snakes');
        element(by.css('button[type="submit"]')).click();

        element(by.id('save-button')).click();

        // make sure our fields are present
        browser.get('/app#/quests/1');
        expect(element(by.binding('quest.name')).getText()).toEqual('snakes');
    });
});
