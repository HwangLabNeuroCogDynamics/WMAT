## Working Memory Alpha Theta (WMAT) ADAPTED FOR ECoG study
# ADD A QUESTION MARK to indicate probe v encoding,
#  add two controls: condition 0-back, they press a button when the picture comes up w/out memorizing anything. 
#  add another one which is load 2 so that we can contrast 2 v 1 load. For this version, change the probe to be a 
   # "Did you see this?" single probe so that it's easier for patients. s
    # BLOCKED design of 1-back and 0-back, 0-back still randomize match nonmatch
        # 
# instead of cueing word, cue arrow, longer encoding and probe times, neutral trials, 1 and 2 stim blocks

from __future__ import absolute_import, division
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
expName='WMAT' # working memory alpha theta
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
win = visual.Window([1680,1050],units='deg',fullscr=True,monitor='testMonitor',checkTiming=True)#

if expInfo['EEG? [y/n]']=='y':
    EEGflag=1
    
else:
    EEGflag=0

if EEGflag:
    filename=os.getcwd()+'/WMAT_data/eeg_data/'+u'/%s_%s_%s' % (expInfo['subject'], expName, expInfo['date'])
    
if EEGflag:
    filename=os.getcwd()+'/WMAT_data/eeg_data/eeg_behav_data'+u'/%s_%s_%s' % (expInfo['subject'], expName, expInfo['date'])
    port=serial.Serial('COM4',baudrate=115200)
    port.close()
    port.open()
    startSaveflag=bytes([201]) #254
    stopSaveflag=bytes([255]) #255
    
    load_two_trig=109
    load_three_trig=111
    load_four_trig=113
    
    active_trig=125
    passive_trig=127
    
    cue_face_trig=115
    cue_scene_trig=117
    
    delay_trig=119
    
    cue_mismatch_noCue_mismatch_trig=101
    cue_mismatch_noCue_match_trig=103
    cue_match_noCue_mismatch_trig=105
    cue_match_noCue_match_trig=107
    
    subNonResp_trig=121
    subResp_trig=123
    
    ITI_trig=129
else:
    filename=os.getcwd()+'/WMAT_data/behav_data/'+u'/%s_%s_%s' % (expInfo['subject'], expName, expInfo['date'])

refresh_rate=int(expInfo['refresh'])

for key in ['escape']:
    event.globalKeys.add(key, func=core.quit)

num_trials=20
num_reps=2 #divisible by 2 so that 1/2 neutral and 1/2 active

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
        ITI=np.random.choice([1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6],1)[0] #averages to around 2 second?
    else:
        ITI=np.random.choice([3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6],1)[0] # averages to around 4 seconds?
    return ITI

