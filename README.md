# MobileApplicationProject

Assalomu Aleykum Mr Otabek Negmatov, i am student of group SE 2-20 Yunusov Nodirbek (SE14053).

My project about Testing system. This system for instructors which teaches individually. His/Her students can solve tests for upgrade their level and strenghten students knowledge

1) Description:

My server side consists from 2 parts:
Admin panel (Django): Admin panel provides a ready-made powerful admin panel for easy controlling of all data. Also the main work of admin_panel controlling database architecture and design (migrations)
Server (FastApi): Server provides all logic of project. All api plans provided here.

Also First steps will be with Admin panel, after entering admin panel with username and password ((2) project initialization) you have to add Admin.

In project has 3 roles. There are admin (SUPER_ADMIN, ADMIN), instructor (INSTRUCTOR) and student (STUDENT).

I will give description of responsibilities for each role and process of project.

1.1) Admin: Admin can fully control (CRUD) Admins, Advertisements, Instructor, Subjects and only view (GET) the Section, Students, Statistics
Firstble Admin will create Subjects for Instructors. Secondble Admin will create Instructor. And if will moment Admin will create Advertisement for sending it for all.
1.2) Instructor: Instructor can fully control (CRUD) Section, Test and only view (GET) the Statistics which students solved of the instructor
Firsteble Instructor will create Section. Secondble create Test for Section
1.3) Student: Student only work with Test. Student can 
(GET) get all, get one and get random tests for solving and 
(PATCH) also can update test when it is solving that test, you can say why te reason is that Instructor can anytime delete test if instructor delete test when student solving it will be problem in checking
(POST) check method when the student solved test the student will request to this endpoint for getting result and that time automatically will create Statistic

Has the model Statistic. Statistic has only two methods (GET, POST). All roles can only view (GET) it. It will be created after Student solved tests and getting the result.

2) Project initialization

2.1) cd server in CMD

2.2) If you have installed Docker on you laptop or PC the process will be easy.
If you do not installed please could you download from this https://docs.docker.com/engine/install/ and install
Open the project in the IDE or Windows Command Prompt (CMD) and type two commands:
2.2.1) docker network create test_system_net
2.2.2) docker-compose up
Project will be initialize and docker will do all.
2.3) You have to configure virtual enviroment for two admin_panel and server.
2.3.1) Admin Panel
2.3.1.1) python -m venv venv
2.3.1.2) vemv\Scripts\activate
2.3.1.3) pip install -r requirements.txt
2.3.1.4) python manage.py makemigrations
2.3.1.5) python manage.py migrate
2.3.1.6) python manage.py super_user (It is django user (username='nodir', password='123456789') for entering Django admin panel and creating Admin in the system)
2.3.1.7) python manage.py runserver 
2.4.2) Server
2.4.2.1) python -m venv venv
2.4.2.2) vemv\Scripts\activate
2.4.2.3) pip install -r requirements.txt
2.4.2.4) python -m src.main


Notice: Please Mr Otabek Negmatov can you edit some places if you initialize project not with Docker.
1) Admin Panel
1.1) Could you open .env file which located in admin_panel and edit database settings (localhost to host places) 
2) Server
2.1) Could you open .env file which located in server and edit database settings and host (localhost to host places) 

This project client side was in telegram bot the reason is that has some endpoints which sends data to bot and also if you want to upload file or image you must to encode it to base64, This project adapted to it.
