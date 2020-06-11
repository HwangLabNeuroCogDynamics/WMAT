5## Working Memory Alpha Theta (WMAT)
# 08/27/19: Changed response loop to exit when subject makes a response (rather than waiting full 2 seconds)
# 07/31/19: change subresp to always be 2 seconds, don't terminate early, fix triggers csv writing
# 07/30/19: adding triggers for cue period
# 07/17/19: adding masks and load 3 condition, shortened delay from 2 to 1 sec

#from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle,uniform,permutation
import os  # handy system and path functions
import sys  # to get file system encoding
import serial #for sending triggers from this computer to biosemi computer
import csv
from psychopy import visual, core
import glob


expInfo = {'subject': '', 'EEG? [y/n]':'n','mm_r_Cue':.5,'mm_r_noCue':.5,'refresh':50} #mm_r (mismatch_ratio) is the likelihood of changes between memory and probe arrays
expName='WMAT_revision' # working memory alpha theta
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1000,700],units='deg',fullscr=True,monitor='testMonitor',checkTiming=True) #1680,1050]


## Set up EEG flags
if expInfo['EEG? [y/n]']=='y':
    EEGflag=1
else:
    EEGflag=0

if EEGflag:
    print(os.getcwd())
    thisDir_save = os.path.dirname(os.path.abspath(__file__))
    thisDir_save=thisDir_save.split('/')
    thisDir_save='/'.join(thisDir_save[:-1])
    thisDir_save=thisDir_save+'/WMAT_data_and_others'
#    filename=os.getcwd()+'/WMAT_data/eeg_data/eeg_behav_data'+u'/%s_%s_%s' % (expInfo['subject'], expName, expInfo['date'])
    filename=thisDir_save+'/WMAT_data/eeg_data/eeg_behav_data'+u'/%s_%s_%s' % (expInfo['subject'], expName, expInfo['date'])
    port=serial.Serial('COM4',baudrate=115200)
    port.close()
    port.open()
    startSaveflag=bytes([201]) #254
    stopSaveflag=bytes([255]) #255
    
    load_two_trig=109
    load_three_trig=111
    load_four_trig=113
    
    cue_face_trig=115
    cue_scene_trig=117
    
    delay_trig=119
    
    cue_mismatch_noCue_mismatch_trig=101
    cue_mismatch_noCue_match_trig=103
    cue_match_noCue_mismatch_trig=105
    cue_match_noCue_match_trig=107
    
    subNonResp_trig=121
    subResp_trig=123
    
    ITI_trig=125
else:
    print(os.getcwd())
    thisDir_save = os.path.dirname(os.path.abspath(__file__))
    thisDir_save=thisDir_save.split('/')
    thisDir_save='/'.join(thisDir_save[:-1])
    thisDir_save=thisDir_save+'/WMAT_data_and_others'
    filename=thisDir_save+'/WMAT_data/behav_data/'+u'/%s_%s_%s' % (expInfo['subject'], expName, expInfo['date'])

refresh_rate=int(expInfo['refresh'])

for key in ['escape']:
    event.globalKeys.add(key, func=core.quit)

num_trials=34 #divisible by 2 so that an equal number of trials are cued FACE as cued SCENE
num_reps=3 # the number of repeats of ea condition, 
## *** THE TOTAL NUM OF BLOCKS will be determined by [the number of conditions]*[number of repeats] *** ##

yes_key='1'
no_key='0'

def wait_here(t):
    interval=1/refresh_rate
    num_frames=int(t/interval)
    for n in range(num_frames): #change back to num_frames
        #fixation.draw()
        win.flip()

def make_ITI():
    if not EEGflag:
        ITI=np.random.choice([2,2.3,2.5,2.7,3,3.3,3.5,3.7],1)[0] #averages to around 2 second?
    else:
        ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI

