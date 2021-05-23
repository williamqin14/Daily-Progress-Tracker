"""
William Qin
5/18/2021
Version 1
"""

#used for file search later
import glob
                    
#finding today's date: mm-dd-YY
from datetime import date
today = date.today()
full_date = today.strftime("%m/%d/%Y")
month = today.month
year = today.year
day = today.day

#create goal object
class Goal:
    def __init__(self,name):
        self.name = name
        
    #create new goal file
    def create(self):
        connect = open(f'{self.name}.txt','w')
        connect.close()
        print(f'New goal "{self.name}" created!')

    #stores goal in memory
    def store_in_memory(self):
        connect = open('dw_memory.txt','w')
        connect.write(self.name)
        connect.close()

    #change goal in memory
    def change_memory(self,name):
        connect = open('dw_memory.txt','w')
        connect.write(name)
        connect.close()

    #returns formatted date. Check parameter '1' for mm/dd/yy, check parameter '2' for mm/dd. 
    def format_date(self,date,check):
        while not date[0].isnumeric():
            date = date.replace(date[0],'')
        if check==1:
            return date
        elif check==2:
            split_date = date.split('/')
            month = split_date[0]
            day = split_date[1]
            return month+'/'+day
        else:
            return 'invalid parameter'

    #returns month
    def month(self,date):
        if not date[0].isnumeric():
            date = date.replace(date[0],'')
        split_date = date.split('/')
        return split_date[0]
    
    #returns day
    def day(self,date):
        if not date[0].isnumeric():
            date = date.replace(date[0],'')
        split_date = date.split('/')
        return split_date[1]

    #returns year
    def year(self,date):
        if not date[0].isnumeric():
            date = date.replace(date[0],'')
        split_date = date.split('/')
        return split_date[2]
        
    #parses data from goal file:
    # self.start_dates = the day the goal was created, and additional days where goal was continued after a break
    # self.tracked_hours = a list of all the tracked days
    # self.text = a list of days that were particularly productive, with text descriptions
    def analyze(self):
        connect = open(f'{self.name}.txt','r')
        data = connect.read()
        data = data.rstrip()
        connect.close()
        
        #split data by line
        data = data.split('\n')
        
        #parse tracked hours from text
        self.start_dates = []
        self.tracked_hours = []
        self.text = {}
        for line in data:
            #skip empty lines
            if len(line)==0:
                continue
            #start date and continued days (!)
            # !05/17/2021:0
            # !#06/01/2021:5
            elif line[0]=='!':
                self.start_dates+=[line]
                self.tracked_hours+=[line]
            #text (@)
            # '05/18/2021': 'text'
            elif line[0]=='@':
                temp = line.split(':',1)
                temp_date = temp[0].replace('@','')
                temp_text = temp[1]
                self.text[temp_date] = temp_text
            #tracked hours (productive day = #)
            # !05/17/2021:0
            # #05/18/2021:5
            # 05/19/2021:3
            else:
                self.tracked_hours+=[line]

    #prints the data out.
    # Shows when the goal was started, when it was continued, how productive each day was,
    # describes particularly productive days, and streaks.
    def display(self):
        self.analyze()
        print(f'Goal: {self.name.capitalize()}')
        is_start_date = True
        streak = 0
        for line in self.tracked_hours:
            
            #parse line
            temp = line.split(':',1)
            temp_date = temp[0]
            temp_hours = temp[1]
            temp_date_m = self.format_date(temp_date,2)
            temp_date_y = self.format_date(temp_date,1)
            
            #check for breakthrough day
            if '#' in temp_date:
                breakthrough = True
            else:
                breakthrough = False
                
            #show start date
            if line in self.start_dates and is_start_date:
                #Start date: 05/17/2021 + 'Hours'
                print(f'Start date: {self.format_date(temp_date,1)}',format('Hours','>27s'))
                #mm/dd:hours + int(hours) + (/'text')
                if breakthrough:
                    print(format(temp_date_m+':','<6s')+format('*'*int(temp_hours),'<23s'),format(temp_hours,f'>18s'),'  /'+self.text[temp_date_y])
                else:
                    print(format(temp_date_m+':','<6s')+format('*'*int(temp_hours),'<23s'),format(temp_hours,f'>18s'))
                streak+=1
                if int(temp_hours)==0:
                    streak = 0
                is_start_date = False
                          
            #show continued date
            elif line in self.start_dates:
                print(f'Streak: {streak}')
                print('-------------------------')
                print(f'Continued: {self.format_date(temp[0],1)}')
                #mm/dd:hours + int(hours) + (/'text')
                if breakthrough:
                    print(temp_date_m+':'+format('*'*int(temp_hours),'<23s'),format(temp_hours,f'>18s'),'  /'+self.text[temp_date_y])
                else:
                    print(temp_date_m+':'+format('*'*int(temp_hours),'<23s'),format(temp_hours,f'>18s'))
                streak+=1
                if int(temp_hours)==0:
                    streak = 0
                    
            #show rest of dates
            else:
                
                #no logged hours
                if int(temp_hours)==0:
                    streak = 0
                    #mm/dd + int(hours)
                    print(temp_date_m+':'+format('*'*int(temp_hours),'<23s'),format(temp_hours,f'>18s'))
                    
                #breakthrough day
                elif breakthrough:
                    #mm/dd:hours + int(hours) + /'text'
                    print(temp_date_m+':'+format('*'*int(temp_hours),'<23s'),format(temp[1],f'>18s'),'  /'+self.text[temp_date_y])
                    streak+=1
                    
                #normal day
                else:
                    temp_date = self.format_date(temp_date,2)
                    #mm/dd:hours + int(hours)
                    print(temp_date_m+':'+format('*'*int(temp_hours),'<23s'),format(temp_hours,f'>18s'))
                    streak+=1
        print(f'Streak: {streak}')

    #puts date and hours into goal file. If productive day, puts text in as well.
    def track(self):
        while True:
            hours = input('Hours today: ')
            if hours=='skip':
                break
            elif hours.isnumeric():
                if int(hours)>=24:
                    print('Are you ling ling?')
                    continue
                else:
                    hours = int(hours)
                break
            else:
                print('Must be a whole number')
                continue

        #secret skip function
        if hours=='skip':
            print('Ok')
        else:
            #determine if there was a breakthrough in productivity
            text = input('Any breakthrough? (Press enter to skip): ').capitalize()
            if text=='':
                breakthrough = False
            elif text in ['Nope','No']:
                print("That's life, don't mind!")
                breakthrough = False
            else:
                breakthrough = True
                print("Nice! That's what I like to see.")

            #determine if today is the day the goal was created
            connect = open(f'{self.name}.txt','r')
            data = connect.read()
            data = data.rstrip()
            connect.close()
            is_start_date = False
            if len(data)==0:
                is_start_date = True
                
            #determine if a day was skipped or not
            if not is_start_date:
                #find previous date and split into year, month, and day
                self.analyze()
                previous_date = self.tracked_hours[len(self.tracked_hours)-1].split(':')
                previous_date = self.format_date(previous_date[0],1)
                previous_date = previous_date.split('/')
                #use date(y,m,d) function to find date difference
                day_dif = date(year,month,day) - date(int(previous_date[2]),int(previous_date[0]),int(previous_date[1]))
                day_dif = day_dif.days
                if day_dif==0:
                    same_day = True
                    skipped_date = False
                elif day_dif==1:
                    skipped_date = False
                    same_day = False
                else:
                    skipped_date = True
                    same_day = False
            else:
                skipped_date = False
                same_day = True

            #bug fix: overwriting start date info had wrong data
            start_overwrite = False
            if same_day:
                if len(data)!=0:
                    is_start_date = True
                    start_overwrite = True
            
            #create data string
            data = full_date+':'+str(hours)
            data_text = '@'+full_date+':'+text
            need_data_text = False
            #look out for start date, breakthough date, continued date/continued and breakthrough 
            if is_start_date or skipped_date:
                if breakthrough:
                    data = '!#'+data
                    need_data_text = True
                else:
                    data = '!'+data
            elif breakthrough:
                data = '#'+data
                need_data_text = True
            else:
                pass

            #log data into goal file
            connect = open(f'{self.name}.txt', 'r')
            file_data = connect.read()
            file_data = file_data.rstrip()
            connect.close()
            file_data = file_data.split('\n')
            start_date = False
            if same_day:
                if len(file_data)==1:
                    start_date = True
                elif file_data[-1][0]=='@':
                    del file_data[-1]
                    del file_data[-1]
                else:
                    del file_data[-1]
            connect = open(f'{self.name}.txt','w')
            if not start_date:
                for line in file_data:
                    connect.write(line+'\n')
            connect.write(data+'\n')
            if need_data_text:
                connect.write(data_text+'\n')
            connect.close()
            if start_overwrite:
                print(f'{full_date} overwritten!')
            elif is_start_date:
                print(f'{full_date} logged!')
            elif same_day:
                print(f'{full_date} overwritten!')
            else:
                print(f'{full_date} logged!')
        
 
