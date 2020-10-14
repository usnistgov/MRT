#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 08:57:31 2019

@author: jkp4
"""

from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import messagebox
import tkinter as tk
import os
import csv
import re
import sounddevice as sd # Would like to replace simple audio as sounddevice gives sound device selectoin contrl
import scipy.io.wavfile
import numpy as np
import time
from datetime import datetime
import configparser
import traceback
import pdb
# Project Tags:
    # TODO: Feature to implement if time allows
    # BUG: Known issue that requires further investigation
    # NOTE: Minor thing to track if issues crop up
class MRT(tk.Tk):
    """Modified Rhyme Test GUI
    
    mrt = MRT() creates a new instance of a tkinter GUI for performing modified rhyme
    tests. mrt.mainloop() runs the GUI.
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Define title font
        self.title_font = tkfont.Font(family="Helvetica", size = 20, weight= "bold")
        # Define button font
        self.button_font = tkfont.Font(family="Helvetica", size = 15)
        
        self.title("Modified Rhyme Test") # Set app title
#        self.geometry("400x800") # Set frame size
        self.attributes('-fullscreen',True)
        self.resizable(0,0) # Fix frame size (not resizable)
        # Don't allow widgets to determine frames's width/height
        self.pack_propagate(0) 
        
        # Force application to update (draw full screen)
        self.update()
        # Grab width of screen
        self.screen_width = self.winfo_width()
        self.x_offset = 0.4*self.screen_width
        #TODO: Get screen height, if < 800 then need to shrink displays..
        
#        self.configure(height=800,width=400) # Set application size
        
        # Initialize test directory as string variable
        self.test_dir = tk.StringVar()
        # Initialize test subdirectories as None
        self.inputLocation = None
        self.outputLocation = None
        self.clipLocation = None
        # Initialize subject and session numbers as None
        self.subject_number = None
        self.session_number = None
        # Query default output audio device
        _,self.audio_device = sd.default.device
        # Store audio device list
#        self.device_list = sd.query_devices()
        self.hostapi_list = sd.query_hostapis()
        self.device_list,self.device_list_ix = self.get_output_audio_devices()
        
        self.all_d_out = sd.query_devices()
        
        #file name for config
        self.config_file_name='config.ini'
        
        # Initialize container frame. Stack different frames here
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight =1)
        
        # Initialize empty frames dictionary
        self.frames = {}
        # Iterate through and initialize different frames
        for F in (StartPage, DemoPage, MRTPage):
            # Get page name
            page_name = F.__name__
            # Initialize frame
            frame = F(parent=container,controller=self)
            # Store in frames dictionary
            self.frames[page_name] = frame
            
            frame.grid(row=0,column=0,sticky="nsew")
        # Show StartPage
        self.show_frame("StartPage")
    def show_frame(self,page_name):
        """Swap between tkinter frames for MRT app"""
        frame = self.frames[page_name]
        frame.tkraise()
        
    def get_output_audio_devices(self):
        """Return output audio devices with at least one output channel"""
        audio_devices = sd.query_devices()
        hostapi_list = sd.query_hostapis()
        output_devices = []
        output_devices_ix = []
        for ix,device in enumerate(audio_devices):
            if(device["max_output_channels"] >= 1):
#                device_str = device + hostapi_list[audio_devices[ix]['hostapi']]['name']
#                output_devices.append(device_str)
                output_devices.append(device)
                output_devices_ix.append(ix)
        return((output_devices,output_devices_ix))
    
    def get_audio_device_name(self):
        """Return current audio device"""
        # Refresh device list
#        self.device_list = sd.query_devices()
        self.device_list,dev_ix = self.get_output_audio_devices()
        self.hostapi_list = sd.query_hostapis()
        # TODO: Filter audio devices to have >= one audio outputs
        # Query default output audio device
        _,self.audio_device = sd.default.device
        d_ix = dev_ix.index(self.audio_device)
        device_name = self.device_list[d_ix]["name"] + self.hostapi_list[self.device_list[d_ix]["hostapi"]]["name"]
        return(device_name)
        
        
        
class StartPage(tk.Frame):
    """Initialization page for MRT GUI
    
    First screen for an MRT. Here users select a test directory, playlist file,
    and the output audio device to use during the test.
    """
    font_style = "Helvetica"
    button_font_size = 20
    message_font_size =20
    
    # Define y points for all tk objects that will be placed in this frame
    welcome_y = 50
    test_dir_y = welcome_y+150 # 200
    dir_message_y = test_dir_y + 50 # 250
    valid_dir_y = dir_message_y + 40 # 290
    valid_dir_ystep = 20
    subject_y = valid_dir_y + 120 # 410
    session_y = subject_y+40 # 450
    audio_y = session_y + 40 # 490
    next_y = 700
    
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Set controller as main MRT object
        self.controller = controller
        
        self.pack()
        
        self.default_test_dir = ".."
        
#        self.controller.update()
#        print(f'width: {self.controller.winfo_width()}')
#        print(f'reqwidth: {self.controller.winfo_reqwidth()}')
        
        
        # Initialize empty dictionary for storing test directory validity information
        self.valid_test_dir = {}
        # Initialize subject and session numbers as None type initially
        self.subject_numbers = None
        self.session_numbers = None
        
        # Inititalize audio device 
        # # This variable is an index for the valid indices array (self.controller.device_list_ix)
        # # s.t. _,self.controller.device_list_ix[self.audio_device_ix.get()] == sd.query_devices()
        self.audio_device_ix = tk.IntVar(self)
        # Set audio device index to current audio device
        self.audio_device_ix.set(self.controller.audio_device)
        # Define trace function when audio device index changes
        self.audio_device_ix.trace("w",self.update_audio_device)
        
        # Initialize audio device
        self.audio_device = tk.StringVar(self)
        # Set to current audio device name