def pracCond(num_load=2,n_practrials=4,demo=False):
    pracDataList=[]
    if demo:
        prac_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin a demo')
    else:
        prac_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin the practice')
    load_num=num_load
    side_toRemember=[]
    for n in range(int(n_practrials/2)):
        side_toRemember.append('face')
        side_toRemember.append('scene')
    side_toRemember_scramble=list(np.random.permutation(side_toRemember))
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
    for trial in range(len(side_toRemember_scramble)):
        ITI=make_ITI()
        fixation.autoDraw=False
        hemis=np.random.choice(['R','L'],2,replace=False) #pick which side the faces display is on and which the scenes are
        faces_hemi=hemis[0]
        scenes_hemi=hemis[1]
        if side_toRemember_scramble[trial]=='face':
            side_to_cue=faces_hemi
        elif side_toRemember_scramble[trial]=='scene':
            side_to_cue=scenes_hemi
        arrow_to_display=cue_arrow['cue_'+side_to_cue]
        print(side_to_cue)
        print(arrow_to_display)
        arrow_to_display.autoDraw=True
        wait_here(0.5) # display cue
        arrow_to_display.autoDraw=False
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
        elif load_num==1:
            faces_display[0].pos=one_items['middle_'+faces_hemi]
            scenes_display[0].pos=one_items['middle_'+scenes_hemi]
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        if demo:
            win.flip()
            core.wait(3)
        else:
            wait_here(1) # display face/scene arrays
        for face in faces_display:
            face.autoDraw=False
            #face.pos=(0,0)
        for scene in scenes_display:
            scene.autoDraw=False
            #scene.pos=(0,0)
        fixation.autoDraw=True
        wait_here(1) #delay 
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        trial_match=match_mismatch_scramble[trial]
        print(trial_match)
        if trial_match=='match':
            corr_resp=yes_key # yes it's the same
        elif trial_match=='mismatch':
            if side_toRemember_scramble[trial]=='face':
                display_to_change=faces_display
                dict_of_images=Img_Face
            elif side_toRemember_scramble[trial]=='scene':
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
        fixation.autoDraw=False
        questionMark.autoDraw=True
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
        questionMark.autoDraw=False
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
        
        fieldnames=['block','load','(cue_ratio,mm_trials,m_trials)','(nonCue_ratio,mm_trials,m_trials)','task_type','response_map',
                    'trialNum','cue_side','match_mismatch_cue','match_mismatch_nonCue','probe_array([faces],[scenes])',
                    'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)','corrResp','subResp','trialCorr?','RT','ITI','trial_trigs','triggers']
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
                
                if EEGflag and expStart==True and k==0:
                    writer.writerow({'block':ThisBlock['block'],'load':ThisBlock['load'],'(cue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)'],
                                    '(nonCue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)'],'task_type':ThisBlock['task_type'],
                                    'response_map':ThisBlock['response_map'],
                                    'trialNum':ThisTrial['trialNum'],'cue_side':ThisTrial['cue_side'],'match_mismatch_cue':ThisTrial['match_mismatch_Cue'],
                                    'match_mismatch_nonCue':ThisTrial['match_mismatch_notCue'],'probe_array([faces],[scenes])':ThisTrial['probe_array([faces],[scenes])'],
                                    'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':ThisTrial['replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'ITI':ThisTrial['ITI'],'trial_trigs':ThisTrial['trial_trigs'],
                                    'triggers':()})
                else:
                    writer.writerow({'block':ThisBlock['block'],'load':ThisBlock['load'],'(cue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)'],
                                    '(nonCue_ratio,mm_trials,m_trials)':ThisBlock['(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)'],'task_type':ThisBlock['task_type'],
                                    'response_map':ThisBlock['response_map'],
                                    'trialNum':ThisTrial['trialNum'],'cue_side':ThisTrial['cue_side'],'match_mismatch_cue':ThisTrial['match_mismatch_Cue'],
                                    'match_mismatch_nonCue':ThisTrial['match_mismatch_notCue'],'probe_array([faces],[scenes])':ThisTrial['probe_array([faces],[scenes])'],
                                    'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':ThisTrial['replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)'],
                                    'corrResp':ThisTrial['corrResp'],'subResp':ThisTrial['subjectResp'],'trialCorr?':ThisTrial['trialCorr?'],
                                    'RT':ThisTrial['RT'],'ITI':ThisTrial['ITI'],'trial_trigs':ThisTrial['trial_trigs'],'triggers':''})

#vis_deg=3.5
dist=6#3.5

one_items={'middle_L':(-dist,0),'middle_R':(dist,0)}
two_items={'upper_R':(dist,0.5*dist),'lower_R':(dist,-0.5*dist),'upper_L':(-1*dist,0.5*dist),'lower_L':(-1*dist,-0.5*dist)}
four_items={'upper_upper_R':(dist,dist),'upper_middle_R':(dist,dist/3),
            'lower_lower_R':(dist,-1*dist),'lower_middle_R':(dist,-1*(dist/3)),'upper_upper_L':(-1*dist,dist),
            'upper_middle_L':(-1*dist,(dist/3)),'lower_lower_L':(-1*dist,-1*dist),'lower_middle_L':(-1*dist,-1*(dist/3))}

#Dictionaries and the corresponding file paths
direc = os.getcwd()+'/localizer_stim/' #_thisDir #'/Users/mpipoly/Desktop/Psychopy/localizer_stim/' #always setup path on the fly in case you switch computers
ext = 'scenes/*.jpg' #file delimiter
faces_ext = 'faces/*.jpg'
faces_list = glob.glob(direc + faces_ext)
scenes_list = glob.glob(direc + ext)
#print(faces_list)
#print(scenes_list)
Img_Scene = {}
Img_Face = {}