#get goal from memory file
connect = open('dw_memory.txt','r')
memory = connect.read()
memory = memory.rstrip()
connect.close()

#check if goal from memory file exists
while True:
    try:
        connect = open(f'{memory}.txt','r')
    except:
        print(f'File "{memory}" not found, choose a goal or create a new one:')
        print()
        for file in glob.glob("*.txt"):
            if file=='dw_memory.txt':
                continue
            print(file[39:].replace('.txt','').capitalize())
        print()
        memory = input('Goal name (Press enter to create new goal): ').capitalize()
        if memory=='':
            new_goal = input('Name of new goal: ')
            goal = Goal(new_goal)
            goal.create()
            goal.store_in_memory()
            memory = new_goal
    else:
        goal = Goal(memory)
        goal.store_in_memory()
        break

#log hours today
goal.track()
print()

#ask user for options
running = True
while running:
    action = input('Press enter to display progress, press anything else for more options: ')
    if action=='':
        print()
        goal.display()
        print()
        action = input('Press enter to quit, press anything else for more options: ')
        if action=='':
            break
        else:
            pass
    while True:
        action = input('"l" to list all goals, "c" to change goal, "n" to create new goal, enter to quit: ')
        if action=='l':
            print()
            print('Current goals:')
            for file in glob.glob("*.txt"):
                if file=='dw_memory.txt':
                    continue
                print(file.replace('.txt','').capitalize())
            print()
        elif action=='c':
            new_goal = input('Change to: ').lower()
            temp = goal
            goal = Goal(new_goal)
            print()
            try:
                goal.display()
            except:
                print(f'File data for "{new_goal}" not found')
                print()
                goal = temp
            else:
                goal.store_in_memory()
                print()
                continue
        elif action=='n':
            while True:
                new_goal = input('Create a new goal: ')
                exists = False
                for file in glob.glob("*.txt"):
                    if file==new_goal+'.txt':
                        print('Goal already exists')
                        exists = True
                        break
                if exists:
                    continue
                confirm = input(f"Confirm '{new_goal}' (y/n): ")
                if confirm=='y':
                    create = True
                else:
                    create = False
                break
            if create:
                goal = Goal(new_goal)
                goal.create()
                ask = input('Would you like to store new goal in memory? ("y" to confirm): ')
                if ask=='y':
                    goal.store_in_memory()
                    print('Goal stored!')
            print()
        elif action=='':
            running = False
            break
        else:
            print('Unknown command')