#        self.audio_device.set(self.controller.device_list[self.audio_device_ix.get()]["name"])
        self.audio_device.set(self.controller.get_audio_device_name())
        # Set device list
        self.device_list = self.controller.device_list
        
        # Initialize int variable to store subject number
        self.subject_number = tk.IntVar(self)
        # Initialize to None 
        self.subject_number.set(None)
        # Set trace function (called when int var value changes through set())
        self.subject_number.trace("w",self.update_subject_number)
        # Initialize session number int var
        self.session_number = tk.IntVar(self)
        self.session_number.set(None)
        # Set trace function
        self.session_number.trace("w", self.update_session_number)
        
        # Make welcome message, test directory button/labels(hidden at first)
        self.make_welcome_message()
        self.make_test_dir()

        # Make subject/session/audio device drop down selectors
        self.make_subject_select()
        self.make_session_select()
        self.make_audio_device_select()
        
        # Make button to continue to MRT
        self.make_next_button()
        
        # Check test directory status
        self.check_test_dir_status()
        
        #read config options from file
        self.read_config()
        
     #read config
    def read_config(self):
        """Read config file and set defaults accordingly
        
        Config file can set default test directory, subject number, session 
        number, and audio device.
        """
        config = configparser.ConfigParser()
        if(os.path.exists(self.controller.config_file_name)):    
            try:
                config.read(self.controller.config_file_name)
            except:
                print('Error reading config file : ',flush=True);
                traceback.print_exc()
                return
                
            try:
                #set test directory
                self.process_test_dir(config['Default']['testdir'])
            except:
                print("Exception while setting test directory : ",flush=True)
                traceback.print_exc()
                
            try:
                self.subject_number.set(config['Default']['SubjectNumbers'])
            except:
                print("Exception while setting subject number : ",flush=True)
                traceback.print_exc()
                
            try:
                self.session_number.set(config['Default']['SessionNumbers'])
            except:
                print("Exception while setting session number : ",flush=True)
                traceback.print_exc()
            
            try:
                #get audio device name from config
                dev_name=config['Default']['AudioDevice']
                self.find_device(dev_name)
    #            self.audio_device.set(dev_name)
            except:
                print("Exception while reading audio device : ",flush=True)
                traceback.print_exc()
#    def write_config(self):
        
    def find_device(self,dev_name):
        """Find audio device matching dev_name
        
        Searches through audio output devices for one that matches dev_name.
        Note that some audio devices are listed multiple times, as they can 
        function with multiple host apis. The search looks for a specific 
        device/host api combination.
        """
        print(f"dev_name: {dev_name}")
        dev_ix = None
        for ix,dev in enumerate(self.controller.device_list):
            api_name = self.controller.hostapi_list[dev["hostapi"]]["name"]
            full_name = dev["name"] + " " + api_name
#            print(f"{dev_name} == {full_name}\n {dev_name == full_name}")
            if(dev_name == full_name):
                dev_ix = ix
                break
#            print("--------------")
        if(dev_ix != None):
            self.audio_device_ix.set(dev_ix)