size=7#3.8#3.5#1.5

for f in range(len(faces_list)):
    Img_Face[str(f)]= visual.ImageStim(win=win, image=faces_list[f],name=str(f),size=size)
for s in range(len(scenes_list)):
    Img_Scene[str(s)]=visual.ImageStim(win=win,image=scenes_list[s],name=str(s),size=size)
print(Img_Face)
#cue_words_dict={'face':visual.TextStim(win,text='face',units='norm',color=(1,1,1)),'scene':visual.TextStim(win,text='scene',units='norm',color=(1,1,1))}

cue_arrow={'cue_L':visual.TextStim(win,text='<',units='norm',color=(1,1,1)),'cue_R':visual.TextStim(win,text='>',units='norm',color=(1,1,1))}

questionMark=visual.TextStim(win, text='?',units='norm', color=(1,1,1))
fixation = visual.TextStim(win, text='+',units='norm', color=(1,1,1))
fixation.size=0.6

intro_msg= visual.TextStim(win, pos=[0, .5],units='norm', text='Welcome to the experiment!')
intro_msg2= visual.TextStim(win, pos=[0, 0], units='norm',text='You will see an arrow on the screen, then a series of face and scene pictures')
intro_msg3=visual.TextStim(win, pos=[0,-0.5],units='norm',text='Press any key to continue')
intro_msg.draw()
intro_msg2.draw() 
intro_msg3.draw()
win.flip()
event.waitKeys()
#intro_mesg4= visual.TextStim(win,pos=[0,.5],units='norm',text='Sometimes you will .')
#intro_mesg5=visual.TextStim(win,pos=[0,0], units='norm',text='Press %s if the pictures match the previous ones you saw, or %s if they do not match' %(yes_key,no_key))
#intro_mesg6=visual.TextStim(win,pos=[0,-0.5],units='norm',text='Press any key to continue.')
#intro_mesg4.draw()
#intro_mesg5.draw()
#intro_mesg6.draw()
#win.flip()
#event.waitKeys()
#win.flip()

encode_time=3
probe_time=3
cue_time=1.5

RT_clock=core.Clock()

resp_map=np.random.choice(['matches','mismatches'],1)[0]
if resp_map=='matches':
    resp_key=yes_key
elif resp_map=='mismatches':
    resp_key=no_key

loads=['1']
active_passive=['active','passive']

stimList=[]
for l in loads:
    for i in range(num_reps):
        stimList.append(l)

taskList=[]
for t in active_passive:
    for i in range(int(num_reps/2)):
        taskList.append(t)

taskList_scramble=list(np.random.permutation(taskList))
stimList_scramble=list(np.random.permutation(stimList))

prac_num_load=1
#pracCond(num_load=prac_num_load,n_practrials=2,demo=True)

#pracCond(num_load=prac_num_load)
blocks={}
for block in range(len(stimList_scramble)):
    if block !=0:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to continue to the next block')
    else:
        info_msg2=visual.TextStim(win, pos=[0,.5], units='norm',text='Press any key to begin experiment')
    
    task=taskList_scramble[block] 
    load_num=int(stimList_scramble[block])
    
    if task=='active':
        task_inst=visual.TextStim(win, pos=[0,0], units='norm',text='This round you will MEMORIZE the pictures. Press %s if the second picture %s the picture you see the first time.' %(resp_key,resp_map))
    elif task=='passive':
        task_inst=visual.TextStim(win, pos=[0,0], units='norm',text='This round you will NOT MEMORIZE the pictures. Please sit back and relax, and keep your eyes on the screen and press 0 when you see the pictures with a ? .')
    
    task_inst.draw()
    core.wait(5)
