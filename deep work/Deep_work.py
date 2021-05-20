"""
WIlliam Qin
5/18/21
Version 1
"""

#finding today's date: mm-dd-YY
from datetime import date
today = date.today()
full_date = today.strftime("%m-%d-%Y")
month = today.month
year = today.year
day = today.day

#create goal object
class Goal:
    def __init__(self,name):
        self.name = name
        
    #create new goal file
    def create_goal(self):
        connect = open(f'{self.name}.txt','w')
        connect.write(str(month)+'/')
        connect.write(str(day)+'/')
        connect.write(str(year)+':')
        connect.write(str(0)+'\n')
        connect.close()
        print('New goal "{self.name}" created!')

    #stores goal in memory
    def store_in_memory(self):
        connect = open('dw_memory.txt','w')
        connect.write(self.name)
        connect.close()

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
            #start date and continued days (!)
            if line[0]=='!':
                temp = line.split(':')
                self.start_dates+=[temp[0].replace('!','')]
                self.tracked_hours+=[line.replace('!','')]
            #text (@)
            elif line[0]=='@':
                temp = line.split(':')
                temp_date = temp[0].replace('@','')
                temp_text = temp[1]
                self.text[temp_date] = temp_text
            #tracked hours (productive day = #)
            else:
                self.tracked_hours+=[line]

    #prints the data out.
    # Shows when the goal was started, when it was continued, how productive each day was,
    # describes particularly productive days, and missed days.
    def display(self):
        print(f'Goal: {self.name.capitalize()}')
        is_start_date = True
        missed_days = 0
        for line in self.tracked_hours:
            #show start date
            if line in self.start_dates and is_start_date:
                temp = line.split(':')
                start_date = temp[0]
                print(f'Start date: {start_date}')
                is_start_date = False
            #show continued date
            elif line in self.start_dates:
                temp = line.split(':')
                continued_date = temp[0]
                print('-------------------------')
                print(f'Continued: {continued_date}')
            #show hours
            else:
                #print out date and stars
                temp = line.split(':')
                temp_date = temp[0]
                temp_hours = int(temp[1])
                #check for breakthrough day
                if '#' in temp_date:
                    breakthrough = True
                else:
                    breakthrough = False
                #no logged hours
                if temp_hours==0:
                    missed_days+=1
                    print(temp_date+':')
                #breakthrough day
                elif breakthrough:
                    temp_date = temp_date.replace('#','')
                    print(temp_date+':',end='')
                    print('*'*temp_hours)
                    print(temp_date+':'+self.text[temp_date])
                #normal day
                else:
                    print(temp_date+':',end='')
                    print('*'*temp_hours)
        print()
        print(f'Missed days: {missed_days}')


goal = Goal('cat')
goal.analyze()
goal.display()
    

'''        
#get goal from memory file
while True:
    connect = open('dw_memory.txt','r')
    memory = connect.read()

    #if nothing stored in memory file, create a new goal
    if len(memory)==0:
        while True:
            new_goal = input('Create a new goal: ')
            confirm = input(f"Confirm '{new_goal}' (y/n): ")
            if confirm=='y':
                break
            else:
                continue

        #store the goal in memory
        connect.close()
        

        #create goal file
        
        continue
        
    #else, retrieve data
    else:
        goal = memory
        connect.close()
        break

'''

"""

#log hours today
while True:
    try:
        hours = int(input('Hours today: '))
    except:
        continue
    else:
        break
print('Good work mate.')
#some logging stuff

#additional actions
check = input('continue? ')
if check=='n':
    print('Good work!')
    #show list
else:
    while True:
        action = input('
"""