## pracCond mirrors trial loop; see trial loop for detailed comments
def pracCond(num_load=2,n_practrials=6,demo=False):
    pracDataList=[]
    if demo:
        prac_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin a demo')
    else:
        prac_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin the practice')
    load_num=num_load
    word_cues=[]
    for n in range(int(n_practrials/2)):
        word_cues.append('face')
        word_cues.append('scene')
    word_cues_scramble=list(np.random.permutation(word_cues))
    match_mismatch_cue=[] #populating this list with each trial's status as a match or mismatch trial
    n_mismatch=int(n_practrials*expInfo['mm_r_Cue'])
    n_match=n_practrials-n_mismatch
    for m in range(n_mismatch):
        match_mismatch_cue.append('mismatch')
    for n in range(n_match):
        match_mismatch_cue.append('match')
    match_mismatch_scramble=list(np.random.permutation(match_mismatch_cue))
    prac_msg2.draw()
    win.update()
    key1=event.waitKeys()
    fixation.color=([1,1,1])
    fixation.draw()
    win.flip() 
    core.wait(3)# pre-block pause
    for trial in range(len(word_cues_scramble)):
        ITI=make_ITI()
        fixation.autoDraw=False
        cue_word=word_cues_scramble[trial]
        cue_word_obj=cue_words_dict[cue_word]
        cue_word_obj.autoDraw=True
        wait_here(0.5) # display cue
        cue_word_obj.autoDraw=False
        fixation.autoDraw=True
        faces_display=[]
        randos=np.random.choice(range(len(Img_Face)),load_num,replace=False)
        for i in randos: #picking random faces, randomly loading indexes of face imgs 
            faces_display.append(Img_Face[str(i)])
        #print(faces_display)
        randos_scene=np.random.choice(range(len(Img_Scene)),load_num,replace=False)
        scenes_display=[]
        for i in randos_scene:
            scenes_display.append(Img_Scene[str(i)])
        randos_mask=np.random.choice(list(Img_Mask.keys()),(load_num*2),replace=False)
        masks_display=[]
        for m in randos_mask:
            masks_display.append(Img_Mask[m])
        hemis=np.random.choice(['R','L'],2,replace=False) #pick which side the faces display is on and which the scenes are
        faces_hemi=hemis[0]
        scenes_hemi=hemis[1]
        if load_num==2:
            faces_display[0].pos=two_items['upper_'+faces_hemi]
            faces_display[1].pos=two_items['lower_'+faces_hemi]
            scenes_display[0].pos=two_items['upper_'+scenes_hemi]
            scenes_display[1].pos=two_items['lower_'+scenes_hemi]
        elif load_num==4:
            faces_display[0].pos=four_items['upper_upper_'+faces_hemi]
            faces_display[1].pos=four_items['upper_middle_'+faces_hemi]
            faces_display[2].pos=four_items['lower_middle_'+faces_hemi]
            faces_display[3].pos=four_items['lower_lower_'+faces_hemi]
            scenes_display[0].pos=four_items['upper_upper_'+scenes_hemi]
            scenes_display[1].pos=four_items['upper_middle_'+scenes_hemi]
            scenes_display[2].pos=four_items['lower_middle_'+scenes_hemi]
            scenes_display[3].pos=four_items['lower_lower_'+scenes_hemi]
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        if demo:
            win.flip()
            core.wait(3)
        else:
            wait_here(1) # display face/scene arrays
        faces_scram=masks_display[:num_load]
        scenes_scram=masks_display[num_load:]
        for face_n in range(num_load):
            face=faces_display[face_n]
            face.autoDraw=False
            faces_scram[face_n].pos=face.pos
            faces_scram[face_n].autoDraw=True
        for scene_n in range(num_load):
            scene=scenes_display[scene_n]
            scene.autoDraw=False
            scenes_scram[scene_n].pos=scene.pos
            scenes_scram[scene_n].autoDraw=True
        fixation.autoDraw=True
        wait_here(1) #delay 
        for fs in faces_scram:
            fs.autoDraw=False 
        for ss in scenes_scram:
            ss.autoDraw=False
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        trial_match=match_mismatch_scramble[trial]
        print(trial_match)
        if trial_match=='match':
            corr_resp=yes_key # yes it's the same
        elif trial_match=='mismatch':
            if cue_word=='face':
                display_to_change=faces_display
                dict_of_images=Img_Face
            elif cue_word=='scene':
                display_to_change=scenes_display
                dict_of_images=Img_Scene
            replace_ind=np.random.choice(range(load_num),1)[0] #randomly pick an index to replace
            replace_stim=display_to_change[replace_ind] # only to initiate while loop 
            while replace_stim in display_to_change: # and randomly switch it with a previously not displayed picture
                rand_choice_key=np.random.choice(list(dict_of_images.keys()),1)[0]
                replace_stim=dict_of_images[rand_choice_key]
            replaced_img=display_to_change[replace_ind]
            replaced_img.autoDraw=False # turn off the old image so that the new one is not overwritten
            replace_stim.autoDraw=True
            replace_stim.pos=replaced_img.pos # transfer over the position
            display_to_change[replace_ind]=replace_stim
            corr_resp=no_key # no, it's not the same as the memory array
        if not demo:
            event.clearEvents()
            max_win_count=int(2/(1/refresh_rate))
            win_count=0
            subRespo=None
            RT_clock.reset()
            while not subRespo:
                win.flip()
                subRespo=event.getKeys(timeStamped=RT_clock,keyList=[yes_key,no_key])
                win_count=win_count+1
                if win_count==max_win_count:
                    break
            print(subRespo)
            if not subRespo:
                trial_Corr=0
            elif subRespo[0][0]==corr_resp:
                trial_Corr=1
            elif subRespo[0][0]!=corr_resp:
                trial_Corr=0
        elif demo:
            probe_pause=visual.TextStim(win, pos=[0,.85],units='norm',text='Is this the same array of photos you saw before? Press %s for yes or %s for no' %(yes_key,no_key))
            probe_pause.draw()
            win.flip()
            event.waitKeys(keyList=[yes_key,no_key])
        for face in faces_display:
            face.autoDraw=False
        for scene in scenes_display:
            scene.autoDraw=False
        fixation.autoDraw=True
        if not demo:
            pracDataList.append(trial_Corr)
        wait_here(ITI)
    if not demo:
        acc_feedback=visual.TextStim(win, pos=[0,.5],units='norm',text='Your accuracy for the practice round was %i percent. Practice again? (y/n)' %(100*(np.sum(pracDataList)/n_practrials)))
        acc_feedback.draw()
        win.update()
        cont=event.waitKeys(keyList=['y','n'])
        fixation.color=([1,1,1])
        if cont[0]=='y':
            pracCond(num_load,n_practrials)

