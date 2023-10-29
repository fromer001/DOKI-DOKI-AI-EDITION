define persistent.playerName = None
define persistent.chatModel = None
define persistent.imgModel = None
#define persistent.charVoice = None
define persistent.chatToken = None
define persistent.imgToken = None

#define truecenter = Position(xalign=0.5, yalign=0.5)

image theme:
    "bg/theme.png"

image warning:
    "bg/warning.png"

image ai_mods:
    "assets/imgs/both.png"
    yalign 0.5
    
image white = "#ffffff"

label splashscreen:
    python:
        s_kill_early = None
        m_deleted = False
        s_deleted = False

        try:
            renpy.file("../characters/monika.chr")
        except:
            with open(f"{config.basedir}/characters/monika.chr", 'w') as f:
                f.write("c29tZSBzZWNyZXRzIGFyZSBiZXN0IGxlZnQgdW50b3VjaGVk")
            m_deleted = True

        try:
            renpy.file("../characters/sayori.chr")
            Show(screen="dialog", message="File error: \"characters/sayori.chr\"\n\nThe file is missing or corrupt.",
                ok_action=Show(screen="dialog", message="The save file is corrupt. Starting a new game.", ok_action=Function(renpy.full_restart, label="start")))
        except: pass
    
    if s_kill_early:
        jump now_everyone_can_be_happy
    if m_deleted:
        return Show(screen="dialog", message="You accidentally deleted me? It's okay! Mistakes happen.", ok_action=Hide("dialog"))
    if s_deleted:
        return Show(screen="dialog", message="File error: \"characters/sayori.chr\"\n\nThe file is missing or corrupt.",
            ok_action=Show(screen="dialog", message="The save file is corrupt. Starting a new game.", ok_action=Function(renpy.full_restart, label="start")))



    if persistent.playerName == 'Sayori':
        return Show(screen="dialog", message="It's far too early for that, please wait a bit longer.",  ok_action=Hide("dialog"))
    elif persistent.playerName == 'Monika':
        return Show(screen="dialog", message="There's no point in saving anymore.\nDon't worry, I'm not going anywhere.", ok_action=Hide("dialog"))

    if persistent.playerName == None:
        scene warning
        $ persistent.playerName = renpy.input("What is your name?", "User", allow=" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789").strip()

    if persistent.chatModel == None:
        "Because the A.I. models arent locally hosted, please follow the steps listed on the github page. https://github.com/syntax-z/DOKI-DOKI-AI-EDITION"
        "If you aren't able to do that at this moment, you can skip all these steps and change them in the settings later. But the game wont work until you complete them"

        "Which Language model would you like to use?"
        "1 is for 'chatGPT' (recommended)"
        $ chatModel = renpy.input("Which AI model would you like to use? (enter '1')", "1", allow="1").strip()
        if chatModel == "1":
            "You chose chatGPT!"
        #elif chatModel == "2":
        #    "You choose Bard!"
        else:
            "Not a valid chat model, change this in the settings once you get the chance!"

        # Ensures that if the user exited out of the game before completing the steps, they can finish
        # when they reload
        $ persistent.chatModel = chatModel

    if persistent.chatToken == None:
        "Do NOT share any of your tokens to ANYONE. Your tokens will be used here strictly for generating responses."
        "If someone you do not trust gets it, they can send multiple request to the API, costing you money."
        "If you think your token has some how been exposed, you can reset it on the official page."
        $ chatToken = renpy.input("Enter your openAI (chatGPT) token: ").strip()

        "If you misclicked or entered the wrong token by accident, you can always change it in the settings."

        $ persistent.chatToken = chatToken

    if persistent.imgModel == None:
        "Which Image generation model would you like to use?"
        "1 is for 'getimgai' (recommended) and 2 is for 'stablediffusionapi' (You can tweak these later in the settings)"
        $ imgModel = renpy.input("Which Image generation model would you like to use?(1 or 2)", "1", allow="12").strip()
        if imgModel == "1":
            "You chose getimgai!"
        elif imgModel == "2":
            "You choose stablediffusionapi!"
        else:
            "Not a valid image model, change this in the settings once you get the chance!"

        "(reminder) Because the A.I. models arent locally hosted, please follow the steps listed on the github page. https://github.com/syntax-z/DOKI-DOKI-AI-EDITION"
        "(reminder) If you aren't able to do that at this moment, you can skip the next step and change them in the settings later. But the game wont work until you complete the steps."

        $ persistent.imgModel = imgModel

    if persistent.imgToken == None:
        $ imgToken = renpy.input("Enter your image generation token: ").strip()
        "If you misclicked or entered the wrong token by accident, you can always change it in the settings."
        $ persistent.imgToken = imgToken

    scene theme

    play music "audio/music/ddlc_theme.mp3" volume 0.6
    with Pause(1)

    show text "Please remember that this is just a game and\nthe Doki's aren't actually real." with dissolve
    $ renpy.pause(3, hard=True)
    hide text with dissolve
    with Pause(1.3)

    return



################################################################################
## Main Menu Animations (Copied from Official Doki Doki Literature Club)
################################################################################

transform menu_bg_move:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat
    parallel:
        ypos 0
        time 0.65
        ease_cubic 2.5 ypos -500