#            if(full_name == dev_name):
#                print(f"found it! It's {full_name}")
#        print("hmmm")
    # %% Welcome Message
    def make_welcome_message(self):
        """Make the welcome message for the MRT StartPage"""
        self.Welcome = tk.Message(self)
        self.WelcomeStr = tk.StringVar()
        self.WelcomeStr.set("Modified Rhyme Test Initialization")
        self.Welcome["textvariable"] = self.WelcomeStr
        self.Welcome["justify"] = "center"
        self.Welcome["font"] = self.controller.title_font
        self.Welcome["width"] = 300
        # Place welcome message
        self.Welcome.place(x=50+self.controller.x_offset,y=self.welcome_y)
        self.update()
        
    # %% Source Directory Identification
    def make_test_dir(self):
        """Make test directory widgets for the MRT StartPage
        
        Defines a button to "Select Test Directory", an associated helper 
        button, an entry to to display the selected test directory, and 
        predefines messages for the validity of each required subdirectory in 
        the selected test directory.
        """
        # Button to select test directory
        self.TestDir = tk.Button(self)
        self.TestDir["text"] = "Select Test Directory"
        self.TestDir["font"] = self.controller.button_font
        self.TestDir["command"] = self.test_dir_pressed
        
        self.TestDir.place(x=50+self.controller.x_offset,y=self.test_dir_y,width=300)
        
        # Test directory help button
        self.TestDirHelp = tk.Button(self)
        self.TestDirHelp["text"] = "?"
        self.TestDirHelp["font"] = ("Helvetica",10)
        self.TestDirHelp["command"] = self.test_dir_help_pressed
        self.TestDirHelp.place(x=365+self.controller.x_offset,y=self.test_dir_y+5,width=20)
         
        # Scrollbar for display of test directory
        scrollbar = tk.Scrollbar(self)
        scrollbar.place(x=50+self.controller.x_offset,y=self.dir_message_y+20,width=300)
        scrollbar["orient"]= "horizontal"
        # Entry to display test directory
        self.dir_message = tk.Entry(self,xscrollcommand=scrollbar.set)
        # Don't allow users to edit entry
        self.dir_message["state"] = "disabled"
        # Set text variable to controller test directory string var
        self.dir_message["textvariable"] = self.controller.test_dir
        self.dir_message["font"] = ("Helvetica",10)
        self.dir_message["width"] = 100
        self.dir_message.place(x=50+self.controller.x_offset,y=self.dir_message_y,width=300)
        # Configure scrollbar to change directory message xview
        scrollbar.config(command=self.dir_message.xview)

        # Subfolders that are required in a proper MRT test directory
        req_subfolds = ["Audio","Playlist","Results"]
        for k,subfold in enumerate(req_subfolds):
           # Initialize message for each required subfolder
           message = tk.Message(self)
           message_str = tk.StringVar()
           message["textvariable"] = message_str
           message["width"]= 300
           message.place(x=50+self.controller.x_offset,y=self.valid_dir_y+k*self.valid_dir_ystep)
           self.valid_test_dir[subfold] = {"valid": False,
                              "message": message,
                              "message_str": message_str}
         
    def test_dir_pressed(self):
        """
        # TODO: Write this
        """
        # Force app to update (can help with slow down with askdirectory)
        self.controller.update()
        # Open directory selection window
        test_dir = tk.filedialog.askdirectory(initialdir = self.default_test_dir, title = "Select test folder")
        
        #make sure a selection was made
        if(test_dir):
            self.process_test_dir(test_dir)

    def process_test_dir(self,dir):
        # Update default
        self.default_test_dir = dir
        # Update test directory string var
        self.controller.test_dir.set(dir)
        # Update input, clip, and output locations
        self.controller.inputLocation = os.path.join(self.controller.test_dir.get(),"Playlist")
        self.controller.clipLocation = os.path.join(self.controller.test_dir.get(),"Audio")
        self.controller.outputLocation = os.path.join(self.controller.test_dir.get(),"Results")

        # If test directory is not empty string
        if(self.controller.test_dir.get() != ""):
            # Update status of test directories
            self.test_dir_status()
        # Force app to update (can help with slow down with askdirectory)
        self.controller.update()
        # Check if we have a valid test directory (enables moving to MRTPage)
        self.check_test_dir_status()
        
    def test_dir_help_pressed(self):
        """Messagebox help message for test directory requirements"""
        
        msg = ("Test directories require three subfolders: Audio, Playlist, "
               "and Results. Audio must contain all the audio for the MRT. "
               "Playlist must contain pregenerated playlist files titled "
               "SubjectX_SessionY.csv. The playlist csvs need the fields "
               "defined by the following header\n"
               '"File","Talker","List","Word","NoiseType","Impairment","Order","Vote","PlayTime","VoteTime","AudioDevice"\n'
               "Results is where MRT results csv files will be saved.")
        tk.messagebox.showinfo("Test Directory Requirements", msg)
    
    def test_dir_status(self):
        """Check if required subfolders exist in current test directory.
        
        Update valid field for each subfold in self.valid_test_dir, and update 
        message_str and message color accordingly.
        """
        for subfold in self.valid_test_dir:
            # Get subfolder path
            spath = os.path.abspath(os.path.join(self.controller.test_dir.get(),subfold))
            # Check if it exists
            isvalid= os.path.exists(spath)
            # Update validity
            self.valid_test_dir[subfold]["valid"] = isvalid
            # Grab message and associated textvariables
            message=self.valid_test_dir[subfold]["message"]
            message_str=self.valid_test_dir[subfold]["message_str"]
            if(isvalid):
                # If valid subfolder set green good to go message
                message_str.set(subfold + " subfolder found.")
                message["foreground"] = "green"
            else:
                # If invalid set red no good message
                message_str.set(subfold + " subfolder not found.")
                message["foreground"]  = "red"
    # TODO: Make subject/session default to next in sequence that doesn't exist in results (e.g. if Subjects 1-3 have sessions 1-4 done, and subect 4 has sessions 1-2 done, default to Subject 4 session 3)
    def check_test_dir_status(self):
        """If current test directory is valid, enables subject dropdown"""
        # List to store validity of each subfolder
        test_dir_status = []
        # Get all validity statuses
        for td in self.valid_test_dir:
            test_dir_status.append(self.valid_test_dir[td]["valid"])
        if(all(test_dir_status) is True):
            # If all are valid
            # Get subject playlists from Playlists subdirectory
            self.get_subject_numbers()
            # Set dropdown list with subject numbers
            self.set_subject_numbers()
        else:
            # If they are not valid
            # Disable subject selection
            self.subject_select["state"] = "disable"
            # Disable Next button
            self.Next["state"] = "disable"
        # Set subject and session numbers to None
        self.subject_number.set(None)
        self.session_number.set(None)
        # Disable session selection
        self.session_select["state"] = "disable"
        
    # %% Subject Drop Down Menus
    def make_subject_select(self):
        """Initialize widgets for selection subject number"""
        self.subject_text = tk.Message(self)
        self.subject_text["text"] = "Subject Number"
        self.subject_text["width"] = 100
        self.subject_text.place(x=50+self.controller.x_offset,y=self.subject_y+5)
        self.subject_select = tk.OptionMenu(self,self.subject_number,"")
        self.subject_select["state"] = "disable"
        self.subject_select.place(x=150+self.controller.x_offset,y=self.subject_y)
        
    def get_subject_numbers(self):
        """Get all subject and session numbers from Playlist subdirectory
        
        Searches throug the playlist directory for files with name structure:
        SubjectX_SessionY.csv
        """
        
        # List files from input location directory
        file_list = os.listdir(self.controller.inputLocation)
        # Subject numbers is a set 
        # show up multiple times as SubjectX_Session1, SubjectX_Session2...
        subject_numbers= set()
        # Session numbers is a dictionary with  subject number keys to a list 
        # of session number values
        session_numbers = {}
        # NOTE: Have minor concerns about validating file name structures here...
        for file in file_list:
            # Split file name into string preceeding split char, split char, and string following split
            subj,split,sesh = file.partition("_")
            # Split preceeding string with "Subject"
            subj_s = subj.split("Subject")
            # Split following string with "Session"
            sesh_s = sesh.split("Session")
            
            if(len(subj_s) == 2):
                # Means that Subject was in string
                # Assume the remainder of string is convertible to int
                subj_num = int(subj_s[1])
            else:
                # Subject was not in string, store subject number as None
                subj_num = None
            if(len(sesh_s) == 2):
                # Means that Session was in string: Have something like ["Session","Y.csv"]
                # Still need to split out Y from csv, Y must be int convertible
                sesh_num = int(sesh_s[1].split(".csv")[0])
            else:
                sesh_num = None
            if(subj_num is not None and sesh_num is not None):
                # Both subj_num and sesh_num are not none:
                # Add subj_num to set
                subject_numbers.add(subj_num)
                if(subj_num in session_numbers):
                    # If subj_num already dictionary key in session_numbers, 
                    # just append sesh_num
                    session_numbers[subj_num].append(sesh_num)
                else:
                    # Otherwise set key to new list with sesh_num
                    session_numbers[subj_num] = [sesh_num]
        # Update frame subject/session values
        self.subject_numbers = subject_numbers
        self.session_numbers = session_numbers
        
    def set_subject_numbers(self):
        """Update subject dropdown values with new subject numbers"""
        # Delete old menu items
        menu = self.subject_select["menu"]
        menu.delete(0,"end")
        for subj_num in self.subject_numbers:
            menu.add_command(label=subj_num,
                             command = lambda value=subj_num: self.subject_number.set(value))
        self.subject_select["state"] = "normal"
        
    def update_subject_number(self, *args):
        try:
            # Try to get current subject number, update controller value
            self.controller.subject_number = self.subject_number.get()
            # Set session numbers with valid values for current subject
            self.set_session_numbers()
        except:
            self.controller.subject_number = None
        
    # %% Session Drop Down Menus
    def make_session_select(self):
        """Initialize widgets for session dropdown selection"""
        self.session_text = tk.Message(self)
        self.session_text["text"] = "Session Number"
        self.session_text["width"] = 100
        self.session_text.place(x=50+self.controller.x_offset,y=self.session_y+5)
        self.session_select = tk.OptionMenu(self,self.session_number,"")
        self.session_select["state"] = "disable"
        self.session_select.place(x=150+self.controller.x_offset,y=self.session_y)
        
    
        
    def set_session_numbers(self):
        """Update session dropdown values with new session numbers"""
        # Delete old menu items
        menu = self.session_select["menu"]
        menu.delete(0,"end")
        for sesh_num in self.session_numbers[self.subject_number.get()]:
            menu.add_command(label = sesh_num,
                             command = lambda value = sesh_num: self.session_number.set(value))
        self.session_number.set(self.session_numbers[self.subject_number.get()][0])
        self.session_select["state"] = "normal"
    def update_session_number(self, *args):
        try:
            # Update contrller session number
            self.controller.session_number = self.session_number.get()
            # Enable next button 
            self.Next["state"] = "normal"
        except:
            self.controller.session_number = None
    # %% Audio Device Drop down
    def make_audio_device_select(self):
        """Initialize widgets for audio device selection"""
        self.audio_text = tk.Message(self)
        self.audio_text["text"] = "Select Audio Device"
        self.audio_text["width"] = 300
        self.audio_text.place(x=50+self.controller.x_offset, y = self.audio_y)
        
        self.audio_select = tk.OptionMenu(self,self.audio_device, "")
        self.audio_select.place(x=50+self.controller.x_offset,y=self.audio_y+20)
        menu = self.audio_select["menu"]
        for ix,device in enumerate(self.controller.device_list):
            menu.add_command(label = device["name"]+ " " + self.controller.hostapi_list[device["hostapi"]]["name"],
                             command = lambda value = ix: self.audio_device_ix.set(value))
    
    
    
    def update_audio_device(self, *args):
        """Update audio device based off menu selection"""
        # Update controller audio device
