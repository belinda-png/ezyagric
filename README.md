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

- **Quick Actions**:
  - "Log Activity" button to create new actual activities
  - "Add Activity" button to create new planned activities

### 3. Farmer Management
- **Register Farmers**: Add new farmers with:
  - Farmer ID
  - Name
  - Phone number
  
- **View Farmer Details**: See all information about a farmer including:
  - Contact information
  - Total farms owned
  - Total acreage
  - List of all farms with locations and sizes

- **Edit/Delete Farmers**: Update or remove farmer records

### 4. Farm Management
- **Add Farms**: Register farms for farmers with:
  - Farm name
  - Size in acres
  - Location
  
- **Edit/Delete Farms**: Manage farm information
- **View Farm Details**: See all farms associated with a farmer

### 5. Season Planning
- **Create Season Plans**: Plan crops for specific seasons with:
  - Crop name
  - Season selection (Season A, B, or C)
  - Status (Planned, Active, Completed)
  - Start date
  
- **View Season Plans**: List all season plans with status badges
- **Season Details**: View all planned and actual activities for a season
- **Season Summary**: Comprehensive analytics including:
  - Completed vs pending activities
  - Overdue tasks count
  - Planned vs actual cost comparison
  - Completion rate percentage
  - Activity status breakdown

### 6. Planned Activities
- **Create Planned Activities**: Plan field activities with:
  - Activity type (Land Preparation, Planting, Weeding, Spraying, Harvesting)
  - Target date
  - Estimated cost in UGX
  
- **View Planned Activities**: List all planned activities
- **Delete Planned Activities**: Remove activities as needed

### 7. Actual Activities
- **Log Actual Activities**: Record completed field work with:
  - Activity type
  - Actual date
  - Actual cost in UGX
  - Notes/observations
  - Link to planned activity
  
- **Edit Actual Activities**: Update activity records
- **Delete Actual Activities**: Remove activity logs

## Technology Stack

- **Backend**: Django 6.0
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3
- **Icons**: Font Awesome 6.0
- **Styling**: Tailwind CSS (partial), Custom CSS
- **Authentication**: Django built-in authentication system



## Database Models

### Farmer
- `farmer_id`: Unique identifier
- `name`: Farmer's full name
- `phone`: Contact phone number

### Farm
- `farmer`: Foreign key to Farmer
- `name`: Farm name
- `size_in_acres`: Farm size
- `location`: Farm location

### SeasonPlan
- `farm`: Foreign key to Farm
- `crop_name`: Name of crop
- `season_name`: Season selection (Season A, B, or C)
- `status`: Status (Planned, Active, Completed)
- `start_date`: Season start date

### PlannedActivity
- `season_plan`: Foreign key to SeasonPlan
- `activity_type`: Type of activity
- `target_date`: Planned date
- `estimated_cost_ugx`: Estimated cost in UGX

### ActualActivity
- `season_plan`: Foreign key to SeasonPlan
- `activity_type`: Type of activity
- `actual_date`: Date completed
- `actual_cost_ugx`: Actual cost in UGX
- `notes`: Additional notes
- `planned_activity`: Foreign key to PlannedActivity (optional)

## URL Routes


| `/` | login_view | Login page |
| `/dashboard/` | dashboard | Main dashboard |
| `/logout/` | logout_view | Logout |
| `/farmer/` | farmers | Farmer list |
| `/add/` | add_farmer | Add farmer |
| `/farmer/<id>/` | farmer_details | Farmer details |
| `/farmer/<id>/edit/` | edit_farmer | Edit farmer |
| `/farmer/<id>/delete/` | delete_farmer | Delete farmer |
| `/farmer/<id>/add_farm/` | add_farm | Add farm |
| `/farm/<id>/edit/` | edit_farm | Edit farm |
| `/farm/<id>/delete/` | delete_farm | Delete farm |
| `/seasonplans/` | seasonplan_list | Season plans list |
| `/seasonplans/create/` | seasonplan_create | Create season plan |
| `/seasonplans/<id>/` | seasonplan_detail | Season plan details |
| `/seasonplans/<id>/summary/` | seasonplan_summary | Season plan summary |
| `/seasonplans/<id>/edit/` | seasonplan_edit | Edit season plan |
| `/seasonplans/<id>/delete/` | seasonplan_delete | Delete season plan |
| `/plannedactivities/` | plannedactivities_list | Planned activities list |
| `/plannedactivities/create/` | plannedactivity_create | Create planned activity |
| `/plannedactivities/delete/<id>/` | plannedactivity_delete | Delete planned activity |
| `/actualactivities/` | actualactivities_list | Actual activities list |
| `/actualactivities/create/` | actualactivity_create | Create actual activity |
| `/actualactivities/edit/<id>/` | actualactivity_edit | Edit actual activity |
| `/actualactivities/delete/<id>/` | actualactivity_delete | Delete actual activity |

## Design Features

### Color Scheme
- **Primary Green (Emerald)**: `#10b981` - Main actions and highlights
- **Dark Green (Forest)**: `#047857` - Sidebar and dark accents
- **Light Green (Mint)**: `#d1fae5` - Backgrounds and badges
- **Cyan/Teal**: `#06b6d4` - Secondary actions
- **Professional Gray**: Various shades for text and borders

### UI Components
- **Sidebar Navigation**: Fixed sidebar with menu items and logout
- **Stat Cards**: Dashboard statistics with icons and trends
- **Season Items**: Card-based display for season plans and activities
- **Forms**: Professional form layouts with validation
- **Tables**: Responsive data tables with proper styling
- **Buttons**: Gradient buttons with hover effects
- **Status Badges**: Color-coded status indicators

## Installation & Setup

### Prerequisites
django(pip install dajngo)
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Create the project and the app **
   ```bash
    admin-djnago startproject then the project
    python manage.py startapp then the app name
   cd farmease
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip freeze > requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5

6. **Rn the project**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser and go to `http://localhost:8000`
   - Login with your superuser credentials

## Usage Guide

### First Time Setup
1. Log in with admin credentials
2. Go to Farmers & Farms section
3. Add your first farmer
4. Add farms for the farmer
5. Create season plans for the farms
6. Add planned activities to season plans
7. Log actual activities as work is completed
8. View summaries to track progress

### Daily Workflow
1. **Morning**: Check dashboard for overdue tasks
2. **During Day**: Log actual activities as they're completed
3. **Evening**: Review season summaries and plan next activities

### Reporting
- Use Season Summary to compare planned vs actual costs
- Track completion rates and overdue tasks
- Monitor total investment across all farms

## Security Features

- **Authentication**: Secure login system with password hashing
- **Session Management**: Sessions expire on browser close
- **CSRF Protection**: Built-in Django CSRF tokens
- **SQL Injection Prevention**: Django ORM protection
- **XSS Prevention**: Template auto-escaping

## Future Enhancements

- Mobile app version
- Weather integration
- Crop yield predictions
- Financial reporting
- Multi-user roles (Admin, Field Officer, Farmer)
- Export to PDF/Excel
- SMS notifications
- GPS location tracking

## Support & Maintenance

For issues or feature requests, please contact the development team.

## License

This project is proprietary and confidential.

## Version History

- **v1.0.0** (Current): Initial release with core features
  - User authentication
  - Farmer and farm management
  - Season planning
  - Activity tracking
  - Dashboard and reporting

---

**Last Updated**: December 2025
**Developed for**: EzyAgric Farm Management
