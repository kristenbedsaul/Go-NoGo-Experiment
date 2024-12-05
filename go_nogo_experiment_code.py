#Go-NoGo Experiment
#10/14/24
#Kristen Bedsaul

#Import modules
from psychopy import gui, core, visual
from psychopy.hardware import keyboard
import random
import csv

#Prep datafile I'm writing out to:
datafile = open('go_nogo_experiment.csv', 'a')
writer = csv.writer(datafile, delimiter = ',')

#Print header row to csv file
writer.writerow(['PID', 'section', 'stimulus', 'key pressed', 'rt', 'accuracy', 'points', 'total points'])

#create dictionary with PID
demographics = {'Last 4 Digits of PID': ''}

#create and show the gui
gui.DlgFromDict(demographics, sortKeys = False)

#save items from gui
pid = demographics['Last 4 Digits of PID']

#Create window and start keyboard
win = visual.Window([800,800], monitor = 'testMonitor', color = 'grey')
kb = keyboard.Keyboard()

#Prep stimuli list (which are my bunny and cat)
bunny = visual.ImageStim(win, image = 'bunny3.jpg', size = (1.5, 2))
cat = visual.ImageStim(win, image = 'cat.jpg', size = (1.5, 1.0))

#Create variables for messages (decoration purposes)
space1_text = 'SPACE'
space1 = visual.TextStim(win, text = space1_text, color = 'green', pos = [-.41, -0.11], bold = True)

#Introduction to experiment
introduction_text = 'Welcome to my Go-NoGo experiment. \
\n\
\nPress              to read the instructions.' 
introduction = visual.TextStim(win, text = introduction_text, color = 'white', wrapWidth = 2, alignText = 'center')
#Drawing and flipping introduction
introduction.draw()
space1.draw()
win.flip()
kb.waitKeys(keyList = ['space'])

#Instructions text for experiment
instructions1_text = 'In this experiment, images of a bunny wearing sunglasses and a cat will QUICKLY appear on the screen. Once the image disappears from the screen, you will respond to the correct image by pressing SPACE.'
instructions2_text = ' You should only respond to this image and withold any response to the other image.'
instructions3_text = 'After the image disappears, if you saw the: '
instructions4_text = '☆ bunny wearing sunglasses → you should respond \
\n    by pressing SPACE as quickly as possible.'
instructions5_text = '☆ cat → you should not respond. \
\n    (do not press SPACE!).'
instructions6_text = 'Press SPACE to begin the experiment.'

#Drawing and flipping instructions
instruction_1st = visual.TextStim(win, text = instructions1_text + instructions2_text, height = 0.08, wrapWidth = 1.75, alignText = 'left', pos = [0, .44])
instruction_2nd = visual.TextStim(win, text = instructions3_text, height = .07, wrapWidth = 1.75, alignText = 'left', pos = [0, -.03], bold = True)
instruction_3rd = visual.TextStim(win, text = instructions4_text, height = .057, wrapWidth = 1.75, alignText = 'left', pos = [.14, -.2])
instruction_4th = visual.TextStim(win, text = instructions5_text, height = .057, wrapWidth = 1.75, alignText = 'left', pos = [.14, -.36])
instruction_5th = visual.TextStim(win, text = instructions6_text, height = .08, wrapWidth = 1.75, pos = [0, -.6])
instruction_1st.draw()
instruction_2nd.draw()
instruction_3rd.draw()
instruction_4th.draw()
instruction_5th.draw()
win.flip()
kb.waitKeys(keyList = ['space'])

#Stimulus 
stimuli = [bunny, bunny, bunny, bunny, bunny, bunny, bunny, bunny, cat, cat]
stimuli_shuffled = random.choices(stimuli, k = 32)

#Establish total points 
total_points = 0

#Create section 1 and 2 functions
def noreward_section(section_num):
    #establish total points for datafile
    global total_points
    
    for stimulus in stimuli_shuffled:
        stimulus.draw()
        win.flip()
        core.wait(.2)
        
        #Resetting clock and collecting key responses
        kb.clock.reset()
        win.flip()
        key_press = kb.waitKeys(keyList = ['space'], maxWait = 1.5)
        
        #establish points for datafile
        points = 0
        
        #Getting timing
        if key_press:
            key = key_press[0].name
            time = key_press[0].rt
        else:
            key = None
            time = None
            
        #Testing accuracy 
        if stimulus == bunny and key == 'space':
            accuracy  = 'Correct!'
        elif stimulus == cat and key is None:
            accuracy = 'Correct!'
        else:
            accuracy = 'Incorrect.'
                    
        #Displaying feedback for section 1 and 2
        feedback1 = visual.TextStim(win, text=accuracy, color = 'green' if accuracy == 'Correct!' else 'red')
        feedback1.draw()
        win.flip()
        core.wait(.25)
        
        #Save data to CSV file
        writer.writerow([pid, section_num, 'bunny' if stimulus == bunny else 'cat', key, time, accuracy, points, total_points])

