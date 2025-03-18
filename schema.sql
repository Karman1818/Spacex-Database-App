use master 
go

drop database if exists SpaceX
go

create database SpaceX
go

use SpaceX 
go




drop table if exists Role
create table Role(
RoleId int identity(1,1) not null,
RoleName varchar(50) CHECK (LEN(RoleName) >=3),
CONSTRAINT PKRole_Id PRIMARY KEY (RoleId) )

insert into Role (RoleName) values ('Scientist'),('Spaceman'),('Captain')


drop table if exists MissionTeam
create table MissionTeam(
MissionTeamId int identity(1,1) not null,
TeamName varchar(50) CHECK (LEN(TeamName) >=2),
CONSTRAINT PkMissionTeam_Id PRIMARY KEY (MissionTeamId) )

insert into MissionTeam (TeamName) values  ('alienX'),('falconY'),('CosmicSpeed')


drop table if exists Employee
create table Employee(
EmployeeId int identity(1,1) not null,
FirstName varchar(50) CHECK (LEN(FirstName) >=3),
LastName varchar(100) CHECK (LEN(LastName) >=3),
StartDate date not null,
Salary int not null CHECK (Salary>=0),
MissionExperience int CHECK (MissionExperience>=0),
EmployeeRoleId int not null foreign key references Role(RoleId) ,
CONSTRAINT PkEmployee_Id PRIMARY KEY (EmployeeId) )

insert into Employee (FirstName, LastName, StartDate, Salary, MissionExperience, EmployeeRoleId) 
values ('Johnny', 'Bravo', '2020-10-10', 10000, 6, 2),('Naruto', 'Uzumaki', '2022-10-10', 8000, 3, 2),('Peter', 'Parker', '2018-06-12', 12000, 8, 1),('Dominic', 'Toretto', '2001-10-10', 30000, 15, 3),
('Gandalf', 'Gray', '2010-10-10', 14000, 6, 1),('Kapitan', 'Bomba', '2007-09-17', 20000, 11, 3),('Ben', 'Tennyson', '2005-01-05', 15000, 13, 2),('Dick', 'Grayson', '2014-02-02', 12000, 12, 1),('Luke', 'Skywalker', '2024-05-09', 18000, '12', 3);

drop table if exists MissionTeam_Employee
create table MissionTeam_Employee(

MissionTeam_EmployeeId int identity(1,1) not null,
MissionTeam_EmployeeEmployeeId int not null foreign key references  Employee(EmployeeId) ,
MissionTeam_EmployeeMissionTeamId int not null foreign key references  MissionTeam(MissionTeamId) ,
CONSTRAINT PkMissionTeam_Employee_Id PRIMARY KEY (MissionTeam_EmployeeId)
)

insert into MissionTeam_Employee (MissionTeam_EmployeeEmployeeId,MissionTeam_EmployeeMissionTeamId) values(1,1),(2,2),(3,1),(4,1),(5,2),(6,2),(7,3),(8,3)



drop table if exists Mission
create table Mission(
MissionId int identity(1,1) not null,
Name varchar(50) CHECK (LEN(Name) >=2),
LaunchDate date not null,
ReturnDate date,
MissionMissionTeamId int not null foreign key references  MissionTeam(MissionTeamId) ,
CONSTRAINT PkMission_Id PRIMARY KEY (MissionId) )

insert into Mission (Name,LaunchDate,ReturnDate,MissionMissionTeamId) values ('Mars','2027-12-30',null,1),('Moon','2025-02-22','2025-06-24',2),('AroundEarth','2024-04-28','2024-08-20',3)
 

drop table if exists Login
create table Login(
LoginId int identity(1,1) not null,
Login varchar(255) not null,
Password VARBINARY(8000) NOT NULL,
CONSTRAINT CHK_PasswordLength CHECK (LEN(Password) >= 16), 
CONSTRAINT PK_Login_Id PRIMARY KEY (LoginId));

INSERT INTO Login (Login, Password)
VALUES 
    ('3lon-m@sk', HASHBYTES('MD5', 'ILikeLetterX')),
    ('ManOfSt33l', HASHBYTES('MD5', 'HappyHogan')),
    ('b@tman', HASHBYTES('MD5', 'IronManSucks'));


drop table if exists Administrator
create table Administrator(
AdministratorId int identity(1,1) not null,
FirstName varchar(50) CHECK (LEN(FirstName) >=3),
LastName varchar(100) CHECK (LEN(LastName) >=3),
AdministratorLoginId int not null foreign key references  Login(LoginId) ,
CONSTRAINT PkAdministrator_Id PRIMARY KEY (AdministratorId) )

insert into Administrator (FirstName,LastName,AdministratorLoginId) values ('Elon','Musk','1'),('Tony','Stark','2'),('Bruce','Wayne','3')

drop table if exists JobApplication
create table JobApplication(
JobApplicationId int identity(1,1) not null,
FirstName varchar(50) CHECK (LEN(FirstName) >=3),
LastName varchar(100) CHECK (LEN(LastName) >=3),
DateOfBirth date,
Email varchar(100) CHECK (LEN(Email) >=7),
Phone varchar(15) CHECK (LEN(Phone) =9),
JobApplicationRoleId int not null foreign key references Role(RoleId) ,
CONSTRAINT PKJobApplication_Id PRIMARY KEY (JobApplicationId) )



