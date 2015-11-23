# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

init python:
    import random

    class Question:
        def __init__(self,desc,choices,answer):
            self.description = desc
            self.choices = choices
            self.answer = choices[answer]

        def get_description(self):
            return self.description

        def get_choices(self):
            random.shuffle(self.choices)
            return self.choices

        def get_menu_choices(self):
            menu_list = []
            choice_list = self.get_choices()
            for choices in choice_list:
                if choices == self.answer:
                    t = (choices,True)
                else:
                    t = (choices,False)
                menu_list.append(t)

            return menu_list

        def check_answer(answer):
            return answer == self.answer

    class QuestionManager:
        def __init__(self):
            self.question_list = []
        def get_random_question(self):
            return self.question_list[renpy.random.randint(0,len(self.question_list)-1)]
        def add_question(self,desc,choices,answer):
            question = Question(desc,choices,answer)
            self.question_list.append(question)


    class Stats:
        def __init__(self):
            self.stats = {
                "str":0,
                "int":0,
                "cha":0
            }
            self.days = 0

            self.classes = {"Biology":"biology",
                            "Drama":"drama",
                            "Gym":"gym"}

            self.picked_classes = []
            self.max_classes = 2
            self.food_choice = 0
            self.chosen_girl = 0
            
        def add_stats(self,stat,amount):
            self.stats[stat]
            if stat in self.stats:
                self.stats[stat] += amount
            else:
                self.stats[stat] = 0

        def get_stats(self,stat):
            if stat in self.stats:
                return self.stats[stat]
            else:
                return None
    
        def get_days(self):
            return self.days
            
        def increment_days(self):
            self.days += 1

        def pick_classes(self,class_type):
            self.picked_classes.append(class_type)

        def reset_classes(self):
            self.picked_classes = []

        def get_available_classes(self):
            choices = []
            for class_type,class_desc in self.classes.items():
                if not(class_type in self.picked_classes):
                    choices.append((class_type,class_desc))
            return choices

        def get_picked_classes(self):
            return self.picked_classes
            
        def get_food_choice(self):
            return self.food_choice
        
        def set_food_choice(self, value):
            self.food_choice = value
        
        def get_chosen_girl(self):
            return self.chosen_girl
            
        def set_chosen_girl(self, girl):
            self.chosen_girl = girl
               
    class Girl:
        def __init__(self, name):
            self.name = name
            self.character = Character(name)
            self.closeness = 3
            self.affection = 0
            self.event = 0

        def add_closeness(self,amount):
            self.closeness += amount
            
        def get_closeness(self,name):
            return self.closeness
            
        def add_affection(self,amount):
            self.affection += amount
            
        def get_affection(self,name):
            return self.affection
            
        def set_name(self,name):
            self.name = name
            
        def get_event(self,name):
            return self.event
            
        def add_event(self):
            self.event += 1
            
    def rng_roll(chance): #chance should be between [0,1]
        return chance > renpy.random.random()


# Declare characters used by this game.
image bg placeholderbg = "background.png"

define p = DynamicCharacter("unknown_name", color="#c8ffc8")
define m = DynamicCharacter("player_name")
define principal = Character("Principal", color="#c8ffc8")

define mom = Character("Mom", color="#c8ffc8")

#Cafe date variables~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
define cafe_asked_count = 0
define cafe_boyfriend = False #variable for recording whether or not player has asked about a boyfriend yet.
define cafe_before= False #record whether you have asked her if she's been here before
define cafe_asked1 = False    
#Restaurant date variables~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
define rest1_asked2 = False
define rest1_asked3 = False
define rest2_asked1 = False

#Music girl variables~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
define girl2_event1_asked1 = False

# The game starts here.
# Initialize stuff here and shove all the tutorial intro stuff here as well.
label start:
    $ bio_qman = QuestionManager()
    $ gym_qman = QuestionManager()
    $ drama_qman = QuestionManager()

    $ bio_qman.add_question("description",["wrong1","wrong2","wrong3","correct"],3)
    $ gym_qman.add_question("description",["wrong1","wrong2","wrong3","correct"],3)
    $ drama_qman.add_question("description",["wrong1","wrong2","wrong3","correct"],3)


    $ player_name = renpy.input("Can I get you to repeat your name please?")
    $ stats = Stats()
    $ girl1 = Girl("Mary")
    $ girl2 = Girl("Catherine")
    $ unknown_name = "???"

    m "My name is %(player_name)s!"
    
    #show placeholder normal at left
    #with moveinbottom
    jump intro

    return

label intro:
    
    principal "Welcome to <insert school name here>. This school consists of the brightest students from all over the city, so congratulations for making it! In order to foster independence and individual growth in each of our students, we’re extremely flexible in what classes you attend. So you’ll be able to choose which class to show up to and what area of study you wish to upgrade in a sense. But be choose wisely. Once you set your classes today, it’ll be permanent for the rest of the year. 
If you’re ready, I can take you on a tour of the school and some of the club rooms. Do you want me to repeat anything?"
    
    menu: 
    
        "I think I'm good.":
            principal "Please follow me, %(player_name)s."
            jump school_tour
        "Can you go over how this works again?":
            jump intro
    
label school_tour:
    
    #show image of economics room
    principal "This is the home economics room. Students come here to learn essential life skills like cooking. Keep in mind that the most sophisticated dishes require an amount of stamina and some creative style."
    
    #show image of girl cooking
    #fade out
    
    #show image of music room
    principal "This is the music room. If you ever want to develop your musical capabilities, then this  the perfect spot to practice! Keep in mind that music is an expression of your personality, but also requires a lot of thought process."
    
    #show tsundere playin piano
    #fade out
 
    #go to general image, office or something
    principal "Well those are just examples of the many facilities this school provides. Make use of your time and be sure to work hard on your academics. Remember that although this is an elite school and your studies are very important, your social life and extra curriculars are crucial in a healthy high school experience too. Good luck on your first day!"
    
    $ stats.reset_classes()
    jump make_schedule

label make_schedule:
    
    if len(stats.get_picked_classes()) == 0:
        "It looks like I have to choose 2 classes to attend."
    $choices = stats.get_available_classes()
    $result = renpy.display_menu(choices)

    call expression result

    if len(stats.picked_classes) < stats.max_classes:
        jump make_schedule
    else:
        $ day = stats.get_days()
        if day == 0: # end the day
            jump end_day_0
        elif day == 1:
            jump extracurricular
        else: 
            return
                    
label end_day_0:
    
    "Phew... That was a long day, I'll head home for today..."
    $ stats.increment_days()
    
    #fade to show end of day 
    
    
    "Time to go to class..."
    $ stats.reset_classes()
    jump make_schedule
    
label gym:
    $ stats.pick_classes("Gym")
    $ question = gym_qman.get_random_question()
    $ desc = question.get_description()
    "Question: %(desc)s"
    $ choices = question.get_menu_choices()
    $ result = renpy.display_menu(choices)
    if result == True:
        $ stats.add_stats("str", 1)
        "Stat raised"
    else:
        "No Stats raised"
    if len(stats.get_picked_classes()) < stats.max_classes:
        "Guess I'll choose Gym for one choice, I still need to pick another."
    return
    
label drama:
    $ stats.pick_classes("Drama")
    $ question = drama_qman.get_random_question()
    $ desc = question.get_description()
    "Question: %(desc)s"
    $ choices = question.get_menu_choices()
    $ result = renpy.display_menu(choices)
    if result == True:
        $ stats.add_stats("str", 1)
        "Stat raised"
    else:
        "No Stats raised"
    $ stats.add_stats("cha", 1)
    if len(stats.get_picked_classes()) < stats.max_classes:
        "Guess I'll choose Drama for one choice, I still need to pick another."
    return 
    
label biology:
    $ stats.pick_classes("Biology")
    $ question = bio_qman.get_random_question()
    $ desc = question.get_description()
    "Question: %(desc)s"
    $ choices = question.get_menu_choices()
    $ result = renpy.display_menu(choices)
    if result == True:
        $ stats.add_stats("str", 1)
        "Stat raised"
    else:
        "No Stats raised"
    $ stats.add_stats("int", 1)
    if len(stats.get_picked_classes()) < stats.max_classes:
        "Guess I'll choose Biology for one choice, I still need to pick another."
    return

label extracurricular:
    "So this is what an elite school is like? Classes seem ridiculously hard. Maybe I should check out those extracurriculars the principal mentioned."
    $ chosen_girl = stats.get_chosen_girl()
    
    if chosen_girl == 0:
        menu:
            "Home Economics Room":
                jump home_ec_room
            "Music Room":
                "I heard there was a music room. I should go check it out."
                jump music_room 
    
    elif chosen_girl == 1: # Mary is chosen
        
        jump home_ec_day_2
        
    elif chosen_girl == 2: # music girl chosen
        
        jump music_day_2

label music_room:
    
    "> As you get closer to the music room, you notice the door cracked open an inch. As you approach, you hear sustained instrument that cuts through the opening."
    # fade to show entering room
    "> Upon entering, you find a girl drawing her bow flawlessly across the strings. She faces the opposite direction, displaying her hair that follows the dynamics of her playing. You’re compelled to sit down at the piano bench, as your eyes and ears perked up to witness her welcoming and mellow style."
    "> The song grows in depth, as the notes create an atmosphere, sustained in emotion. Her upper body sways intimately with the music, while the hair on the back of your neck rise gradually. you find yourself enveloped by her music."
    
    "Wow… she’s pretty amazing, I need to know this girl’s name."
    "> Her playing approaches the end. You feel anxiety rising up as you stand to attempt talking to her."
    "Now’s my chance to talk to her!"
    
    m "Hey, I just heard you playing and you were pretty awesome!"
    "> She looks back to be slightly surprised, not knowing you were there. Her expression instantly reads 'who the hell are you?'"
    p "I thought I closed the door, how did you get in?"
    m "Oh no, it was opened. Sorry I didn’t know know you wanted to be alone."
    p "I’m practicing, so if you don’t mind, I have a concert to prepare for."
    "> Immediately she gets back to playing, but this time. Her playing loses its warmth, and immediately has an air of superiority."
    
    m "I never caught your name, by the way."
    "> The violin lets out a shriek, and she turns to you in frustration."
    p "Did you not hear me earlier?"
    m "I did, but I don't want to."
    "> Looking frustrated and agitated, she clenches the neck of the violin and stick."
    p "Ugh! Who do you think you are anyways!?"
    m "I’m %(player_name)s. Your playing was pretty inspiring to listen to. What’s your name?"
    "> She holds a frown."
    p "Catherine… I suppose it’s not a HUGE inconvenience if you listen, just try to keep quiet, and don’t do anything to distract me or I am going to kick you out."
    $ unknown_name = "Catherine"
    "This girl’s scary."
    "> She moves to her music stand again raising her bow into position. This time she continues to play, but still not as welcoming and warm as the first time."
    "> You start to get into the music, leaning back while tapping your feet."
    "> Noticing the dust on your elbows after sitting back, you notice the piano."
    "Oh man, this piano’s pretty dusty. I also haven’t touched one of these in a couple years. Now let’s see what we have here…"
    "> You lift the key covering."
    
    $ int_check = stats.get_stats("int")
    menu:
        "Play with her":
            jump play_with_her
        
        "Just sit and listen to her play the violin":
            "> You stay seated and simply listen to her playing."
            menu:
                "Play with her":
                    jump play_with_her
                
                "Attempt to talk to Catherine as shes playing":
                    m "How did you get into playing violin?"
                    "> She plays louder and more aggressively."
                    $ girl2.add_closeness(-1)
                    menu:
                        "Play with her":
                            jump play_with_her
                            
        "Attempt to talk to Catherine as shes playing":
            m "How did you get into playing violin?"
            "> She plays louder and more aggressively."
            $ girl2.add_closeness(-1)
            
            menu: 
                "Play with her":
                    jump play_with_her
                
                "Just sit and listen to her play the violin":
                    "> You stay seated and simply listen to her playing."
                    menu:
                        "Play with her":
                            jump play_with_her         
   
