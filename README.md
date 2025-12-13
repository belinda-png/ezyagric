# EzyAgric - Farm Management System

A comprehensive Django-based farm management application designed for field officers to efficiently manage farmers, farms, season plans, and agricultural activities.

## Project Overview 

EzyAgric is a web application that enables field officers to:
- Register and manage farmers and their farm properties
- Create and track season plans for different crops
- Plan agricultural activities with estimated costs
- Log actual field activities and costs
- View detailed summaries comparing planned vs actual performance
- Track overdue tasks and investment metrics

### 2. Dashboard
- **Overview Statistics**:
  - Total Farmers count
  - Active Seasons count
  - Overdue Tasks count
  - Estimated Investment total
### 3. Farmer Management
- Register, view, edit and delete Farmers
- view farmers details includin the farms and the acreage

### 4. Farm Management
- Add, edit and delete Farms
  - Trac farm size and location

### 5. Season Planning
-Create season plans by crops and season
 - Track status (planned, active or completed)
 - View season sumarries with cost and activity analytics 

### 6. Planned Activities
-Schedule farming activities with target dates and estimated costs

### 7. Actual Activities
-Log completed activities with actual dates, cost and notes
 - Link actual actual activities as planned ones

## Technology Stack
- Backend: Django
- Database:SQLite
- Frontend: html and css
- Icons: Font Awesome

## Database Models
Farmer: farmer_id, name, phone
Farm: farmer, name, size_in_acres, location
SeasonPlan: farm, crop_name, season_name, status, start_date
PlannedActivity: season_plan, activity_type, target_date, estimated_cost_ugx
ActualActivity: season_plan, activity_type, actual_dateactual_cost_ugx, notes, planned_activity

## Installation & Setup
Python 3.14.0
pip 
virtual enviroment
django 5.2.7



## testing and deployment steps
** install all the dependencies
pip instll -r requirements.txt
pip freeze > requirements.txt
** test 
python manage.py test 
pytest
