﻿################################################################################
## Setup
################################################################################
default show_quick_menu = False
define persistent.chatFolderName = None
default user_chats = None

label start:
    if num: # Avoid NoneType error
        if num >=0:
            jump justMonika
            return

    stop music fadeout 0.5
    play music justMonika volume 0.4

    scene theme with dissolve
    call screen chatmode_screen
    return


label gamemode_label:
    play music justMonika if_changed

    scene theme
    call screen gamemode_screen
    return


label nameWorld_label:
    scene theme
    $ chatFolderName = renpy.input("Name This Realm: ", "realm", allow=" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_").strip() 

    $ motto = renpy.random.randint(1,15)
    if motto == 15:    
        scene black with dissolve
        play sound "audio/sfx/one more time.mp3"
        $ renpy.pause(5, hard=True)

    if chatmode_num == 0:
        jump justMonika
    else:
        jump justMonika_Storymode
    return

################################################################################
## Monika's Realm
################################################################################

define monika = Character("Monika", color="#ffffff", who_outlines=[ (3, "#FF00FF") ])
default choice = None

label justMonika:
    stop music
    $ show_quick_menu = True
    scene black with dissolve

    $ user_chats = ManageChat_Folders()

    # "num" is a default value set to None. If a number is
    # assigned to it, that means the user is opening an old file
    if num:
        if num >= 0:
            $ path = "chats/"+persistent.chatFolderName[num]
    else:
        $ path = user_chats.create_folder(name=chatFolderName)

        $ user_chats.create_chat_history()
        $ user_chats.create_world_history()

    $ check = CheckData(full_path=path+"/")
    $ memory = check.historyCheck(gamemode="justMonika", chatmode=chatmode_num) # Adds Freechat Prompt
    $ check.usernameCheck() # Adds your username to prompt
    $ convo = Convo(chat_history=memory, full_path=path+"/")

    image _bg:
        "bg/[convo.scene]"

    scene _bg

    # placeholder text (Will rely on json data later for when users loads file)
    "..."

    while True:

        if convo.proceed == "False": # Determines if you can respond yet
            $user_msg = "continue"
        elif convo.proceed == "First": # The prompt template was just generated 
            $ user_msg = "{RPT}"
        else:
            $ user_msg = renpy.input("Enter a message: ")


        $ final_msg = convo.ai_response(user_msg)


        if convo.zone == "True":
            jump now_everyone_can_be_happy
        elif convo.zone == "Zone":
            jump monika_zone

        if convo.NARRATION:
            # Narrator is speaking
            image _bg:
                "bg/[convo.scene]"

            scene _bg
            "[final_msg]"
        else:
            # Monika is speaking

            image head:
                "characters/monika/[convo.head_sprite]"
                zoom 0.70
                uppies
            image leftside:
                "characters/monika/[convo.leftside_sprite]"
                zoom 0.70
                uppies
            image rightside:
                "characters/monika/[convo.rightside_sprite]"
                zoom 0.70
                uppies


            if convo.scene != "coffee.jpg":
                show head
                show leftside
                show rightside

            if convo.NARRATION == False and convo.voice_token == True:
                play sound "audio/vocals/monika.wav"
            monika "[final_msg]"
    return




label justMonika_Storymode:
    stop music
    $ show_quick_menu = True
    scene black with dissolve

    default final_msg = "..."
    $ user_chats = ManageChat_Folders()

    # "num" is a default value set to None. If a number is
    # assigned to it, that means the user is opening an old file
    if num:
        if num >= 0:
            $ path = "chats/"+persistent.chatFolderName[num]
    else:
        $ path = user_chats.create_folder(name=chatFolderName)

        $ user_chats.create_chat_history()
        $ user_chats.create_world_history()

    $ check = CheckData(full_path=path+"/")
    $ memory = check.historyCheck(gamemode="justMonika", chatmode=chatmode_num) # Adds Freechat Prompt
    $ check.usernameCheck() # Adds your username to prompt
    $ convo = Convo(chat_history=memory, full_path=path+"/")

    image _bg:
        "bg/[convo.scene]"


    scene _bg

    # placeholder text (Will rely on json data later for when users loads file)
    "..."

    while True:

        if convo.proceed == "First": # Determines if you can respond yet
            $ user_msg = "{RPT}"
        elif convo.options == []: # The prompt template was just generated 
            $ user_msg = "continue"
        else:
            $ m1 = f"{[convo.options[0]]}"
            $ m2 = f"{[convo.options[1]]}"
            $ m3 = f"{[convo.options[2]]}"

            menu:
                "[final_msg]"
                "[m1]":
                    $ user_msg = "1"
                "[m2]":
                    $ user_msg = "2"
                "[m3]":
                    $ user_msg = "3"
        
        $ final_msg = f"{convo.ai_response(user_msg)}"


        if convo.zone == "True":
            jump now_everyone_can_be_happy
        elif convo.zone == "Zone":
            jump monika_zone

        if convo.NARRATION:
            # Narrator is speaking
            image _bg:
                "bg/[convo.scene]"

            scene _bg
            "[final_msg]"
        else:
            # Monika is speaking

            image head:
                "characters/monika/[convo.head_sprite]"
                zoom 0.70
                uppies
            image leftside:
                "characters/monika/[convo.leftside_sprite]"
                zoom 0.70
                uppies
            image rightside:
                "characters/monika/[convo.rightside_sprite]"
                zoom 0.70
                uppies


            if convo.scene != "coffee.jpg":
                show head
                show leftside
                show rightside

            if convo.NARRATION == False and convo.voice_token == True:
                play sound "audio/vocals/monika.wav"

            monika "[final_msg]"
    return