label play_with_her:
    if int_check >= 1:
            $ girl2.add_closeness(1)
            "> You pick up where there’s an opening, and accompany her. The first few moments feel sluggish and your hands feel clumsy, but after a few bars you’re able to familiarize yourself. You peek over your shoulder to notice that Catherine’s posture is rigid; she doesn’t seem like she’s used to someone playing with her. Her playing begins to become harsher and her facial expression suddenly becomes unimpressed."
            "Hmm…She hasn’t stopped playing yet... I’ll just keep going to see where this takes me."
            "> You listen to her carefully and do your best to follow her, trying to avoid taking over or not supporting her enough. You remember the feeling from before: the chill in your spine, hair upright, and heightened senses."
            "> You can’t see her now, but you’d like to imagine she also is feeling the same way you do."
            "> You listen carefully, and end the song."
            "I think my finish was coordinated with her pretty well. Granted not perfect, but pretty good I think."
            p "That was terrible."
            "> Catherine crosses her arms again and turns her back on you with a puff of air."
            p "But..not bad for an impromptu."
            "> You can’t see the expression on her face but her response makes you smile."
            
            menu:
                "Lightly joke":
                    m "You’re amazing at the violin. But yeah, thanks, Cathy!"
                    $ girl2.add_closeness(-1)
                    p "That’s not my name, I hate being called Cathy."
                    m "I’m sorry. It’s nice to meet you Catherine!"
                "Be humble":
                    m "Thanks Catherine, but I’m still pretty rusty. I haven’t played since junior high. Your playing earlier inspired me!"
                    "> Catherine looks flustered but trying keep an exaggerated mature composure" # guess image here instead of description
                    p "..."
                    p "Of course! I’m training to be the best you know. It’s nice to meet you too I guess."
            
            m "Well, I think i might take another shot at playing the piano."
            p "What!? what do you mean?"
            m "I’ll be around the music room more often, I like listening to you play and the way you played the violin has inspired me to get back into playing the piano."
            p "Who said you could be in here?"
            m "Would you be opposed? I need to practice a little more, and you could tell me how I’m doing."
            p "I don’t have time to deal with an amateur like you. Ugh....but I guess it’s sort of useful having an accompanist. JUST FOR PRACTICE. Come by tomorrow, don’t be late or else I’ll kick you out."  
            
            # end day
        
        else:
            "> You try to think of what to play, but the keys starts to look more and more like a puzzle. You play the keys but it just makes a loud obstruction to The girl’s music."
            "> She stops midway, pointing the violin bow at you."
            p "What did I just say? Why are you even touching the piano, if you don’t have the capacity to play it?"
            "Oh crap."
            m "W-well I haven’t played since junior high, so I’m rusty, I mean just a little rusty or maybe a lot depending on who’s judging that is. I’m usually better I just need to brush up. Actually, I think I might take another shot at playing the piano if you’ll give me a chance."
            p "What? what do you mean?"
            m "I want to be around the music room more often, I like listening to you play and the way you played the violin has inspired me to get back into playing the piano."
            p "You’re terrible. Why should I even give you another chance."
            "> Catherine's eyes look hard and unforgiving."
            m "Please give me another chance! I won’t disappoint you. I’ll leave you alone if I do not meet your standards next time!"
            "> Catherine’s eyes suddenly soften but turns cold again so fast that you’re not sure if you were seeing right."
            p "I..Fine. I’ll give you a shot. Be here tomorrow and don’t be late, or else."
            "> She turns her back to you again. You’re not sure what else to say and you take this as your cue to leave. You get up and just about as you exit the room, you hear Catherine say something else."
            p "If you’re really serious about this, you don’t want to waste your chance or you’ll regret it. Believe me."
            "> She immediately lifts her bow again and starts up playing again, ignoring you. You leave."
    
    # show image of bedroom at night?
    m "That was a long day, time to hit the sack."
    $ stats.increment_days()
        
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump music_day_2
        
label music_event_check_1:
    # music room option
    $ closeness = girl2.get_closeness("Catherine")
    $ day = stats.get_days()
    $ event_num = girl2.get_event("Catherine")
    
    if day < 5 and closeness > -3 and closeness < 5:
        # continue on with music
        return
    elif day >= 5:
        # too long trigger failure event
        jump girl2_failure
    elif closeness <= -3:
        # lost too much closeness
        jump girl2_failure
    elif day < 5 and closeness >= 5 and event_num == 0:
        # trigger event 1 as day < 5 and closess > 5
        # set the event value to 1
        $ girl2.add_event()
        jump music_event_1
    
label music_event_check_2:
    
    $ closeness = girl2.get_closeness("Catherine")
    $ event_num = girl2.get_event("Catherine")
    if closeness >= 8 and event_num == 1:
        $ girl2.add_event()
        jump music_event_2
    else:
        return
    
label music_day_2:
    # should not go to events yet for now
    #call music_event_check_1
    #call music_event_check_2
    #call music_event_check_3
    
    "> You enter the music room to see Catherine already practicing on her violin"
    p "Hey, you actually came. I hope you are prepared."
    m "I think so! I practiced all of last night!"
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")
    
    menu:
        "Classical (no reqs)":
            "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
            p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
            $ girl2.add_closeness(1)
            
        "Rock (Strength 2, Charm 2)":
            p "Rock today? okay I’ll give it a try."
            if str_check >= 2 and cha_check >=2:
                "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
                p "That went better than I thought." # she coughs
                p "I meant for you obviously, I knew that I would be great. That was interesting though. Maybe we should experiment like this more."
                $ girl2.add_closeness(2)
            else:
                "> As you begin to play for the first few bars, you are able to stay on beat with Catherine, However, as the song intensifies, you stress out and begin to play fast and louder. The sounds created by piano overpowers the violin and there is dissonance in the music being played. Despite this, Catherine and  you imagine to finish the piece."
                p "That was terrible. The piano is suppose to accompany the violin not the other way around... But I guess this is a huge improvement from yesterday. I guess I will let you continue coming to the music room because you are dedicated to improve and you kind of have potential.."
                $ girl2.add_closeness(-2)
        
        "Jazz (Charm 2, Intelligence 2)":
            p "OH! I LOVE JAZZ!"
            if cha_check >= 2 and int_check >= 2:
                "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
                p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
                $ girl2.add_closeness(2)
            else:
                "> As you begin to play for the first few bars, you are able to stay on beat with Catherine, However, as the song intensifies, you stress out and begin to play fast and louder. The sounds created by piano overpowers the violin and there is dissonance in the music being played. Despite this, Catherine and  you imagine to finish the piece."
                p "That was terrible. The piano is suppose to accompany the violin not the other way around... But I guess this is a huge improvement from yesterday. I guess I will let you continue coming to the music room because you are dedicated to improve and you kind of have potential.."
                $ girl2.add_closeness(-2)
                
    m "That was a long day, time to hit the sack."
    $ stats.increment_days()
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump music_day_3

label music_day_3:
    # check for events
    if girl2_event1_asked1 = False:
        call music_event_check_1
        call music_event_check_2
    girl2_event1_asked1 = False
    "> You enter the music room to see Catherine already practicing on her violin"
    p "Hey, you actually came. I hope you are prepared."
    m "I think so! I practiced all of last night!"
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")
    
    menu:
        "Classical (no reqs)":
            "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
            p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
            $ girl2.add_closeness(1)
            
        "Folk (Strength 2, Charm 3)":
            p "Really? Okay, I’m not very used to folk, but if you want."
            if str_check >= 2 and cha_check >=3:
                "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
                p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
                $ girl2.add_closeness(2)
            else:
                "> As you begin to play for the first few bars, you are able to stay on beat with Catherine, However, as the song intensifies, you stress out and begin to play fast and louder. The sounds created by piano overpowers the violin and there is dissonance in the music being played. Despite this, Catherine and  you imagine to finish the piece."
                p "That was terrible. The piano is suppose to accompany the violin not the other way around... But I guess this is a huge improvement from yesterday. I guess I will let you continue coming to the music room because you are dedicated to improve and you kind of have potential.."
                $ girl2.add_closeness(-2)
        
        "Blues (Charm 2, Intelligence 3)":
            p "Alright, if you want."
            if cha_check >= 2 and int_check >= 3:
                "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
                p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
                $ girl2.add_closeness(2)
            else:
                "> As you begin to play for the first few bars, you are able to stay on beat with Catherine, However, as the song intensifies, you stress out and begin to play fast and louder. The sounds created by piano overpowers the violin and there is dissonance in the music being played. Despite this, Catherine and  you imagine to finish the piece."
                p "That was terrible. The piano is suppose to accompany the violin not the other way around... But I guess this is a huge improvement from yesterday. I guess I will let you continue coming to the music room because you are dedicated to improve and you kind of have potential.."
                $ girl2.add_closeness(-2)
                
    m "That was a long day, time to hit the sack."
    $ stats.increment_days()
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump music_day_4
    