#    word_cues=[]
#    for n in range(int(num_trials/2)):
#        word_cues.append('face')
#        word_cues.append('scene')
#    word_cues_scramble=list(np.random.permutation(word_cues))
    cue_side=np.random.choice(['R','L'],1)[0]
    
    match_mismatch_cue=[] #populating this list with each trial's status as a match or mismatch trial
    n_mismatch=int(num_trials*expInfo['mm_r_Cue'])
    n_match=num_trials-n_mismatch
    print(n_mismatch)
    print(n_match)
    for m in range(n_mismatch):
        match_mismatch_cue.append('mismatch')
    for n in range(n_match):
        match_mismatch_cue.append('match')
    match_mismatch_cue_scramble=list(np.random.permutation(match_mismatch_cue))
    
    match_mismatch_Nocue=[] #populating this list with each trial's status as a match or mismatch trial
    n_mismatch_nc=int(num_trials*expInfo['mm_r_noCue'])
    n_match_nc=num_trials-n_mismatch_nc
    print(n_mismatch_nc)
    print(n_match_nc)
    for m in range(n_mismatch_nc):
        match_mismatch_Nocue.append('mismatch')
    for n in range(n_match_nc):
        match_mismatch_Nocue.append('match')
    match_mismatch_Nocue_scramble=list(np.random.permutation(match_mismatch_Nocue))
    
    info_msg2.draw()
    win.update()
    key1=event.waitKeys()
    fixation.color=([1,1,1])
    fixation.draw()
    win.flip() 
    core.wait(3)# pre-block pause
    
    trialDataList=[]
    
    for trial in range(num_trials):
        ITI=make_ITI()
        
        fixation.autoDraw=False
        
        cue=cue_arrow['cue_'+cue_side]
        cue.autoDraw=True
        
        wait_here(cue_time) # display cue
        
        cue.autoDraw=False
        fixation.autoDraw=True
        
        faces_display=[]
        randos_face=np.random.choice(list(Img_Face.keys()),load_num,replace=False)
        for i in randos_face: #picking random faces, randomly loading indexes of face imgs 
            faces_display.append(Img_Face[i])
        
        randos_scene=np.random.choice(list(Img_Scene.keys()),load_num,replace=False)
        scenes_display=[]
        for k in randos_scene:
            scenes_display.append(Img_Scene[k])
        
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
            
        elif load_num==1:
            
            faces_display[0].pos=one_items['middle_'+faces_hemi]
            scenes_display[0].pos=one_items['middle_'+scenes_hemi]
            
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
            
        if EEGflag:
            if task=='active':
                thisEncoding_trig=active_trig
            elif task=='passive':
                thisEncoding_trig=passive_trig
            
            win.callOnFlip(port.write,bytes([thisEncoding_trig]))
        wait_here(encode_time) # display face/scene arrays
        
        for face in faces_display:
            face.autoDraw=False
            #face.pos=(0,0)
        for scene in scenes_display:
            scene.autoDraw=False
            #scene.pos=(0,0)
        
        if EEGflag:
            win.callOnFlip(port.write,bytes([delay_trig]))
        
        fixation.autoDraw=True
        
        wait_here(2) #delay 
        
        for face in faces_display:
            face.autoDraw=True
        for scene in scenes_display:
            scene.autoDraw=True
        trial_cue_match=match_mismatch_cue_scramble[trial]
        print(trial_cue_match)
        trial_noCue_match=match_mismatch_Nocue_scramble[trial]
        
        if trial_cue_match=='match':
            #corr_resp=yes_key # yes it's the same
            if task=='active':
                corr_resp=yes_key
            elif task=='passive':
                corr_resp='n/a'
            
            replaced_img_cue_pos='n/a'
            replaced_img_cue_name='n/a'
        elif trial_cue_match=='mismatch':
            
            if task =='active':
                #f resp_map=='matches':
                 #   corr_resp='n/a'
                #elif resp_map=='mismatches':
                corr_resp=no_key
            elif task=='passive':
                corr_resp='n/a'
            
            if cue_side == faces_hemi:
                display_to_change=faces_display
                dict_of_images=Img_Face
            elif cue_side == scenes_hemi:
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
            
            #corr_resp=no_key # no, it's not the same as the memory array
        
        if trial_noCue_match=='match':
            
            replaced_img_noCue_pos='n/a'
            replaced_img_noCue_name='n/a'
            
        elif trial_noCue_match=='mismatch':
            
            if cue_side != faces_hemi:
                noCue_display_to_change=faces_display
                dict_of_images2=Img_Face
            elif cue_side != scenes_hemi:
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
        fixation.autoDraw=False
        questionMark.autoDraw=True
        if EEGflag:
            if trial_cue_match=='match':
                if trial_noCue_match=='match':
                    this_probe_trig=cue_match_noCue_match_trig
                elif trial_noCue_match=='mismatch':
                    this_probe_trig=cue_match_noCue_mismatch_trig
            elif trial_cue_match=='mismatch':
                if trial_noCue_match=='match':
                    this_probe_trig=cue_mismatch_noCue_match_trig
                elif trial_noCue_match=='mismatch':
                    this_probe_trig=cue_mismatch_noCue_mismatch_trig
            win.callOnFlip(port.write,bytes([this_probe_trig]))
        event.clearEvents()
        max_win_count=int(probe_time/(1/refresh_rate))
        win_count=0
        subRespo=None
        RT_clock.reset()
        while not subRespo:
            win.flip()
            subRespo=event.getKeys(timeStamped=RT_clock,keyList=[yes_key,no_key])
            win_count=win_count+1
            if win_count==max_win_count:
                break
        fixation.autoDraw=True
        questionMark.autoDraw=False
        print(subRespo)
        
        if not subRespo: # if there's no response
            
            if EEGflag:
                #port.write(bytes([subNonResp_trig]))
                port.write(bytes([subNonResp_trig]))
                respTrigname='NoResp'
                resptrig=subNonResp_trig
  
            trial_Corr=0 # even in the passive condition they should be responding, so if they don't then mark it wrong
            rt='none'
            subKEY='none'
            
        elif subRespo: #else if they responded
            
            if EEGflag:
                port.write(bytes([subResp_trig]))
                respTrigname='resp'
                resptrig=subResp_trig
            if subRespo[0][0]==corr_resp: #and if they were supposed to, mark it right
                trial_Corr=1
                rt=subRespo[0][1]
                subKEY=subRespo[0][0]
            elif corr_resp=='n/a' and subRespo[0][0]=='0': #if this is passive condition, mark it right for selecting '0'
                trial_Corr=1
                rt=subRespo[0][1]
                subKEY=subRespo[0][0]
            else:
                trial_Corr=0
                rt=subRespo[0][1]
                subKEY=subRespo[0][0]
                
        
        if EEGflag:
            Thistrial_data= {'trialNum':(trial),'cue_side':cue_side,'match_mismatch_Cue':trial_cue_match, 'match_mismatch_notCue':trial_noCue_match,
                            'corrResp':corr_resp,'subjectResp':subKEY,'trialCorr?':trial_Corr,'RT':rt, 
                            'ITI':ITI,'hemis (face,scene)':(faces_hemi,scenes_hemi),
                            'probe_array([faces],[scenes])':([face.image.split('/')[-1] for face in faces_display],[scene.image.split('/')[-1] for scene in scenes_display]),
                            'replaced_image(cue_name,cue_pos,notCue_name,notCue_pos)':(replaced_img_cue_name,replaced_img_cue_pos,replaced_img_noCue_name,replaced_img_noCue_pos),
                            'trial_trigs':(thistrialFlag,probetrig,resp_trig)}
        else:
            Thistrial_data= {'trialNum':(trial),'cue_side':cue_side,'match_mismatch_Cue':trial_cue_match, 'match_mismatch_notCue':trial_noCue_match,
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
        
        blocks.update({'blockInfo_%i'%(block):{'block':block,'load':load_num, 'task_type':task,'response_map':resp_map,'(mismatch_ratio_Cue,mismatch_trials_Cue,match_trials_Cue)':(expInfo['mm_r_Cue'],n_mismatch,n_match),
                        '(mismatch_ratio_nonCue,mismatch_trials_noncue,match_trials_noncue)':(expInfo['mm_r_noCue'],n_mismatch_nc,n_match_nc),'trialsData':trialDataList}})
        
        make_csv(filename)