def make_csv(filename):
    with open(filename+'.csv', mode='w') as csv_file:
    
       # {'block':block,'load':load_num, '(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)':(expInfo['mm_r_Cue'],n_mismatch,n_match),
        #'(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)':(expInfo['mm_r_noCue'],n_mismatch_nc,n_match_nc),'trialsData':trialDataList}})
        #{'trialNum':(trial),'cue_word':cue_word,'match_mismatch_Cue':trial_cue_match, 'match_mismatch_notCue':trial_noCue_match,
         #                   'corrResp':corr_resp,'subjectResp':subKEY,'trialCorr?':trial_Corr,'RT':rt, 
          #                  'ITI':ITI,'hemis (face,scene)':(faces_hemi,scenes_hemi),
           #                 'probe_array([faces],[scenes])':([face.image.split('/')[-1] for face in faces_display],[scene.image.split('/')[-1] for scene in scenes_display]),
            #                'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':(replaced_img_cue_name,replaced_img_cue_pos,replaced_img_noCue_name,replaced_img_noCue_pos),
             #               'trial_trigs':(thistrialFlag,probetrig,resp_trig)}
        
        fieldnames=['block','load','(cue_ratio,mm_trials,m_trials)','(nonCue_ratio,mm_trials,m_trials)',
                    'trialNum','cue_word','match_mismatch_cue','match_mismatch_nonCue','probe_array([faces],[scenes])',
                    'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)','corrResp','subResp','trialCorr?','RT','ITI','trial_trigs']
        #fieldnames is simply asserting the categories at the top of the CSV
        writer=csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        print('\n\n\n')
        for n in range(len(blocks.keys())): # loop through each block
            blocks_data = list(blocks.keys())[n]
            ThisBlock=blocks[blocks_data] #grabbing the block info for this block
            #print(ThisBlock)
            #print('\n')
            for k in range(len(ThisBlock['trialsData'])): #this should be the # of trials
                ThisTrial=ThisBlock['trialsData'][k] #grabbing the trial info out of data for this trial
                
                if EEGflag:
                    writer.writerow({'block':ThisBlock['block'],'load':ThisBlock['load'],'(cue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)'],
                                    '(nonCue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)'],
                                    'trialNum':ThisTrial['trialNum'],'cue_word':ThisTrial['cue_word'],'match_mismatch_cue':ThisTrial['match_mismatch_Cue'],
                                    'match_mismatch_nonCue':ThisTrial['match_mismatch_notCue'],'probe_array([faces],[scenes])':ThisTrial['probe_array([faces],[scenes])'],
                                    'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':ThisTrial['replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'ITI':ThisTrial['ITI'],'trial_trigs':ThisTrial['trial_trigs']})
                else:
                    writer.writerow({'block':ThisBlock['block'],'load':ThisBlock['load'],'(cue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)'],
                                    '(nonCue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)'],
                                    'trialNum':ThisTrial['trialNum'],'cue_word':ThisTrial['cue_word'],'match_mismatch_cue':ThisTrial['match_mismatch_Cue'],
                                    'match_mismatch_nonCue':ThisTrial['match_mismatch_notCue'],'probe_array([faces],[scenes])':ThisTrial['probe_array([faces],[scenes])'],
                                    'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':ThisTrial['replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'ITI':ThisTrial['ITI'],'trial_trigs':ThisTrial['trial_trigs']})


## Setting up the distance from the center of the arrays around fixation, changes with the # of items per side
#vis_deg=3.5
dist=9#6 for mac laptop

two_items={'upper_R':(dist,0.5*dist),'lower_R':(dist,-0.5*dist),'upper_L':(-1*dist,0.5*dist),'lower_L':(-1*dist,-0.5*dist)}
three_items={'upper_R':(dist,0.66*dist),'middle_R':(dist,0),'lower_R':(dist,-0.66*dist),'upper_L':(-1*dist,0.66*dist),'middle_L':(-1*dist,0),'lower_L':(-1*dist,-0.66*dist)}
four_items={'upper_upper_R':(dist,dist),'upper_middle_R':(dist,dist/3),
            'lower_lower_R':(dist,-1*dist),'lower_middle_R':(dist,-1*(dist/3)),'upper_upper_L':(-1*dist,dist),
            'upper_middle_L':(-1*dist,(dist/3)),'lower_lower_L':(-1*dist,-1*dist),'lower_middle_L':(-1*dist,-1*(dist/3))}

##Dictionaries and the corresponding file paths
direc = os.getcwd()+'/localizer_stim/' #_thisDir #'/Users/mpipoly/Desktop/Psychopy/localizer_stim/' #always setup path on the fly in case you switch computers
ext = 'scenes/*.jpg' #file delimiter
faces_ext = 'faces/*.jpg'
mask_ext = 'scrambled/black_and_white/*.jpg'
faces_list = glob.glob(direc + faces_ext)
scenes_list = glob.glob(direc + ext)
masks_list= glob.glob(direc + mask_ext )
#print(faces_list)
#print(scenes_list)
Img_Scene = {}
Img_Face = {}
Img_Mask = {}

size=5.5#3.8 for mac laptop 

## Gathering the images from the RDSS to display in stimuli arrays
for f in range(len(faces_list)):
    Img_Face[str(f)]= visual.ImageStim(win=win, image=faces_list[f],name=str(f),size=size)
for s in range(len(scenes_list)):
    Img_Scene[str(s)]=visual.ImageStim(win=win,image=scenes_list[s],name=str(s),size=size)
for m in range(len(masks_list)):
    Img_Mask[str(m)]=visual.ImageStim(win=win,image=masks_list[m],name=str(m),size=size)

cue_words_dict={'face':visual.TextStim(win,text='face',units='norm',color=(1,1,1)),'scene':visual.TextStim(win,text='scene',units='norm',color=(1,1,1))}

fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6

## Present instruction screens
intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see the word FACE or SCENE on the screen, then a series of face and scene pictures')
intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')
intro_msg.draw()
intro_msg2.draw() 
intro_msg3.draw()
win.flip()
event.waitKeys()
intro_mesg4= visual.TextStim(win,pos=[0,.5],units='norm',text='Pay attention to the pictures matching the word cue given.')
intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Press %s if the pictures match the previous ones you saw, or %s if they do not match' %(yes_key,no_key))
intro_mesg6=visual.TextStim(win,pos=[0,-0.5],units='norm',text='PLEASE ALWAYS KEEP YOUR EYES ON THE CROSS IN THE MIDDLE OF THE SCREEN. Press any key to continue.')
intro_mesg4.draw()
intro_mesg5.draw()
intro_mesg6.draw()
win.flip()
event.waitKeys()
win.flip()

RT_clock=core.Clock()

## Set up the frequency of the conditions to be run through in order to count the number of blocks
loads=['2','3','4']

stimList=[]
for l in loads:
    for i in range(num_reps):
        stimList.append(l) # len(stimList) will be the # of blocks

stimList_scramble=list(np.random.permutation(stimList)) # scramble the order

if EEGflag:
    port.write(startSaveflag) # begin saving EEG data to BDF

pracCond(n_practrials=4,demo=True) # if Demo=True, subjects will be prompted to respond at their own pace
prac_num_load=2
pracCond(num_load=prac_num_load)

## Enter block loop
blocks={}
for block in range(len(stimList_scramble)):
    
    if block !=0:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to continue to the next block')
    else:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin experiment')
    
    ## Grab the load # for this block 
    load_num=int(stimList_scramble[block])
    
    ## Create a list of 'face' or 'scene' strings which will tell us which side to Cue for ea trial
    word_cues=[]
    for n in range(int(num_trials/2)):
        word_cues.append('face')
        word_cues.append('scene')
    word_cues_scramble=list(np.random.permutation(word_cues))
    
    ## Defined whether each trial will be a match or a mismatch 
    match_mismatch_cue=[] #populating this list with each trial's status as a match or mismatch trial for the CUEd array
    n_mismatch=int(num_trials*expInfo['mm_r_Cue'])
    n_match=num_trials-n_mismatch
    print(n_mismatch)
    print(n_match)
    for m in range(n_mismatch):
        match_mismatch_cue.append('mismatch')
    for n in range(n_match):
        match_mismatch_cue.append('match')
    match_mismatch_cue_scramble=list(np.random.permutation(match_mismatch_cue)) # scramble the order
    
    match_mismatch_Nocue=[] #populating this list with each trial's status as a match or mismatch trial for the NON CUEd array
    n_mismatch_nc=int(num_trials*expInfo['mm_r_noCue'])
    n_match_nc=num_trials-n_mismatch_nc
    print(n_mismatch_nc)
    print(n_match_nc)
    for m in range(n_mismatch_nc):
        match_mismatch_Nocue.append('mismatch')
    for n in range(n_match_nc):
        match_mismatch_Nocue.append('match')
    match_mismatch_Nocue_scramble=list(np.random.permutation(match_mismatch_Nocue))
    
    info_msg2.draw() # display the intro text for this block
    win.update()
    key1=event.waitKeys()
    fixation.color=([1,1,1])
    fixation.draw()
    win.flip() 
    core.wait(3)# pre-block pause
    
    trialDataList=[]
    
    ## Enter trial loop
    for trial in range(len(word_cues_scramble)):
        ITI=make_ITI()
        
        fixation.autoDraw=False
        
        cue_word=word_cues_scramble[trial]
        cue_word_obj=cue_words_dict[cue_word] 
        cue_word_obj.autoDraw=True
        
        if EEGflag:
            if cue_word=='face':
                thisCuetrig=cue_face_trig
            else:
                thisCuetrig=cue_scene_trig
            win.callOnFlip(port.write,bytes([thisCuetrig]))
        
        wait_here(0.5) # display cue #######################################
        
        cue_word_obj.autoDraw=False
        fixation.autoDraw=True
        
        faces_display=[]
        randos_face=np.random.choice(list(Img_Face.keys()),load_num,replace=False) # randomly select faces
        for i in randos_face: #picking random faces, randomly loading indexes of face imgs 
            faces_display.append(Img_Face[i])
        
        randos_scene=np.random.choice(list(Img_Scene.keys()),load_num,replace=False) # randomly select scenes
        scenes_display=[]
        for k in randos_scene:
            scenes_display.append(Img_Scene[k])
            
        randos_mask=np.random.choice(list(Img_Mask.keys()),(load_num*2),replace=False)
        masks_display=[]
        for m in randos_mask:
            masks_display.append(Img_Mask[m])
        
        hemis=np.random.choice(['R','L'],2,replace=False) #pick which side the faces display is on and which the scenes are
        faces_hemi=hemis[0]
        scenes_hemi=hemis[1]
        
        
        ## assigning the locations of the scene pictures and face pictures, where faces_hemi and scenes_hemi indicate the left or the right side of the screen
        if load_num==2:
            
            faces_display[0].pos=two_items['upper_'+faces_hemi]
            faces_display[1].pos=two_items['lower_'+faces_hemi]
            scenes_display[0].pos=two_items['upper_'+scenes_hemi]
            scenes_display[1].pos=two_items['lower_'+scenes_hemi]
            
        if load_num==3:
            
            faces_display[0].pos=three_items['upper_'+faces_hemi]
            faces_display[1].pos=three_items['lower_'+faces_hemi]
            faces_display[2].pos=three_items['middle_'+faces_hemi]
            scenes_display[0].pos=three_items['upper_'+scenes_hemi]
            scenes_display[1].pos=three_items['lower_'+scenes_hemi]
            scenes_display[2].pos=three_items['middle_'+scenes_hemi]
            
        elif load_num==4:
            
            faces_display[0].pos=four_items['upper_upper_'+faces_hemi]
            faces_display[1].pos=four_items['upper_middle_'+faces_hemi]
            faces_display[2].pos=four_items['lower_middle_'+faces_hemi]
            faces_display[3].pos=four_items['lower_lower_'+faces_hemi]
            scenes_display[0].pos=four_items['upper_upper_'+scenes_hemi]
            scenes_display[1].pos=four_items['upper_middle_'+scenes_hemi]
            scenes_display[2].pos=four_items['lower_middle_'+scenes_hemi]
            scenes_display[3].pos=four_items['lower_lower_'+scenes_hemi]
        
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        
        if EEGflag:
            if load_num==2:
                thisEncoding_trig=load_two_trig
            elif load_num==3:
                thisEncoding_trig=load_three_trig
            elif load_num==4:
                thisEncoding_trig=load_four_trig
            win.callOnFlip(port.write,bytes([thisEncoding_trig]))
        
        wait_here(1) # display face/scene arrays ##########################
        
        faces_scram=masks_display[:load_num]
        scenes_scram=masks_display[load_num:]
        for face_n in range(load_num):
            face=faces_display[face_n]
            face.autoDraw=False
            faces_scram[face_n].pos=face.pos
            faces_scram[face_n].autoDraw=True
        for scene_n in range(load_num):
            scene=scenes_display[scene_n]
            scene.autoDraw=False
            scenes_scram[scene_n].pos=scene.pos
            scenes_scram[scene_n].autoDraw=True
        
        fixation.autoDraw=True
        
        if EEGflag:
            win.callOnFlip(port.write,bytes([delay_trig]))
        
        wait_here(2) #delay ############################################
        
        for m in range(load_num):
            faces_scram[m].autoDraw=False
            scenes_scram[m].autoDraw=False
        
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        trial_cue_match=match_mismatch_cue_scramble[trial]
        print(trial_cue_match)
        trial_noCue_match=match_mismatch_Nocue_scramble[trial]
        
        ## If this trial is a match trial, we keep everything the same for the cued array
        ## But if not, then we have to randomly select one of the stimuli from the cued array to replace with another face or scene
        if trial_cue_match=='match':
            corr_resp=yes_key # yes it's the same
            replaced_img_cue_pos='n/a'
            replaced_img_cue_name='n/a'
        elif trial_cue_match=='mismatch':
            
            if cue_word=='face':
                display_to_change=faces_display
                dict_of_images=Img_Face
            elif cue_word=='scene':
                display_to_change=scenes_display
                dict_of_images=Img_Scene
                
            replace_ind=np.random.choice(range(load_num),1)[0] #randomly pick an index to replace
            replace_stim=display_to_change[replace_ind] # only to initiate while loop 
            while replace_stim in display_to_change: # and randomly switch it with a previously not displayed picture
                rand_choice_key=np.random.choice(list(dict_of_images.keys()),1)[0]
                replace_stim=dict_of_images[rand_choice_key]
            
            replaced_img=display_to_change[replace_ind]
            replaced_img_cue_pos=replaced_img.pos
            replaced_img_cue_name=replaced_img.image.split('/')[-1]
            
            replaced_img.autoDraw=False # turn off the old image so that the new one is not overwritten
            replace_stim.autoDraw=True
            replace_stim.pos=replaced_img.pos # transfer over the position
            display_to_change[replace_ind]=replace_stim
            
            corr_resp=no_key # no, it's not the same as the memory array
        
        ## Do the same for the opposite, uncued array
        if trial_noCue_match=='match':
            
            replaced_img_noCue_pos='n/a'
            replaced_img_noCue_name='n/a'
            
        elif trial_noCue_match=='mismatch':
            
            if cue_word !='face':
                noCue_display_to_change=faces_display
                dict_of_images2=Img_Face
            elif cue_word !='scene':
                noCue_display_to_change=scenes_display
                dict_of_images2=Img_Scene
            
            replace_ind2=np.random.choice(range(load_num),1)[0] #randomly pick an index to replace
            replace_stim2=noCue_display_to_change[replace_ind2] # only to initiate while loop 
            while replace_stim2 in noCue_display_to_change: # and randomly switch it with a previously not displayed picture
                rand_choice_key=np.random.choice(list(dict_of_images2.keys()),1)[0]
                replace_stim2=dict_of_images2[rand_choice_key]
            
            replaced_img2=noCue_display_to_change[replace_ind2]
            replaced_img_noCue_pos=replaced_img2.pos
            replaced_img_noCue_name=replaced_img2.image.split('/')[-1]
            
            replaced_img2.autoDraw=False # turn off the old image so that the new one is not overwritten
            replace_stim2.autoDraw=True
            replace_stim2.pos=replaced_img2.pos # transfer over the position
            noCue_display_to_change[replace_ind2]=replace_stim2
        
        if EEGflag:
            if trial_cue_match=='match':
                if trial_noCue_match=='match':
                    thisMatch_flag=cue_match_noCue_match_trig
                elif trial_noCue_match=='mismatch':
                    thisMatch_flag=cue_match_noCue_mismatch_trig
            elif trial_cue_match=='mismatch':
                if trial_noCue_match=='match':
                    thisMatch_flag=cue_mismatch_noCue_match_trig
                elif trial_noCue_match=='mismatch':
                    thisMatch_flag=cue_mismatch_noCue_mismatch_trig
            win.callOnFlip(port.write,bytes([thisMatch_flag]))
        
        event.clearEvents()
        max_win_count=int(2/(1/refresh_rate))
        win_count=0
        subRespos=[]
        RT_clock.reset()
        while win_count != max_win_count: # subject reponse #######################################
            win.flip()
            subRespo=event.getKeys(timeStamped=RT_clock,keyList=[yes_key,no_key])
            win_count=win_count+1
            if subRespo:
                subRespos.append(subRespo)
                win_count = max_win_count
        
        print(subRespos)
        if not subRespos:
            if EEGflag:
                port.write(bytes([subNonResp_trig]))
                respTrigname='NoResp'
                resptrig=subNonResp_trig
            trial_Corr=-1
            rt='none'
            subKEY='none'
        else:
            subResponse=subRespos[0]
            if subResponse[0][0]==corr_resp:
                if EEGflag:
                    port.write(bytes([subResp_trig]))
                    respTrigname='resp'
                    resptrig=subResp_trig
                trial_Corr=1
                rt=subResponse[0][1]
                subKEY=subResponse[0][0]
            elif subResponse[0][0]!=corr_resp:
                if EEGflag:
                    port.write(bytes([subResp_trig]))
                    respTrigname='resp'
                    resptrig=subResp_trig
                trial_Corr=0
                rt=subResponse[0][1]
                subKEY=subResponse[0][0]
        
        if EEGflag:
            Thistrial_data= {'trialNum':(trial),'cue_word':cue_word,'match_mismatch_Cue':trial_cue_match, 'match_mismatch_notCue':trial_noCue_match,
                            'corrResp':corr_resp,'subjectResp':subKEY,'trialCorr?':trial_Corr,'RT':rt, 
                            'ITI':ITI,'hemis (face,scene)':(faces_hemi,scenes_hemi),
                            'probe_array([faces],[scenes])':([face.image.split('/')[-1] for face in faces_display],[scene.image.split('/')[-1] for scene in scenes_display]),
                            'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':(replaced_img_cue_name,replaced_img_cue_pos,replaced_img_noCue_name,replaced_img_noCue_pos),
                            'trial_trigs':(thisCuetrig,thisEncoding_trig,delay_trig,thisMatch_flag,resptrig)}
        else:
            Thistrial_data= {'trialNum':(trial),'cue_word':cue_word,'match_mismatch_Cue':trial_cue_match, 'match_mismatch_notCue':trial_noCue_match,
                            'corrResp':corr_resp,'subjectResp':subKEY,'trialCorr?':trial_Corr,'RT':rt, 
                            'ITI':ITI,'hemis (face,scene)':(faces_hemi,scenes_hemi),
                            'probe_array([faces],[scenes])':([face.image.split('/')[-1] for face in faces_display],[scene.image.split('/')[-1] for scene in scenes_display]),
                            'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':(replaced_img_cue_name,replaced_img_cue_pos,replaced_img_noCue_name,replaced_img_noCue_pos),
                            'trial_trigs':''}
        trialDataList.append(Thistrial_data)
        
        print(Thistrial_data)
        
        for face in faces_display:
            face.autoDraw=False
        for scene in scenes_display:
            scene.autoDraw=False
        
        if EEGflag:
            win.callOnFlip(port.write,bytes([ITI_trig]))
        fixation.autoDraw=True
        wait_here(ITI)
        
        blocks.update({'blockInfo_%i'%(block):{'block':block,'load':load_num,
                        '(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)':(expInfo['mm_r_Cue'],n_mismatch,n_match),
                        '(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)':(expInfo['mm_r_noCue'],n_mismatch_nc,n_match_nc),
                        'trialsData':trialDataList}})
        
        make_csv(filename)


if EEGflag:
    port.write(stopSaveflag)