#        print(f"self.audio_device_ix.get(): {self.audio_device_ix.get()}")
#        print(f"self.controller.device_list_ix: {self.controller.device_list_ix}")
#        print(f"self.controller.all_d_out: \n{self.controller.all_d_out}")
        self.controller.audio_device = self.controller.device_list_ix[self.audio_device_ix.get()]
#        print(f"self.controller.audio_device: {self.controller.audio_device}")
#        self.controller.audio_device = self.audio_device_ix.get()
        audio_device = self.controller.device_list[self.audio_device_ix.get()]
        self.audio_device.set(audio_device["name"] + " " + self.controller.hostapi_list[audio_device["hostapi"]]["name"])
        # Update sound device (first input is input, second is output)
        sd.default.device = None,self.controller.audio_device
    # %% Move to test when done
    def make_next_button(self):
        """Initialize widget for button to continue to MRTPage"""
        self.Next = tk.Button(self)
        self.Next["text"] = "Start Session"
        self.Next["font"] = self.controller.title_font
        self.Next["command"] = self.start_MRT
        self.Next["state"] = "disable"
        self.Next.place(x=50+self.controller.x_offset,y=self.next_y,width=300)
        
    #start MRT test, save defaults and show window 
    def start_MRT(self):
        """Save paramters to config file and move to next screen of MRT
        
        Saves selected test directory, subject number, session number, and 
        audio device to the config file. If session number is 1, sends user to 
        the demographics page, otherwise sends to MRT page.
        """        
        config = configparser.ConfigParser()
        config['Default']={'TestDir':self.default_test_dir,
                            'SubjectNumbers':str(self.controller.subject_number),
                            'SessionNumbers':str(self.controller.session_number),
                            'AudioDevice':self.audio_device.get()}
        
        # Check if last session for this subject
        if(self.controller.session_number == max(self.session_numbers[self.controller.subject_number])):
            # Check if last subject in general
            if(self.controller.subject_number == max(self.session_numbers.keys())):
                # Also last subject
                # Set next subject to be lowest number subject
                next_subj = min(self.session_numbers.keys())
            else:
                # Not last subject,
                # Set next subject
                next_subj = self.controller.subject_number + 1
            # Set next session to be lowest number session for that subject
            next_sesh = min(self.session_numbers[next_subj])
        else:
            # Not last session for this subject
            # Keep subject the same
            next_subj = self.controller.subject_number
            # Iterate session
            next_sesh = self.controller.session_number + 1
                
            
        config['Next'] = {'TestDir': self.default_test_dir,
                          'SubjectNumbers':str(next_subj),
                          'SessionNumbers':str(next_sesh),
                          'AudioDevice':self.audio_device.get()}
        with open(self.controller.config_file_name, 'w') as configfile:
            config.write(configfile)
        
        if(self.session_number.get() == 1):
            self.controller.show_frame("DemoPage")    
        else:
            self.controller.show_frame("MRTPage")
        
        