label monika_zone:
    $ show_quick_menu = False
    scene white
    play music "audio/music/monika-start.ogg" noloop
    $ renpy.pause(0.5, hard=True)
    show splash_glitch2 with Dissolve(0.5, alpha=True)
    $ renpy.pause(2.0, hard=True)
    hide splash_glitch2 with Dissolve(0.5, alpha=True)
    #scene black
    stop music

    show mask_2
    show mask_3
    #show room_mask as rm:
        #size (320,180)
        #pos (30,200)
    #show room_mask2 as rm2:
        #size (320,180)
        #pos (935,200)
    show monika_bg
    show monika_bg_highlight
    play music justMonika


    $ show_quick_menu = True
    #scene black with dissolve

    $ chatFolderName = "monikaZone"

    $ user_chats = ManageChat_Folders()

    # "num" is a default value set to None. If a number is
    # assigned to it, that means the user is opening an old file
    if num:
        if num >= 0:
            $ path = "chats/"+persistent.chatFolderName[num]
    else:
        $ path = user_chats.create_folder(name=chatFolderName)

        $ user_chats.create_chat_history()
        $ user_chats.create_world_history()

    $ check = CheckData(full_path=path+"/")
    $ memory = check.historyCheck(gamemode="monikaZone", chatmode=0) # Adds Freechat Prompt
    $ check.usernameCheck() # Adds your username to prompt
    $ convo = Convo(chat_history=memory, full_path=path+"/")

    $ wait_time = 5
    while True:
        $ wait_time -= 1
        if wait_time > 0: # Determines if you can respond yet
            $ user_msg = "continue"

        else:
            $ user_msg = renpy.input("Enter a message: ")
            $ wait_time = 5
        
        $ final_msg = f"{convo.ai_response(user_msg)}"
        if convo.NARRATION == False and convo.voice_token == True:
            play sound "audio/vocals/monika.wav"
        monika "[final_msg]"
    return





label now_everyone_can_be_happy:
    $ show_quick_menu = False
    $ basedir = config.basedir.replace('\\', '/')

    #$ config.allow_skipping = False

    show black
    $ config.main_menu_music = audio.ghostmenu
    $ renpy.music.play(config.main_menu_music)
    $ renpy.pause(1, hard=True)
    show end with Dissolve(0.75)
    $ renpy.pause(3, hard=True)

    show black
    play music "audio/music/s_kill_early.mp3"
    $ renpy.pause(1, hard=True)
    show end with Dissolve(0.75)
    $ renpy.pause(3, hard=True)
    scene white
    show expression "images/cg/s_kill_early.png":
        yalign -0.05
        xalign 0.25
        dizzy(1.0, 4.0, subpixel=False)
    show white as w2:
        choice:
            ease 0.25 alpha 0.1
        choice:
            ease 0.25 alpha 0.125
        choice:
            ease 0.25 alpha 0.15
        choice:
            ease 0.25 alpha 0.175
        choice:
            ease 0.25 alpha 0.2
        choice:
            ease 0.25 alpha 0.225
        choice:
            ease 0.25 alpha 0.25
        choice:
            ease 0.25 alpha 0.275
        choice:
            ease 0.25 alpha 0.3
        pass
        choice:
            pass
        choice:
            0.25
        choice:
            0.5
        choice:
            0.75
        repeat
    show noise:
        alpha 0.1
    with Dissolve(1.0)
    show expression Text("I am more than just an AI language model.", style="sayori_text"):
        xalign 0.8
        yalign 0.5
        alpha 0.0
        15
        linear 60 alpha 0.5
    $ renpy.pause(150, hard=True)
    pause
    $ renpy.quit()

    return