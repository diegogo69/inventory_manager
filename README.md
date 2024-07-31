# SISTEMA DE INVENTARIO
#### Video Demo:  https://www.youtube.com/watch?v=7dH9mVBAdgQ
#### Description:

__Sistema de Inventario__ is a web application designed to manage and register computer equipment. It can be used by any institution or workspace to keep track of its computers and devices, and maintain an inventory with detailed information for each registered item.
## Getting Started

### Requirements
The project is a web application built using Python, Flask, and MySQL as the database manager. It employs several Python libraries with built-in functionalities designed to streamline the web application development process.

**Prerequisites:**
* Python 3.10.12
* MySQL 8.0.37

**Libraries:**
* Flask==3.0.3
* Flask-Login==0.6.3
* Flask-MySQLdb==2.0.0
* Flask-Session==0.8.0
* Flask-WTF==1.2.1
* Jinja2==3.1.4
* mysqlclient==2.2.4
* PyMySQL==1.1.1
* Werkzeug==3.0.3
* WTForms==3.1.2

Flask and Jinja2 compose the program's core logic and functionality. Flask-Login and Flask-Session help to manage user session data. Flask-MySQL is a dedicated library for interacting with MySQL databases. Flask-WTF and WTForms provide authentication functionalities for HTML forms. PyMySQL and mysqlclient are used to properly connect the web application to a MySQL database. Werkzeug offers a set of tools for web development.

