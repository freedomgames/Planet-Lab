# PlanetLab Frontend

Welcome to PlanetLab's frontend folder! Here, you'll find all the code and documentation for the fun stuff happening on the frontend!

## Basics

PlanetLab is being built as a single-page application. This means that there are no hard refreshes, and all content is served through AJAX. This allows the application to be faster and more responsive. PlanetLab is being built mostly as a _content management system_ with user-facing gamification, and so requires a great amount of control over HTTP requests.

## Technologies

This is an **AngularJS**-based project. We are using the **UI-Router** to handle states and nested views. **TinyMCE** is our current choice of WYSIWYG. We may, at some point, integrate a library like Underscore (or Lo-Dash, if that's  your jam), but that's only if there's a need. (There could be. They have some shiny filters over there...)

If you are unfamiliar with any of these projects, I highly recommend a good Google search for each and any. They are all fairly well documented, and you should have no trouble picking it up! However, if you do, please talk to Maia.

## Getting Started

To get started working with the frontend, please review the User Stories document we will provide, and select a task. (Ideally, we will be updating this frequently.) This will offer a very specific description of what technologies you will need to integrate, what you will need to build, and what (if any) database calls will be required.

Once you have selected a task, please make sure you have forked the repo. Pull down this fork to your local machine. Follow all of Walt's instructions in the backend/README file to get the webserver and local db up and running. Make a user on the login screen, then login && view the app!

_With regards to your fork: I loosely follow (and I'm pretty sure Walt also follows) the [git-flow](https://github.com/nvie/gitflow) method of feature development. No matter how you slice it, you should probably be developing in branches. If you don't want to, that's  your choice, however. Whatever blows your hair back, I suppose._

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

If you have any questions about this file structure, ask Maia.
Please read [this doc](app/README.md) to understand how to reference
assets with src links during development and in production.

## Contributing

Some notes on contributing to the frontend:

* Please follow this style guide as much as possible, save for the file structure (see above): https://github.com/mgechev/angularjs-style-guide

* When you have completed a feature and you'd like it to be included in the main repo for everyone to pull into their versions, please create a pull request on the main repo (freedomgames/Planet-Lab). (**Make sure you are pulling FROM your repo TO the main one!** Not that it truly matters, but the other way around simply won't work. Double-check before you submit the pull request that changes are flowing the right way!)

* If you have time, please comment on other people's pull requests. (However, I am *extremely* terrible at this. So.)

* Re: code style, please use four spaces (not tabs) for consistency's sake. I don't care what code editor you use, however, but if you're going to use a code editor that injects strange folders (lovingly side-eyeing _you_, JetBrains), please add those folders to your personal .gitignore before you commit any of those shenanigans. If someone else opens up the repo with your strange files in them, things could get weird. Real weird.

* Please be kind about your whitespace. Don't overdo it, but don't try to minify it, either. We'll take care of that in the end. Just make it legible. Please?

* Comment when you can. This is especially important for your brilliantly-written, extremely-lean piece of code that does mysterious things with only a few keystrokes. If the coder you were two years ago would have no freaking clue what's happening (aside from most [basic] Angular things... we'll let that slide, or we'd be writing novels), you should probably type a quick note. Even if everyone else gets it immediately, it can't hurt.

## Important Notes

**PLEASE MAKE SURE YOU'RE PULLING INTO YOUR FORK OFTEN!** Seriously, work with the latest code! Before you do anything, merge the main repo into yours, and then pull down to your local. This will seriously reduce the risk of conflicts. (And once there are multiple people working frequently on the front or the backend, this will greatly aid development! Don't want you to hotfix a bug that's already squashed, for example.)

If you have any questions, PLEASE ask Maia! She will do her best to answer them.