label music_day_4:
    # check for events, day is 4 here
    if girl2_event1_asked1 = False:
        call music_event_check_1
        call music_event_check_2
    girl2_event1_asked1 = False # reset it now that checks are done
    
    "> You enter the music room to see Catherine already practicing on her violin"
    p "Hey, you actually came. I hope you are prepared."
    m "I think so! I practiced all of last night!"
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")
    
    menu:
        "Classical (no reqs)":
            "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
            p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
            $ girl2.add_closeness(1)
            
        "Latin (Strength 3, Charm 4)":
            p "Very very interesting. I don’t know how to start… ummm… here goes nothing."
            if str_check >= 3 and cha_check >=4:
                "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
                p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
                $ girl2.add_closeness(2)
            else:
                "> As you begin to play for the first few bars, you are able to stay on beat with Catherine, However, as the song intensifies, you stress out and begin to play fast and louder. The sounds created by piano overpowers the violin and there is dissonance in the music being played. Despite this, Catherine and  you imagine to finish the piece."
                p "That was terrible. The piano is suppose to accompany the violin not the other way around... But I guess this is a huge improvement from yesterday. I guess I will let you continue coming to the music room because you are dedicated to improve and you kind of have potential.."
                $ girl2.add_closeness(-2)
        
        "J-pop (Charm 3, Intelligence 4)":
            p "Oh great! I have this song from a dating sim game I wanted to play!"
            if cha_check >= 3 and int_check >= 4:
                "> It is like Catherine and you have performed before. You accidently play the wrong keys here and there, but you are able to stay on beat and made sure that the piano does not overpower the violin."
                p "Wow. I am impressed. Even though there were some errors, that was a huge improvement from yesterday. You have redeemed yourself. You are free to come back anytime you want and I don't mind playing with you again… It was kind of fun."
                $ girl2.add_closeness(2)
            else:
                "> As you begin to play for the first few bars, you are able to stay on beat with Catherine, However, as the song intensifies, you stress out and begin to play fast and louder. The sounds created by piano overpowers the violin and there is dissonance in the music being played. Despite this, Catherine and  you imagine to finish the piece."
                p "That was terrible. The piano is suppose to accompany the violin not the other way around... But I guess this is a huge improvement from yesterday. I guess I will let you continue coming to the music room because you are dedicated to improve and you kind of have potential.."
                $ girl2.add_closeness(-2)
                
    m "That was a long day, time to hit the sack."
    $ stats.increment_days()
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump girl2_failure

label girl2_failure:
    
    "GAME OVER"
    return
    
label music_event_1:
    # triggered from closeness
    $ day = stats.get_days()
    "> You enter the music room quietly; you see Catherine on the floor curled up in a kneeling position. Sprawled around her are vibrantly coloured posters and unopened markers."
    menu:
        "Hey Catherine… should I come by another time? You look busy right now..":
            p "I am busy at the moment. Leave me alone."
            $ girl2.add_affection(-1)
            "> You decide to leave her alone"
            $ girl2_event1_asked1 = True 
            if day == 3:
                jump music_day_3
            elif day == 4:
                jump music_day_4
            
        "Don't say anything yet":
            "> You decide to watch her and see what she’s doing. You notice her tugging on her hair occasionally and letting out fits of frustration"
            "> ring ring ring"
            p "sigh..."
            p "Hi Mom."
            p "… I’m at school still making posters for the concert."
            p "… No, I don’t think I’ll be home in time for dinner."
            p "… I know, I still need to practice, don’t worry I’ll be fine."
            "> Catherine’s tone sounds a little frustrated at this point"
            p "… Don’t worry about it-- I said I’ll be fine!"
            p "… I’m sorry for lashing out, I am just frustrated right now."
            p "… You too, bye..."
            "I wonder why she sounded so angry at the end of her conversation."
            "> You walk nearer to her without her noticing and upon closer inspection, notice that she’s making posters for some sort of concert"
            m "Hey Catherine, what are all these for? Do you need help with something?"
            p "Oh! Hi %(player_name)s."
            "> She seems embarrassed that you’re seeing her like this"
            p "I’m trying to make posters for this concert; I need to promote it. No need for help, I’m perfectly capable of doing this myself."
            m "Of course, of course! If I help you now though we’ll have time to play some music. I’ve been looking forward to it all day."
            p "Hmmm… that’s a fair argument."
            "> She still seems embarrassed for accepting your help but at the same time, satisfied"
            "> You end up kneeling beside her. As you sit she retracts a couple inches away from where you’re sitting"
            "She doesn’t seem that comfortable with me maybe I should try to make some conversation."
            menu:
                "What is the concert for?":
                    $ girl2.add_affection(1)
                    p "This is my opportunity to be the greatest violinist of our time."
                    m "What…?"
                    p "A representative from the most prestigious music schools in the UK was invited to view my performance. Basically I’m being evaluated before actually going there to do my audition for the school."
                    m "Uh huh... congrats, Cathy!"
                    p "Idiot. Don't call me that."
                    m "hahahahaha!"
                    "> She furiously starts sketching her posters"
                        menu:
                            "What do you need me to do?":
                                jump music_event_1_part_2
                    
                "What do you need me to do?":
                    jump music_event_1_part_2
        
label music_event_1_part_2:
    p "Can you just sketch details, in pencil?"
    m "Don’t you want me to do more than that?"
    p "No. I can’t have any clumsy mistakes."
    "> You look at the posters in front of her"
    m "But you didn’t even colour in the lines."
    "> Caterine is flustered"
    p "N-no! That’s for visual effect! I guess it’s hard to appreciate for an uncultured eye."
    m "That is debatable."
    p "Just get to work!"
    
    "> You work for some time, not saying anything to each other"
    "> You look at your clock and notice that the sun is starting to set"
    "> You look towards the window and you see the sunlight give a warm colouring to the surroundings. The chalk dust in the air highlights the sun rays giving the room a calm atmosphere"
    "> Your eye wander the room and lead to Catherine, in the middle of the room and under the sun rays. She’s intently finishing up the final touches on the posters"
    "> She looks like she’s in a spotlight. She looks so natural in it, like she was made to be in a spotlight. Light passes through her hair giving it an ethereal look. It drapes down, and on her shoulders. By observing her alone, you feel unsettled and begin to feel hot. From your chest and back, traveling up to the side of your neck, your body is uncomfortably warm"
    "> She tucks her hair behind her ear, as she finishes up the final touches, but is then surprised catching you staring at her, from the side of her view"
    
    p "...Why are you staring at me?"
    menu:
        "Is it hot in here?":
            $ girl2.add_affection(-1)
            p "No not really, why are you sweating? That’s kinda gross."
            "WHY AM I SWEATING???"
            m "uh gah… don’t worry about it. It’s just hot."
            p "... o--okay..."
            menu:
                "Sorry you just looked really good today":
                    $ girl2.add_affection(-1) 
                    p "Oh… umm thanks…"
                    "Uhhh maybe I shouldn’t have said that, she probably thinks I’m weird."
                    "> You don’t really know how to follow up on that response, so you decide to let the awkward space settle for a moment"
                    menu:
                        "Wow, the posters look amazing! We did a good job":
                            jump music_event_1_part_3
                "Wow, the posters look amazing! We did a good job":
                    jump music_event_1_part_3
                    
        "Sorry you just looked really good today":
            $ girl2.add_affection(-1)
            p "Oh… umm thanks…"
            "Uhhh maybe I shouldn’t have said that, she probably thinks I’m weird."
            "> You don’t really know how to follow up on that response, so you decide to let the awkward space settle for a moment"
            menu:
                "Is it hot in here?":
                    $ girl2.add_affection(-1) 
                    p "No not really, why are you sweating? That’s kinda gross."
                    "WHY AM I SWEATING???"
                    m "uh gah… don’t worry about it. It’s just hot."
                    p "... o--okay..."
                    menu:
                        "Wow, the posters look amazing! We did a good job":
                            jump music_event_1_part_3
                "Wow, the posters look amazing! We did a good job":
                    jump music_event_1_part_3
                            
        "Wow, the posters look amazing! We did a good job":
            jump music_event_1_part_3

label music_event_1_part_3:
    $ girl2.add_affection(1) 
    "> She looks happy at your comment"
    p "Thanks, and I guess you aren’t super useless."
    m "Thanks?..."
    "At least I’m not ‘super useless’..."
    m "I was thinking we should probably get to practicing soon."
    p "Oh! haha --of course, I didn’t forget about that---"
    "sureee..."
    
    "> Catherine and you are finished making the posters for the concert and put them around the school"
    
    m "Do you want to play now?"
    p "Uh. Sure. What do you want to play?"
    menu: 
        "Beethoven violin Sonata o. 9 Op.47":
            
        "Chopin Tristesse Etudes in E major":
            
        "Rondo Capriccioso- Saint-Saens":
            
    # "> After music plays for x time or whatever"
    m "That was fun!"
    p "Yeah.. You're getting better."
    m "Here's an idea... do you think that I could play with you in your concert?"
    p "OF COURSE NOT!!! This is actually important."
    menu:
        "Change your mind":
            $ girl2.add_affection(-1)
            m "Whatever, It’s not like I cared enough to help anyways."
            "> She looks pretty mad at that last comment"
            p "You don’t have to be so butthurt about it."
            "Maybe I shouldn’t have thought out loud."
            
        "Try to convince her":
            $ girl2.add_affection(1)
            m "What?! Why not? I think it would be fine, Cathy! If you ever want an accompanist, I’ll be around."
            "> She avoids eye contact and slightly blushes"
            p "...Thanks, I’ll think about it. BUT I TOLD YOU NOT TO CALL ME THAT."
            
    "> Catherine huffs"
    p "Anyways, I should get going."
    "> She starts to pack up quickly and begins to rush out"
    m "I’ll see you tomorrow then."
    p "…Yeah"
    "Hmm she seems a little off. Was it something I said?"
    $ day = stats.get_days()
    if day == 3:
        jump music_day_3
    elif day == 4:
        jump music_day_4
    
