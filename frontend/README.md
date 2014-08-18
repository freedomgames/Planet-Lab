# PlanetLab Frontend

Welcome to PlanetLab's frontend folder! Here, you'll find all the code and documentation for the fun stuff happening on the frontend!

## Basics

PlanetLab is being built as a single-page application. This means that there are no hard refreshes, and all content is served through AJAX. This allows the application to be faster and more responsive. PlanetLab is being built mostly as a _content management system_ with user-facing gamification.

## Current Maintainers

* [maiamcguinness](https://github.com/maiamcguinness)
* [waltaskew](https://github.com/waltaskew)

## Technologies

This is an **AngularJS**-based project. We are using the **UI-Router** to handle states and nested views. **TinyMCE** is our current choice of WYSIWYG. We may, at some point, integrate a library like Underscore or Lo-Dash if need be.

If you are unfamiliar with any of these projects, I highly recommend a good Google search for each and any. They are all fairly well documented, and you should have no trouble picking it up! However, if you do, please talk to a maintainer.

## Getting Started

To get started working with the frontend, please review the User Stories document we will provide, and select a task. (Ideally, we will be updating this frequently.) This will offer a very specific description of what technologies you will need to integrate, what you will need to build, and what (if any) database calls will be required.

Once you have selected a task, please make sure you have forked the repo. Pull down this fork to your local machine. Follow the instructions in the [backend/README file](../backend/README.md) to get the webserver and local db up and running. Make a user on the login screen, then login && view the app!

## File Structure

The file structure for the frontend chunk of this repo is currently as follows:

    frontend
    |
    |--- app
           |
           |--- app.html (main html file)
           |
           |--- index.html (welcome page)
           |
           |--- featurename
           |      |
           |      |--- controller (js)
           |      |
           |      |--- view (html)
           |      |
           |      |--- styles (css)
           |
           |--- vendors (includes)

If you have any questions about this file structure, ask a maintainer.
Please read [this doc](app/README.md) to understand how to reference
assets with src links during development and in production.

## Contributing

* Use four-space tabs and follow this style guide for JavaScript coding guidelines: http://google-styleguide.googlecode.com/svn/trunk/javascriptguide.xml

* Follow this style guide for best Angular practives, save for the file structure (see above): https://github.com/mgechev/angularjs-style-guide

* Your code will be minified later, so please be generous with whitespace and comments to aid readability.

* Fork https://github.com/freedomgames/Planet-Lab and send pull requests for your new features against the master branch of this repo.

* If you have time, please comment on other people's pull requests.

## Important Notes

Be sure to pull from the upstream repo frequently.

New backend development may necessitate updating your database schema.
The simplest way to apply the new schema is to run:
```
foreman run flush_db -e .dev_env
```
However, this will result in an emtpy database
(deleting any users, quests or other resources you may have created.)
