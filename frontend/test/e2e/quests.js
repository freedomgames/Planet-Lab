'use strict';

var sh = require('execSync');


describe('Quest CRUD', function() {
    beforeEach(function() {
        // flush the database between tests
        var statusCode = sh.run(
            'cd "$(git rev-parse --show-toplevel)" && bin/flush_db');
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

    it('should create and retrieve quests', function() {
        // user's quest page should initially be empty
        browser.get('/app#/user/quests');
        expect(element.all(by.repeater('quest in quests')).count()).toEqual(0);

        // save a new quest
        browser.get('/app#/quests/new');
        element(by.binding('quest.name')).click();
        element(by.css('input[type="text"]')).sendKeys('snakes');
        element(by.css('button[type="submit"]')).click();

        element(by.id('save-button')).click();

        // make sure our fields are present
        browser.get('/app#/quests/1');
        expect(element(by.binding('quest.name')).getText()).toEqual('snakes');

        // user's quest page should have the new quest
        browser.get('/app#/user/quests');
        expect(element.all(by.repeater('quest in quests')).count()).toEqual(1);
    });
});