label music_event_2:
    # triggered from closeness
    "> You receive a text from Catherine"
    p "'Come to the music room for a minute'"
    "> You walk into the music room, no music is being played which is strange"
    "> You see Catherine leaning against the window sill. She’s looking out the window smiling. She’s looking at the trees swaying in the breeze"
    "I guess it’s a good day out."
    "> The warm lighting gives her a glow, where she seems so peaceful. For some reason everything seems so vibrant"
    "> Catherine sees your reflection in the window and turns around to address you with a smile on her face"
    p "Can I ask you for a favour?"
    
    menu:
        "Yeah, of course":
            $girl2.add_affection(1)
        "Sure, if you act a litter nicer to me":
            $girl2.add_affection(-1)
    
    "She looks pretty concerned, I wonder what this about"
    p "So... the concert..."
    m "Yeah?"
    p "Apparently I’m required to have an accompanist."
    m "Oh? and?"
    "> You try not to crack a smile knowing whats coming"
    p "So... I... may need you to play as my accompanist."
    m "I don’t know... I thought I wasn’t good enough?"
    "I’m not sure if I should be teasing her at a situation like this, but I need to milk this opportunity."
    "> She seems surprised at your response like she was expecting you to agree right away. Her face turns mad red and squeezes her eyes shut"
    p "Please! This is my only opportunity! I know I’ve been mean to you this whole time."
    "> Her eyes begin to water"
    p "But I just get so frustrated when I can’t do anything myself because people won’t see me as strong, but now I need someone and I find myself with no one else to lean on. Please..."
    "Oh crap. She’s super serious right now."
    menu:
        "Yeah don’t worry, I said I was going to be around if you needed me, right? Let’s start practicing for it!":
            jump music_event_2_part_2

label music_event_2_part_2:
    "> You arrive outside of the music room. The suit you’re wearing makes you feel stiff and limited in mobility"
    "I think I look okay, I can’t tell with only the moonlight"
    "> You receive a text from Catherine"
    p "'Hey, I’m on the balcony'"
    "> You get to the top of the building, and through a wide set of glass double doors you see her in a white dress. As you pass the doors, the scenery opens wide overlooking the city dotted with streetlights and cars"
    "> You lean on the wide railing, next to her. On the side of your vision her dress and skin glow in the moonlight. both of you don’t look at each other, but enjoy the expanded scenery"
    menu:
        "You look good in this lighting":
            $girl2.add_affection(-1)
            p "What about other lightings?"
            "Oops, I guess that came out wrong."
        "It's a beautiful night":
            $girl2.add_affection(1)
            p "Yeah, it is."
            
    m "It’s the big day huh? How are you feeling?"
    p "My palms are a little sweaty and my head is all jumbled with worries."
    m "It will be fine, don’t worry about it. Let’s just try our best!"
    p "I need this to be perfect..."
    menu:
        "Downplay it to make her feel more at ease":
            $girl2.add_affection(-1)
            m "Calm down a little, it’s not a big deal."
            p "Haven’t you been listening at all?"
            "Oh crap that wasn’t smart of me."
            menu:
                "Reassure her":
                    m "Well it’s an important day to you right? You want to get into the school?"
                    p "..."
                    m "What’s with the silence?"
                    
        "Reassure her":
            $girl2.add_affection(1)
            m "Well it’s an important day to you right? You want to get into the school?"
            p "..."
            m "What’s with the silence?"
            
    p "To be completely honest, I couldn’t care less if I went to the music academy or not. Not anymore anyways..."
    m "I thought that was your goal? To become the greatest violinist of our time?"
    p "I mean, excelling at playing the violin is a goal and passion, but I want this to say I was able to do it too."
    m "Sounds like a lot of work for some recognition."
    p "I know... But you don’t know what it’s like, always having people holding your hand while you do anything, not letting you take your own steps, not letting you take any credit... or maybe you do... or you could at least try understanding."
    "> At this moment she turns and looks up at you, with both eyes. The moonlight reflects off of them, for a moment captivating you. At this angle you’re able to see her red lips and rosy cheeks. You feel like a pin went through your chest"
    m "I think I can understand. What if I said that even though I’m here, as your accompanist, I see everything you’ve worked towards, and I think you have definitely proved that you are more than capable of handling yourself?"
    "> She smiles and her eyes look away"
    p "I’d be happy…"
    "> She sees your watch"
    p "Oh! it’s almost time to go! Quick smell my perfume, make sure it smells good!"
    "> She pulls back her hair, and leans forward, exposing her neck to you"
    "> You don’t have time to react smoothly, you quickly lean in to smell"
    "> When you breathe in the scent, it’s like fireworks begin going off your head. This feeling travels down through the rest of your body, but you feel something briefly press against your cheek"
    p "That was for good luck...and for listening to me."
    "> She covers her mouth, and avoids eye contact, blushing"
    m "Thanks..."
    p "D-don’t look at me like that, you’re wasting time."
    "> She grabs your hand and leads you through the doors into the building"
    
    "> You feel like a ragdoll as she makes sharp corners towards back-stage. She stops abruptly and turns around quickly to face you. Her eyes are shining with excitement and nervousness"
    p "Ready?"
    m "Your palms are sweaty"
    "Oh God, I literally could have said anything else."
    "> She pulls her hand quickly away and picks up her violin"
    p "Don’t get full of yourself. Let’s do this."
    "> You walk out onto stage, as you look out you don’t see a single face, but you feel everyone stare. The silence permeates"
    "> You take a seat at the piano and wait for her signal"
    "> You hear her draw her bow across her strings. Her playing is colourful and vibrant, full of expression. As the song progresses, you feel her stage presence is powerful, and you do what you can to support her. You notice your head nodding, and feeling the momentum of the keys. You feel each other’s playing styles as you progress to the end"
    # cue music here
    
    "> You reach the end of the song, and you get up to stand next to her. When you approach her, she holds out her hand in front of you, you grab it then both of you bow. The audience gives you a large applause"
    "> Both of you walk off stage"
    p "We did it!"
    menu:
        "Hug her":
            $ girl2.add_affection(1)
            m "Yeah, good job!"
            "> You hug her. you intended to have a quick hug, but it lingers for a while longer"
            p "I’m really thankful for you helping me out."
        "Talk about the Academy":
            $ girl2.add_affection(-1)
            m "You did it, you’re sure to get in now! I’m glad it went well."
            p "Oh... yeah right. thanks..."
            
    m "We should celebrate!"
    p "Celebrate? what do you have in mind?"
    m "How about Karaoke?"
    p "Karaoke?"
    m "Yeah, that thing where you sing in a room..."
    p "I know what it is, but why Karaoke?"
    m "Why not? you’ve been so stressed out on music lately, this is a good way to destress with music."
    "> She sighs"
    p "Okay..."
    m "GREAT! LET’S GO"
    jump music_event_3
            
label music_event_3:
    # karaoke event here, success or failure
    m "Here we are."
    p "Y-yeah..."
    m "What’s wrong, Cathy?"
    p "I’ve never sung in front of anyone..."
    m "So wait, you’re telling me that you can get on a stage in front of hundreds of people, but you can’t sing in front of me?"
    p "IT’S DIFFERENT, The violin has a good voice."
    menu:
        "Reassure her":
            $ girl2.add_affection(1)
            m " It can’t be that bad, don’t worry, I’m not here to judge you."
            p "Liar..."
            m "PROMISE."
            "> She rolls her eyes"
            p " Don’t say I didn’t warn you."
            
        "Joke":
            $ girl2.add_affection(-1)
            m "Well that’s a shame, I guess that’s the problem with hiding behind an instrument your whole life."
            p "Aren’t you a tad bit conceited?"
            m "That came out wrong..."
            p "Yeah it did."
    
    p "Well... let’s get this over with."
    "> You place your hands on her shoulders and guide her into the karaoke room"
    m "Come on, don’t worry it’s going to be fun!"
    "> When you sit down, you place songs in the playlist. As one of them is about to begin, you notice out of the corner of your eye, Catherine clutching the mic with both hands. she holds it with her arms retracted close to her chest"
    m "C’mon lighten up! It’s just us. Okay deep breaths."
    "> You take 2 short consecutive breaths out, followed by one drawn out exhale"
    "> She bursts out laughing"
    p "That’s what you do when you’re giving birth!"
    m "THEN YOU HAVE NOTHING TO WORRY ABOUT!"
    "> She laughs"
    p "Alright, alright I’m ready."
    "> Her shoulders relax, and she takes a deep breath"
    "> The music starts playing, You start the song slow. following the lyrics her voice takes you by surprise. You are taken back for moment to the point where you stop singing out of disbelief. Her voice actually is powerful and smooth"
    "SHE LIED TO ME"
    "> You decide to just go with it. You have an almost a deja vu moment, as if you were her accompanist again. Naturally, you begin to harmonize with her. It must be from practising with her. At one point of the song, you both feel each other pushing your diaphragms to their limit. You look at each other trying not to laugh"
    "> You see her under the fluorescent rose lighting of the room, she looks like she’s really having enjoying herself. She looks at you and smiles as the song ends"
    p "That was great!"
    "> She begins laughing uncontrollably while leaning forward"
    "> She beings to lose balance as she falls forward, and falls in your direction. You react by trying to catch her with both arms, but her momentum catches you off guard and pushes you back. You fall directly on your butt"
    p "OH! I’M SO SORRY ARE YOU OKAY?"
    "> She immediately panics and clumsily tries helping you up"
    m "Probably just fractured my tailbone, but I’m fine."
    p "SERIOUSLY?"
    m "Don’t worry... I’m just kidding"
    p "Don’t scare me like that..."
    m "Since when did you start worrying about me so much?"
    "> Her cheeks instantly turn red"
    p "I-I don’t know what you’re talking about... Idiot."
    menu:
        "Hey, if you want to talk about something, I’m listening":
            $ girl2.add_affection(1)
            p "..."
            
        "Oh alright":
            $ girl2.add_affection(-1)
            p "... Why do you have to be so dense all the time?"
            
    "> She sighs"
    p "Look... It’s been really hard for me to be comfortable around you."
    m "What do you mean?"
    p "In the short time I’ve known you, I don’t think I’ve ever felt so close to anyone. At first I couldn’t stand you being around, but you just kept persisting to help me out and to help you out. Then well I guess you just grew on me."
    m "Is that a bad thing?"
    p "No… I’m just a little confused, that’s all… I’ve grown up in a well off family, and I always was given opportunities, as if they were served to me on a silver platter. I never felt like I earned anything. I eventually just hated it when people helped me accomplish tasks, people always checking up on me saying 'Do you need help with that?' As if I couldn’t handle myself, as if I was completely incapable of doing anything. I started to be secluded from people, and refuse people that tried to get close to me."
    m "What about now?"
    p "I don’t know anymore. I guess you could say that you’re now an exception to the rule."
    "> She smiles, leans back into the couch, and stares blankly towards the karaoke lyrics rolling"
    p "You know, it’s funny. I try to push people away, but then one person is just able to push through all the walls I set up. I didn’t want to trust that person, but I end up leaning on them the most, when I’m in need."
    "> She shifts her weight, so that her rests upon your shoulder"
    "> You feel a tension while your beats per minute skyrocket. It’s like your head is going to explode from built up pressure"
    m "H-hey Ca--"
    p "Just be quiet for a moment..."
    "> Neither of you move while the karaoke lyrics roll and the rose lights pulsate in the room. From this atmosphere, you just enjoy each other’s presence"
    menu:
        "Hey Cathy, do you want to go out with me?":
            # check affection level
            $ affection = girl2.get_affection("Catherine")
            # if success:
            if affection > 6: # NUMBER CAN VARY
                p "Does it look like I don’t want to?"
                m "Well maybe you just wanted to be friends."
                p "Sometimes I can’t believe how clueless you can be... So I’ll say it plainly: I want to go out with you."
                "> She wraps her arms around your torso, smiling. You both continue to bask in the emotions until it’s time to go"
                p "Thank you for everything, I’m really glad to have met you in my life..."
                jump music_event_3_part_2
            # if failure:
            else:
                p "Does it look like I don’t want to?"
                m "Well maybe you just wanted to be friends."
                p "Sometimes I can’t believe how clueless you can be... But, I can’t..."
                m "..."
                p "I got into the academy..."
                m "Oh... Congrats..."
                "> She wraps her arms around your torso, and begins to have tears streaming down her face"
                p "I’m so sorry... as much as I want to be with you... this is a really important opportunity."
                m "No of course... I couldn’t expect you to drop everything for me..."
                "> You both sit and try to savour the moment. She latches onto you tight, not wanting to let go. You sit trying to hold on to each other’s presence inevitably comes to an end"
                p "Thank you for everything, I’m really glad to have met you in my life..."
                jump girl2_fail_end
    
