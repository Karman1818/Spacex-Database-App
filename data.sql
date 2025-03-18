
create login marceli with password = 'karman';
create user marceli for login marceli;
create role viewers
alter role viewers add member marceli
grant select on database::SpaceX to viewers
grant insert on database::SpaceX to viewers
grant delete on database::SpaceX to viewers
grant execute on database::SpaceX to viewers


use SpaceX
go

create or alter view vw_CurrentMission
as
select e.FirstName+' '+e.LastName as fullName,m.LaunchDate,m.ReturnDate,m.Name,r.RoleName,mt.TeamName from Employee as e left join Role as r on e.EmployeeRoleId=r.RoleId left join MissionTeam_Employee as me on 
e.EmployeeId = me.MissionTeam_EmployeeEmployeeId left join MissionTeam as mt on mt.MissionTeamId = me.MissionTeam_EmployeeMissionTeamId left join Mission as m on
m.MissionMissionTeamId = mt.MissionTeamId

go

create or alter view vw_MissionsAndData
as
select m.Name,mt.TeamName,m.LaunchDate,m.ReturnDate from Employee as e left join Role as r on e.EmployeeRoleId=r.RoleId left join MissionTeam_Employee as me on 
e.EmployeeId = me.MissionTeam_EmployeeEmployeeId left join MissionTeam as mt on mt.MissionTeamId = me.MissionTeam_EmployeeMissionTeamId left join Mission as m on
m.MissionMissionTeamId = mt.MissionTeamId

go

create or alter view vw_SpacemanAndCaptains
as
select e.FirstName,e.LastName,e.Salary,e.StartDate,r.RoleName,MissionExperience  from Employee as e left join Role as r on e.EmployeeRoleId=r.RoleId left join MissionTeam_Employee as me on 
e.EmployeeId = me.MissionTeam_EmployeeEmployeeId left join MissionTeam as mt on mt.MissionTeamId = me.MissionTeam_EmployeeMissionTeamId left join Mission as m on
m.MissionMissionTeamId = mt.MissionTeamId

go

create or alter view vw_Scientist
as
select e.FirstName,e.LastName,e.Salary,e.StartDate,MissionExperience  from Employee as e left join Role as r on e.EmployeeRoleId=r.RoleId left join MissionTeam_Employee as me on 
e.EmployeeId = me.MissionTeam_EmployeeEmployeeId left join MissionTeam as mt on mt.MissionTeamId = me.MissionTeam_EmployeeMissionTeamId left join Mission as m on
m.MissionMissionTeamId = mt.MissionTeamId where r.RoleName = 'Scientist'

go

create or alter proc sp_MoveJobApplicationToEmployee @JobApplicationId int , @salary int , @MissionExperience int 
as
begin

begin tran


insert into Employee (FirstName, LastName, StartDate, Salary, MissionExperience, EmployeeRoleId)
    values (
        (select FirstName from JobApplication where JobApplicationId = @JobApplicationId),
        (select LastName from JobApplication where JobApplicationId = @JobApplicationId),
        getdate(), 
        @Salary, 
        @MissionExperience, 
        (select JobApplicationRoleId from JobApplication where JobApplicationId = @JobApplicationId)
    );

delete from JobApplication where JobApplicationId = @JobApplicationId


commit tran

end












