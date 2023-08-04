init python:
    #TODO: Add Async functions to reduce pauses

    import json
    from dotenv import load_dotenv
    import openai
    import os
    import random
    import requests
    import math

    load_dotenv(".env")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open(config.basedir + "/game/prompt_templates.json", "r") as f:
        prompt = json.load(f)


    class ManageChat_Folders:
        def __init__(self):
            self.chat_path = "chats/"
            self.full_path = ""
            self.msg_history = "chat_history.json"
            self.saved_actions = "saved_actions.json"
            self.saved_data = {
                                "Scene": "club.png",
                                "Proceed": "First",
                                "head_sprite": "smile.png",
                                "leftside_sprite": "1l.png",
                                "rightside_sprite": "1r.png",
                                "zone": "None"
                            }
            self.chat_history = []
            

        
        def create_folder(self, name):
            """Creates specific folder in `chats` to store all
            realms.
            """
            path = self.chat_path+name

            i = 1
            while True:
                self.full_path = f"{config.basedir}/{path}_{i}"
                if not os.path.exists(self.full_path):
                    os.makedirs(self.full_path, mode=0o777)
                    break
                else:
                    i += 1
            
            return self.full_path


        def create_chat_history(self):
            """.json for logging chat history with monika & user"""
            try:
                with open(self.full_path+"/"+self.msg_history, "r") as f:
                    chat_history = json.load(f)

                self.chat_history = chat_history
                return chat_history
            except FileNotFoundError:
                with open(self.full_path+"/"+self.msg_history, "w") as f:
                    chat_history = []
                    json.dump(chat_history, f, indent=2)

                self.chat_history = chat_history
                return chat_history


        def create_world_history(self):
            """A .json for saving specific scenes such as:

            background, sprite, music and cinematic"""
            try:
                with open(self.full_path+"/"+self.saved_actions, "r") as f:
                    saved_data = json.load(f)

                self.saved_data = saved_data
                return saved_data
            except FileNotFoundError:
                with open(self.full_path+"/"+self.saved_actions, "w") as f:
                    saved_data = json.dump(self.saved_data, f, indent=2)

                self.saved_data = saved_data
                return saved_data








    class CheckData(ManageChat_Folders):
        def __init__(self, full_path):
            super().__init__()
            self.full_path = full_path
            self.ddlc_mode = {'justMonika': [0, 1], 'monikaZone': [2, 3]}

        def historyCheck(self, gamemode, chatmode):
            """
            Checks if chat_history is an empty list. If it is,
            it is overwrited with a prompt template

            Just Monika:
            0 is freechat
            1 is story mode

            ----

            Monika Zone:
            2 is freechat
            3 is story mode
            """
            try:
                self.chat_history[0]
            except IndexError:
                for m in self.ddlc_mode:
                    if m == gamemode:
                        with open(self.full_path+self.msg_history, "w") as f:
                            json.dump(prompt[self.ddlc_mode[m][chatmode]], f, indent=2)

                        with open(self.full_path+self.msg_history, "r") as f:
                            chat_history = json.load(f)
                        self.chat_history = chat_history
                        return chat_history
                            


        def usernameCheck(self):
            """
            Checks if the player has a registered username.
            If they do then it rewrites the first index of chat_history
            (aka the prompt template) to include it.

            This will make Monika address you by your name if
            necessary
            """
            if persistent.playerName != None:
                try:
                    prompt_name = self.chat_history[0]["content"].replace("<name>", persistent.playerName)
                    self.chat_history[0]["content"] = prompt_name

                    with open(self.full_path+self.msg_history, "w") as f:
                        json.dump(self.chat_history, f, indent=2)
                except IndexError:
                    return "File Currently Doesn't Exist"
                return prompt_name
            return "Username is not defined"


    #TODO if the head_sprite returns a fullbody then the sides should be neutral

    class Convo(CheckData):
        def __init__(self, chat_history, full_path):
            super().__init__(full_path)
            self.full_path = full_path
            self.chat_history = chat_history
            self.head_sprite_dict = {'angry': 'monika serious.webp',
                            'annoyed': 'annoyed.png',
                            'blushing': 'monika blushing.png',
                            'concerned': 'curious.png',
                            'crying': 'cry.png',
                            'curious': 'curious.png',
                            'embarrassed': 'embarrassed.png',
                            'flabbergasted': 'monika flabbergasted.png',
                            'flirty': 'high.png',
                            'glad': 'glad.png',
                            'happy': 'smile.png',
                            'horny': 'monika horny.png',
                            'horrified': 'monika horrifiedYelling.png',
                            'nervous': 'nervous.png',
                            'playful frown': 'monika playfulFrown.webp', 
                            'playful smile': 'monika playfulSmile.webp', 
                            'really happy': 'smileOpenMouth.png', 
                            'resolve': 'annoyed_speaking.png', 
                            'sad': 'sad.webp', 
                            'scared': 'monika scared.png', 
                            'serious': 'monika serious.webp', 
                            'shocked': 'monika shocked.png', 
                            'worried': 'worried.png'
                            }
            self.leftside_sprite_dict = {'explain': '2l.png',
                            'relaxed': '1l.png',
                            'none': 'mtea.png',
                            }
            self.rightside_sprite_dict = {'explain': '2r.png',
                            'relaxed': '1r.png',
                            'none': 'mtea.png',
                            }
            self.bg_scenes = {"bedroom": "bedroom.png", "club": "club.png", "class": "class.png",
            "coffee shop": "coffee.jpg", "hallway": "hallway.png", "kitchen": "kitchen.png",
            "mc house": "house.png", "user house": "house.png", "user's house": "house.png", "house": "house.png",
            "sidewalk": "sidewalk.png"}
            self.context_words = [
                "[SCENE] club", "[SCENE] hallway", "[SCENE] coffee shop", "(done)", "(continue)",
                "[CONTENT]", "[MUSIC]", "[NARRATION]"
            ]
            self.NARRATION = False
            self.options = []
            self.proceed = self.saved_data["Proceed"]
            self.scene = self.saved_data["Scene"]
            self.head_sprite = self.saved_data["head_sprite"]
            self.leftside_sprite = self.saved_data["leftside_sprite"]
            self.rightside_sprite = self.saved_data["rightside_sprite"]
            self.zone = self.saved_data["zone"]




        def append_to_chat_history(self, role, msg):
            """Stores updated history of ai and user"""
            self.chat_history.append({"role": role, "content": msg})
            with open(self.full_path+self.msg_history, "w") as f:
                json.dump(self.chat_history, f, indent=2)

        def update_in_saved_actions(self, data, action):
            """Stores mood, visible chars, music in the current scene"""
            self.saved_data[data] = action
            with open(self.full_path+self.saved_actions, "w") as f:
                json.dump(self.saved_data, f, indent=2)


        def control_mood(self, mood):
            """Display different facial expressions"""
            emotions = ["angry", "blushing", "flabbergasted", "horrified",
                    "playful frown", "playful smile", "scared", "shocked", "serious",
                    "crying"]
            for h in self.head_sprite_dict:
                if "[MOOD] "+h in mood:
                    self.update_in_saved_actions("head_sprite", self.head_sprite_dict[h])
                    self.head_sprite = self.head_sprite_dict[h]

                    if h in emotions:

                        self.update_in_saved_actions("leftside_sprite", self.leftside_sprite_dict["none"])
                        self.leftside_sprite = self.leftside_sprite_dict["none"]

                        self.update_in_saved_actions("rightside_sprite", self.rightside_sprite_dict["none"])
                        self.rightside_sprite = self.rightside_sprite_dict["none"]

                        return
                elif self.head_sprite in emotions:
                    self.update_in_saved_actions("leftside_sprite", self.leftside_sprite_dict["none"])
                    self.leftside_sprite = self.leftside_sprite_dict["none"]

                    self.update_in_saved_actions("rightside_sprite", self.rightside_sprite_dict["none"])
                    self.rightside_sprite = self.rightside_sprite_dict["none"]
                    


            for l in self.leftside_sprite_dict:
                if "[BODY] "+l in mood:
                    self.update_in_saved_actions("leftside_sprite", self.leftside_sprite_dict[l])
                    self.leftside_sprite = self.leftside_sprite_dict[l]

            for rr in self.rightside_sprite_dict:
                if "[BODY] "+rr in mood:
                    self.update_in_saved_actions("rightside_sprite", self.rightside_sprite_dict[rr])
                    self.rightside_sprite = self.rightside_sprite_dict[rr]


        def control_scene(self, scene):
            """Display different scenes"""
            for s in self.bg_scenes:
                if f"[SCENE] {s}" in scene:
                    self.update_in_saved_actions("Scene", self.bg_scenes[s])
                    self.scene = self.bg_scenes[s]
                    return self.saved_data["Scene"]

        def control_proceed(self, mode):
            """Determines if the user can respond to the AI at this moment"""
            self.update_in_saved_actions("Proceed", mode)
            self.proceed = mode
            return self.saved_data["Proceed"]




        def remove_context_words(self, reply):
            """Get rid of keywords and return a clean string"""
            if "[CINEMATIC]" not in reply and "[NARRATION]" not in reply and "[CONTENT]" not in reply:
                self.update_in_saved_actions("zone", "True")
                self.zone = "True"
            elif "[MOOD] crying" in reply:
                self.update_in_saved_actions("zone", "Zone")
                self.zone = "Zone"

            if "[NARRATION]" in reply:
                if "(done)" in reply:
                    self.control_proceed("True") # User can now respond to AI
                    self.NARRATION = True
                else:
                    self.control_proceed("False") # Narrator is still speaking
                    self.NARRATION = True

            else:
                self.NARRATION = False

            if "[OPTION 1]" in reply and reply != "[OPTION] None":
                self.options = []
                options = reply.split("\"")
                self.options.append(options[1])
                self.options.append(options[3])
                self.options.append(options[5])
            else:
                self.options = []
            
            reply = reply.split("[BODY]")
            reply = reply[0].split("[MOOD]")[0]
            for ctx in self.context_words:
                reply = reply.replace(ctx, "")

            for ops in self.options:
                reply = ' '.join([word for word in reply.split(ops) if ops not in word])
            reply = reply.replace("[OPTION 1]", "").replace("[OPTION 2]", "").replace("[OPTION 3]", "").replace("\"", "")

            return reply


        def monika_speaks(self, reply):
            """Convert Monika's text into vocals"""
            url = "https://app.coqui.ai/api/v2/samples/from-prompt/"
            payload = {
                "prompt": "An 18 year old girl with a sweet voice",
                "emotion": "Neutral",
                "speed": 1,
                "text": reply
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Bearer oD3znDrz0gNNSKraFBBnnqUtnexoLyFlgRwUGk7zYfs3o32F72u2uCu4uPwU3tZF"
            }

            response = requests.post(url, json=payload, headers=headers)
            response_data = json.loads(response.text)

            with open(config.basedir +"/game/audio/vocals/aud.json", "w") as f:
                json.dump(response_data, f, indent=2)
            with open(config.basedir +"/game/audio/vocals/aud.json", "r") as f:
                aud = json.load(f)

            url = aud["audio_url"]
            response = requests.get(url)

            with open(config.basedir +"/game/audio/vocals/monika.wav", "wb") as f:
                f.write(response.content)
            return True



        def ai_response(self, msg, role="user"):
            """Gets ai generated text based off given prompt"""
            # Log user input
            self.append_to_chat_history(role, msg)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=self.chat_history,
                temperature=0.6
                )
            
            ai_reply = response.choices[0].message.content
            # Log AI input
            self.append_to_chat_history('assistant', ai_reply)

            self.control_mood(ai_reply)
            self.control_scene(ai_reply)
            final_res = self.remove_context_words(ai_reply)
            if self.NARRATION != True:
                self.monika_speaks(final_res)
            return final_res








    #  Copied & Pasted Class from Official Doki Doki game (I am not a psychopath)
    class ParticleBurst:
        """Animates the particles in the main menu when the user first
        launches the game
        """
        def __init__(self, theDisplayable, explodeTime=0, numParticles=20, particleTime = 0.500, particleXSpeed = 3, particleYSpeed = 5):
            self.sm = SpriteManager(update=self.update)
            
            self.stars = [ ]
            self.displayable = theDisplayable
            self.explodeTime = explodeTime
            self.numParticles = numParticles
            self.particleTime = particleTime
            self.particleXSpeed = particleXSpeed
            self.particleYSpeed = particleYSpeed
            self.gravity = 240
            self.timePassed = 0
            
            for i in range(self.numParticles):
                self.add(self.displayable, 1)
        
        def add(self, d, speed):
            s = self.sm.create(d)
            speed = random.random()
            angle = random.random() * 3.14159 * 2
            xSpeed = speed * math.cos(angle) * self.particleXSpeed
            ySpeed = speed * math.sin(angle) * self.particleYSpeed - 1
            s.x = xSpeed * 24
            s.y = ySpeed * 24
            pTime = self.particleTime
            self.stars.append((s, ySpeed, xSpeed, pTime))
        
        def update(self, st):
            sindex=0
            for s, ySpeed, xSpeed, particleTime in self.stars:
                if (st < particleTime):
                    s.x = xSpeed * 120 * (st + .20)
                    s.y = (ySpeed * 120 * (st + .20) + (self.gravity * st * st))
                else:
                    s.destroy()
                    self.stars.pop(sindex)
                sindex += 1
            return 0

    #  Copied & Pasted Class from Official Doki Doki game
    class AnimatedMask(renpy.Displayable):
        
        def __init__(self, child, mask, maskb, oc, op, moving=True, speed=1.0, frequency=1.0, amount=0.5, **properties):
            super(AnimatedMask, self).__init__(**properties)
            
            self.child = renpy.displayable(child)
            self.mask = renpy.displayable(mask)
            self.maskb = renpy.displayable(maskb)
            self.oc = oc
            self.op = op
            self.null = None
            self.size = None
            self.moving = moving
            self.speed = speed
            self.amount = amount
            self.frequency = frequency
        
        def render(self, width, height, st, at):
            
            cr = renpy.render(self.child, width, height, st, at)
            mr = renpy.render(self.mask, width, height, st, at)
            mb = renpy.Render(width, height)
            
            
            if self.moving:
                mb.place(self.mask, ((-st * 50) % (width * 2)) - (width * 2), 0)
                mb.place(self.maskb, -width / 2, 0)
            else:
                mb.place(self.mask, 0, 0)
                mb.place(self.maskb, 0, 0)
            
            
            
            cw, ch = cr.get_size()
            mw, mh = mr.get_size()
            
            w = min(cw, mw)
            h = min(ch, mh)
            size = (w, h)
            
            if self.size != size:
                self.null = Null(w, h)
            
            nr = renpy.render(self.null, width, height, st, at)
            
            rv = renpy.Render(w, h)
            
            rv.operation = renpy.display.render.IMAGEDISSOLVE
            rv.operation_alpha = 1.0
            rv.operation_complete = self.oc + math.pow(math.sin(st * self.speed / 8), 64 * self.frequency) * self.amount
            rv.operation_parameter = self.op
            
            rv.blit(mb, (0, 0), focus=False, main=False)
            rv.blit(nr, (0, 0), focus=False, main=False)
            rv.blit(cr, (0, 0))
            
            renpy.redraw(self, 0)
            return rv

    def monika_alpha(trans, st, at):
        trans.alpha = math.pow(math.sin(st / 8), 64) * 1.4
        return 0
    