transform menu_nav_move:
    subpixel True
    xoffset -500
    time 1.5
    easein_quint 1 xoffset 0

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (1200 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

transform particle_fadeout:
    easeout 1.5 alpha 0


transform dizzy(m, t, subpixel=True):
    subpixel subpixel
    parallel:
        xoffset 0
        ease 0.75 * t xoffset 10 * m
        ease 0.75 * t xoffset 5 * m
        ease 0.75 * t xoffset -5 * m
        ease 0.75 * t xoffset -3 * m
        ease 0.75 * t xoffset -10 * m
        ease 0.75 * t xoffset 0
        ease 0.75 * t xoffset 5 * m
        ease 0.75 * t xoffset 0
        repeat
    parallel:
        yoffset 0
        ease 1.0 * t yoffset 5 * m
        ease 2.0 * t yoffset -5 * m
        easein 1.0 * t yoffset 0
        repeat


image menu_bg:
    topleft
    "gui/polka.png"
    menu_bg_move

image menu_nav:
    "gui/overlay/main_menu.png"
    menu_nav_move

image menu_logo:
    "gui/logo.png"
    subpixel True
    xcenter 240
    ycenter 120
    zoom 0.25
    menu_logo_move


image monika_menu:
    subpixel True
    "gui/monika.png"
    xcenter 1000
    ycenter 640
    zoom 1.00
    menu_art_move(1.00, 1000, 1.00)


image natsuki_menu:
    subpixel True
    "gui/natsuki.png"
    xcenter 750
    ycenter 385
    zoom 0.58
    menu_art_move(0.58, 750, 0.58)


image sayori_menu:
    subpixel True
    "gui/sayori.png"
    xcenter 510
    ycenter 500
    zoom 0.68
    menu_art_move(0.68, 510, 0.68)


image yuri_menu:
    subpixel True
    "gui/yuri.png"
    xcenter 600
    ycenter 335
    zoom 0.60
    menu_art_move(0.54, 600, 0.60)


image particles_menu:
    2.481
    xpos 224
    ypos 104
    ParticleBurst("gui/particle.png", explodeTime=0, numParticles=40, particleTime=2.0, particleXSpeed=3, particleYSpeed=3).sm
    particle_fadeout





################################################################################
## Custom Animations
################################################################################



transform uppies:
    yalign 1.35
    easeout 0.4 yalign 1.0
    easein 0.4 yalign 1.35



################################################################################
## Gamemodes
################################################################################


image justMonika_txt:
    "gui/gamemode/justMonika_txt.png"
    zoom 0.25
    ypos 180
    xpos 370

image justMonika_desc:
    "gui/gamemode/justMonika_desc.png"
    zoom 0.25
    ypos 180
    xpos 540




################################################################################
## Sayori CG
################################################################################



image end:
    "gui/end.png"


image noise:
    truecenter
    "images/cg/noise1.jpg"
    pause 0.1
    "images/cg/noise2.jpg"
    pause 0.1
    "images/cg/noise3.jpg"
    pause 0.1
    "images/cg/noise4.jpg"
    pause 0.1
    xzoom -1
    "images/cg/noise1.jpg"
    pause 0.1
    "images/cg/noise2.jpg"
    pause 0.1
    "images/cg/noise3.jpg"
    pause 0.1
    "images/cg/noise4.jpg"
    pause 0.1
    yzoom -1
    "images/cg/noise1.jpg"
    pause 0.1
    "images/cg/noise2.jpg"
    pause 0.1
    "images/cg/noise3.jpg"
    pause 0.1
    "images/cg/noise4.jpg"
    pause 0.1
    xzoom 1
    "images/cg/noise1.jpg"
    pause 0.1
    "images/cg/noise2.jpg"
    pause 0.1
    "images/cg/noise3.jpg"
    pause 0.1
    "images/cg/noise4.jpg"
    pause 0.1
    yzoom 1
    repeat





################################################################################
## Monika CG
################################################################################

image mask_test = AnimatedMask("#ff6000", "mask_mask", "maskb", 0.10, 32)
image mask_test2 = AnimatedMask("#ffffff", "mask_mask", "maskb", 0.03, 16)
image mask_test3 = AnimatedMask("#ff6000", "mask_mask_flip", "maskb", 0.10, 32)
image mask_test4 = AnimatedMask("#ffffff", "mask_mask_flip", "maskb", 0.03, 16)



image room_mask = Composite((1280, 720), (0, 0), "mask_test", (0, 0), "mask_test2")
image room_mask2 = Composite((1280, 720), (0, 0), "mask_test3", (0, 0), "mask_test4")



image splash_glitch2 = "images/bg/splash-glitch2.png"


image mask_child:
    "images/cg/child_2.png"
    xtile 2

image mask_mask:
    "images/cg/mask.png"
    xtile 3

image mask_mask_flip:
    "images/cg/mask.png"
    xtile 3 xzoom -1


image maskb:
    "images/cg/maskb.png"
    xtile 3

image mask_test = AnimatedMask("#ff6000", "mask_mask", "maskb", 0.10, 32)
image mask_test2 = AnimatedMask("#ffffff", "mask_mask", "maskb", 0.03, 16)
image mask_test3 = AnimatedMask("#ff6000", "mask_mask_flip", "maskb", 0.10, 32)
image mask_test4 = AnimatedMask("#ffffff", "mask_mask_flip", "maskb", 0.03, 16)

image mask_2:
    "images/cg/mask_2.png"
    xtile 3 subpixel True
    block:
        xoffset 1280
        linear 1200 xoffset 0
        repeat

image mask_3:
    "images/cg/mask_3.png"
    xtile 3 subpixel True
    block:
        xoffset 1280
        linear 180 xoffset 0
        repeat

image monika_room = "images/cg/monika_room.png"
image monika_room_highlight:
    "images/cg/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika_bg_highlight.png"
    function monika_alpha

