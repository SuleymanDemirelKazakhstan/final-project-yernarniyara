## Mindmap
 https://miro.com/app/board/o9J_lTqjWQU=/

## Risks\
 - The PWA part of the application may e hard to code and there might be difficulties to adapt it to all smartphones \
 - There might be difficulties in providing our system to a medical institution\
 
 ## Non-functional requirements 
 - The application must be built in Python and Django as a backend and HTML/CSS/JS on frontend side\
 - The application must be hosted on hoster.kz as a simple and most useful solution\
 - The application must have map on a website with points with donation centers\
 - The application must have two sides: for clients and for medical institution workers\
 - The application must be responsive\
 - The application must work in all modern browsers\
 - The application must have a PWA version of a website in order to easily use it on a smartphones as an app\
 - The application must support approximately 500 users simultaneously\

## Page Description for donors
| Page | Description  |
|---|---|
|Main Page <br/> /home | 1. Logo Branding <br/> 2. Categories on site <br/> 3. Login <br/> 4. Beautiful Illustration <br/> 5. Advantages of blood donation <br/> 6. Examples of bonuses and achievements <br/> 7. Instructions |
| Login Page <br/> /login | 1. Login and Password fields <br/> 2. Login button <br/> 3. Forgot password <br/> 4. Register if no account  |
|  Registration <br/> /registration | 1. Information insert <br/>  |
|  Profile Page <br/> /profile | 1. Last blood donation <br/> 2. User card with all info <br/> 3. Last blood analysis  |

## Page Description for medical-institution-panel
| Page | Description  |
|---|---|
|Homepage/Dashboard <br/> /dashboard | 1. Number of donors in current institution in Chart <br/> 2. Total number of donors per day/week/month|
| Tables with database of donors <br/> /tables | 1. Table of current donors in particular institution <br/> 2. Overall donors <br/> 3. Potential donors to send requests to   |
|  List of needed blood <br/> /inneed | 1. Graph with currently available blood <br/> 2. Graph with blood that blood donation center currently needs  |

## Page Description for admin-institution-panel
All of the medical-institution-panel fields plus extra information
| Page | Description  |
|---|---|
| Characteristics for potential donors <br/> /potential-donors-characteristics | 1. Table with potential donors and their blood|
| Tables with number of used bonuses for medical instituion <br/> /bonuses | 1. Table of currently used bonuses <br/> 2. Bonuses overall number in graph|
| Approving waitlist for registered medical institution workers <br/> /to-approve-workers | 1. Table with workers who are waiting access to create a new account  |
| Table with currently approved people <br/> /approved-workers | 1. Table with workers who are currently working using the system  |

## Page description for superuser-panel
| Page | Description  |
|---|---|
|Homepage/Dashboard <br/> /dashboard-superuser | 1. Number of donors in all institutions in Chart <br/> 2. Total number of donors per day/week/month|
| Tables with database of donors <br/> /tables | 1. Table of current donors in all institutions |
| Tables with database of medical workers by instituions <br/> /tables | 1. Table of current workers sorted by a medical institution |


## Work done during Week3
 - Developed structure for the website pages\
 - Decided which Python packages we will use: Django, Jinja2\
 - Developed advanced design\
 - Began work on administrator panel\
 - Developing database architecture for the project\