label music_event_3_part_2:
    "> A few days have passed since that day"
    "> Your phone rings"
    m "Hello?"
    p "Hi %(player_name)s."
    m "Hey, Cathy!"
    p "I got the results from the evaluation."
    menu:
        "Great! this will be a great opportunity for you!":
            p "It is good..."
            m "I'll see you at the music room then."
            
        "Oh I see, how do you feel about it?":
            p "Hmm... I don’t know if I really want to go anymore."
            m "What about being the greatest violinist ever?"
            p "Well I just wanted to talk to you about it too, wanna meet in the music room?"
            m "Sure."
            
    "> You arrive to the music room"
    "> You see her again against the window sill"
    m "Hey, Cathy."
    p "Hey..."
    m "Did you want to talk about it?"
    p "I’ll just get to the point: Do you want me to go or not?"
    m "Wait what? For the Academy? why does my opinion matter?"
    p "Because it matters to me... because you’re important to me."
    m "Oh..."
    p "So tell me, do you want me to stay or not?"
    menu:
        "I want you to stay":
            jump girl2_good_end
            
        "I think you should take the opportunity":
            m "I completely support your decision." 
            p "Ohh... haha... Yeah, thanks for supporting me"
            m "Yeah, of course."
            "> She sighs"
            p "Well I guess this is what I asked for."
            m "Don’t worry, I think you’ll go really far with it. You’ll be able to experience a lot of great things, especially living in the UK independently."
            p "Yeah you’re right..."
            "> She seems frustrated about something"
            p "I don’t get it! I haven’t even known you for that long, but all the sudden you’ll be out of my life. I tried so hard to be independent and do things on my own, and when I finally get the chance, I don’t want it. I end up depending on you anyways. I even said 'yes', when you asked me out!"
            menu:
                "We can still keep in touch":
                    m "Hmm... You didn’t necessarily depend on me, you could always do it by yourself, I was just an accompanist. Besides we can still keep in touch."
                    p "Yeah... that’s a fair argument."
                    "> She shoves her face into your chest and latches around your torso"
                    p "...Will you remember me?"
                    m "What if told you I will?"
                    p "That would make me happy... Well... Goodbye then..."
                    m "This isn’t 'goodbye', it’s just a 'see you later'..."
                    jump girl2_bad_end
                    
                "Change your mind":
                    m "I'm just trying to not be selfish but believe me when I say I really do want you to stay. You're important to me and it would hurt to watch you leave."
                    jump girl2_good_end
                    
        "You should make the decision yourself":
            "> Catherine seems frustrated"
            p "I don't get it! I haven't even known you for that long, but all the sudden you'll be out of my life. I tried so hard to be independent and do things on my own, and when I finally get the chance, I don’t want it. I end up depending on you anyways. I even said 'yes', when you asked me out!"
            m "This is finally your chance to be independent."
            m "This is what you wanted. What you worked for. You made it and you shouldn't let me hold you back."
            p "...Is it so wrong to have someone to lean on at least sometimes...I thought I could depend on you. We’ve been through a lot together...I really had feelings for you."
            m " I didn’t mean it like that..."
            p "Forget it. You’re right. I don’t know what I was thinking. I’ll go ahead with the academy. Thank you for everything. Let’s both work hard on our separate paths."
            "> Catherine starts walking towards the door but stops at your side. She glances up towards you quickly but then looks away and continues out the door, leaving you behind. You’re left alone standing in the silent music room and you have a feeling you won’t be playing the piano for a long time"
            jump girl2_bad_end
            
label girl2_bad_end:
    "GAME OVER"
    return

label girl2_good_end:
    "> She smiles"
    p "hahaha! You’re funny."
    "> She continues to laugh at you, but you stand there confused at what just happened"
    m "I think I'm lost."
    p "I already declined the offer, so whether you like it or not, looks like you’re going to be stuck with me."
    m "Oh hahaha… I thought you were asking seriously."
    p "Well I was asking, then I could figure out how much you like me hehe..."
    m "charming haha..."
    p "So? what say you? Do I need to make you smell my perfume again?"
    m "Yeah... yeah, I do."
    "> She leans over, then you feel something press against your cheek"
    p "Besides, I already said yes to you. You’re my new dream. You’re mine."
    
    "YOU WIN"
    return
    
label girl2_fail_end:
    "GAME OVER"
    return
    
label home_ec_room:
    # show image of room
    # play sound of sizzling noise
    
    # you have chosen Mary as the girl 
    $ stats.set_chosen_girl(1)
    
    "> As you enter the room, you hear a sizzling noise. The fragrances tickle your nose as you enter the room. Your sight is drawn to the centre of the room, to a girl. She looks up to acknowledge you, and she gives a friendly but shy smile."
    
    p "Hello, I haven’t seen your face around, are you new?"
    
    m "Yeah, I just transferred here recently. Is this the cooking club?"
    
    p "Yes! you’ve come to the right place."
    
    m "Where do I sign up?"
    
    p "Well… you kind of need to cook in this club. Show me what you can do first, and then we can talk about your membership."
    
    "> You realize that you’ve only been here for a day, and the only culinary experience you have comes from instant ramen."
    
    p "Hello? You blanked out for a second, haha. what do you plan on making for me?"
    
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")
    
    menu: 
        "Chocolate chip cookies (Strength 1, Charm 1)":
            if str_check >= 1 and cha_check >= 1:
                "> Miraculously, you remember a recipe for chocolate cookies, and manage to put them together."
                $ girl1.add_closeness(1)
                $ stats.set_food_choice(0)
                jump girl_1_convo_1
            else:
                "> You don't remember how to make this, time to guess!"
                $ girl1.add_closeness(-1)
                $ stats.set_food_choice(1)
                jump girl_1_convo_1
        
        "Instant Ramen (No reqs)":
            "> You decide that it’s would be more efficient to make what you know the best. Conveniently, you remember that you brought along a spare package of instant noodles to school with you. You pull it out of your backpack and proceed to open the plastic wrapping."
            $ girl1.add_closeness(-1)
            $ stats.set_food_choice(2)
            jump girl_1_convo_1
        
        "Beef Carpaccio (Strength 2)":
            "> You decide that it would be best to go big or go home. If you managed to pull this off, she would be incredibly impressed. Unfortunately, you do not have the knowledge of the ingredients or techniques need to put this dish together. You improvise as you go."
                
            if str_check >= 2:
                $ stats.set_food_choice(3)
                jump girl_1_convo_1
            else:
                $ stats.set_food_choice(4)
                jump girl_1_convo_1
            
label girl_1_convo_1:

    "> As you’re working, you can’t help notice the awkward silence settling in. You glance over to her and end up making eye contact. You realize that you could probably use this time to get to know her."

    menu: 
        "Ask her for her name":
            m "Soooo… I actually never caught your name, my names %(player_name)s."
    
            p "Oh, sorry about that! I’m Mary, I am president of the cooking club. I'm also in my senior year."
            # change the name of p to Mary
            $ unknown_name = "Mary"
            
            menu:
                "Ask her why she joined the cooking club":
                    p "It's just a hobby, nothing that serious."
            
        "Ask her why she joined the cooking club":
            p "It's just a hobby, nothing that serious."
            
            menu:
                "Ask her for her name":
                    m "Soooo… I actually never caught your name, my names %(player_name)s."
    
                    p "Oh, sorry about that! I’m Mary, I am president of the cooking club. I'm also in my senior year."
                    # change the name of p to Mary
                    $ unknown_name = "Mary"
            
    $ get_food = stats.get_food_choice()
    if get_food == 0 or get_food == 1:
        $ food = "cookies are"
    elif get_food == 2:
        $ food = "instant ramen is"
    else:
        $ food = "beef carpaccio is"
    m "Looks like the %(food)s done!"
    
    $ get_food = stats.get_food_choice()
    if get_food == 0 or get_food == 3:
        jump made_good_food_1
    elif get_food == 1:
        jump made_bad_food_1
    elif get_food == 2:
        "> You peek at her eyes to get some idea of what she may be thinking, but it’s not really discernible. You watch nervously as she takes a bite. This is your favorite flavor of instant noodles. After swallowing, she hesitates for a moment, and her eyes bulge. Violently she clasps her mouth and supports herself with the edge of the counter. She spits out your creation."
        jump made_bad_food_1
    else:
        "> You peek at her eyes to get some idea of what she may be thinking, but it’s not really discernible. You watch nervously as she takes a bite, wondering if you put in enough sriracha sauce to mask the overbearing taste of durian. After swallowing, she hesitates for a moment, and her eyes bulge. Violently she clasps her mouth and supports herself with the edge of the counter. She spits out your creation."
        jump made_bad_food_1
        
