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

        // enter text in the text fields
        var textFields = [
            ['quest.name', 'snakes'],
            ['quest.summary', 'ladders'],
            ['quest.pbl_description', 'monads mo problems'],
            ['quest.mentor_guide', 'be cool to kids'],
            ['quest.hours_required', '4'],
            ['quest.minutes_required', '7'],
            ['quest.max_grade_level', '6'],
            ['quest.min_grade_level', '3']
        ]
        var editText = function(modelName, text) {
            element(by.binding(modelName)).click();
            var input = element(by.css('.editable-input'));
            input.clear();
            input.sendKeys(text);
            element(by.css('button[type="submit"]')).click();
        };

        browser.get('/app#/quests/new');
        for (var i=0; i < textFields.length; i++) {
            var modelName = textFields[i][0];
            var text = textFields[i][1];
            editText(modelName, text);
        }
        // Play with the list editor widget for inquiry questions
        // and video links, playing with the add and delete buttons
        element(by.id('quest.inquiry_questions-add-another-btn')).click();
        element(by.id('quest.inquiry_questions-add-another-btn')).click();
        element(by.id('quest.inquiry_questions-0-input')).sendKeys('a');
        element(by.id('quest.inquiry_questions-1-input')).sendKeys('b');

        element(by.id('quest.video_links-add-another-btn')).click();
        element(by.id('quest.video_links-add-another-btn')).click();
        element(by.id('quest.video_links-0-input')).sendKeys('v1');
        element(by.id('quest.video_links-1-input')).sendKeys('v2');
        element(by.id('quest.video_links-1-delete-btn')).click();

        element(by.id('save-button')).click();

        // check out the quest we just saved
        browser.get('/app#/quests/1');
        // make sure our text fields are present
        for (var i=0; i < textFields.length; i++) {
            var modelName = textFields[i][0];
            var text = textFields[i][1];
            expect(element(by.binding(modelName)).getText()).toEqual(text);
        }
        // make sure the list editor fields are present
        expect(element(by.id('quest.inquiry_questions-0-input'))
               .getAttribute('value')).toEqual('a');
        expect(element(by.id('quest.inquiry_questions-1-input'))
               .getAttribute('value')).toEqual('b');

        expect(element(by.id('quest.video_links-0-input'))
               .getAttribute('value')).toEqual('v1');
        // the one we deleted should be gone
        expect(element.all(
            by.id('quest.video_links-1-input')).count()).toEqual(0);

        // user's quest page should have a link to the new quest
        browser.get('/app#/user/quests');
        expect(element.all(by.repeater('quest in quests')).count()).toEqual(1);

        // let's click on it and do some editing
        element.all(by.repeater('quest in quests')).then(function(quests) {
            expect(quests[0].getText()).toEqual('snakes');
            quests[0].element(by.tagName('a')).click();
        })
        expect(element(by.binding('quest.summary')).getText()).toEqual('ladders');
        editText('quest.summary', 'magic');
        element(by.id('save-button')).click()
        // make sure our edit stuck
        browser.get('/app#/quests/1');
        expect(element(by.binding('quest.summary')).getText()).toEqual('magic');
    });
});
