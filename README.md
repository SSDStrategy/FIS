# FIS

This repository contains the implementation of the Dutch Forensics system for the Secure Software Development course by
University of Essex.

# Instruction to run

* Install the required dependencies (it is suggested to set up a virtual env):

``pip install -r /path/to/requirements.txt``

* Run as a process:

  ``flask run -h localhost -p 5005 src/auth/Authenticate``

  this is going to start the authentication service


* Run as a separate process:

  ``flask run src/web/application``

# Differences between implementation and proposal

The list that follows represents the differences or the incomplete implementations realized versus what we designed in
the beginning.

* RBAC authorization model hasn't been implemented. Instead, in PermissionRepository has been implemented a simpler
  mechanism.
* JsonWebToken are not used. Instead, the system verifies the credential and store current username in the session.
* Search hasn't been implemented.
* Pagination is incomplete feature.

# Project structure
###Source code
In the folder `src` there are all the project sources. The system is composed by 4 modules:

* web, defines the web layer with all the templates and endpoint.
* core, contains business logic, service classes and authorization.
* data, defines the models through ORM definition (SqlAlchemy) and repository classes to implement CRUD operations on
  the entities using the sqlalchemy ORM module.
* auth, microservice for authentication.

As we declared in our design document, the base system composed by the data and core modules, is reusable and
object-oriented. In fact future development could for example implement REST API based on these modules. Or complete the
implementation of a RBAC authorization model, or other improvements, this is mainly achieved because of good
programming techniques have been applied like SOLID principles.

Database used in this implementation is sqlite for the simplicity of setup and usage. Obviously it cannot keep up with
the demand of a live system, this can be resolved using more appropriate database engine as Postgres or MySQL, and the
use of SQLAlchemy ORM perfectly support to change database engine without any code modification.

### Test
In the folder `test` there are tests of the main classes using pytest framework. 