label made_bad_food_1:
    
    p "It was... uh... not bad... "

    "> she forces a smile and pushes your food a few inches away"

    m "Sorry about that, maybe you can teach me some basics?"
    
    p "mmm… that sounds okay i suppose...come by tomorrow and I’ll teach you a little of what I know."
    
    jump end_day_1
    
label made_good_food_1:
    
    p "It was good!"
    
    "> Mary gives a warm smile"
    
    p "I’ll let you into the club! I need a sous chef to help me with a project. If you’re free come by tomorrow after class"
    
    jump end_day_1
    
label end_day_1:
    
    # show image of bedroom at night?
    m "That was a long day, time to hit the sack."
    $ stats.increment_days()
    
    jump start_day_2
    
label start_day_2:
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump home_ec_day_2
    
label girl1_check_1:
    
    $ closeness = girl1.get_closeness("Mary")
    $ day = stats.get_days()
    $ event_num = girl1.get_event("Mary")
    
    if day < 5 and closeness > -3 and closeness < 5:
        # continue on with cooking
        return
    elif day > 5:
        # too long trigger failure event
        jump girl1_failure
    elif closeness <= -3:
        # lost too much closeness
        jump girl1_failure
    elif day < 5 and closeness >= 5 and event_num == 0:
        # trigger event 1 of cafe as day < 5 and closess > 5
        # set the event value to 1
        $ girl1.add_event()
        jump cafe_date1
        
label girl1_check_2:
    
    $ closeness = girl1.get_closeness("Mary")
    $ event_num = girl1.get_event("Mary")
    if closeness >= 7 and event_num == 1:
        $ girl1.add_event()
        jump restaurant_date1
    else:
        return
        
label girl1_check_3:
    
    $ closeness = girl1.get_closeness("Mary")
    $ event_num = girl1.get_event("Mary")
    if closeness >= 10 and event_num == 2:
        jump girl1_home_date
    else:
        return
    
label home_ec_day_2:
    
    # check closeness
    call girl1_check_1
    call girl1_check_2
    call girl1_check_3
    
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")

    m "maybe I should drop by the club room, Mary might be there too."
    
    menu:
        "Blueberry Muffin (No reqs)":
            "> The muffins looks great!"
            p "Wow! They're so fluffy, but the top is so crisp. Good job!"
            $ girl1.add_closeness(1)
            
        "Creme brule (Intelligence 2, Charm 2)":
            if int_check > 2 and cha_check > 2:
                # sucess
                "> The Creme brule looks great! nice golden caramelize on it! Looks delicious!"
                p "Looks great. I'm impressed."
                $ girl1.add_closeness(3)
            else:
                # failure
                "> The Creme brule turned out completely black... You think that you burnt it..."
                p "Uhh... is this even edible?"
                $ girl1.add_closeness(-3)
                
        "Lasagna (Strength 2, Charm 2)":
            if str_check > 2 and cha_check > 1:
                "> The lasagna looks great! The cheese is perfectly melted."
                p "The Lasagna looks awesome! The layers look so even!"
                $ girl1.add_closeness(2)
            else:
                "> You reach into the oven and pull out what looks like a pile of plain pasta."
                p "I think you didn't use enough tomato sauce... it looks pretty dry."
                $ girl1.add_closeness(-2)
    
    $ stats.increment_days()

label day_3:
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump home_ec_day_3

label home_ec_day_3:
    
    call girl1_check_1
    call girl1_check_2
    call girl1_check_3
    
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")
    
    menu:
        "Cinnamon Buns (No reqs)":
            "> The Cinnamon Buns turned out great! The icing looks shiny and delicious!"
            p "Looks so good! Can't wait to try it."
            $ girl1.add_closeness(1)
            
        "Assorted Sashimi (Charm 3, Strength 3)":
            if int_check > 3 and str_check > 3:
                "> The sashimi is perfectly sliced."
                p "Wow! Looks so good I almost don't want to eat it!"
                $ girl1.add_closeness(3)
            else:
                "> The slices turned out oddly-shaped and uneven. You see pieces of bones and scales mixed in with the fish."
                p "Uhh... It's okay. We can always get some more expensive fish."
                $ girl1.add_closeness(-3)
                
        "Carbonara (Strength 2, Charm 2)":
            if str_check > 2 and cha_check > 2:
                "> The pasta turned out perfectly cooked! The aroma of the sauce fills the air."
                p "That smells so good!"
                $ girl1.add_closeness(2)
            else:
                "> The pasta looks like a pile of mush..."
                p "I think the pasta is way too overcooked..."
                $ girl1.add_closeness(-2)
            
    $stats.increment_days()

label day_4:
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump home_ec_day_4
    
label home_ec_day_4:

    call girl1_check_1
    call girl1_check_2
    call girl1_check_3
    
    $ str_check = stats.get_stats("str")
    $ int_check = stats.get_stats("int")
    $ cha_check = stats.get_stats("cha")

    p "Well... I just feel like I need some inspiration right now. I wish I could try some new food somewhere. Do you have any suggestions %(player_name)s?"

    menu:
        "Mac and Cheese (No reqs)":
            "> The cheese is perfectly melted and crisp on the surface of the casserole dish."
            p "I can't wait to try this! Looks fantastic!"
            $ girl1.add_closeness(1)
            
        "Beef Stroganoff (Strength 4, Charm 4)":
            if str_check > 4 and cha_check > 4:
                "> The pasta turned out perfectly cooked! The aroma of the sauce fills the air."
                p "That smells so good!"
                $ girl1.add_closeness(2)

            else:
                "> The pasta looks like a pile of mush..."
                p "I think the pasta is way too overcooked..."
                $ girl1.add_closeness(-2)
                
        "Lemon Meringue Pie (Intelligence 3, Charm 3)":
            if int_check > 3 and cha_check > 3:
                "> The pie is firm and the meringue keeps it's form."
                p "Congratulations! The browning of the meringue is beautiful!"
                $ girl1.add_closeness(2)
            else:
                "> The filling is too liquidy; it will not hold its shape."
                p "I think that you over baked the pie."
                $ girl1.add_closeness(-2)
                
    $stats.increment_days()


#WHAT I ADDED
#================================================================================================================================================
#Girl 1 - Cafe Date ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

label cafe_date1 :
    if cafe_asked_count == 0 :
        "> You and Mary spend some time casually talking at a local cafe. A warm glow shines through the windows."
    
        "> Mary is looking off to the distance, her face showing little expression."
        
        "> Your orders arrive at the table."
        
        p "Thank you!"
    
        "{i}She seems distracted. Maybe I should be more engaging. What should I ask her?{/i}"
    else:
        "{i}What should I ask her?{/i}"
    menu:
        "Do you have a boyfriend?" if not cafe_boyfriend:
            $ cafe_asked_count += 1
            $ girl1.add_closeness(-1)
            p "Excuse me? Where is this coming from all of a sudden? What does it matter to you anyways?"
            
            "> Mary looks displeased."
                
            "{i} Maybe I should I should drop the topic...{/i}"
            $ cafe_boyfriend = True
            jump cafe_date1
        
        "C'mon, just tell me." if cafe_boyfriend:
            $ cafe_asked_count += 1
            $ girl1.add_closeness(-1)
            p "mmm... you really are persistent."
                
            "> Mary looks very uncomfortable."
                
            p "Oh yeah... I remembered there was something I had to do back home. Sorry to leave you so suddenly. Here's some money for the bill."
            jump cafe_date_badending
                
        
        "What do you want to be?" :
            $ cafe_asked_count += 1
            p "Hmm.. not sure. Medicine? Engineering? Something in those professional fields. What do you think?"
            
            menu :
                "Sounds great!I'll support you if you ever need help." :
                    $ girl1.add_closeness(-1)
                    p "Yeah... It does, doesn't it?"
                    
                    "> Mary forces a smile. She lets out a small sigh."
                    
                    "That's how life is supposed to go, right? That was, I can meet my mom's expectations... I guess that's most important after all.."
                    
                    "> You sense a hint of frustration in her voice. The tension gets to you and things become too awkward for you to say anything else."
                    
                    "> The rest of your date went on without much dialogue."
                    
                    jump cafe_date_badending
                    
                "What about being a chef?" :
                    $ girl1.add_closeness(2)
                    jump mary_backstory1
                    
                    
        "What do you usually come here?" if not cafe_before:
            $ cafe_asked_count += 1
            $ cafe_before = True 
            $ girl1.add_closeness(1)
            p "Yeah! I love coming here for the pastries and desserts!"
            
            " > Mary looks more excited as she rapidly counts her fingers."
            
            p "Everything here is good, black forest cake, gingersnaps, cinnamon buns... "
            
            p "YOU SHOULD TRY THE TIRAMISU HERE!"
            
            p "..."
        
            p "oops.. Haha, sorry. I'm usually more calm."
            
            "> Mary takes a therapeutic breath."
            
            m "Hahaha, don't worry. It's really kind of cute."
            
            "> Mary blushes. Her eyes drop to her latte."
                                     
            jump cafe_date1
            
        "How are classes?" if not cafe_asked1: 
            $ cafe_asked_count += 1
            $ cafe_asked1 = True
            p "Ehhh not bad, classes are same old. Nothing that interesting."
            
            jump cafe_date1

label mary_backstory1 :
    p "Hmm... I don’t know. It’s not the most stable career out there, ahah."
    
    m "So?"
    
    p "Soooo… that’s being pretty unrealistic… It’s too selfish for me to just think about what I want to do… I mean, when I get older I have to think about supporting a family, and taking care of kids, so that they can go to university. At least that’s what my mom thinks."
    
    "> Mary lets out a heavy sigh as her eyes roll back and she leans back into her chair. Her posture sinks and her eyes fall down to her cup."
    menu: 
        "Joke" :
           #$girl1.add_closeness(-1)
           m "Oh... Talk to me about it. Tell Dr.Fill about your problems."
           
           p " Uhmm... I'd rather not talk about it right now."
           
           m "Feel free to talk to me anytime."
           
           p "Yeah, thanks."
           
        "Console" :
            $girl1.add_closeness(1)
            m" That's rough. If you ever want to talk about it sometime, I'll be here."
              
            p "Thanks. Maybe another time."
            
            m "Yeah, anytime!"
    
    p "Ahh.. It's getting pretty late, I should head home."
    
    m "Yeah, same. It was fun hanging out with you today!"
    
    jump cafe_date_goodending


