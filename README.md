# DoctorReviews API

## Introduction

> This is an API for doctor reviews that I worked on for the CareDash API challenge. If you have any questions, let me know. 

## Table of Contents:
* [Getting Setup](#setup)
* [Comments](#Comments) <br />
	* [Design Considerations](#design-considerations)
    * [Scalibilty Issues](#scalability-issues)

<a name="setup" />

## Getting Setup

> #### Clone Repository
>  ```https://github.com/neel376/DoctorReviewAPI.git```

> #### Enter the directory
>  ```cd DoctorReviewAPI```

> #### Install modules
>  ```pip install flask-mysqldb```
>  ```pip install Flask``


> #### Configure db.yaml file
> 	* Fill out fields
> 	* replace ``"mysql_host"`` with "localhost" and ``"mysql_user"`` with your username. <br/>



> #### Get and run MySQL
>	* [Download here](https://dev.mysql.com/downloads/) <br />
>.  * Or run ```brew install mysql```
>	* Run the MySQL server <br />



<a name="Comments" />

## The API

### Design Considerations
>	* Separate queries into a file for doctors and a file for doctor reviews. <br />
>	* Use less SQL calls by using more JOIN clauses. <br />
>	* Display the deleted data after it's been deleted.  <br />
>	* Implement an UPDATE request. <br />
>	* Create automated unit testing. <br />

### Scalability issues
>	* Implement caching using Redis. <br />
>	* Index the database. <br />






