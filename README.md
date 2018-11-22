# Full-stack frameworks milestone project

[![Build Status](https://travis-ci.org/samalty/full-stack-project.svg?branch=master)](https://travis-ci.org/samalty/full-stack-project)

This is project management web application which provides companies with a simple and effective means of informing and updating 
their clients on the progress of ongoing projects. The premise is that a company would white-label the application, open its own 
administrators account, and invite its clients to set up their own account.

From here, the hosting firm and their clients will have access to their own unique dashboards, where they can add, update and 
manage the status of new jobs as required. The jobs held within a client's dashboard is only accessible by them and the administrator, 
meaning the hosting firm can update the client on the project through consistent updates, while the client has freedom to update the 
scope and prioritisation of projects.

A project will be closed as soon as it is signed off and the client has paid the project fee, which is carried out via the application's 
payment feature. Users also have access to a blog, the contents of which is visible to all users of the platform. Here the hosting firm 
will post updates regarding the services that they offer in newsletter-type format, while clients are invited to post testimonials, all 
of which can be upvoted by other users. Clients also have access to a direct messaging platform between themselves and the administrator 
to discuss projects.

## UX

This application was developed with the needs of two particular types of users in mind: SMEs and freelancers looking for a free and simple 
way to manage their workload and engage with their clients, and the clients themselves. This can be summarised with a number of user stories:

- As an SME/freelancer, I want to adopt an online scheduling platform, so that I can better manage my workload
- As an SME/freelancer, I want to invite my clients to access this platform, so that I can keep them updated on the progress of work
- As an SME/freelancer, I want to encourage discourse between my clients and my organisation, to further promote our services
- As a client that outsources, I want continuous updates on the progress of outstanding work, so I can ensure deadlines are met
- As a client that outsources, I want a simple way to update the scope and prioritisation of projects, so that my business needs are met
- As a client that outsources, I want project progress and payment to be documented in the same place, for a more cohesive engagement

Mockups created for this project can be found within the 'planning' folder.

## Features

- Login/register form: Ensures clients have access to a secure workspace whereby they can amend the scope of, approve, sign off, monitor the progress of, and pay for projects.
- Forum: Allows admin to share company updates with clients. Enables clients to upvote preferred posts and provide testimonials for work completed, while potentially assisting as a means of networking between clients.
- Customisable profile: Helps clients who post within the forum to distinguish themselves, assisting with prospective networking opportunities with other clients of the admin.
- Project planner: Simple form by which admin can create a project plan, detailing a project description, fee, deadline and task descriptions. Once created, this project is accessible as a ticket to the designated project client via their own workspace.
- Project editor: Allows clients to edit certain details of existing project plans before approving, such as project and task descriptions.
- Status update: Enables admin to update the status of tasks - which in turn update the status of the overall project - via a select form within the project detail page. Clients can use their equivalent page to approve and sign off projects.
- 'Order by' function: A select form whereby the selected option reorders projects by a specific attribute (deadline, launched date, status and priority). This helps admin to prioritise their workload and informs clients on what agreed work they can expect to receive next.
- Sideways scrolling buttons: Enables users to conveniently scroll between infinite project tickets while maintaining a simple and easy-to-absorb dashboard. This has been specially customised for ease of use via mobile.
- Secure payment platform: Incorporating Stripe, clients have access to a secure platform through which they can pay for projects once signed off. Once payment has been submitted, the 'paid' status of the project is updated.

## Technologies used

- Python: The underlying code, including views, models, forms, routes, and the majority of functionality, was written using Python.
- Django: This project was written using the Django web framework. Django authentication was used to create a secure login feature.
- HTML: HTML was used to help structure the website.
- CSS: The appearance of the website was enhanced using CSS. The stylesheet is available in the static folder.
- Bootstrap: The Bootstrap front-end web framework was used to help structure the website, and in particular to assist in making the application mobile-friendly.
- Javascript/jQuery: jQuery logic has been used to develop certain pieces of functionality, specifically within the user dashboard. The custom jQuery logic is available in the static folder.
- Stripe: This project makes use of the Stripe API for secure online transactions. Stripe javascript logic, necessary for payment processing, is also contained within the static folder.

## Testing

All of the key aspects of this project were subject to extensive unit-testing. There is a 'tests.py' file within each of the 'accounts', 
'blog', 'dashboard' and 'payment' folders, documenting automated tests used to evaluate each individual view, model, form and function, 
when entering both valid and invalid inputs. Each test page can be run within the terminal. At the top of each test page, the input 
required to run the file in the terminal is detailed.

In addition to unit-testing, additional code which has since been removed was used to ensure that certain functionality was updating the 
database as required when it was called upon in the browser. For example, if I were to update the project description of a project via 
the edit function, I would add a print statement within the function, requesting that it print out the updated project description. I 
used the same technique when manually testing buttons designed to update the 'approved' and 'signed off' statuses of projects from false 
to true.

Other testing was conducted within the browser, such as that to ensure that error messages were being returned as required. For example, 
the plan_project function throws a validation error if a user creates a project and attempts to set a deadline within a week. I couldn't 
identify the correct syntax to test that the specific validation error message was being returned within my unit tests, so I simply tested 
it out by attempting to create some invalid projects within the application. Similarly, I struggled to devise an automated test for my 
order_projects jQuery function, so I created a range of projects with differing statuses, deadlines, priorities and launch dates, and 
manually tested the orders by which projects were being returned.

This project was developed using a mobile-first approach. A Google Chrome screen resolution tester was consistently used throughout 
development to ensure that pages and functionalities were easy to navigate and use via various platforms and screen sizes.

The app was extensively tested across a range of browsers on both Windows and Mac operating systems, including Chrome, IE, Firefox, 
Microsoft Edge, and Opera, using CrossBrowserTesting.com's free service. Though they were fully functional across all other browser 
types, the horizontal scrolling buttons on the main dashboard were unresponsive when accessed via Firefox. 

This posed an issue as, by default, my table's x-axis scrollbar was set at the bottom of the page, meaning Firefox users wouldn't be 
aware that they could scroll sideways until reaching the bottom of the page. To overcome this, I created another x-axis scrollbar above 
the table with the same width properties, and used jQuery logic to make either scrollbar responsive to the other. Testing of this was 
conducted manually within the browser. Once I had confirmed that this worked across all browsers and platforms, I changed the display 
property of the bottom scrollbar to hidden. Code was also introduced to ensure that the scrolling buttons don't appear in Firefox browsers. 
Other than this, there were no cross-browser issues with functionality or design.

## Known issues

Within the urls.py file in the blog folder, the url pattern for the create_or_edit_post page begins with a forward slash. For some reason, 
removing this forward slash would result in a 404 error whenever the url would be called. I was unable to resolve this issue, and so the 
forward slash remains.

## Deployment

The final project was pushed to Github, before being deployed to Heroku by way of connecting to the Github workspace. A Heroku Postgres 
database was included as an add-on when setting up the app in Heroku. Heroku came with its own database URL within config variables, which 
I was required to replicate within the env.py file in Cloud9, before copying the remaining cnfig variables from the env.py file to Heroku.

Certain settings within the settings.py file were reconfigured so that static and media files would be hosted within and imported into a 
cloud-based S3 bucket created using Amazon Web Services. 'gunicorn' was installed via the bash terminal to allow the project to connect to 
Heroku, and 'psycopg2' was installed to enable the project to interact with the SQL database. The requirements.txt file was duly updated. 
A Procfile was added to convey to Heroku the type of app that it is hosting. Finally, 'full-stack-frameworks-project.herokuapp.com' was 
added to the allowed hosts within the settings.py file, before being pushed to git, to authorise Heroku as a host, before deploying the 
master branch.

With the premise being that companies would white-label this application and offer it to their clients, the project demo assumes that the 
application has been adopted by a fictional company called 'ABC Copywriting'. While when previewing the project, you are able to register 
and login to new 'client' accounts, much of the functionality is only accessible to the superuser. To access this account, the username is 
'ABCopy' and the password is '1_a9b9c_1'. To test the payment feature, log in using the following credentials: 'GWT_ltd' (username), 
'gwtharry82' (password). This account's dashboard contains a completed, unpaid project where the payment feature is accessible.

## Credits

### Content

Javascript logic necessary for payment processing via Stripe has been lifted from the Stripe API.

### Media

Images and media used within this project were accessed via a Google search for images labeled for noncommercial reuse.