label cafe_date_goodending :
    $ girl1.add_closeness(1)
    "> After a while of more small talk, you guys finish your food. You both stand up and she looks at you."
    
    p "I really enjoyed this. We should get together more often."
    
    "> You hold the door open for her and you guys part ways. as you’re walking, you look back to catch her peeking over her shoulder, as well. You both wave at each other."
    
    "> The date was a success! You managed to get closer to Mary"
    
    jump return_to_which_day
    
label cafe_date_badending :
    $ girl1.add_closeness(-1)
    "> You guys finish your food. Mary stands up and looks away."
            
    p "Well... have a goodnight."
    
    "> Mary leaves first and you are left alone. You sit for a moment to avoid getting in her way. As you leave the cafe, she is no where in sight."
    
    "> You were unsuccessful in this date."
    
    jump return_to_which_day
    
    #cue bad game ending?

    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Girl 1 - Restaurant Date

label restaurant_date1 :
    if not rest1_asked2 and not rest1_asked3 :
        "> The hostess leads you to your table, and both of you get in each other’s way trying to decide where each of you will sit. As you two take your respective seats, you chuckle to each other."
    
        p "Ahah, wow.. this place sure is fancy." 
    
        "> Awkward silence follows."
    
        "> Mary looks a little flustered."
    
        "> QUICK! SAY SOMETHING TO HER YOU FOOL!"
    
    menu:
        "You look very pretty today." if not rest1_asked2 : 
            $ rest1_asked2 = True
            $ girl1.add_closeness(1)
            p "O-Oh."
            
            "> Mary blushes and can’t seem to look you in the eye. You hope this is a good sign? Your compliment doesn’t do anything to spark any conversation, rather, she seems even more flustered. "
            jump restaurant_date1
            
        "What else do you like about cooking?" : 
            jump restaurant_date2 
            
        "We look like a real couple!" if not rest1_asked3 : #no effect
            $ rest1_asked3 = True
            p "Uhm.."
            
            "> Mary looks confused."
            
            p "We're not... sorry, I just don't think we're on the same page.."
            
            "> Mary looks a little shy about it but not annoyed or anything. She seems even more flustered than before."
            
            jump restaurant_date1
            
            
label restaurant_date2:
    if not rest2_asked1:
        "> The corners of her mouth raise ever so slightly, but her eyes wince a little."
            
        p "I’ve been really curious about ever since I was little. Cooking made me feel some sort of wonder and eventually it just grew into a passion."
            
        "> She shifts her glass back and forth. Her eyes follow the glass. She lets out a shallow sigh."
            
        p "Something about cooking makes me feel unique, you know? Haha, sometimes I like to pretend that I’m really good at it. "
        
        "> Her glass slows down, and her smile fades to concern."
            
        p "But... In the end it's just a hobby..."
    
    "> Mary becomes silent, her eyes wander down to her glass."
            
    menu :
        "> Reassure." if not rest2_asked1: #chance to gain closeness
            $ rest2_asked1 = True
            m "Just a hobby? But you're the president of the cooking club!"
            
            p "Titles don’t really mean a whole lot, you haven’t even tried my cooking."
            
            menu :
                "I feel like there’s a pretty easy solution to that." : #stat requirement to say? (+2)
                    $ girl1.add_closeness(2)
                    
                    "> Mary leans forward. Her eyes are on you as she smirks."
                    
                    p "Well, don't expect much if I cook all by myself."
                    
                    m "Haha, I doubt I'll be much help to you. You're on your own!"
                    
                    "> The two of you joke together. Mary playfully punches your shoulder as the two of you roll back laughing in your seats."
                
                "Joke" : #-1
                    $ girl1.add_closeness(-1)
                    m "Yeah I guess. I mean, how many people even ran for president anyway?"
                    
                    p "Yeah, right..?"
                    
                    "> Mary forces a smile."
                
                "You’ve tried mine. We should make something together, and you can teach me a few things.": #(+1)
                    $ girl1.add_closeness(1)
                    p "Sounds like a fun time. Haha, alright then."
                    
                    "> Mary smiles as you two think of things to make together."
                    
            jump restaurant_date2
                
        "> Question." : #backstory opener
            m "It seems like cooking means a lot more to you. You seem upset. What's wrong?"
            
            jump mary_backstory2
            
label mary_backstory2:
    "> Mary rolls her eyes, she sits back in her chair, while letting her posture sink and her sight drops to her glass."
    
    p "I know she means well, and it’s not like she’s being mean about it. I just feel this pressure not to disappoint her? I don’t even know why I’m telling you all of this. I’ve only known you for a couple days, sorry."
    
    m "Honestly Mary, don’t worry I’m completely fine with it. Have you ever told her how you feel about cooking?"
    
    p "I’ve sort of suggested being a chef, but she avoids really talking about it much. she redirects the conversation, or tells me that 
       “It would be better to keep it as a hobby.”... My dad was a chef, and my mom loved him, but she would sometimes get worried that he was a little too invested in his passion for cooking. 
       When he had holidays, brought me into the kitchen, and taught me how to cook. I really loved those moments, and that’s when I fell in love with cooking hehe..."
    
    m "What about your dad? what does he think?"
    
    "> Mary pauses for a moment. She takes a prolonged deep breath."
    
    p " He would have said “do it!” He was the nonchalant character that brought life to the family. 
        My mom and dad were a strange couple, they both worked hard, but it’s funny cause my mom was the bread-winner, my dad baked the bread. hahaha... 
        But he’s not here to say that anymore..."
    
    m "I'm really sorry to hear that..."
    
    p "Thanks. I was about 14 at the time, so I’ve come to accept it… He really loved his work. Sometimes my dad would work 16 hours a day, prepping the restaurant, and working late. "
    
    p "The doctors said that he needed to take more breaks or he may suffer from stress, but my dad is the kind of guy who wouldn’t accept that. He had a heart attack, and it almost seemed out of the blue. 
       It turns out the stressed caused high blood pressure and lead to heart failure."

    p "My mom and I were devastated. Cooking for me lets me keep a memory of him living. I think for my mom, seeing me cook, just reminds her of a passion that took dad away."
    
    m "{i}What should I say to her?{/i}"
   
    menu: # choices should not decrease stats at this point of date
        "Keep cooking a secret." :
            
            m "You should continue pursuing a professional career to keep your mom happy. But try to keep cooking as a secret hobby for as long as possible so you can keep doing what you love."
           
            "> Mary smiles a little, but doesn't seem satisfied."
            
            p "Haha, maybe you're right. But having to keep this a secret forever doesn't seem possible."
            
            "> Mary goes silent for a moment. She doesn't seem to be feeling well." 
            
        "Don't listen to your mom." :
            m "It’s really considerate of you to try and make your mom happy, but I think you deserve to be happy too, even if it means going against her wishes."
            
            p "But how can I have happiness without my mom’s approval? She’s still important to me so her wishes are important as well...."
            
            p "...Sorry. I know you're just trying to help. That means a lot to me. Thanks."
            
            "> Mary goes silent for a moment."
            
        "Talk to your mom about it.":
            $ girl1.add_closeness(2)
            m "It sounds like you’re pretty torn and I think expressing your feelings towards your mom would be a pretty good step forward. She probably wants you to be as happy just as much as you want her to be happy."
            
            "> Mary looks contemplative. Her expression turns sour."
            
            p"No…I can’t. You don’t know my mom. She would never understand. This is important to me. What if I end up losing all of it? I wouldn’t be able to…"
            
            "> Mary looks like she's on the verge of tears."
            
            p "..I'm sorry."
    
    "> You comfort Mary. After a while she seems to recover and insists that she is okay. You both continue talking about different subjects, but she seems distracted."
    
    p "Hey.. thanks for today. I'm glad we got to spend more time with each other. It feels good talking to you about my problems."
    
    p "Well.. Have a goodnight."
    
    m "Goodnight."
    
    "> Mary gives you a warm smile before turning around. The two of you part ways in front of the restaurant."
    
    m "{i}Was she really okay..?{/i}"
    
    jump return_to_which_day
            
#label restaurant_ending:
    
#label restaurant_badending:
    

