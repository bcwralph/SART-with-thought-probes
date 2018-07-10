import os, sys, pygame, random, csv, inputbox, text_wrapper
pygame.init()
clock=pygame.time.Clock()

hasSelfCaught = True

#set window
window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
center = window.get_rect().center
pygame.mouse.set_visible(False)
fps = 60

#Default Font
fontName = pygame.font.match_font('Times New Roman')
defaultFontSize = 28
font = pygame.font.Font(fontName, defaultFontSize)
mask_font_size = 100

#set colours
grey = (128,128,128)
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
pink = (255,192,203)
backgroundColour = black
stimColour = white

#mask
mask = pygame.image.load("mask.png")
mask_rect = mask.get_rect()
mask_rect.center = center

#set keys
escapeKey = pygame.K_ESCAPE
endKey = pygame.K_e
toggleKey = pygame.K_t
continueKey = pygame.K_s
responseKey = pygame.K_SPACE
selfCaughtKey = pygame.K_m

#display messages
text_pos = (100,100)
wrapSize = (1200,1200)
text_spacing = 1

waitScreen = text_wrapper.drawText("Waiting for the researcher...",
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

taskInstructions = text_wrapper.drawText("In this experiment, you will be presented with the digits 1-9 in the center of the screen."
+" Your task is to press the SPACEBAR in response to each digit except for when that digit is a '3'."
+" For example, if you see the digit '1,' press the spacebar, '4,' press the spacebar, '3,' DO NOT press the spacebar, '7,' press the spacebar."
+"\n\nPlease give equal importance to both the speed and accuracy of your responses."
+'\n\nIn addition, every once in a while, the task will temporarily stop and you will be presented with a thought-sampling screen'
+' that will ask you to indicate whether you were ON TASK or MIND WANDERING just before the thought-sampling screen appeared.',
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

mwInstructionsP1 = text_wrapper.drawText('Being ON TASK means that, JUST BEFORE the thought-sampling screen appeared,'
+' you were focused on completing the task. Some examples of ON TASK thoughts include thoughts about your performance'
+' on the task or thoughts about your response.'
+'\n\nOn the other hand, MIND WANDERING means that, JUST BEFORE the thought-sampling screen appeared,'
+' you were thinking about something completely unrelated to the task. Some examples of MIND WANDERING include thoughts about what'
+' to eat for dinner, thoughts about plans you have with friends, or thoughts about an upcoming test. Any thoughts that you have'
+' that are not related to this task count as MIND WANDERING.'
+'\n\nThe thought-sampling screen will look like this:'
+'\n\nSTOP!'
+'\nWhich of the following best characterizes your mental state JUST BEFORE this screen appeared:'
+'\n\n     (1) On TASK'
+'\n\n     (2) MIND WANDERING'
+'\n\nPlease use the keyboard to select the response option that best describes your mental state just before this screen appeared.',
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

if not hasSelfCaught:
    additionalInstructions = "\n\nDo you have any questions?"+"\n\nWhen you are ready to proceed, please press the SPACEBAR to begin the practice session."
else:
    additionalInstructions = ""

mwInstructionsP2 = text_wrapper.drawText('MIND WANDERING can also occur either because you INTENTIONALLY decided to think about things'
+' that are unrelated to the task, OR because your thoughts UNINTENTIONALLY drifted away to task-unrelated thoughts, despite your best intentions'
+' to focus on the task.'
+'\n\nWhen the thought-sampling screen is presented, if you indicate that you are MIND WANDERING, we will also ask you to indicate'
+' whether the MIND WANDERING you are experiencing is INTENTIONAL or UNINTENTIONAL.'
+'\n\nIf you indicate that you are MIND WANDERING on the previous thought-sampling screen, you will then be presented with the following thought-sampling screen:'
+'\n\nWhich of the following best characterizes your MIND WANDERING:'
+'\n\n     (1) INTENTIONAL MIND WANDERING'
+'\n\n     (2) UNINTENTIONAL MIND WANDERING'
+'\n\nPlease use the keyboard to select the response option that best describes your mind wandering.'
+additionalInstructions,
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

selfCaughtInstructions = text_wrapper.drawText("Sometimes, without seeing a thought-sampling screen, you may be aware that you are MIND WANDERING."
+"\n\nAny time you are aware that you are mind wandering during the task, we would like you to indicate this by pressing"
+" the 'm' key. You will then be asked to indicate whether the mind wandering you were experiencing was INTENTIONAL or UNINTENTIONAL."
+"\n\nYou are now going to complete a brief practice session to help you to become familiar with the task."
+"\n\nDo you have any questions?"
+"\n\nWhen you are ready to proceed, please press the SPACEBAR to begin the practice session.",
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

pracOver = text_wrapper.drawText("The practice trials are now over. Any questions?",
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

taskOver = text_wrapper.drawText("Please notify the researcher that you have finished the task.",
stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

probeScreenOne = text_wrapper.drawText('STOP!'
+'\nWhich of the following best characterizes your mental state JUST BEFORE this screen appeared:'
+'\n\n     (1) On TASK'
+'\n\n     (2) MIND WANDERING'
+'\n\nPlease use the keyboard to select the response option that best describes your mental state just before this screen appeared.',
white, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

probeScreenTwo = text_wrapper.drawText('Which of the following best characterizes your MIND WANDERING:'
+'\n\n     (1) INTENTIONAL MIND WANDERING'
+'\n\n     (2) UNINTENTIONAL MIND WANDERING'
+'\n\nPlease use the keyboard to select the response option that best describes your mind wandering.',
white, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

resume = text_wrapper.drawText("Please press the 's' key to resume the task", white, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

def generateQuestions():
    font=pygame.font.Font(fontName, defaultFontSize)
    qInstruct = text_wrapper.drawText("Please answer the following questions with reference to the task you just performed."
    +"\n\nIndicate your response to each question by pressing the corresponding number key on the keyboard (using the numbers 1-0, with 0 indicating 10)."
    +"\n\nDo your best to use the full range of the scales to most accurately capture your experience."
    +"\n\nPress the 's' key to begin.",
    stimColour, surface=pygame.transform.scale(window, wrapSize), lineSpacing = text_spacing, font=font)

    MOTIVATION = text_wrapper.drawText("How motivated were you to do well on the tasks in this experiment?"
    +"\n\n1) Not at all motivated \n2) \n3)  \n4)  \n5) \n6) \n7) \n8) \n9) \n10) Extremely motivated",
    stimColour, surface=pygame.transform.scale(window, (1200,1200)), lineSpacing = text_spacing, font=font)

    questArray = {MOTIVATION[0]:''}
    return qInstruct, questArray, MOTIVATION

if not hasSelfCaught:
    instructionList = [taskInstructions[0],mwInstructionsP1[0],mwInstructionsP2[0]]
else:
    instructionList = [taskInstructions[0],mwInstructionsP1[0],mwInstructionsP2[0], selfCaughtInstructions[0]]

#trial parameters
stimList=["1", "2", "3", "4", "5", "6", "7", "8", "9"]
numPracticeBlocks = 2
numPracticeTrials = numPracticeBlocks*len(stimList)
numBlocks = 100
numTrials = numBlocks*len(stimList)

sizeList=["48", "72", "94", "100", "120"]
trialSizeList = []
#create balanced & randomized list of font size
for i in range(numTrials/len(sizeList)):
    random.shuffle(sizeList)
    for i in sizeList:
        trialSizeList.append(i) 

#probe information
num_probes = 18 # in 50 trial blocks (900 / 50) = 18
probeList=[]
probeBlocks=range(0,950,50)
for i in range(num_probes):
    probeList.append(random.randint(probeBlocks[i],probeBlocks[i+1]-1))

stim_duration = 250
mask_duration = 900
trial_duration = stim_duration+mask_duration

def drawStim(stimulus, size):
    font = pygame.font.Font(fontName,size)
    stim = font.render(stimulus, True, stimColour, backgroundColour)
    stim_rect = stim.get_rect()
    stim_rect.center = center
    window.blit(stim,stim_rect)
    return stim_rect

def coverStim(stim_rect):
    pygame.draw.rect(window,backgroundColour,stim_rect)

def coverMask(mask_rect):
    pygame.display.update(pygame.draw.rect(window,backgroundColour,mask_rect))

def drawScreen(text_to_draw):
    pygame.display.update([window.fill(backgroundColour), window.blit(text_to_draw,text_pos)])

def responseLoop():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == escapeKey: 
                endExperiment()
            elif event.type == pygame.KEYDOWN and event.key == continueKey:
                done = True
        clock.tick(fps)

def getReady():
    font = pygame.font.Font(fontName,defaultFontSize)
    stim = font.render("Get Ready...", True, stimColour, backgroundColour)
    stim_rect = stim.get_rect()
    stim_rect.center = center
    
    pygame.display.update([window.fill(backgroundColour), window.blit(stim,stim_rect)])
    pygame.time.wait(trial_duration)
    
    pygame.draw.rect(window,backgroundColour,stim_rect)
    #mask_rect = drawStim("X", mask_font_size)
    pygame.display.update([window.fill(backgroundColour), window.blit(mask,mask_rect)])
    pygame.time.wait(mask_duration)

    coverMask(mask_rect)
    #pygame.display.update(window.fill(backgroundColour))

def drawProbe(stop, probeOneResp, probeTwoResp, probeType):
    if probeType == "probe": #if probe caught, draw first probe asking about on-task or mind wandering
        drawScreen(probeScreenOne[0])
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == escapeKey: 
                    endExperiment()
                elif event.type == pygame.KEYDOWN and event.key == endKey:
                    done = True
                    stop = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    done = True; probeOneResp="on_task"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    done = True; probeOneResp="MW"
            clock.tick(fps)
        
    if not stop and probeOneResp != "on_task":#Otherwise, if on-task not selected, ask Deliberate/Spontaneous
        drawScreen(probeScreenTwo[0])
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == escapeKey: 
                    endExperiment()
                elif event.type == pygame.KEYDOWN and event.key == endKey:
                    done = True
                    stop = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    done = True; probeTwoResp="int"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    done = True; probeTwoResp="unint"
            clock.tick(fps)   
    
    drawScreen(resume[0])
    responseLoop()

    getReady()
    
    return stop, probeOneResp, probeTwoResp, probeType

def runBlock(stop, recordData, block, trialCounter, probeList):
    random.shuffle(stimList)

    for stim in stimList:
        stimSize = int(trialSizeList[trialCounter])
        stim_rect = drawStim(stim, stimSize)

        stimulus_at = pygame.time.get_ticks()
        end_at = stimulus_at + trial_duration

        mask_on = False
        has_pressed = False
        RT = ""
        omission = 1
        comission = 0
        probeType=''
        probeOneResp=''
        probeTwoResp=''

        while pygame.time.get_ticks() < end_at and not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    endExperiment()
                if event.type == pygame.KEYDOWN and event.key == endKey: 
                    stop = True
                    break
                if event.type == pygame.KEYDOWN and event.key == responseKey and not has_pressed:
                    RT = pygame.time.get_ticks() - stimulus_at
                    has_pressed = True
                    omission = 0
                    if int(stim) == 3:
                        comission = 1
                if event.type==pygame.KEYDOWN and event.key == selfCaughtKey and hasSelfCaught:
                    stop, probeOneResp, probeTwoResp, probeType = drawProbe(stop, probeOneResp, probeTwoResp, "self")
                    omission = 0
                    break

            if not mask_on and pygame.time.get_ticks()-stimulus_at >= stim_duration:
                coverStim(stim_rect)
                #drawStim("X", mask_font_size)
                window.blit(mask,mask_rect)
                mask_on = True

            pygame.display.update()
            clock.tick(fps)

        if trialCounter in probeList:
            stop, probeOneResp, probeTwoResp, probeType = drawProbe(stop, probeOneResp, probeTwoResp, "probe")

        if recordData == True:
            data.append([subject, sona_id, subject_sex, subject_age, t, trialCounter, stim, stimSize, omission, comission, RT, probeType, probeOneResp, probeTwoResp])

        trialCounter+=1
        coverMask(mask_rect)
        if stop:
            break

    return stop, trialCounter

#general loop for 10-point scale questionnaire items
def drawQs(item, qKeys):    
    window.fill(backgroundColour)
    window.blit(item, text_pos)
    pygame.display.update()
    response=''
    done = False
    stop = False
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == endKey: stop = True
            elif event.type==pygame.KEYDOWN:
                if event.key == pygame.K_1: done=True; response=1
                elif event.key == pygame.K_2:done=True; response=2
                elif event.key == pygame.K_3:done=True; response=3
                elif event.key == pygame.K_4:done=True; response=4
                elif event.key == pygame.K_5:done=True; response=5
                elif event.key == pygame.K_6:done=True; response=6
                elif event.key == pygame.K_7:done=True; response=7
                elif event.key == pygame.K_8:done=True; response=8
                elif event.key == pygame.K_9:done=True; response=9
                elif event.key == pygame.K_0:done=True; response=10
                else:continue
            else:continue
        if stop:break
        clock.tick(fps)
    
    questArray[item]=response
    return stop, questArray

def saveData():
    headers = ["subject", "sonaID", "gender", "age", "block", "trialCounter", "stimulus", "size", "omission", "comission", "RT", "probeType", "probeOneResp", "probeTwoResp", "MOTIVATION"]
    with open ("data/"+str(subject)+"_data.csv","wb") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i in data:
            writer.writerow(i)
        f.flush()
        f.close()

def endExperiment():
    saveData()
    pygame.quit()
    sys.exit() 

#collect subject information
subject = str(inputbox.ask(window, 'Subject'))
sona_id = str(inputbox.ask(window, 'Sona ID'))
subject_age = str(inputbox.ask(window, 'age'))
subject_sex = str(inputbox.ask(window, 'gender'))

data = []

#### Wait Screen
drawScreen(waitScreen[0])
responseLoop()

#### Instructions
for i in instructionList:
    drawScreen(i)
    responseLoop()

### Practice trials
pygame.display.update(window.fill(backgroundColour))
practiceProbe = [numPracticeTrials/2]
recordData = False
trialCounter = 0
getReady()
stop = False
for p in range(numPracticeBlocks):
    stop, trialCounter = runBlock(stop, recordData, p, trialCounter, practiceProbe)
    if stop:
        break

### Practice Over
drawScreen(pracOver[0])
responseLoop()

### Do Experiment
pygame.display.update(window.fill(backgroundColour))
recordData = True
trialCounter = 0
stop = False
getReady()
for t in range(numBlocks):
    stop, trialCounter = runBlock(stop, recordData, t, trialCounter, probeList)
    if stop == 1:
        break

### Any Questionnaires?
qInstruct, questArray, MOTIVATION = generateQuestions()
drawScreen(qInstruct[0])
responseLoop()
qKeys = questArray.keys()
random.shuffle(qKeys)
for item in qKeys:
    stop, questArray = drawQs(item, qKeys)
    if stop:
        break

data.append([subject, sona_id, subject_sex, subject_age, 'questionnaire', 'questionnaire', 'null', 'null', 'null', 'null', 'null', 'null', 'null', 'null', questArray[MOTIVATION[0]]])

### End Screen
drawScreen(taskOver[0])
done=False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            done = True
    clock.tick(fps)
endExperiment()