# %% Demographics Page
class DemoPage(tk.Frame):
    """Demographics questions page"""
    font_size = 15
    font = "Helvetica"
    instructions_y = 50
    discipline_y = 400
    age_y = 500
    gender_y = 600
    next_y = 700
    def __init__(self,parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        
        
        self.make_next_button()
        self.make_instructions()
        self.make_discipline_select()
        self.make_age_select()
        self.make_gender_select()
        
    def make_instructions(self):
        """Initialize instruction/information message"""
        self.instructions = tk.Message(self)
        self.instructions['text'] = ("Please enter some basic demographics "
                         "information. Your selections will not be associated "
                         "with your MRT responses in publications and will only "
                         "be published as aggregate statistics.")
        self.instructions["justify"] = "center"
        self.instructions["font"] = self.controller.title_font
        self.instructions["width"] = 300
        
        self.instructions.place(x=50+self.controller.x_offset,y=self.instructions_y)
        
    def make_discipline_select(self):
        """Make a selection button for disciplines"""
        # TODO: Users should be able to pass in disciplines argument when calling MRT()
        self.discipline_text = tk.Message(self)
        self.discipline_text['text'] = ("Please select the discipline closest "
                           "to your own")
        self.discipline_text["justify"] = "center"
        self.discipline_text["width"] = 300
        self.discipline_text["font"] = (self.font, self.font_size)
        self.discipline_text.place(x=50+self.controller.x_offset, y = self.discipline_y)
        
        disciplines = ["Fire", "Police", "EMS", "Other"]
        self.discipline = tk.StringVar(self)
        self.discipline.set("Other")
        
        self.discipline_select = tk.OptionMenu(self,self.discipline, *disciplines)
        self.discipline_select.place(x=150+self.controller.x_offset,y=self.discipline_y+55)
#        menu = self.discipline_select['menu']
#        
#        for disc in disciplines:
#            menu.add_command(label = disc,
#                             command = lambda value = disc: self.discipline.set(value))
    
    def make_age_select(self):
        """Initialize age selection widgets"""
        self.age_text = tk.Message(self)
        self.age_text["text"] = ("Please select your age range")
        self.age_text["justify"] = "center"
        self.age_text["width"] = 300
        self.age_text["font"] = (self.font, self.font_size)
        self.age_text.place(x=50+self.controller.x_offset, y = self.age_y)
        
#        age_ranges = ["18 to 24", "25 to 39", "40 to 60", "60 plus"]
        age_ranges = ["Under 30", "30 - 39", "40 - 49", "50 - 59", "60 plus"]
        self.age = tk.StringVar(self)
        self.age.set(age_ranges[0])
        self.age_select = tk.OptionMenu(self,self.age,*age_ranges)
        self.age_select.place(x=150+self.controller.x_offset,y=self.age_y+40)
        
    def make_gender_select(self):
        """Initialize gender entry widgets"""
        self.gender_text = tk.Message(self)
        self.gender_text["text"] = ("Please enter your gender")
        self.gender_text["justify"] = "center"
        self.gender_text["width"] = 300
        self.gender_text["font"] = (self.font, self.font_size)
        self.gender_text.place(x=50+self.controller.x_offset, y = self.gender_y)
        
        self.gender= tk.StringVar(self)
        self.gender.trace("w", self.check_gender_entry)
        self.gender_entry = tk.Entry(self,textvariable=self.gender)
        self.gender_entry.place(x=100+self.controller.x_offset,y=self.gender_y+30)
        
    def check_gender_entry(self, *args):
        """Check that gender entry has at least one alpha character"""
        gender = self.gender.get()
        has_alpha = any(c.isalpha() for c in gender)
        
        if(has_alpha):
            self.Next["state"] = "normal"
        else:
            self.Next["state"] = "disable"
            
    def make_next_button(self):
        """Initialize widget for button to continue to MRTPage"""
        self.Next = tk.Button(self)
        self.Next["text"] = "Start Session"
        self.Next["font"] = self.controller.title_font
        self.Next["command"] = self.start_MRT
        self.Next["state"] = "disable"
        self.Next.place(x=50+self.controller.x_offset,y=self.next_y,width=300)
        
    def start_MRT(self):
        """Save demographics information and continue to MRT session"""
        subject_number = self.controller.subject_number
        
        results_dir = os.path.join(self.controller.test_dir.get(), 'Results')
        
        # Record when test finishes
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        fname = "Subject" + str(subject_number) + "_Demographics_" + now_str + ".csv"
        fpath = os.path.join(results_dir,fname)
        header = ["Discipline", "Age" ,"Gender"]
        with open(fpath,"w",newline="") as demo_file:
            csv_writer = csv.writer(demo_file,delimiter= ",")
            csv_writer.writerow(header)
            row = [self.discipline.get(), self.age.get(), self.gender.get()]
            csv_writer.writerow(row)
        self.controller.show_frame("MRTPage")
# %% MRT Session
class MRTPage(tk.Frame):
    """Modified rhyme test page where MRT trials are performed"""
    font_style = "Helvetica"
    button_font_size = 20
    message_font_size =20
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        
        # Define word list
        self.wordList = self.MRT_keywords()
        # set trial number
        self.trial_number = 0         
        # Initialize start screen
        self.start_screen()
        
    def set_session_name(self):
        """Define session name based off subject and session numbers"""
        # Define session name
        self.session_name = ("Subject" + str(self.controller.subject_number) + 
                             "_Session" + str(self.controller.session_number) + 
                             ".csv")
        
    def load_session_playlist(self):
        """Load session playlist from Playlist subdirectory based off session name"""
        # Load session play list
        with open(os.path.join(self.controller.inputLocation,self.session_name), mode="r") as csv_file:
            self.ssPL = [{k: v for k, v in row.items()}
            for row in csv.DictReader(csv_file, skipinitialspace=True)]
        # Resave ssPL orders as list of ints
        for row in self.ssPL:
            row["Order"] = [int(m) for m in re.findall(r"[0-9]+",row["Order"])]
        # Define total number of trials
        self.session_length= len(self.ssPL)
        
    def MRT_keywords(self):
        """Generate list of Modified Rhyme Test keywords
        
        The Modified Rhyme Test (MRT) consists of 300 stimulus words. 
        The words all are structued with consonant-vowel-consonant sounds. 
        The words are organized into 50 lists. Within each list either the 
        leading or trailing consonant varies. In this way all the words of a 
        particular list "rhyme". This is either in the traditional sense as 
        with the list 'went', 'sent', 'bent', 'dent', 'tent', 'rent' or in a 
        less traditional sense, e.g. 'pat', 'pad', 'pan', 'path', 'pack', 
        'pass'.
        """
        # Define MRT keywords list
        wordList = [['went', 'sent', 'bent', 'dent', 'tent', 'rent'], 
                    ['hold', 'cold', 'told', 'fold', 'sold', 'gold'], 
                    ['pat', 'pad', 'pan', 'path', 'pack', 'pass'],
                    ['lane', 'lay', 'late', 'lake', 'lace', 'lame'], 
                    ['kit', 'bit', 'fit', 'hit', 'wit', 'sit'], 
                    ['must', 'bust', 'gust', 'rust', 'dust', 'just'],
                    ['teak', 'team', 'teal', 'teach', 'tear', 'tease'], 
                    ['din', 'dill', 'dim', 'dig', 'dip', 'did'], 
                    ['bed', 'led', 'fed', 'red', 'wed', 'shed'], 
                    ['pin', 'sin', 'tin', 'fin', 'din', 'win'], 
                    ['dug', 'dung', 'duck', 'dud', 'dub', 'dun'], 
                    ['sum', 'sun', 'sung', 'sup', 'sub', 'sud'], 
                    ['seep', 'seen', 'seethe', 'seek', 'seem', 'seed'],
                    ['not', 'tot', 'got', 'pot', 'hot', 'lot'],
                    ['vest', 'test', 'rest', 'best', 'west', 'nest'], 
                    ['pig', 'pill', 'pin', 'pip', 'pit', 'pick'], 
                    ['back', 'bath', 'bad', 'bass', 'bat', 'ban'],
                    ['way', 'may', 'say', 'pay', 'day', 'gay'], 
                    ['pig', 'big', 'dig', 'wig', 'rig', 'fig'],
                    ['pale', 'pace', 'page', 'pane', 'pay', 'pave'],
                    ['cane', 'case', 'cape', 'cake', 'came', 'cave'],
                    ['shop', 'mop', 'cop', 'top', 'hop', 'pop'],
                    ['coil', 'oil', 'soil', 'toil', 'boil', 'foil'], 
                    ['tan', 'tang', 'tap', 'tack', 'tam', 'tab'],
                    ['fit', 'fib', 'fizz', 'fill', 'fig', 'fin'],
                    ['same', 'name', 'game', 'tame', 'came', 'fame'], 
                    ['peel', 'reel', 'feel', 'eel', 'keel', 'heel'], 
                    ['hark', 'dark', 'mark', 'bark', 'park', 'lark'], 
                    ['heave', 'hear', 'heat', 'heal', 'heap', 'heath'], 
                    ['cup', 'cut', 'cud', 'cuff', 'cuss', 'cub'],
                    ['thaw', 'law', 'raw', 'paw', 'jaw', 'saw'], 
                    ['pen', 'hen', 'men', 'then', 'den', 'ten'], 
                    ['puff', 'puck', 'pub', 'pus', 'pup', 'pun'],
                    ['bean', 'beach', 'beat', 'beak', 'bead', 'beam'],
                    ['heat', 'neat', 'feat', 'seat', 'meat', 'beat'], 
                    ['dip', 'sip', 'hip', 'tip', 'lip', 'rip'], 
                    ['kill', 'kin', 'kit', 'kick', 'king', 'kid'],
                    ['hang', 'sang', 'bang', 'rang', 'fang', 'gang'],
                    ['took', 'cook', 'look', 'hook', 'shook', 'book'],
                    ['mass', 'math', 'map', 'mat', 'man', 'mad'],
                    ['ray', 'raze', 'rate', 'rave', 'rake', 'race'], 
                    ['save', 'same', 'sale', 'sane', 'sake', 'safe'],
                    ['fill', 'kill', 'will', 'hill', 'till', 'bill'],
                    ['sill', 'sick', 'sip', 'sing', 'sit', 'sin'],
                    ['bale', 'gale', 'sale', 'tale', 'pale', 'male'],
                    ['wick', 'sick', 'kick', 'lick', 'pick', 'tick'], 
                    ['peace', 'peas', 'peak', 'peach', 'peat', 'peal'], 
                    ['bun', 'bus', 'but', 'bug', 'buck', 'buff'], 
                    ['sag', 'sat', 'sass', 'sack', 'sad', 'sap'], 
                    ['fun', 'sun', 'bun', 'gun', 'run', 'nun']]
        return(wordList)
    
    def start_screen(self):
        """Initialize the welcome screen of the MRT test"""
        # Initialize welcome button
        self.make_welcome()
        # Initialize start button 
        self.make_start_button()
        
    def make_welcome(self):
        # Initialize welcome message
        self.Welcome = tk.Message(self)
        # Set text, font and width
        self.Welcome["text"] = ("Welcome to the Modified Rhyme Test. Please press "
                    "start to begin the test.")
        self.Welcome["justify"] = "center"
        self.Welcome["font"] = (self.font_style,self.message_font_size)
        self.Welcome["width"] = 300
        
        # Place welcome message
        self.Welcome.place(x=50+self.controller.x_offset,y=50)
        
        
    def make_start_button(self):
        """Initialize start button widget"""
        # Initialize start button
        self.StartButton = tk.Button(self)
        # Set text and font
        self.StartButton["text"] = "Start"
        self.StartButton["font"] = (self.font_style,self.button_font_size)
        
        # Define callback function on click
        self.StartButton["command"] = self.start_button_pushed
        
        # Place start button
        self.StartButton.place(x=150+self.controller.x_offset,y=200,width=100,height=50)
        
    def start_button_pushed(self):
        """Start MRT test when start button pushed"""
        # Delete start screen
        self.clear_start_screen()
        
        self.set_session_name()
        # Load session playlist
        self.load_session_playlist()
        
        # Set up instructions, play buttons, and word buttons
        self.make_instructions()
        self.make_play_button()
        self.make_word_buttons()
        # Label word buttons
        self.label_words()
        self.set_word_state("disable")
        self.make_trial_counter()
        
    def clear_start_screen(self):
        """Delete welcome screen after start button pushed"""
        # Delete welcome message and start button
        self.Welcome.destroy()
        self.StartButton.destroy()
    
    def make_instructions(self):
        """Initialize widget for trial instructions"""
        self.Instructions = tk.Message(self)
        
        self.Instructions["text"] = ("Please select the indicated word from "
                         "the choices below:")
        self.Instructions["justify"] = "center"
        self.Instructions["font"] = (self.font_style, self.message_font_size)
        self.Instructions["width"] = 300
        self.Instructions.place(x=50+self.controller.x_offset,y=50)
        
    def make_play_button(self):
        """Initialize widget for play button"""
        self.PlayButton = tk.Button(self)
        
        self.PlayButton["text"] = "Play"
        self.PlayButton["font"] = (self.font_style, self.button_font_size)
        
        self.PlayButton["command"] = self.play_button_pushed
        
        self.PlayButton.place(x=150+self.controller.x_offset,y=200, width=100, height = 50)
        
    def make_word_buttons(self):
        """Initialize widgets for word buttons"""
        self.Wordbuttons = list()
        
        for k in range(6):
            # Each button constant x
            x = 125
            # Move subsequent buttons down the app
            y = 300 + k*75
            # Make a new button, append it to list
            self.Wordbuttons.append(self.make_word_button(x=x,y=y,ix=k))
        
        
    def make_word_button(self,x,y,ix):
        """Word button widget constructor"""
        self.wb = tk.Button(self)
        
        self.wb["text"] = "Word"
        self.wb["font"] = (self.font_style, self.button_font_size)
        # Word button commands must be lambda so that the identifier of the 
        # button pressed can be determined
        self.wb["command"] = lambda: self.word_button_pushed(ix)
        
        self.wb.place(x=x+self.controller.x_offset,y=y,width=150,height=50)
        return(self.wb)
    
    def label_words(self):
        """Label word buttons according to session playlist list and order"""
        # Extract current list index
        batch = int(self.ssPL[self.trial_number]["List"])
        # Get order to display words
        order = self.ssPL[self.trial_number]["Order"]
        
        # List indices are saved in 1-50, convert to (0-49)
        word_list = self.wordList[batch-1]
        for ix,wb in enumerate(self.Wordbuttons):
            wb["text"] = word_list[order[ix]]
            
    def set_word_state(self,state):
        """Enable or disable word buttons"""
        for wb in self.Wordbuttons:
            wb["state"] = state
    
    def make_trial_counter(self):
        """Initialize widget to display trial counter"""
        self.trial_counter = tk.Message(self)
        self.trial_counter["text"] = "Trial " + str(self.trial_number+1) + " of " + str(self.session_length)
        self.trial_counter["font"] = (self.font_style,10)
        self.trial_counter["justify"] = "left"
        self.trial_counter["width"] = 100
        self.trial_counter.place(x=300+self.controller.x_offset,y=775)
        
    def update_trial_counter(self):
        """Update trial counter"""
        self.trial_counter["text"] = "Trial " + str(self.trial_number+1) + " of " + str(self.session_length)
        
    def play_button_pushed(self):
        self.PlayButton.destroy()
        
        self.start_trial()
        
    def start_trial(self):
        """Initialize a new MRT trial"""
        clip_path = os.path.join(self.controller.clipLocation,self.ssPL[self.trial_number]["File"])
        # Read wav file
        fs,clip = scipy.io.wavfile.read(clip_path)
        # Play clip, record play time
        self.play_time = self.play_clip(clip,fs)
        
        # Save time start for voting timing later
        self.vote_start = time.time()
        
    def play_clip(self,raw_clip,fs,pad=0.2):
        """Play audio clip, hold until done playing"""
        # Record time of play starting
        play_start  = time.time()
        # Pad clip with 200 ms of silence at end
        # BUG: Noticed that sd.play occasionaly prematurely cuts off audio, pad to avoid this
        clip = np.pad(raw_clip,[0,np.int16(np.round(fs*pad))],mode="constant")
        # Play clip, with blocking to prevent action while clip is playing
        sd.play(clip,fs)
        # Hold GUI until clip is done, re-enable buttons
        # Do not use blocking via sd as this prevents GUI from refreshing and causes clicks on disabled buttons to register as soon as they are enabled later
        self.after(int(len(clip)/fs*1e3),lambda: self.set_word_state("normal"))
        # Record when clip finishes
        play_end = time.time()
        
        # Play time for the audio clip
        play_time = play_end - play_start
        return(play_time)
        
    def word_button_pushed(self,ix):
        """Record vote and end trial"""
        # Record when vote was cast
        vote_end = time.time()
        # Disable word buttons
        self.set_word_state("disable")
        # Record button index
        vote = self.ssPL[self.trial_number]["Order"][ix]
        
        # End trial
        self.end_trial(vote,vote_end)
        
    def end_trial(self,vote,vote_end):
        """Finish MRT trial"""
        # Store results
        self.ssPL[self.trial_number]["Vote"] = vote+1
        # Calculate vote time
        vote_time = vote_end - self.vote_start
        # Store play and vote times
        self.ssPL[self.trial_number]["PlayTime"] = self.play_time
        self.ssPL[self.trial_number]["VoteTime"] = vote_time
        self.ssPL[self.trial_number]["AudioDevice"] = self.controller.get_audio_device_name()
        # Increment trial number
        self.trial_number += 1
        
        if(self.trial_number == self.session_length):
            # End the test when trial number has reached session length
            self.end_test()
        else:
            # Relabel words for next batch
            self.label_words()
            # Update the trial counter
            self.update_trial_counter()
            # Force the GUI to update and reflect changes
            self.controller.update()
            # Start next trial
            self.start_trial()
            
    def end_test(self):
        """Conclude MRT session"""
        # Remove buttons and instructions
        for wb in self.Wordbuttons:
            wb.destroy()
        self.Instructions.destroy()
        
        # Set the quit screen
        self.make_quit_screen()
        
        # Record when test finishes
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        # Save unique results file
        session_name = self.session_name.replace(".csv","_"+now_str+".csv")
        
        session_path = os.path.join(self.controller.outputLocation,session_name)
        with open(session_path, mode="w",newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter = ",")
            csv_writer = csv.DictWriter(csv_file,fieldnames = self.ssPL[0].keys())
            csv_writer.writeheader()
            for trial in self.ssPL:
                csv_writer.writerow(trial)
        

        config = configparser.ConfigParser()
        #file name for config

        if(os.path.exists(self.controller.config_file_name)):    
            # Read config file
            try:
                config.read(self.controller.config_file_name)
            except:
                print('Error reading config file : ',flush=True);
                traceback.print_exc()
                return
            # Update and write config file
            try:
                config['Default'] = config['Next']
                with open(self.controller.config_file_name, 'w') as configfile:
                    config.write(configfile)    
            except:
                print("Exception while updating config file")
                traceback.print_exc()
                
        # Activate close button
        self.activate_close_button()
    
    
    def make_quit_screen(self):
        """Initialize widgets for a quit screen"""
        # Set thank you message
        self.Thanks = tk.Message(self)
        self.Thanks["text"] = ("Thank you for participating in the PSCR "
                         "MRT. Click Close to end the test.")
        self.Thanks["justify"] = "center"
        self.Thanks["font"] = (self.font_style, self.message_font_size)
        self.Thanks["width"] = 300
        self.Thanks.place(x=50+self.controller.x_offset,y=50)
        
        # Set close button
        self.CloseButton = tk.Button(self)
        self.CloseButton["text"] = "Close"
        self.CloseButton["justify"] = "center"
        self.CloseButton["font"] = (self.font_style, self.message_font_size)
        
        self.CloseButton["command"] = self.close_button_pushed
        
        # Close button should be disabled, and only enabled once the results 
        # have been saved
        self.CloseButton["state"] = "disable"
        
        self.CloseButton.place(x=150+self.controller.x_offset,y=200,width=100,height=50)
        
    def activate_close_button(self):
        self.CloseButton["state"] = "normal"
        
    def close_button_pushed(self):
        # Destroy the application
        self.controller.destroy()

if(__name__ == "__main__"):
    # Create mrt instance
    mrt = MRT()
    # Initialize
    mrt.mainloop()