#==================================================================================================================================================================
label girl1_home_date:
    m "I remember you mentioned before that I never tasted your cooking. If it’s okay with you, I’d really like to try some today."

    p "Oh, so you did remember!" 

    "{i}she seems shy but happy{/i}"

    p "Then, why don’t we go back to my house? I have all the ingredients there."

    "You and Mary head back to her place. You feel tenser than usual, despite the fact you’ve recently spent a lot of time with her. In the corner of your eye you catch her peeking slightly in your directly, but she immediately redirects her vision forward after being noticed."

    p "Today is really beautiful, although I don’t know what we’d do if there wasn’t a breeze."

    "As you approach her house, your eyes follow her as she leaps ahead. She moves forward and her hair swings, and pushes a scent towards you, pleasantly resonates with the core of your body"

    "For a second you get hung on the scent for a moment as you’re both entering, and you have a blank stare. She turns to notice you"

    #(o.o) face
    p "You look like you’re lost"

    m "E-ehh "

    "{i}you shake your head, but flustered you don’t know how to recover smoothly{/i}"

    # :) face
    p "hehehe, the kitchen is this way"

    "She leads you into the kitchen, and immediately moves to the different corners of the kitchen, in an a rehearsed efficiency. You pick up some newspapers to attempt helping"

    p "No, not there hahaha"

    "she pulls them out of your hands and sets them aside, then turns to you"

    p "Everything is set! What do you want to eat?"
    call girl1_home_date_choice

    #mom drama stuff
    "{i}Doorbell rings{/i}"

    mom "Hey Mary, I’m home from my business trip!"

    p "Oh crap, my mom is home. Hi mom!"

    "{i}Mom sees you{/i}"

    mom "Who is this, Mary? Why are you guys alone together?"

    p  "Uh, this is my friend, <insert name>. We are just hanging out after school mom. There is nothing to worry about."

    mom "You shouldn’t be inviting people over when I’m on a business trip. Shouldn’t you be studying too? It’s a school night!"

    p "I-I just wanted to relieve some stress, it’s just a little bit of cooking."

    "the discussion gets heated, and you stand there as if you are not even in the room"

    mom "Mary, you should be using your time more wisely. What happen to the money i gave you to buy food with? You should be focusing on getting into university, so you can get a career. You spend too much time in that cooking club, or whatever."

    p "I didn’t use it; it is still in your office. What if I wanted to be a chef? Like dad?"
    "Her mom, is taken back for a moment"

    mom "…Don’t you remember what happened to your father? I can’t let that happen to you, Mary, I can’t lose both of you like that. "

    p "What happen to dad was unfortunate, but.."

    mom "No buts! Don’t try to argue with me. Escort your friend out and then go to your room."

    menu:
        "Leave the house":
            "GG"
            return
            #replace return with jump to game over screen
        "Talk to mom":
            m "Can I speak with you in private?"
            mom "Fine."
            "Mary leaves"
            m "I may not know what happened to your husband and I understand where you are coming from, but I don’t think you are approaching the right way. "
            mom "Are you trying to tell me what to do?"
            m "No, but I just want to tell you about my experience. My parents wanted my older brother to go into medicine and put a lot of pressure and expectations on him. "
            m "Because of this, he unfortunately got a stress induced heart attack and passed away. Even when he was studying medicine, he was not happy and did not feel like he was living life. "
            m "My parents have learnt the hard way that letting your child follow their passion is the best for their lives. "
            m "Letting Mary pursue her passions of cooking will help her de-stress from school and there are plenty of jobs in the food industry! She has the talent for it!"
            "{i}mom is speechless{/i}" 
            "Moments later, she goes upstairs to get Mary"
            mom "Is cooking your passion in life?"
            p "Yes"
            mom "I will let you continue your cooking has a hobby on one condition. You keep your school marks up."
            p "Of course. Thank you mom!"
            mom "Go have fun cooking"
            "Mary goes back in the kitchen; Mom goes into her office"

    "It feels a little weird.What should you do?"
    menu:
        "Sit in the living room and play video games":
            p "Ehhh… I’d be nice if you helped me out" #:S face
            m "Oh! sorry about that"
            "{i}You rush to the kitchen, you aren’t really good at this are you?{/i}"
            #negative
        "Go into the kitchen and offer your assistance":
            label girl1_home_date_kitchen:
                m "Let me help you, Mary."
                p "Sure! can you preheat the oven for me?"
                #positive
                "you agree and you continue to be on the side and help her where you can."
                "as she carefully measures dry ingredients from a 20kg flour bag, the wet ingredients are your responsibility."
                "{i}The parts start to come together as you both share each other’s presence. once in a while her elbow brushes against yours.{/i}"

                p "Oh sorry <she looks up at you for a brief moment and catches your eye"
                m D"on’t apologize, it’s alright." 
                "{i}Her eyes widen slightly, but immediately both of you look away and refocus on the preparations.{/i}"
                "{i}in the corner of her eye, you see a bead of sweat trailing down from her temple to the front of her neck. You see her cheeks flooded with red.{/i}"
                "{i}This makes you blush too, and your breaths seem shallower{/i}"
                p "WOW! it’s getting hot in here! oh my! how hot did you preheat that oven??"
                "{i}she looks at the temperature{/i}" 
                p "Oh! look 350 degrees, perfect! and wasn’t it hot today?" 
                "{i}frantically she wipes her sweat, but knocks her bowl of flour off the table. Luckily your reactions catch the bowl, but leave the flour across the floor.{/i}"
                p "OH NO! ahhh…."
                menu:
                    "somebody’s got a lot of cleaning to do":
                        $ girl1.add_closeness(-1)
                        #negative
                        p "just get me more flour"
                    "It’s okay, don’t worry! I’ll grab you some more flour.":
                        $ girl1.add_closeness(1)
                        #positive
                        "IN THIS BLOCK"
                "{i}you struggle with the heavy flour bag, trying to get it level with the counter. You release the weight of the bag in front of her.{/i}"
                "{i}You failed to realize that the top of the bag was open, releasing a shower of flower that covers her face and yours, as you both look up to see the flying ingredients{/i}"

                m "You got some… umm flour all over you"

                "{i}You brush the flower off her shoulders, as you gently avoid making awkward physical contact.{/i}"

                p "Well… I could only assume, but my lenses are completely covered hahaha… I can’t see a thing."
                
                m "Here I got it for you"

                "{i}you lean in, as you lift the frames off her eyes.{/i}" 
                "Her brown eyes fixated on you. unprepared, you find your face lingering mere inches away from her’s."

                menu:
                    "{b}JUST DO IT!!{/b}":
                        "maybe it’s something in the air, besides flour, but you didn’t decide to take the relationship one step further, you want the leap of faith."
                        "{i}you wipe the flour off her cheeks, and find your hands resting on the back of her neck{/i}"
                        "{i}Before you know it, your hand pulls her towards you. Anticipation building, you close your eyes.{/i}"
                        "{i}you feel something press against your lips{/i}"
                        "{i}...{/i}"
                        "{i}something doesn’t feel right. As you open your eyes you find your mouth, cupped by her hand. Mary eye still wide opening, smiling{/i}"

                        p "I may not be able to see that well without glasses, but I’m not blind. Don’t get me wrong, I can’t deny that I have feeling for you, but let’s take it slow. ;) LMAOOO"

                        "{i}she lifts your hands off of her, she holds you palm open and examines it. You both turn slightly towards the counter to face shoulder to shoulder.{/i}"
                        "{i}still examining your hand, she places her hand on top of your’s as if comparing hand sizes{/i}"

                        p "you know, you have pretty soft hands. I think I’ll hold on to them for a while."

                        "{i}both her and your hands begin to offset a little, you decide not to resist, progressing to interlock fingers.{/i}"
                        return #replace with jump to win screen
                    "Go back to baking":
                        "{i} You pull away to avoid embarrassment{/i}"
        "Look around for any photo albums that she may have":
            "you stray away from the kitchen and walk along the line of photos, many of them focused around Mary as a child. "
            "In the photos that you look skim across, many of them almost bleak, she has no expression. Soccer team, School class photos, Academic achievement photos, in none of them she is smiling."
            "You pick one with her flour all over her face as a kid, her glasses caked in powder, but her smile being the only distinguishable thing."

            "{i}Mary glances over{/i}"
            p "Ek! nooo! that’s such an embarrassing picture of me!"
            m "HAHAH, Really? I think it’s pretty cute"
            "{i}Her cheeks grow red from being flushed{/i}"
            p "D-don’t say things like that!" 
            "{i}even with this statement, she holds back a smile{/i}" 
            p "Are you going to help me bake or what?"
            menu:
                "Yes":
                    jump girl1_home_date_kitchen
                "Why is this the only happy photo?":
                    p "I don’t really know. This is the first time when my mom let me bake all by myself, but I ended up dropping the flour bag, and made a huge mess all over the place." 
                    p "Nothing else really excited me that much. I didn’t do that many extra curriculars, and any I ended up signing up for got in the way of school." 
                    p "My parents really wanted me to do get good grades, so I never stayed in an activity for more than a couple months." 
                    p "But I mean, I get where they're coming from, I have to do well in school, or else I can’t get into university, get a job, and marry some guys with a stable job. How will I help support the kids I’ll have?"

                    "{i}you say something supportive{/i}" #replace
                    p "haha… you always have the right thing to say… most of the times :P"
                    "{i}she grabs on to your arm and brings you back to the kitchen{/i}"
                    jump girl1_home_date_kitchen

    jump end_day_1 
    #return


label girl1_home_date_choice:
    menu:
        "Chimichurri Rack of Lamb" :
            p "Wow! Your taste is pretty extravagant huh?"
            menu:
                "You don’t have to cook it if you don't want to.":
                    p "You don’t think I can do it?"
                    p "I’ll prove you wrong. "
                    $ girl1.add_closeness(-1)
                    #negative
                " I really want to eat this.":
                    "{i}Mary seems intimidated by the challenge but finds her resolve.{/i}"
                    "I’ll do my best!"
                    $ girl1.add_closeness(1)
                    #positive/neutral 
        "Instant noodles":
            p "Common..are you taking my offer seriously here?"
            #negative
            call girl1_home_date_choice
            return
        "Triple Layer Chocolate Cake":
            "{i}She seems surprised by your request{/i}"
            p "I thought you’d choose something harder. Why did you choose a cake?"
            menu:
                "I didn’t want you to work too hard.":
                    p "What? Don’t worry so much...I can handle it. But alright, if that’s what you want."
                    #negative
                "So we can share it when you’re done.":
                    p "Are you usually this corny? haha. But alright, if that’s what you want."
                    #neutral 
                "I already know how great your cooking skills are. So i want you to make me something that’s meaningful.":
                    p "Meaningful?"
                    m "Each layer of the cake represents each place we’ve spent time together and how far we’ve come building on our relationship. One layer at a time."
                    p "{i}blushiesssssss{/i} O-oh." 
                    "{i}Mary seems flustered but pleased by your thought.{/i}"
                    p " Alright, I-I’ll get started then" # :) face
                    #positive
    "Mary goes begins cooking the dish and you’re left sitting in her living room alone."
    return 

# -----------------------------------------------------------------------------------------------------------------

label return_to_which_day:
    $ day = stats.get_days()
    if day == 1:
        jump end_day_1
    elif day == 2:
        jump day_2
    elif day == 3:
        jump day_3
    elif day == 4:
        jump day_4
    else:
        jump day_5

label day_5:
    
    "Another day at school..." 
    $ stats.reset_classes()
    call make_schedule
    jump girl1_failure
    
label girl1_failure:
    
    "GAME OVER"
    # failed, end game here
    return
                

#the main daytime routine.
label daytime:
    $ stats.days += 1
    $ temp = stats.days
    "this is the daytime routine (Day %(temp)d)"
    call raisestat #go to raisestat routine

    if stats.days < 5:
        jump daytime #jump to daytime again

    "ya out of time"

    return #end game

#routine for raising stats
label raisestat:
    call randomquiz
    menu:
        "What Stat to raise"

        "Strength":
            $ stats.add_stats("str",1)
            $ temp = stats.get_stats("str")
            "strength is now [temp]."
        "Intelligence" if stats.get_stats("str") > 1: 
            $ stats.add_stats("int",1)
            $ temp = stats.get_stats("int")
            "intelligence is now [temp]."
        "Charm" if stats.get_stats("str") + stats.get_stats("int") > 3:
            $ stats.add_stats("cha",1)
            $ temp = stats.get_stats("cha")
            "charm is now [temp]."
    return 

