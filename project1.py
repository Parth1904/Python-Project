# Import libraries
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Creating an empty DataFrame with specific columns to store vehicle data
Vehicle_data_df = pd.DataFrame(columns=["Vehicle Type","Vehicle_No","Mode Of Payment","Mobile No","Entry Time","Exit Time"])

# Base Vehicle class
class Vehicle:
    def __init__(self,vT,vN):
        self.Vehicle_type=vT
        self.Vehicle_no=vN
        
    def display_vehicle(self):
        print("Vehicle type:", self.Vehicle_type)
        print("Vehicle No:", self.Vehicle_no)

# Calculating charges based on duration type
    def calculate_charges(self):
        
        duration_type = input("Enter duration type (hourly/daily/monthly): ").strip().lower()
        duration = int(input(f"Enter duration in {duration_type}: "))

        if duration_type == "hourly":
            charges = duration * self.rate
            period = "Hourly"
        elif duration_type == "daily":
            charges = duration * self.rate * 24  
            period = "Daily"
        elif duration_type == "monthly":
            charges = duration * self.rate * 24 * 30 
            period = "Monthly"
        else:
            print("Invalid duration type!")
            return None, None

        return charges, period
            
# Bike class inherits from Vehicle class      
class Bike(Vehicle):
    def __init__(self,vT,vN,sO,sO2W,mBN):
        super().__init__(vT,vN)
        self.Start_option=sO
        self.Space_of_2W=sO2W
        self.Mobile_Number=mBN
        self.rate= 20 # Rate per hour for bike parking
        
    def display_bike(self):
        print("Bike Info")
        print("Start option:", self.Start_option)
        print("Space of 2W:", self.Space_of_2W)
        print("Mobile Number of User:", self.Mobile_Number)
            
# Car class inherits from Vehicle class        
class Car(Vehicle):
    def __init__(self,vT,vN,nD,sO4W,mCN):
        super().__init__(vT,vN)
        self.num_doors=nD
        self.Space_of_4W=sO4W
        self.Mobile_Number=mCN
        self.rate=40  # Rate per hour for car parking
        
    def display_car(self):
        print("Car Info")
        print("Number of Doors:", self.num_doors)
        print("Space of 4W:", self.Space_of_4W)
        print("Mobile Number of User:", self.Mobile_Number)
        
# Truck class inherits from Vehicle class 
class Truck(Vehicle):
    def __init__(self,vT,vN,s,soT,tMN):
        super().__init__(vT,vN)
        self.size=s
        self.Space_of_Truck=soT
        self.Mobile_Number=tMN
        self.rate=60 # Rate per hour for truck parking
        
    def display_truck(self):
        print("Truck Info")
        print("Size of Truck:", self.size)
        print("Space of Truck:", self.Space_of_Truck)
        print("Mobile Number of User:", self.Mobile_Number) 
        
# User inputs for vehicle details     
Vehicle_type=(input("Enter a Vehicle type:"))
Vehicle_no=int(input("Enter a vehicle Number:"))

# Choice selection for type of vehicle
choice = int(input("what would you like to park; Bike/Car/Truck 0/1/2 :"))

# Creating an instance of the selected vehicle type
if choice == 0:
    
    Start_option=input("Enter Start Option:")
    Space_of_2W=30
    Mobile_Number=int(input("Enter a Mobile Number of User:"))
    vehicle = Bike(Vehicle_type, Vehicle_no, Start_option, Space_of_2W,Mobile_Number)
    vehicle.display_bike()
        
elif choice == 1:
        
    num_doors=int(input("Enter number of doors:"))   
    Space_of_4W=40 
    Mobile_Number=int(input("Enter a Mobile Number of User:"))
    vehicle = Car(Vehicle_type, Vehicle_no, num_doors, Space_of_4W,Mobile_Number)
    vehicle.display_car()
    
else:
    
    size=input("Enter a size:")
    Space_of_Truck=50
    Mobile_Number=int(input("Enter a Mobile Number of User:"))
    vehicle =Truck(Vehicle_type, Vehicle_no, size, Space_of_Truck,Mobile_Number)
    vehicle.display_truck()

# Record of entry and exit times
entry_Time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
exit_Time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Payment mode input
mode_Payment=input("Enter Payment Mode (Cash, Card and upi):")

# Calculate parking charges
charges, period = vehicle.calculate_charges()
if charges is not None:
    print(f"Parking Charges ({period}): {charges:2f}")

# Creating a dictionary to store data of parked vehicle     
Vehicle_Data={
        "Vehicle Type":[Vehicle_type],
        "Vehicle_No":[Vehicle_no],
        "Mode of Payment":[mode_Payment],
        "Mobile Number":[Mobile_Number],
        "Entry Time":[entry_Time],
        "Exit Time":[exit_Time]
    }

# Convert the dictionary to DataFrame and save to CSV
df = pd.DataFrame(Vehicle_Data)

file_name = "parking_data.csv"

# Appending new data to file if it exists, otherwise creating a new file
if os.path.isfile(file_name):
    df.to_csv(file_name,mode='a', header=False, index=False)

else:
    df.to_csv(file_name,mode='w', header=True, index=False)

 # Reading parking data CSV file for report generation   
df = pd.read_csv("parking_data.csv", parse_dates=["Entry Time", "Exit Time"])

# Ensuring date columns are in datetime format
df["Entry Time"] = pd.to_datetime(df["Entry Time"])
df["Exit Time"] = pd.to_datetime(df["Exit Time"])

# Function to generate daily report
def generate_daily_report():
    daily_report = df.groupby(df["Entry Time"].dt.hour).size().reset_index(name="Number of vehicles")
    print("Daily Report:\n",daily_report)
    return daily_report

# Function to generate weekly report
def generate_weekly_report():
    weekly_report = df.groupby(df["Entry Time"].dt.isocalendar().week).size().reset_index(name="Number of Vehicles")
    print("Weekly Report:\n",weekly_report)
    return weekly_report

# Function to generate monthly report
def generate_monthly_report():
    monthly_report = df.groupby(df["Entry Time"].dt.month).size().reset_index(name="Number of Vehicles")
    print("Monthly Report:\n",monthly_report)
    return monthly_report

# Generate and save reports  
daily_report = generate_daily_report()
weekly_report = generate_weekly_report()
monthly_report = generate_monthly_report()

# Saving reports as CSV files
daily_report.to_csv("daily_report.csv", index=False)
weekly_report.to_csv("weekly_report.csv", index=False)
monthly_report.to_csv("monthly_report.csv", index=False)

# Plotting daily report
plt.figure(figsize=(10, 5))
plt.bar(daily_report["Entry Time"], daily_report["Number of vehicles"], color='skyblue')
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Vehicles")
plt.title("Daily Vehicle Entry Report")
plt.xticks(range(0, 24)) 
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Plotting weekly report
plt.figure(figsize=(10, 5))
plt.plot(weekly_report["week"], weekly_report["Number of Vehicles"], marker='o', color='orange')
plt.xlabel("Week Number")
plt.ylabel("Number of Vehicles")
plt.title("Weekly Vehicle Entry Report")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Plotting monthly report
plt.figure(figsize=(10, 5))
plt.bar(monthly_report["Entry Time"], monthly_report["Number of Vehicles"], color='lightgreen')
plt.xlabel("Month")
plt.ylabel("Number of Vehicles")
plt.title("Monthly Vehicle Entry Report")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()