#Create section 3 and 4 functions
def reward_section(section_num):
    #establish points for datafile
    global total_points 
    for stimulus in stimuli_shuffled:
        stimulus.draw()
        win.flip()
        core.wait(.2)
        
        #Resetting clock and collecting key responses
        kb.clock.reset()
        win.flip()
        key_press = kb.waitKeys(keyList = ['space'], maxWait = 1.5)
        
        #Getting timing
        if key_press:
            key = key_press[0].name
            time = key_press[0].rt
        else:
            key = None
            time = None
        
        #establish indiv. point system for each trial
        points = 0
        
        #test accuracy and assign points
        if stimulus == bunny and key == 'space':
            accuracy  = 'Correct!'
            if time <= 0.4:
                points += 100
                total_points += 100
            elif time > 0.4 and time < 0.6:
                points += 50
                total_points += 50
            else:
                points += 25
                total_points += 25
        elif stimulus == cat and key is None:
            accuracy = 'Correct!'
        else:
            accuracy = 'Incorrect.'
            points -= 100
            total_points -= 100
         
        #Displaying feedback for sections 3 and 4
        if stimulus == bunny or stimulus == cat and key:
            feedback2_text = (' You got ' + str(points) + ' points.' if stimulus == bunny or stimulus == cat and key else '')
            feedback2 = visual.TextStim(win, text = accuracy + feedback2_text, color = 'green' if accuracy == 'Correct!' else 'red')
            feedback2.draw()
            win.flip()
            core.wait(.25)
        
        else:
            feedback2_text = ('')
            feedback2 = visual.TextStim(win, text = feedback2_text)
            feedback2.draw()
            win.flip()
            core.wait(.25)
        
        #Save data to CSV file
        writer.writerow([pid, section_num, 'bunny' if stimulus == bunny else 'cat', key, time, accuracy, points, total_points])
        
#Section 1 (no reward)
def section1():
    noreward_section(section_num = 1)

#Section 2 (no reward)
def section2(): 
    noreward_section(section_num = 2)
    
#Section 3 (reward)
def section3():
    #Instructions for section 3
    pointinstruction_text = 'This section involves a point system. \
    \n\
    \nYou will receive points based on \
    \nthe timing and accuracy of your response. \
    \n\
    \n\
    \nPress SPACE to begin.'
    pointinstruction = visual.TextStim(win, text = pointinstruction_text, color = 'white', wrapWidth = 2)
    pointinstruction.draw()
    win.flip()
    kb.waitKeys(keyList = ['space'])
    
    #Run reward section
    reward_section(section_num = 3)
    
    #Conclusion for section 3
    conclusion_text = 'You have completed this section. \
    \n Press SPACE to continue.'
    conclusion = visual.TextStim(win, text = conclusion_text, wrapWidth = 2)
    conclusion.draw()
    win.flip()
    kb.waitKeys(keyList = ['space'])

#Section 4 (reward)
def section4():
    #Instructions for section 4
    pointinstruction_text = 'This section involves a point system. \
    \n\
    \nYou will receive points based on \
    \nthe timing and accuracy of your response. \
    \n\
    \n\
    \nPress SPACE to begin.'
    pointinstruction = visual.TextStim(win, text = pointinstruction_text, color = 'white', wrapWidth = 2)
    pointinstruction.draw()
    win.flip()
    kb.waitKeys(keyList = ['space'])
    
    #Run reward section
    reward_section(section_num = 4)  
    
    #Conclusion for section 4
    conclusion_text = 'You have completed this section. \
    \n Press SPACE to continue.'
    conclusion = visual.TextStim(win, text = conclusion_text, wrapWidth = 2)
    conclusion.draw()
    win.flip()
    kb.waitKeys(keyList = ['space'])
    
#Run sections in randomized order
function_list = [section1, section2, section3, section4]
random.shuffle(function_list)
for func in function_list:
    func()
    
#Tell user how many points they got
if total_points > 3000:
    final_text = 'You recieved a total of ' + str(total_points) + ' points. You just got a million dollars!'
else: 
    final_text = 'You recieved a total of ' + str(total_points) + ' points. No million dollars.'
end_experiment_text = 'Press SPACE to exit the experiment.'
final_feedback = visual.TextStim(win, text = final_text, color = 'green' if total_points > 3000 else 'red', bold = True)
end_experiment = visual.TextStim(win, text = end_experiment_text, pos = [0, -0.5])
final_feedback.draw()
end_experiment.draw()
win.flip()
kb.waitKeys(keyList = ['space'])
    
#Closing out of everything
datafile.close()
win.close()
core.quit()