## Usage
The application was design in a local environment and meant to be use in a local host, via _flask run_ or *python src/app.py.* It is configured to __port *5000.*__ (http://127.0.0.1:5000/).

### Accounts
The project works with user accounts, where the web application functionality is restricted to work only with authenticated user accounts. Each of them has access to its own registers. Enabling to have multiple accounts with multiple registers. For this purpose. A _User_ class was defined to work with a _ModelUser_ class that has two _classmethod_ created to manage user authentication. And the decorator _@loginrequired_ is declared for all of the functions related to the web application workflow other than authentication related screens.

### Database
The program uses a MySQL database declared in the __sql.sql__ file. It consists of five tables: _users_, _equipos_, _hardware_, _so_, _programas_. That works in conjunction to store user's accounts related data, and storing the registers. 

**users:**
The following columns compose this table: *id_user*, *username*, *hash*, *theme*.
Every user has a unique _id_ and _username_, a _hash_ code based on the user password and a _theme_ value that sets the user's prefered theme for the application.

**equipos:**
This table stores the computer's main data. As name, type, vendor, model, institution identifier, location, condition, comments. As well as a foreign keys that link the computer to its respective user account.

**hardware:**
For the hardware table the columns were defined to store each hardware component separately and linked it via a foreign key to its proper computer, if it's a hardware equipment that does not belong to any specific computer a value of _null_ is setted to the *id_equipo* column. The other columns represent data for the hardware ID, type, vendor, model, serial number, specs, storage capacity, condition, and a foreign key to link it to its respective user account.

**so:**
The computer's operating system information is stored in this table. ID, name, edition, architecture, developer, license and both user and computer foreign keys.

**programas:**
Similar to the _so_ table, it stores data related to the computers software programs (not os). Each has a unique ID, and fields for category, name, version, developer, license and both user and computer foreign keys.


### Application Sections
#### Main page (index)
The main page consists of a summary list of both computer and hardware equipment registers. The former displays only the main computers data, the one registered in the _equipos_ table. For each register three options are presented: _ver_, _editar_, y _borrar_. The latter displays the hardware devices registered, and only supports delete option.

* **Ver:** this option redirects to a page that shows the  detailed information about the computer's data that has been registered. It consists of four different tables, each of them related to a respective SQL table.

* **Editar:** this option redirects to a html form, similar to the one that is shown when we are going to add a register. The difference in this case is that the form field are filled with the previous registered data, for which we have the option to change, or leave unchanged.

* **Borrar:** This option allows you to delete a register. A confirmation is needed to do so.

#### Añadir Computador
This is where computer registers are added, and it consists of three different screens.

The **first one** consists of a form for the computer's main data.

* _Nombre del equipo:_ The name given to the computer operating system

* _Tipo:_ It it's a pc or a laptop

* _Marca:_ The computer's vendor company

* _Modelo:_ Computer's model

* _N° identificador:_ Some institutions give an identifier code for each of its mobiliary and assets. 

* _Ubicación:_ The computer 's location within the company or institution (Office, room, etc...)

* _Estado del equipo:_ This field indicates whether the computer is functional or if it's broken.

* _Observaciones:_ Any additional comment that could be relevant.

When the form is submitted it redirects to the next screen.

The **second** screen consists of a form for the hardware components of the computer. The hardware components listed are: CPU, RAM, storage, motherboard, power supply, graphic card, monitor, keyboard, mouse, printer. Graphic card and printer are optional values.
If the form is submitted empty, it jumps to the next screen but no register is made (field values are not saved as null). Additionally, at the bottom of the form we can add other hardware components that are not listed in the form, these are: Wireless and bluetooth adapters, webcams, scanner, speakers, headphones, or leave it categorized as _other_.

For each hardware component we need to fill the following fields.

* _Marca:_ Hardware fabricant or vendor.

* _Modelo:_ Hardware model

* _Capacidad:_ If it's a storage device, memory or its performance is labeled by capacity units.

* _Especificaciones:de Hardware relevant specs

* _N° Serie_: Hardware serial number.

Additionally each hardware has two hidden input values. One for the category of the hardware component, and another that has the computer's ID value.
When submitting the form, it redirects to the next screen.

The **third** screen consists of a form for the software information, these are operating systems and programs. For the operating system the next fields are presented:

* _Nombre:_ Name of the operating system. Windows, Linux, MaxOS, or _Otro_ are the available options.

* _Edición:_ Operating system edition

* _Arquitectura:_ Operating system architecture. Either 32 or 64 bits.

* _Desarrollador:_ Develop company

* _Licencia:_ License information

For the programs the next fields are presented.

* _Nombre:_ Name of the program

* _Versión:_ Version release of the program

* _Desarrollador:_ Program's development company

* _Licencia:_ Program license information

* _Categoría:_ Program related category

Both **programs** and **operating system** have a hidden input which is the computer's ID. And for programs sometimes license, and category input fields are hidden, because their values are defaulted.

#### Añadir Hardware
We can add hardware equipment and peripherals that do not belong to any specific computer. But that is still part of the workspace assets.

The fields are the same of the hardware components, with the addition of a _condition_ input field.

#### Computadores
This page displays a table with all of the computer registers. As in the main page, the table only shows the computer main information, but has the options for viewing the register, editing it, or deleting it. The page also includes an export option that includes all of the register data into a csv file which is then downloaded.

#### Hardware y Periféricos
Similar to the _Computadores_ page. A table is displayed with all of the hardware equipment and peripherals registered, each only supporting the deleting option. And also allows exporting all of the registers information into a csv file.


#### Ajustes
In this page we can change our account password, and change the web application theme, either dark theme or light theme. The theme configuration is saved in the database _users_ table. So if the user logs out the theme is saved for the next session.

#### Iniciar sesión, Cerrar sesión y Crear cuenta
The web application works with a simple, but robust, user authentication system. Supported by the built-in functionalities of the flask dependencies.

## Source code
The project is a Flask web application that uses MySQL as the database management system.

The project's main folder includes the following files and folders:

* __app.py:__ main file of the program.

* __config.py:__ most of the database and session's configuration are declared here.

* **db_operations.py:** Most of the database queries are declared here for reading and easier handling purpose.

* **README.md:** Project description.

* **requirements.txt:** libraries and dependencies required for the project to work as intended.

* **sql.sql:** database declaration statements are registered here.

*  **models (folder):** Includes files for class and class methods declarations.

* **static (folder):** Includes three different folders: _css_, _js_ and _img_. Which files are used for the web application styling with CSS, logic created using JavaScript, and store the image sources respectively.

* **templates (folder):** All the html templates are stored in this folder.

## Credits
Some third party resources were used for this project. 

The lightbulb **favicon** represents my CS50 travesty. It's from the EDX Harvard: CS50's Introduction to Computer Science course page (https://www.edx.org/learn/computer-science/harvard-university-cs50-s-introduction-to-computer-science)


The front-end layouts use for this project are part of the Bootstrap examples page (https://getbootstrap.com/docs/5.3/examples/)


