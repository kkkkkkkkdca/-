
label welcometoHungwood:
    scene bg forestpathday
    $ RodinPose = 1
    show rodin neutral at center
    with fade
    "After a long and profitable journey, the merchant [player_name] is grateful to see Hungwood Village draw near.  As much as he loves to be a traveling merchant, his home village always calls to him."
    show rodin smile
    #$ rodinpose = "pants"
    "There’s nothing better than catching up with friends at the inn and recuperating in his own cottage at the end of the day."
    "His herb garden needs tending to, no doubt.  But his best friend, Dorik, helps mind it for him while he’s away."
    $ RodinPose = 4
    show rodin thoughtful
    "Maybe he can find a hunky guy to sleep with tomorrow?  There were a few good options.  Hungwood Village was the capital of the land of Hungwood, after all."
    FE "Stop right there, Handsome!"
    $ RodinPose = 3
    show rodin shocked at sprite25 with move
    play sound "Cinematic stinger.mp3"
    show fireelement evilsmile at sprite45 with dissolve
    with hpunch
    play music "BattleMedium.mp3" fadeout 3.0 fadein 2.0
    "A Beefy Fire Elemental leaped into the road before him!"
    "[player_name] is shocked and concerned.  Enemies of this sort have never been this close to Hungwood Village before."
    "Why hadn’t the heroes cleared the area?"
    $ RodinPose = 1
    show rodin neutral
    "Perhaps he’s a friendly one?  Those who live in peace with the villagers are of course welcome—and are usually up for a bit of fun."
    "[player_name] would remain unsure of his intentions until his first move.  Then he could decide whether to kill him for his loot or seduce him for some fun."
    FE "Ah ha ha!  All alone, hmm?  Heh heh heh heh!  And you’re a fine one, aren’t you?  Big and strong...just how I like ‘em!"
    "Well...that didn’t clear up his motives, but at least he was open to {i}some fun{/i}."
    FE "You wouldn’t know where I could find Dorik the Dwarf, would you?  Tell me, and I’ll make your death quick!"
    $ RodinPose = 3
    show rodin shocked
    "Dorik--?  He’s looking for his close friend Dorik?!"
    $ RodinPose = 2
    show rodin angry
    Rodin "What do you want with Dorik?"
    FE "Ahh!  So, he does live here!  Tell me where he is.  Now!"
    Rodin "Absolutely not."
    FE "You’ll tell me or I’ll burn you where you stand!"
    $ RodinPose = 2
    show rodin sneer
    "That settled it.  He needed to take out this enemy before he can find his friend."


    $ lust_battle = True
    $ fire_element = FireElement()
    scene bg uouui
    show rodin_sprite:
        xpos 630 ypos 250
    show fire_element_sprite:
        xpos 970 ypos 250
    with dissolve
    play sound "Cinematic stinger.mp3"
    pause 0.5
    Rodin "What is your kind doing so close to our village in the first place?"
    FE "I’m not leaving until I find Dorik the dwarf!  C’mon, Sexpot, tell me where he is!"
    "He obviously wasn’t going to help him find Dorik, but still, [player_name] might be able to seduce the fight out of him.  That was often better than killing needlessy—and a hell of a lot more fun."
    "That approach did pose its own risks, however.  As strong as [player_name] was, if too many enemies managed to seduce {i}him{/i} he would become an enemy himself!"
    "No, he would always try to control things if he went the seduction route.  Then again—just killing him outright was always an option."
    #"At least then he’d be sure he wouldn’t harm Dorik, and [player_name] would get some loot out of the bargain."

    $ tutorial_step = 1
    $ tutorialdone = False
    menu:
        "See Battle Tutorial":
            pass
        "Skip Battle Tutorial":
            $ tutorial_step = 13
            $ tutorialdone = True

    pause 0.1
    hide rodin_sprite
    hide fire_element_sprite
    call setup_fire_element from _call_setup_fire_element
    $ reset_floating_numbers()
    
    $ reset_effects()
    $ rodin.reset_all_cooldowns()
    $ rodin.clear_all_status()

    hide screen actor_overlay
    
    $ reset_effects()
    
    python:
        final_of_battle(all_allies)

        defeated_enemies = [e for e in enemies if (not e.alive) or getattr(e, "lusted_out", False)]
        xp_reward = sum(e.xp_reward for e in defeated_enemies) # XP total somado
        rewards = []

        if xp_reward > 0:
            party_gain_xp(xp_reward)
            add_reward("xp", xp_reward)
            
        for e in defeated_enemies:
            give_loot_for_enemy(e, rewards, inventario)
        rewards = consolidate_rewards(rewards)

    if battle_result == "victory":
        play sound "69_Enemy_death_01.mp3"
        $ total_items = len(rewards)
        $ last_index = total_items - 1
        $ anim_time = 2.0
        $ delay_per_item = 0.5
        $ total_time = (last_index * delay_per_item) + anim_time
        
        play sound "LootSound03.mp3"
        
        show screen reward_list_center(rewards)
        pause total_time
        hide screen reward_list_center
        "The Fire Elemental has been vanquished!"
        hide screen battle_sprites with dissolve
        hide screen turn_order_display
        hide screen actor_overlay
        scene bg forestpathday
        $ RodinPose = 1
        show rodin neutral at sprite3
        play music "NeutralFast.mp3" fadein 2.0
        with fade
        
    elif battle_result == "lust_victory":
        $ lust_battle = True
        hide screen turn_order_display
        hide screen actor_overlay
        $ total_items = len(rewards)
        $ last_index = total_items - 1
        $ anim_time = 2.0
        $ delay_per_item = 0.5
        $ total_time = (last_index * delay_per_item) + anim_time
        play sound "LootSound03.mp3"
        show screen reward_list_center(rewards)
        pause total_time
        hide screen reward_list_center

        battlesign "You have seduced the Fire Elemental!"
        
        hide screen battle_sprites with dissolve
        $ quick_menu = True
        call final_fire_lust from _call_final_fire_lust_1

    elif battle_result == "lust_defeat":
        hide screen turn_order_display
        hide screen actor_overlay
        $ rodin_outlust += 1
        $ temp_math = 10 - rodin_outlust
        "[player_name] has been seduced by the enemy!  [temp_math] more times and he will become an enemy himself!"
        hide screen battle_sprites with dissolve
        $ rodin.lp = 0
        $ rodin.lusted_out = False
        $ quick_menu = True
        call final_fire_lust from _call_final_fire_lust_4

    elif battle_result == "defeat":
        hide screen turn_order_display
        play sound "17_Def_buff_01.mp3"
        "You have succumbed to your injuries."
        hide screen battle_sprites with dissolve
        jump game_over

    elif battle_result == "escape":
        hide screen turn_order_display
        hide screen battle_sprites
        hide screen actor_overlay
        show rodin_sprite:
            xpos 630 ypos 250
        show fire_element_sprite:
            xpos 970 ypos 250
        pause 0.5
        "You escaped the enemy."
        hide rodin with dissolve
        play sound "51_Flee_02.mp3"
        pause 0.5
        scene bg forestpathday
        $ RodinPose = 1
        show rodin neutral at sprite3
        play music "NeutralFast.mp3" fadein 2.0
        with fade

    $ quick_menu = True
    hide screen show_floating_number
    jump VNContinues


label VNContinues:
    $ RodinPose = 4
    show rodin thoughtful
    "The encounter left [player_name] addled.  Why was that enemy hunting his friend Dorik?"
    $ RodinPose = 1
    show rodin neutral
    "He was formidable—an actual elemental.  Anyone who encountered him without skill would have been killed."
    $ RodinPose = 4
    show rodin thoughtful
    "Again he wondered where the heroes were.  The traveling adventurers who rested in Hungwood’s inn and bought items from the many vendors there—himself included."
    "How could they have missed a Fire Elemental?"
    $ RodinPose = 1
    show rodin neutral
    "He took a sobering breath and pressed on."
    hide rodin with dissolve
    "While he was eager to head home and rest, he decided to visit Dorik first.  Perhaps he knew what was going on."
    
    $ DorikPose = 2
    scene bg blacksmith with fade
    show minoc neutral at sprite15 with dissolve
    show dorik neutral at sprite3 with dissolve
    "[player_name] was also eager to report his sales to his best friend.   It was his first time on the peninsula, after all, and a risk they’d both agreed to."
    $ RodinPose = 1
    show rodin smile at sprite5 with dissolve
    Rodin "Ho, Dorik!  I’ve returned.  It’s good to see you again."
    $ DorikPose = 5
    show dorik shocked
    Dorik "Bowels and craters! [player_name]! Thank the gods you’re back in one piece!"
    $ RodinPose = 3
    show rodin shocked
    "[player_name]’s smile faded at once.  This was not the pleasant reunion he expected."
    Rodin "Why would you say that, my friend?"
    $ DorikPose = 1
    show dorik sad
    Dorik "Oh, there’re dark things afoot in Hungwood!  It grows more dangerous by the day!"
    Dorik "Enemies stalk the streets in broad daylight! Livestock’s been raided, cabins pillaged! By my beard, it’s been madness!"
    $ RodinPose = 1
    show rodin sad
    "[player_name] kept his gaze steady while absorbing the desperation in Dorik’s voice.  This was a mighty, runecasting dwarf, who feared little.  For him to be so troubled..."
    Rodin "What...what of the heroes?"
    $ DorikPose = 5
    show dorik shocked 
    Dorik "They’re gone!  We know not where, or even when.  But they’ve been gone long enough for all manner of scourge to run rampant in our village."
    $ RodinPose = 4
    show rodin thoughtful
    Rodin "But...how can this be?  If there was an enemy mighty enough to defeat them, we would have heard of it."
    $ DorikPose = 1
    show dorik sad
    Dorik "I’ve as many questions as you have, my friend.  I don’t know what to do!  Things have never been so grave in Hungwood."
    Dorik "This may not be the land of my birth, but, by gods, it became the land of my heart!  I’ll not let it fall to ruin."
    $ RodinPose = 1
    show rodin sad
    Rodin "Damn."
    "[player_name]’s stomach tightened with dread.  Enemies were not just on the road to his dear village, but within the village itself.  How could this have happened?"
    $ DorikPose = 2
    show dorik neutral
    Dorik "You heard nothing during your travels?  How was the journey to the peninsula?"
    "[player_name] swallowed some spittle down a tightening throat."
    $ RodinPose = 1
    show rodin neutral
    Rodin "I thought it was a wonderful trip.  I completely sold out of everything you made for me."
    Dorik "Good, good.  At least one thing went right."
    "[player_name] pursed his lips."
    Rodin "I...see you have a new apprentice?"
    $ DorikPose = 5
    show dorik shocked 
    Dorik "Bowels and craters!  Right, of course.  This damnable menace has me acting like a blasted ogre!"
    $ DorikPose = 2
    show dorik neutral
    Dorik "This is Minoc, the best apprentice in all the 9 realms.  Minoc, this is my good friend and merchant partner [player_name].  He’s helped me through some dark times, and I’d gladly lay my life down for him."
    $ RodinPose = 1
    show rodin smile
    Rodin "A pleasure to meet you."
    show minoc mouthopen
    Minoc "And you."
    $ RodinPose = 1
    show rodin neutral
    "The minotaur managed a smile despite the concern in his eyes.  The troubles of the village must have weighed upon him also."
    show minoc neutral
    "[player_name] tried to lighten the mood."
    $ RodinPose = 1
    show rodin smile
    Rodin "Best apprentice in all the 9 realms, hm? That’s high praise indeed coming from Dorik."
    Minoc "I’ve been really eager to prove myself.  I’ve dreamed of training under a dwarven master since I was a calf. I just hope I can keep up."
    $ DorikPose = 2
    show dorik smile
    $ RodinPose = 1
    show rodin neutral
    Dorik "The bull’s too modest. His work is nearly as good as mine, and in such a short time!  I can even trust him to run things on his own most days."
    $ RodinPose = 1
    show rodin smile
    Rodin "Wonderful.  Then you’ll have double the goods for me to sell next time."
    $ DorikPose = 1
    show dorik sneer
    Dorik "You’re off your crock, [player_name]! Who can think of  trade at a time like this?  I tell you, the walls are falling in on us!  Not even the streets of Hungwood Village are safe!"
    $ RodinPose = 4
    show rodin thoughtful
    Rodin "You’re right.  I guess the reality of this mess hasn’t sunken in yet. I...I hesitate to tell you this, but..."
    $ RodinPose = 1
    show rodin neutral
    Rodin "I ran into a Fire Elemental on the road to the village.  Dorik--he was looking for you."
    $ DorikPose = 5
    show dorik shocked
    Dorik "For me?!  By my beard--why?!"
    Rodin "I don’t know.  I didn’t get that far.  I just had to subdue him however I could."
    $ DorikPose = 5
    show dorik shocked
    Dorik "A blasted fire elemental of all things?  Not a wraith nor a wisp but an elemental?!  Good gods!  Those are the last kinds of customers I need!"
    $ RodinPose = 1
    show rodin sad
    Rodin "It took the breath out of me to see such a thing so close to our village. I never had a reason to feel so...{i}unsafe{/i} in Hungwood.  I’d hoped it was just a freak occurrence."
    $ DorikPose = 1
    $ DorikFireBeard = "visible"
    show dorik angry
    Dorik "By the gods, no!  There’s all sorts of wicked things infiltrating us!  Without the heroes, our poor village guardian can’t keep up."
    $ RodinPose = 1
    show rodin sad
    Rodin "It sounds as though I’ve no choice but to help with this menace.  But how much good can I do if the heroes are truly gone?  You know how I feel about...{i}adventuring{/i}."
    $ DorikPose = 1
    $ DorikFireBeard = "invisible"
    show dorik sad
    Dorik "I know of your misgivings well enough, but there’s no helping it.  You’re too good a man to let Hungswood fall into a pit of mire!"
    Dorik "I’ll stand with you, by gods! I can still cast a rune and throw a hammer.  We’ll go on patrol together."
    $ RodinPose = 1
    show rodin neutral
    Rodin "I’ll be a lot less miserable with you at my side.  Still, the enemies will just keep coming if we don’t find out what’s happened to our heroes."
    $ DorikPose = 1
    show dorik sneer
    Dorik "Oh, it’s a damnable situation to be sure.  Those heroes kept us so safe we took them for granted.  Now they’re all gone!  It’s like they vanished into thin air!"
    $ DorikPose = 2
    show dorik neutral
    Dorik "...But never mind that for now.  You’ve had a long journey, [player_name].  Go home and rest a night at least.  We’ll make better sense of this in the morning."
    "[player_name] nods while sighing deeply.  He’d expected to relax for a week, collect more goods from Dorik, and then head back out to the southern villages."
    "Now it seemed even a meager leaf-caster such as him was one of the few remaining who could protect his village."
    "He’s a merchant, not a hero nor even an adventurer.  It’s true he’d mastered a bit of leaf-casting to guard his wares on the road, but he can’t stand up to the kind of enemies the heroes tackled."
    "{i}And he didn’t want to.{/i}"
    "His head was going in circles, but the shadows were growing long.  He had to get home before it was too dark."
    Rodin "What a mess.  I’ll see you tomorrow to reckon with—all of this."
    Dorik "Rest well, and do be careful!"
    hide rodin with dissolve
    Rodin "Goodbye, Dorik.  Minoc."
    $ DorikPose = 1
    show dorik sad
    Dorik "Fuck."
    scene bg villagenight with dissolve
    "As much as he’d dreaded it, night fell, and [player_name] was still not at his home."
    stop music fadeout 3.0
    "He used instinct to find his way in the dimness."
    play music "ForestNight.mp3" fadein 1.0
    show bg cabinnight with fade
    "When he drew near, he realized there was light coming from a window."
    play music "BattleMedium.mp3" fadeout 2.0 fadein 2.0
    $ RodinPose = 3
    show rodin shocked at sprite2 with dissolve
    "He froze.  No one should be in his home, and there was no chance an old fire was still burning.  He’d been gone for weeks."
    $ RodinPose = 4
    show rodin thoughtful
    "Perhaps a neighbor (as few as he had out here) had set up in his cabin to wait for him?  To warn him about the new threat?"
    hide rodin with dissolve
    "He crept around the back and chanced a peek into a window."
    "Then it was as if his chest seized.  This was no neighbor!"
    "An enemy had invaded his home!"
    "He sat on [player_name]’s couch with his heels propped on the axe-hewn table [player_name] had forged with his own two hands."
    $ RodinPose = 3
    show rodin shocked at sprite2 with dissolve
    "He stood in shock; his heart thundered and his mind raced. This was his sanctuary, his castle--a place he’d built and made perfect.  It was the only home that he’d owned outright."
    stop music fadeout 3.0
    "Who would dare violate him this way? This was Hungwood, damn it!  He’d never had to deal with an intruder before."
    $ RodinPose = 3
    show bg black with dissolve
    show rodin shocked at sprite3 with move
    Rodin "No--!"
    play music "SadBumper.mp3" fadein 2.0 noloop
    "But then he realized he had.  Oh gods...{i}he had{/i}.  And all at once the harrowing memory surfaced from where he’d buried it long ago."
    "He’d found the door of his childhood home...ripped off its hinges."
    "He’d dropped his firewood to run inside--"
    show rodin sad
    "And...and he saw...his mother...and his father..."
    "...mutilated..."
    $ RodinPose = 1
    show rodin sad
    "They lay slain on the cabin floor.  The gruesome site would be forever etched in his memory...along with the {i}laughter{/i}."
    play sound "HorrathLaugh.mp3"
    "Someone—some {i}thing{/i} was still there.  He heard it, but did not see it.  His ears rang with the vile criminal’s haunting laughter."
    "He was just a boy--a child.  What could he do?  There was...nothing.  Nothing except to run as far and fast as his legs would take him."
    "And to this day he’s left wondering: why?  For gods’ sake, why?!  His father was a lower druid, his mother a merchant."
    "Just...why?"
    $ RodinPose = 2
    show bg cabinnight with dissolve
    show rodin sneer at sprite2 with move
    Rodin "No."
    play sound "TenseFast.mp3" fadein 2.0 fadeout 3.0
    "[player_name] shook his head and snapped himself back to reality.  That was ancient history—and he was no longer a helpless boy."
    $ RodinPose = 2
    show rodin angry #Pan back out suddenly on this line.
    Rodin "No!"
    "This was his home. He’d worked hard to earn it, and he wouldn't give it up without a fight."
    $ RodinPose = 2
    show rodin sneer
    Rodin "Ho!  Intruder!  Come out and face me!"
    pause 1.0
    play sound "DoorSqueak.mp3" 
    queue sound "DoorSlam.mp3" 
    $ RodinPose = 2
    show rodin angry at sprite2 with move
    show bandit evilsmile at sprite4 with dissolve
    Bandit "Intruder, hm?  How do you know this isn’t my house?"
    Rodin "Because it’s {i}mine{/i}."
    Bandit "That so?  Nice place you got here.  I like the little herb garden out back.  Spiced up my meals real nice."
    Rodin "..."
    $ RodinPose = 1
    show rodin neutral
    Rodin "Look. I’ve had a long journey and need to rest.  Neither of us want this to end in bloodshed.  Just pack up your things and move on.  I’ll even help you."
    Bandit "Don’t be so hasty.  What say we share the cabin?  I wouldn’t mind shacking up with a stud like you.  Heh heh."
    show bandit sneer
    Bandit "Either way—I don’t plan on leaving."
    $ RodinPose = 2
    show rodin sneer
    "Right.  It seemed there was no helping it."
    hide rodin with dissolve
    hide bandit with dissolve
    pause 0.5
    $ rodin.lusted_out = False
    $ rodin.lp = 0

    python:
        bandit = BanditenemyA()

    show rodin_sprite:
        xpos 630 ypos 250
    with dissolve
    show bandit_idle_sprite:
        xpos 921 ypos 228 zoom 0.49 xzoom-1
    with dissolve
    stop music fadeout 2.0
    "[player_name] looked him over, and his heart began to race.  The man clearly had the mind of an enemy.  One too many had seduced him to their ways—but he could be made right with a little care. "
    "That was his best play.  This was a formidable foe, and [player_name] still suffered the effects of his first encounter."
    pause 0.1
    hide rodin_sprite
    hide bandit_idle_sprite
    $ battle_result = None
    $ reset_floating_numbers()
    play music "Battle2Medium.mp3" fadein 2.0
    call setup_bandit from _call_setup_bandit

    $ reset_effects()
    python:
        for ally in allies:
            ally.reset_all_cooldowns()

    hide screen actor_overlay

    
    python:
        final_of_battle(all_allies)

        defeated_enemies = [e for e in enemies if (not e.alive) or getattr(e, "lusted_out", False)]
        xp_reward = sum(e.xp_reward for e in defeated_enemies) # XP total somado
        rewards = []

        if xp_reward > 0:
            party_gain_xp(xp_reward)
            add_reward("xp", xp_reward)
            
        for e in defeated_enemies:
            give_loot_for_enemy(e, rewards, inventario)
        rewards = consolidate_rewards(rewards)

    if battle_result == "victory":
        hide screen turn_order_display
        hide screen actor_overlay
        $ bandit.pose("weak")
        $ total_items = len(rewards)
        $ last_index = total_items - 1
        $ anim_time = 2.0
        $ delay_per_item = 0.5
        $ total_time = (last_index * delay_per_item) + anim_time
        play sound "LootSound03.mp3"
        show screen reward_list_center(rewards)
        pause total_time
        hide screen reward_list_center

    elif battle_result == "lust_victory":
        $ lust_battle = True
        hide screen turn_order_display
        $ total_items = len(rewards)
        $ last_index = total_items - 1
        $ anim_time = 2.0
        $ delay_per_item = 0.5
        $ total_time = (last_index * delay_per_item) + anim_time
        play sound "LootSound03.mp3"
        show screen reward_list_center(rewards)
        pause total_time
        hide screen reward_list_center
        battlesign "You have seduced the Bandit!"

        hide screen turn_order_display
        hide screen actor_overlay
        show rodin_sprite:
            xpos 630 ypos 250
        show bandit_idle_sprite:
            xpos 921 ypos 228 zoom 0.49 xzoom-1
        pause 0.5
        hide screen battle_sprites with dissolve
        $ quick_menu = True
        call final_bandit_lust from _call_final_bandit_lust
        
    elif battle_result == "lust_defeat":
        hide screen turn_order_display
        hide screen actor_overlay
        $ rodin_outlust += 1
        $ temp_math = 10 - rodin_outlust
        "[player_name] has been seduced by the enemy!  [temp_math] more times and he will become an enemy himself!"
        $ quick_menu = True
        hide screen battle_sprites with dissolve
        $ rodin.lusted_out = False
        $ rodin.lp = 0
        $ quick_menu = True
        call final_bandit_lust from _call_final_bandit_lust_3

    elif battle_result == "defeat":
        hide screen turn_order_display
        play sound "17_Def_buff_01.mp3"
        "You have succumbed to your injuries."
        hide screen battle_sprites with dissolve
        jump game_over

    elif battle_result == "escape":
        hide screen turn_order_display
        hide screen battle_sprites
        hide screen actor_overlay
        show rodin_sprite:
            xpos 630 ypos 250
        show bandit_idle_sprite:
            xpos 970 ypos 250 zoom 0.47 xzoom-1
        pause 0.5
        "You escaped the enemy."
        hide rodin with dissolve
        play sound "51_Flee_02.mp3"

    $ quick_menu = True
    hide screen show_floating_number
      
    if battle_result == "victory":
        show bg cabinnight
        show rodin_sprite:
            xpos 630 ypos 250
        show bandit_idle_sprite:
            xpos 921 ypos 228 zoom 0.49 xzoom-1
    else:
        
        $ rodin.lp = 0
        show bg cabinnight
        show rodin_sprite:
            xpos 630 ypos 250
        show bandit_idle_sprite:
            xpos 921 ypos 228 zoom 0.49 xzoom-1
        with fade
        
    play music "Miniboss.mp3" fadeout 2.0 fadein 2.0
    if battle_result == "lust_victory":
        $ bandit = BanditenemyA()
        $ bandit.lp = 60
        Rodin "Thanks...thanks for that.  Good luck to you."
    Bandit "Heh heh heh, you think we’re leaving?"
    Rodin "...‘We’re’?"
    Bandit "You were real sweet.  Real obedient.  Now get lost."
    
    
    $ inventario.add_item(Timberfang, 1)
    $ grant_murag_skills(murag)
    $ murag.weapon = Timberfang
    $ murag.recalc_stats()
    $ active_murag = True
    $ all_allies = [rodin, murag]
    
    $ battle_result = None
    
    call setup_bandit_party from _call_setup_bandit_party
    
    if battle_result == "escape":
        pass

    $ battle_context = None
    $ quick_menu = True

    $ RodinPose = 3
    $ MuragPose = 1
    scene bg villagenight
    show rodin shocked at sprite2
    show murag shocked at sprite4
    with fade

    play music "Village.mp3" fadeout 1.0 fadein 2.0
    Murag "Damn!  That was close.  Good thing that shooting star got me wandering towards your place!"
    Rodin "It...it {i}was{/i} close. Thank you. You saved my life."
    $ MuragPose = 2
    show murag smile
    Murag "No problem!  That was fun! Plus that one bandit was naked. Did you see?  Ha ha ha!"
    $ RodinPose = 1
    show rodin smile
    Rodin "I’m [player_name]."
    Murag "The name’s Murag.  Pleased to meet you."
    Murag "I never knew elves could be as beefy as you--or hairy!"
    show rodin neutral
    Rodin "Er...I’m actually a human."
    $ MuragPose = 1
    show murag shocked
    Murag "Oh!  Right!  I forgot there were humans, too.  Well...that makes more sense."
    $ RodinPose = 4
    show rodin thoughtful
    Rodin "You said you had a camp near my cottage?"
    $ MuragPose = 2
    show murag flustered
    Murag "I mean—it’s a nice spot and close to a water source.  I wanted to stay near the village so I could check it out when I built my nerve up."
    $ RodinPose = 3
    show rodin shocked
    Rodin "Oh!"
    $ MuragPose = 1
    show murag neutral
    Murag "I’m kind of out on my own for the first time. I...uh...I didn’t really fit in with the rest of the tribe.  A while ago, I just got fed up and left."
    $ RodinPose = 1
    show rodin neutral 
    Murag "I didn’t know what to expect away from the tribe, but it couldn’t be worse than what I was going through.  What did I have to lose?"
    Rodin "That’s understandable."
    $ MuragPose = 2
    show murag smile
    Murag "I figured I’d do some adventuring.  Maybe make some new friends?  Seems like I’m off to a good start.  I mean, no way I’d want to do this all on my own.  I’m just...used to working in a group."
    $ RodinPose = 1
    show rodin smile
    Rodin "I’m happy to call you a friend, Murag.  I can’t believe how lucky I was to have you show up when you did."
    Murag "Right?  Must be fate!"
    $ RodinPose = 1
    show rodin neutral
    Rodin "And I’m glad to meet an adventurer.  There’s a need for your kind more than ever now."
    $ MuragPose = 3
    show murag thoughtful
    Murag "Oh yeah?  I thought there were plenty of us out here already, but I’d find a way to make it work.  It’s not like I could go back to my tribe."
    Rodin "You couldn’t?"
    $ MuragPose = 2
    show murag flustered
    Murag "Er...I mean...I didn’t want to.  Because I didn’t fit in.  That’s why I left."
    Rodin "Right."
    $ MuragPose = 1
    show murag neutral
    $ RodinPose = 1
    show rodin neutral
    Rodin "Things have changed.  There’s some kind of menace brewing.  That’s why there’s so many enemies now."
    $ MuragPose = 1
    show murag neutral
    Murag "Huh.  Maybe that’s good for me?  Or bad.  I don’t really know yet.  I just started.  Seems like fate is finally looking up for me—starting with your fight back there."
    Rodin "Follow me.  I’m friends with the village blacksmith.  I’ll fill you in on the way."
    $ MuragPose = 2
    show murag smile
    Murag "Lead the way.  And it can’t be all that bad.  I mean, I’ve been through worse."
    Rodin "You have?"
    $ MuragPose = 2
    show murag flustered
    Murag "Uh...I mean.  Back with my tribe.  When I didn’t fit in...like I said."
    Rodin "Oh."
    $ MuragPose = 2
    show murag smile
    Murag "But now fate dropped me into your fight, and I’m going to be fighting a menace.  Best day ever!"
    $ RodinPose = 1
    show rodin smile
    "The awkward orc’s enthusiasm was contagious.  [player_name] already liked him, and the {i}look{/i} of him.  Besides--he was right.  Things were finally looking up."
    stop music fadeout 3.0
    hide rodin with dissolve
    hide murag with dissolve
    "It was dark in the village, but [player_name]’s instincts were true.  He led the  orc to the shop and home of his best friend Dorik."
    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2

    scene bg black with fade
    scene bg insidedorikhouse with fade
    play music "Miniboss.mp3" fadeout 2.0 fadein 2.0
    Dorik "My hands...!"
    Dorik "Hands of fire!"
    Dorik "I did it for you!  Don’t you see?!"
    Dorik "I did it for all of us!"
    show minoc base at sprite35 with dissolve
    Minoc "Dorik?"
    Dorik "I did it for all of us!  But most of all you!  How can you be so cruel!  So ungrateful!  Damn you!"
    Dorik "HANDS OF FIRE!"
    stop music fadeout 1.0
    show minoc mouthopen
    Minoc "Dorik!  Wake up!"
    Dorik "...What?  What in blazes?!"
    show minoc base
    Minoc "Dorik...may I enter your room?"
    Dorik "...Minoc?"
    $ DorikPose = 1
    show dorik sad at sprite15 with dissolve
    Minoc "Are you okay?  I think you were having a nightmare."
    Dorik "No.  Not a nightmare."
    Dorik "Night terrors."
    Dorik "Had them for years, by the gods."
    Minoc "Oh."
    Dorik "But they stopped.  I thought I was getting better."
    Dorik "It’s this blasted menace."
    Dorik "It’s triggered them all over again."
    Minoc "Of course.  We’re all on edge now."
    play sound "Knocking.mp3"
    $ DorikPose = 5
    show dorik shocked
    Dorik "Who could that be?! It’s the middle of the night?!"
    hide minoc with dissolve
    Minoc "I’ll go see."
    $ DorikPose = 2
    show dorik neutral
    Dorik "Be careful!"
    pause 1.0
    show dorik neutral at DorikSprite1 with move
    show rodin neutral at sprite04 with dissolve
    show murag neutral at sprite65 behind rodin with dissolve
    show minoc base at sprite55 behind dorik with dissolve
    play music "Sad.mp3" fadein 2.0
    Rodin "I’m sorry to burst in on you like this, Dorik.  My house was taken over by enemies.  I had to flee."
    Rodin "These enemies wouldn’t go down.  They’re more wicked and brazen than they’ve ever been."
    $ DorikPose = 1
    $ DorikFireBeard = "visible"
    show dorik angry
    Dorik "Damn these evil scum!  I knew things had gone to hell!  Taking over people’s homes like they own them!"
    Rodin "If it wasn’t for Murag stepping in, I’d be dead."
    $ DorikPose = 2
    $ DorikFireBeard = "invisible"
    show dorik neutral
    Dorik "Thank you, Murag.  Any friend of [player_name]’s is a friend of mine."
    $ MuragPose = 2
    show murag smile
    Murag "Wow!  Two new friends in one day!  And I got to see a bull person!  I didn’t know there were bull people!"
    Minoc "I’m Minoc, Dorik’s apprentice."
    Murag "Pleased to meet you!"
    $ DorikPose = 1
    show dorik sad
    Dorik "But what are we to do?  The villagers are defenseless against enemies like that."
    $ MuragPose = 1
    show murag neutral
    pause 1.0
    Minoc "Whenever we’ve had trouble before we’ve always gone to the village guardian.  Gildrath."
    $ DorikPose = 2
    show dorik neutral
    Minoc "I bet he knows the source of the menace.  And if he doesn’t, he can use his dragon rune magic to ask the Ancients for answers."
    $ RodinPose = 1
    show rodin smile
    Rodin "Of course.  If anyone knows what’s going on it will be our guardian."
    Dorik "Then that’s what we’ll do.  In the morning."
    show rodin neutral
    Dorik "Come, I’ll find a place for you both to rest.  You must be exhausted, [player_name]."
    Rodin "Thank you, my friend."
    hide dorik with dissolve
    hide rodin with dissolve
    hide minoc with dissolve
    stop music fadeout 3.0

    $ MuragPose = 2
    show murag smile
    Murag "Wow, this is such a great house.  Is this your guild banner?  I’ve heard of guilds before."
    $ MuragPose = 1
    show murag flustered
    Dorik "Come, Murag!"
    pause 0.5
    hide murag with dissolve
    scene bg black with fade
    centered "{cps=20}{size=+15}The next morning...{/size}{/cps}"

    $ rodin.alive = True
    $ rodin.set_pose("idle")
    $ rodin.hp = rodin.get_stat('hp_max')
    $ rodin.mp = rodin.get_stat('mp_max')
    $ rodin.lp = 0
    $ rodin.clear_all_status()
    $ murag.alive = True
    $ murag.set_pose("idle")
    $ murag.hp = murag.get_stat('hp_max')
    $ murag.mp = murag.get_stat('mp_max')
    $ murag.lp = 0
    $ murag.clear_all_status()
    python:
        for ally in all_allies:
            ally.reset_all_cooldowns()

    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2

    scene bg villageday
    show dorik neutral at DorikSprite1
    show murag neutral at sprite80
    show rodin neutral at sprite3
    with fade
    Dorik "He’s usually at the village gate."
    $ RodinPose = 3
    show rodin shocked
    Rodin "Yes, I see him there—but look!"
    $ MuragPose = 1
    show murag shocked
    $ can_use_inventory = False
    $ DorikPose = 5
    show dorik shocked
    Murag "That’s the biggest spider I’ve ever seen!"
    $ renpy.notify("Gildrath doesn't have items on this battle.")
    
    $ reset_effects()
    python:
        for ally in allies:
            ally.reset_all_cooldowns()

    $ inventario.add_item(Wardblade, 1)
    $ active_gildrath = True
    $ gildrath.weapon = Wardblade
    $ grant_gildrath_skills(gildrath)
    $ gildrath.recalc_stats()

    $ active_dorik = True
    $ dorik.weapon = Glyphbearer
    $ inventario.add_item(Glyphbearer, 1)
    $ grant_dorik_skills(dorik)
    $ dorik.recalc_stats()
    
    # $ dorik.get_skill("dispelrune").level = 1
    # $ dorik.get_skill("furnacebrand").level = 1
    # $ dorik.get_skill("stonecarvedward").level = 1
    # $ dorik.get_skill("hammerflare").level = 1
    # $ dorik.get_skill("witheringsigil").level = 1
    # $ dorik.get_skill("moltenaegis").level = 1
    # $ dorik.get_skill("blazestep").level = 1
    # $ dorik.get_skill("searinglockglyph").level = 1
    # $ dorik.get_skill("heatshatterrune").level = 1
    # $ dorik.get_skill("worldseal").level = 1
    # $ dorik.get_skill("heavenbreakersigil").level = 1
    # $ dorik.get_skill("dragonseal").level = 1



    $ quick_menu = False
    $ battle_y_offset = 0
    $ allies = [gildrath]

    $ spiderB = giantspiderB()
    $ spiderB.hp_max = 100
    $ spiderB.hp = 100
    $ spiderboss = giantspiderBoss()
    $ enemies = [spiderB, spiderboss]

    play music "BattleMedium.mp3" fadein 2.0
    scene bg citygatebattle
    show gildrath_sprite:
        xpos 630 ypos 250
    show spiderb_sprite:
        xpos 970 ypos 250
    show giantspiderboss_sprite:
        xpos 1170 ypos 250
    with fade
    pause 0.2
    
    #$ battle_y_offset = 150
    hide gildrath_sprite
    hide spiderb_sprite
    hide giantspiderboss_sprite
    $ battle_context = "spiders_gil"
    call battle(allies, enemies, lust_battle=False) from _call_battle_10
    
    $ lust_battle = False
    $ battle_y_offset = 0
    $ quick_menu = True
    
    $ allies = [rodin, dorik, murag, gildrath]
    $ gildrath.clear_all_debuffs() 
    $ dorik.clear_all_debuffs() 
    $ rodin.clear_all_debuffs() 
    $ clint.clear_all_debuffs() 
    $ murag.clear_all_debuffs() 

    $ battle_y_offset = 0
    $ reset_effects()
    
    python:
        final_of_battle(all_allies)
        defeated_enemies = [e for e in enemies if (not e.alive) or getattr(e, "lusted_out", False)]
        xp_reward = sum(e.xp_reward for e in defeated_enemies) # XP total somado
        rewards = []

        if xp_reward > 0:
            party_gain_xp(xp_reward)
            add_reward("xp", xp_reward)
            
        for e in defeated_enemies:
            give_loot_for_enemy(e, rewards, inventario)
        rewards = consolidate_rewards(rewards)

    if battle_result == "victory":
        hide screen turn_order_display
        hide screen actor_overlay
        play sound "69_Enemy_death_01.mp3"

        $ total_items = len(rewards)
        $ last_index = total_items - 1
        $ anim_time = 2.0
        $ delay_per_item = 0.5
        $ total_time = (last_index * delay_per_item) + anim_time
        play sound "LootSound03.mp3"
        show screen reward_list_center(rewards)

        pause total_time
        hide screen reward_list_center
        "The spiders have been vanquished."
        hide screen battle_sprites with dissolve

    elif battle_result == "defeat":
        hide screen turn_order_display
        play sound "17_Def_buff_01.mp3"
        "The party succumbed to their injuries."
        hide screen battle_sprites with dissolve
        jump game_over

    $ quick_menu = True
    hide screen show_floating_number


    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2
    $ GildrathPose = 1

    scene bg citygateday
    play music "Sad.mp3" fadeout 1.0 fadein 2.0
    show murag neutral at sprite1
    show gildrath neutral at sprite55
    show rodin neutral at sprite355
    show dorik neutral at DorikSprite2
    with fade
    "The guardian remained unsteady on his feet after his ordeal.  He produced a small healing potion, drank it, and then regarded them."
    Gildrath "I thank you, [player_name], Dorik, and you, orc."
    $ MuragPose = 2
    show murag smile
    Murag "Murag."
    Gildrath "I’ve been battling all day.  The enemies are growing stronger."
    "The guardian guardian spoke in a calm, even tone.  [player_name] knew he’d existed for thousands of years and was rarely stirred to emotion."
    $ MuragPose = 1
    $ DorikPose = 1
    $ DorikFireBeard = "visible"
    show dorik angry
    show murag neutral
    Dorik "Damn these monsters!  We nearly lost our guardian this day!"
    Rodin "This is what we came to talk to you about.  Do you know what’s going on?  Where are the heroes?"
    Gildrath "One by one the heroes went missing, until finally, all were gone."
    Gildrath "Without them, enemies encroach upon us with impunity.  I have scarcely had time to rest."
    $ RodinPose = 1
    $ MuragPose = 1
    show rodin sad
    show murag sad
    Rodin "I’m sorry."
    Murag "Oh man, if a dragon is getting burnt out then this is super-serious.  I mean, dragons are extra tough, plus they have dragon rune magic and--"
    Gildrath "You three are formidable, and if I were to join you, we could purge the village of danger.  However, without our heroes, more enemies will just return."
    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2
    $ DorikFireBeard = "invisible"
    $ GildrathPose = 1

    show murag neutral
    show dorik neutral
    show rodin neutral
    show gildrath neutral
    Rodin "So--you don’t know what happened to them?"
    Gildrath "I do not."
    $ DorikPose = 1
    show dorik sad
    $ RodinPose = 1
    show rodin sad
    $ MuragPose = 1
    show murag sad
    Dorik "Bowels and craters!  Damn our luck!  You were our only hope on getting to the bottom of things!"
    $ MuragPose = 3
    show murag thoughtful
    Murag "Didn’t that bull say he could ask the Ancients or something?"
    $ DorikPose = 2
    show dorik neutral
    $ RodinPose = 1
    show rodin neutral
    Rodin "You’re right.  I’d forgotten about that."
    $ MuragPose = 2
    show murag smile
    Murag "Yay!  I’m helping!"
    Gildrath "Hmm."

    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2
    $ GildrathPose = 1
    show murag neutral
    show dorik neutral
    show rodin neutral
    show gildrath neutral
    Gildrath "There is a way to ask the Ancients who see all.  I can use my Dragon runes to beckon them.  But they would demand an offering."
    $ RodinPose = 4
    show rodin thoughtful
    Rodin "An offering?"
    Gildrath "Since it is spring, a fertility ritual would please them."
    $ RodinPose = 3
    show rodin shocked
    Gildrath "Would one of you mate with me in a rune circle so our question may be answered?"
    $ DorikPose = 5
    show dorik shocked
    $ MuragPose = 1
    show murag shocked
    "He said it so plainly, as if he asked for something ordinary.  [player_name] couldn’t imagine living so long that he’d become indifferent to even that."
    $ RodinPose = 1
    show rodin neutral 
    Rodin "I’ll do anything to protect Hungwood."
    "Sex with such a gorgeous dragonoid was no great ask.  [player_name] knew he’d enjoy himself, even if the ancient dragon was bored."
    Murag "Wow, you said that fast."
    $ RodinPose = 3
    show rodin blush
    $ DorikPose = 1
    show dorik neutral
    Dorik "There’s no shame in it, if that’s what must be done!  ...And I’m no mood."
    $ MuragPose = 1
    show murag blush
    Murag "I’m in the mood.  Heh...?"
    Murag "Nah, that’s okay.  Nevermind.  Go ahead, Buddy.  You called dibs.  Er...can you forget I said that?  Fuck...literally just met a dragon for the first time and...:mutters:"
    $ DorikPose = 2
    show dorik neutral
    $ MuragPose = 1
    show murag neutral
    Dorik "Right.  We need to know what we’re up against."
    Gildrath "Very well.  Dorik and Murag, will you guard this gate so I may go to the woods and perform the ritual with [player_name]?"
    $ MuragPose = 2
    $ DorikPose = 1
    show dorik sneer
    show murag smile
    Dorik "Yes!  Do whatever it takes!"
    Murag "Sure thing!  I like being useful."
    #stop music fadeout 2.0
    hide rodin with dissolve
    hide gildrath with dissolve
    pause 0.5
    
    $ RodinPose = 1
    $ GildrathPose = 1
    scene bg woodsclearingday with fade
    pause 0.5
    show gildrath neutral at sprite2 with dissolve
    show rodin neutral at sprite4 with dissolve
    Gildrath "Give me a moment to draw the rune circle."
    hide gildrath with dissolve
    Rodin "Mm."
    "He drew a circle on the ground that was large enough to fit two adults."
    $ RodinPose = 3
    show rodin blush
    Rodin "Is this...er...boring to you?"
    $ RodinPose = 1
    show rodin neutral
    
    $ GildrathUnder = "soft"
    $ GildrathTop = "invisible"
    $ GildrathSleeves = "invisible"
    $ GildrathPose = 3
    show gildrath smile at sprite2 with dissolve
    "The dragonoid paused to meet his eyes.  Was that a smile?  [player_name]’s brow rose."
    Gildrath "If you wish to know the truth—interludes like this tend to be the only things that I {i}don’t{/i} find boring."
    $ GildrathPose = 1
    show gildrath neutral
    Rodin "Oh.  Well, all for the better then.  I’d hate to have to annoy you with some sex ritual."
    "Again Gildrath took a moment to gaze deeply into [player_name]’s eyes."
    Gildrath "You don’t annoy me, [player_name].  I find you...interesting."
    $ RodinPose = 3
    show rodin shocked
    "This wasn’t how he expected things to proceed at all."
    Rodin "Why would I be interesting to someone like you?  Who’s seen everything a million times over already?"
    Gildrath "There are still things that happen rarely enough to give me pause.  Like a man, who’s destined to become a great druid, choosing to become a mere merchant instead."
    $ RodinPose = 1
    show rodin neutral
    Gildrath "It’s not often one chooses their own path, rather than do what’s expected of them."
    $ RodinPose = 1
    show rodin neutral 
    Rodin "Hmm."
    "His brow twitched.  Of course there were reasons for that, but he didn’t presume Gildrath wanted to know all the trauma of his past.  Still...he was a bit proud to have piqued the interest of an ancient dragonoid like Gildrath."
    "[player_name] found him intimidating with all his great wisdom and power.  Frankly, he considered the sexy dragonoid entirely out of his league."
    "Though, right now he might start to think he had a chance.  Wouldn’t that be something?  A simple merchant partnered with an immortal dragonoid guardian?"
    "A smile teased the edges of his lips at the thought, but he didn’t let it germinate."
    "Gildrath had finished drawing an elaborate rune in the circle.  He looked it over a moment before giving a slight nod of approval."
    hide gildrath with dissolve
    "Gildrath stood in the center of the ring and offered his hand to [player_name]."
    Gildrath "Come."
    $ RodinPose = 3
    show rodin blush
    pause 0.5
    hide rodin with dissolve
    pause 0.5
    scene GildrathRodinRitual1
    play music "SexySlow.mp3" fadein 2.0
    with fade
    "[player_name] caught the scent of him up close—musky and woodsy, as if he was part of the forest itself. "
    "Gildrath’s beautiful cock was hard and waiting for him. Could it be that what [player_name] sensed earlier was true, and this was about more than just the ritual for Gildrath?"
    scene GildrathRodinRitual2 with dissolve
    Gildrath "Don’t be intimidated, [player_name]. Do what comes naturally."
    "[player_name] swallowed.  Does he mean get straight to the point?  Probably, yes.  It was a proper ritual after all.  Not a honeymoon."
    scene GildrathRodinRitual3 with vpunch
    "After some hasty self-lubrication, [player_name] moved to straddle Gildrath and slowly lowered himself onto his cock. He slid smoothly onto him as though his cock was sized for [player_name]."
    "The dragonoid let out a soft gasp of surprise."
    Gildrath "Well, I did tell you to do what comes naturally..."
    "What?  Wait...was he supposed to start with foreplay after all?  Damn it!  [player_name] felt like an over-eager teenager.  But he would have done things right had he known!"
    scene GildrathRodinRitual4 with dissolve
    "There was no going back now.  [player_name] moved slowly up and down on him, letting him stretch his passage more open with each movement."
    "Gildrath let out a grunt and clutched his thigh. His soft gasps surrounded [player_name] like the whispers of the wind in the leaves."
    Gildrath "You have...oh, gods...you have a hidden talent, Druid..."
    scene GildrathRodinRitual5 with dissolve
    "[player_name] was far from becoming a druid yet, but he wouldn’t sully the mood by correcting him.  ‘Druid’ was the fate he’d turned away from to become a merchant.  Didn’t Gildrath know this?"
    "[player_name] chanced a gaze into the dragonoid eyes. He saw the reflection of a deep forest, further cementing the manner of creature he was with.  "
    "They continued tensing and flexing, and [player_name] grew comfortable on his cock.  Though he was large, he was not so girthy as to hurt him.  Just big enough to mash [player_name] in all the right places. "
    "The profound gaze he was locked in made him start to understand—this is about life. The quickening of his heartbeat, the electricity shooting up his spine as Gildrath filled him. This is what the Ancients want."
    scene GildrathRodinRitual6 with dissolve
    "[player_name]’s cockhead slapped his belly as he moved faster. The warmth of his sweat-damp skin stoked the fire building in his balls. Gildrath watched the rhythmic motion of his cock as if mesmerized."
    "[player_name] leaned back to angle Gildrath’s cock toward his prostate. His swollen head rubbed into [player_name]’s sweet spot, making him gasp and bounce greedily for more. "
    "[player_name] didn’t feel shy anymore. He barely remembered the purpose of the ritual. He was lost in a haze of pleasure."
    Gildrath "Ungghhh!"
    scene GildrathRodinRitual7 with dissolve
    "He realized he was behaving foolishly once again.  Gildrath was too noble for a hasty fuck.  He could tell the dragonoid was one to savor things.  So he leaned forward and gave into his urge to squeeze Gildrath’s glorious pecs."
    "Curls of smoke poured from Gildrath’s nostrils as his breath turned ragged. The air smelled like an autumn bonfire. "
    scene GildrathRodinRitual8 with dissolve
    "Precum leaked from [player_name]’s slit onto the dragonoid’s abs. Gildrath’s long, flexible tongue slid out of his mouth to lap it up."
    "[player_name]’s eyes bulged.  He never knew Gildrath had a tongue like that. "
    Gildrath "Mmm... you’re delicious. I want to taste more of you..."
    "Gildrath’s tongue spiraled around [player_name]’s cock, enveloping him in wet heat. The tip of his tongue moved to tease his slit. The slippery tongue gliding around [player_name]’s most inner recesses made [player_name]’s eyes roll back."
    Rodin "Hnngh!  Unnnghh!"
    "Gildrath’s tongue slid into [player_name]’s cockhole, sending electrifying pleasure to his every nerve ending as it breached him."
    Rodin "Oh gods!  Gildrath!"
    scene GildrathRodinRitual6 with dissolve
    "[player_name] began to ride him with abandon, dislodging the invading tongue. Each plunge downward made Gildrath mash into his sweet spot, sending waves of shivery pleasure through him."
    "[player_name] was lost to the animalistic pleasure, to the scent of Gildrath’s sweat, and to the heat that built in his loins."
    scene GildrathRodinRitual9 with dissolve
    Rodin "Hrrggghhh!"
    play sound "RuneAttack.mp3"
    "The runes flared as [player_name] shot waves of hot seed onto Gildrath’s chest and into his waiting mouth. He eagerly swallowed every drop he could catch."
    Gildrath " Urrrghh!  Unngh!"
    "Gildrath let out a roar as he pumped [player_name] full of hot cum.  The gusher shot deep into his guts, filling him to overflowing."
    "Stars erupted in [player_name]’s vision, and he went weak with pleasure. He collapsed onto Gildrath’s chest, connected by a layer of warm cum."
    scene GildrathRodinRitual10 with dissolve
    "A soft breeze cooled the sweat on [player_name]’s overheated skin. He became a gasping heap on the dragonoid in the aftermath."
    Gildrath "Look..."
    play sound "RuneAttack.mp3"
    "[player_name] opened his eyes to see the circle fill with soft green light.  He heard musical whispers in the leaves."
    Gildrath "The Ancients are pleased.  They speak to me."
    "The reminder that this had been all for a ritual made [player_name] consider prying himself from their wetness, and resuming some distance between them."
    "But he’d been wrong to presume Gildrath hadn’t wanted foreplay.  He didn’t want to make the same mistake about cuddling."
    "He remained in place, his breathing settling into the same rhythm as the heated dragonoid beneath him.  Then...he felt a scaled arm close around his back, embracing him."
    stop music fadeout 2.0
    
    $ GildrathUnder = "pants"
    $ GildrathTop = "visible"
    $ GildrathSleeves = "visible"
    "Thank goodness he was right.  There was time for cuddling after all."
    pause 0.5

    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2
    $ GildrathPose = 1
    scene bg citygateday
    show murag neutral at sprite1
    show dorik neutral at DorikSprite2
    with fade
    pause 0.3
    play music "Sad.mp3" fadein 2.0
    show rodin neutral at sprite355 behind dorik with dissolve
    show gildrath neutral at sprite55 behind murag with dissolve

    Rodin "We did it.  We got an answer."
    $ DorikPose = 5
    show dorik shocked
    Murag "Oh good!  (Er...that’s what we wanted, right?)"
    Dorik "Then—you know what’s happened to the heroes?"
    Gildrath "There is a former knight of the king who was banished from his post for committing unspeakable acts.  He has since obtained immense dark powers. "
    Gildrath "He’s used these powers to get revenge on the kingdom by enslaving all its heroes."
    $ RodinPose = 3
    $ MuragPose = 1
    show rodin shocked
    show murag shocked
    Dorik "Enslaving?!  Dear gods!"
    Murag "Yeah--that’s definitely bad."
    Gildrath "His dark powers have allowed him to control them—and turn them into enemies in their own right."
    Murag "Holy shit on a stick!  He can turn people into enemies?!"
    Rodin "What...what can we do?"
    $ DorikPose = 1
    $ DorikFireBeard = "visible"
    show dorik angry
    Dorik "We’ve got to fight him—that’s what!"
    Murag "Yeah.  Sounds like we got to rescue all the heroes and take out that knight."
    $ MuragPose = 1
    show murag neutral
    "[player_name] blinked.  The way Murag summed it up so frivolously showed how new to the game he was."
    $ RodinPose = 1
    show rodin sad
    "This knight had access to magic that let him take out every one of their powerful heroes.  Facing him would be a monumental challenge—one where they could very easily be killed before they even reached the first hero."
    Gildrath "You can do it, [player_name]."
    $ RodinPose = 3
    show rodin shocked 
    Rodin "I...I can?"
    Gildrath "The Ancients shared about more than just our mission.  If any of us might succeed at this—it’s you."
    Rodin "...!"
    "What was he saying?  The Ancients talked about {i}him{/i}?!  He must be joking...or just trying to build his confidence disingenuously."
    $ MuragPose = 2
    show murag smile
    Murag "That’s great!  See?  Fate’s on our side!"
    Dorik "[player_name] is full of untapped potential.  I’ve always said so."
    $ RodinPose = 1
    show rodin sad
    Rodin "I...I’m just a merchant."
    Gildrath "You will become more."
    $ MuragPose = 1
    show murag neutral
    $ DorikPose = 2
    $ DorikFireBeard = "invisible"
    show dorik neutral
    $ RodinPose = 4
    show rodin thoughtful
    Rodin "..."
    Gildrath "And we must face this threat or the kingdom, and all its  people, will fall.  Chaos and villainy will reign.  And we will die in any case."
    $ RodinPose = 1
    show rodin neutral
    "Well, when he put it that way...it sounded like it was best to go out fighting."
    Rodin "You’ll join us?"
    Gildrath "Where you lead, I will follow."
    $ RodinPose = 3
    show rodin shocked
    Rodin "Where {i}I{/i} lead?!"
    $ MuragPose = 2
    show murag smile
    Murag "Sure, why not? You’re a nice guy."
    Dorik "You’re the best of us to lead.  I’ve no doubt of that.  And sounds like Gildrath feels the same."
    $ RodinPose = 1
    show rodin neutral
    "[player_name] remained unsure.  A city guardian sounded like the one who should guide them. [player_name] had just wrapped his head around the crisis in Hungwood, and now it seemed he’d be leading a group of adventurers to fight it."
    "This was never what he wanted.  The more he’s dragged into this, the harder it will be to return to his normal life.  He was a simple merchant and leaf-caster."
    "Or was he something more?"
    Gildrath "I cannot leave my post until Hungwood is cleared of enemies.  Will you all help me?"
    Rodin "Of course.  We must make sure Hungwood is safe before anything else."
    $ MuragPose = 2
    show murag smile
    Murag "I’m in!"
    Dorik "We can ask around as we do to see if anyone knows where the heroes are."
    $ MuragPose = 1
    show murag neutral
    Rodin "Then...let’s do it."
    Dorik "I’ll find you all later.  I must prepare Minoc to take over things for a while."
    Gildrath "I must set up runes at the village gate to ensure no new enemies enter after we’ve cleared the ones already here."
    Rodin "Right.  Then Murag and I will go to the market and see if anyone knows what’s going on."
    Murag "Yeah!  That sounds great.  Let’s do that!"
    Gildrath "I’ll be along soon."
    hide gildrath with dissolve
    hide dorik with dissolve
    $ RodinPose = 1
    $ MuragPose = 2
    show murag flustered at sprite25
    show rodin neutral at sprite4
    with move
    Murag "No one’s going to mind me being in the market, right?  Since I’m an orc and all?"
    $ RodinPose = 1
    show rodin smile
    Rodin "Don’t worry.  You’re not the first orc to go on his own, and as long as you’re with me everyone will know you don’t plan on any trouble."
    $ MuragPose = 2
    show murag smile
    Murag "Guess I’ll be sticking with you then, Buddy!"
    "That was fine with [player_name].  Murag’s optimism might keep him from obsessing over the mess they were in."
    scene bg villageday with dissolve
    python:
        objectives = [
            {"desc": _("Talk to the Vendor in Items Shop."), "done": talkshopkeeper > 0},
            {"desc": _("Talk to the Blacksmith in Weapon Shop."), "done": talkblacksmith > 0},
            {"desc": _("Check the Knob Polishers stall."), "done": talkknobpolisher > 0},
            {"desc": _("Check the Sausage stall."), "done": talksausage > 0},
            {"desc": _("Check out the Inn."), "done": talkinn > 0},
        ]

        # Eggplant só entra na lista se desbloqueado
        if all([talkshopkeeper, talkblacksmith, talkknobpolisher, talksausage, talkinn]):
            objectives.append({"desc": _("Check out the Eggplant stall."), "done": talkeggplant > 0})

        renpy.show_screen("mission_updateALT", _("Exploring Hungwood."), objectives, "main")
    
    $ battle_context = None
    $ quick_menu = False
    $ renpy.pause()
    hide screen mission_updateALT with dissolve

    pause 0.5
    call explore_city from _call_explore_city

label continueeDemo:
    $ quick_menu = True
    scene bg villageday 
    $ city_intro_done = True
    stop music fadeout 3.0
    $ RodinPose = 1
    $ MuragPose = 1
    show murag neutral at sprite4
    show rodin neutral at sprite2 
    with dissolve
    play music "NeutralMedium.mp3" fadein 2.0 fadeout 1.0
    Rodin "Looks like we have our first destination once we deal with the enemies plaguing Hungwood."
    $ MuragPose = 2
    show murag smile
    Murag "Yeah!  I can’t wait to get that guy’s husband free for him.  He’ll be so happy!"
    "Was it confidence or just his lack of experience that made him so sure?  [player_name] worried that they had no idea what they’d be facing.  Could they even help?  Or would they die trying?"
    "He kept his misgivings to himself.  Destroying the orc’s enthusiasm would help no one."
    $ RodinPose = 1
    show rodin smile
    Rodin "You’re one special orc.  You really care about helping people."
    Murag "Heh.  Sure.  That’s what always got me in trouble back home.  But that’s what adventuring is all about, right?"
    Rodin "Mm."
    $ MuragPose = 1
    show murag blush
    Murag "It was fun hanging out with you today.  I never got to do stuff like this back with my tribe.  All the orcs ever want to do is battle, challenge each other, and talk about battle."
    $ RodinPose = 1
    show rodin neutral 
    Murag "And if you try to bring up other stuff, they think you’re weird and annoying."
    Rodin "I can see why you didn’t fit in."
    $ RodinPose = 1
    show rodin smile
    Murag "Today I got to talk to people, go around a market, hang out with you—it’s like my whole life changed overnight."
    Rodin "For the better, I hope?"
    "And he also hoped Murag wouldn’t end up regretting leaving his tribe after all the danger they were about to embark on."
    $ MuragPose = 2
    show murag smile
    Murag "Heck yeah!"
    $ RodinPose = 1
    show rodin smile
    pause 0.3
    hide rodin
    hide murag
    with dissolve
    pause 0.5

    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2
    $ GildrathPose = 1
    scene bg citygateday
    show murag neutral at sprite2
    show dorik neutral at DorikSprite1
    show gildrath neutral at sprite55
    show rodin neutral at sprite355
    with fade
    Rodin "We got some information in the market.  Our first enslaved hero is in the cave west of Hungwood."
    Murag "Yep!  His husband says he’s turned into a zombie who just tries to kill anyone who goes into the cave."
    $ GildrathArm = 2
    $ GildrathPose = 1
    show gildrath thoughtful
    Gildrath "Hmm."
    Rodin "There’s a banished knight named Horrath causing all the trouble.  He’s apparently become a powerful wizard."
    Gildrath "Hmmmm."
    "The group waited as the wheels in Gildrath’s head turned."
    Gildrath "This is potent magic stronger than I would think a former knight could wield."
    Gildrath "The hero is likely controlled by the Spell of Servitude, where he worships Horrath as his master and despises all others."
    Gildrath "This spell can be broken if he is defeated enough to regain consciousness, and then he can grant his servitude to another temporarily who makes love to him."
    $ RodinPose = 3
    show rodin shocked
    Gildrath "After that he will be free."
    $ RodinPose = 1
    show rodin neutral
    $ GildrathArm = 1
    $ GildrathPose = 1
    show gildrath neutral
    "Sex is the answer once more?  Seemed to be a trend.  As if the gods divining their adventure were somehow motivated to find every possible way to include sex scenes along the way."
    $ DorikPose = 2
    show dorik neutral
    Dorik "Then we have our mission."
    Murag "And maybe the hero can tell us some more once he snaps out of it.  Like: what even {i}is{/i} a knight?"
    Gildrath "Let us clear Hungwood of enemies and then proceed to the cave."
    Rodin "Right.  We’ll fix this mess so we can all get back to our lives."
    "Gildrath darted a glance at him and locked eyes.  [player_name]’s brow quivered.  Did he say something wrong?"
    Gildrath "..."
    Gildrath "Lead the way, [player_name]."
    "[player_name] braced himself with a deep breath, then led the others onward."
    stop music fadeout 3.0
    hide dorik with dissolve
    hide murag with dissolve
    hide rodin with dissolve
    hide gildrath with dissolve



    hide screen mission_update with dissolve

    scene mapa1
    call screen ClintExample
    jump clint_intro



label gil_entrance_dialogue:
    hide screen turn_order_display
    hide screen battle_sprites
    hide screen actor_overlay
    show gildrath_sprite:
        xpos 630 ypos 250
    show spiderb_sprite:
        xpos 970 ypos 250
    show giantspiderboss_sprite:
        xpos 1170 ypos 250
    with None
    $ quick_menu = True
    Dorik "Good gods!  He’s on his last breath!"
    Rodin "Not if I can help it!"
    
    show gildrath_sprite:
        xpos 630 ypos 250
        linear 0.5 xpos 210 ypos 250
    with move
    pause 0.3
    show rodin_sprite:
        xpos 435 ypos 250
    with dissolve
    Rodin "Let me help!"
    $ rodin.set_pose("buff")
    
    $ allies = [rodin, gildrath, murag, dorik]
    python:
        allies, enemies = assign_positions(allies, enemies)
        state.ally_ids = [a.id for a in allies]
        state.lustable_ids = [
            e.id for e in enemies
            if getattr(e, "lustable", False)
        ]

    play sound "Healsound02.mp3"
    python:
        show_effect("effect_back", gildrath, "HealSpellBack", dx=-135, dy=-10, zoomm=0.5, duration=1.2)
        show_effect("effect_front", gildrath, "HealSpellFront", dx=-135, dy=-10, zoomm=0.5, duration=1.2)
    
    $ gildrath.clear_all_debuffs() 
    $ heal_amount = gildrath.get_stat('hp_max')
    $ gildrath.heal(heal_amount)
    $ show_floating_number(gildrath, +heal_amount, "heal")

    Gildrath "[player_name]...?  Thank you."
    pause 0.1
    show murag_sprite:
        xpos 630 ypos 250
    show dorik_sprite:
        xpos 0 ypos 250
    with dissolve
    $ rodin.set_pose("idle")
    Murag "We can’t let you guys have all the fun!"
    Dorik "We’re here for you, Guardian!"
    
    $ rodin.set_pose("idle")
    $ reset_effects()
    Gildrath "Thank the gods."
    
    $ can_use_inventory = True
    hide gildrath_sprite
    hide rodin_sprite
    hide murag_sprite
    hide dorik_sprite
    hide spiderb_sprite
    hide giantspiderboss_sprite
    $ quick_menu = False
    call battle(allies, enemies, lust_battle=False) from _call_battle_11
    return



screen ClintExample():
    tag world_map
    modal True
    add "map/MAP_hungwood.png"
    add "map/exagon_idle.png" pos (807, 400)
    add "map/exagon_idle.png" pos (807, 215)
    add "map/exagon_idle.png" pos (807, 585)

    add "map/exagon_idle.png" pos (660, 310)
    add "map/exagon_idle.png" pos (512, 215)
    add "map/exagon_idle.png" pos (362, 125)
    add "map/exagon_idle.png" pos (212, 215)

    add "map/exagon_idle.png" pos (362, 310)

    add "map/exagon_idle.png" pos (660, 495)
    add "map/exagon_idle.png" pos (512, 400)
    add "map/exagon_idle.png" pos (362, 495)
    add "map/exagon_idle.png" pos (212, 400)

    add "map/exagon_idle.png" pos (362, 680)

    add "map/exagon_idle.png" pos (955, 310)
    add "map/exagon_idle.png" pos (1105, 215)
    add "map/exagon_idle.png" pos (1253, 125)
    add "map/exagon_idle.png" pos (1400, 215)

    add "map/exagon_idle.png" pos (1253, 310)

    add "map/exagon_idle.png" pos (955, 495)
    add "map/exagon_idle.png" pos (1105, 400)
    add "map/exagon_idle.png" pos (1253, 495)
    add "map/exagon_idle.png" pos (1400, 400)
    add "map/exagon_idle.png" pos (1400, 585)

    imagebutton auto "map_exagon_%s" pos (1400, 585) action Return()
    add "exagon_hover" pos (1400, 585) at blink_fast


label clint_intro:
    $ active_clint = True
    $ inventario.add_item(Moonfang_bow, 1)
    $ clint.weapon = Moonfang_bow
    $ grant_clint_skills(clint)
    $ clint.recalc_stats()
    
    scene bg villagehomes
    show bg villagehomes 
    camera:
        subpixel True 
        xpos 950
    with fade
    stranger "Call them off, Baron. You don’t want things to get {i}messy{/i}.  Fair warning!"
    
    $ RodinPose = 3
    $ MuragPose = 1
    $ DorikPose = 5
    $ GildrathPose = 3

    show gildrath shocked:
        subpixel True xpos 0.15
    show murag shocked:
        subpixel True xpos -0.55
    show dorik shocked:
        subpixel True xpos -0.35 ypos 0.25
    show rodin shocked:
        subpixel True xpos 0.0 ypos 0.05

    play music "TenseMedium.mp3" fadein 2.0
    with dissolve
    Rodin "...!"

    
    show dorik shocked:
        subpixel True xpos -0.39
    show rodin shocked:
        subpixel True xpos 0.11
    with move
    
    $ ClintPose = 3
    show clint shocked:
        subpixel True xpos -0.14 ypos 0.05
    with dissolve



    stranger "Oh!"
    $ ClintPose = 4
    show clint smile
    #stranger "Ah!  Perfect!  Witnesses."  Though I do wish I’d been better dressed to meet you all.
    Aristocrat "Stop right there!"
    $ ClintPose = 4
    show clint neutral

    show ogre neutral:
        subpixel True xpos 0.52
    show bear neutral:
        subpixel True xpos 1.12
    show aristocrat sneer:
        subpixel True xpos 0.86 ypos 0.14

    pause 0.5
    camera:
        subpixel True 
        linear 0.5 xpos -958 
        
    with Pause(0.5)
    camera:
        xpos -958 
    Aristocrat "Hand that wretched thief over to me!  He stole an entire chest of pearls from me!"

    camera:
        subpixel True 
        linear 0.5 xpos 950
        
    with Pause(0.5)
    camera:
        xpos 950

    $ RodinPose = 1
    $ MuragPose = 1
    $ ClintPose = 2
    $ DorikPose = 2
    $ GildrathPose = 1
    show gildrath neutral
    show rodin neutral
    show dorik neutral
    show murag neutral
    show clint flustered
    stranger "Heh—that’s a bit of an exaggeration.  And I assure you--I’m far from wretched."
    $ ClintPose = 4
    show clint neutral
    stranger "I didn’t so much as steal the pearls—I just gave them back to the divers you’ve been exploiting to get them."
    pause 0.5
    show aristocrat angry
    camera:
        subpixel True 
        linear 0.5 xpos -958 
        
    with Pause(0.5)
    camera:
        xpos -958 
    Aristocrat "Don’t listen to him!  He’s a disgusting thief and a violent were creature.  Hand him over right now—"
    Rodin "I would hear him."
    show aristocrat shocked
    pause 0.5
    camera:
        subpixel True 
        linear 0.5 xpos 950
    with Pause(0.5)
    camera:
        xpos 950

    Gildrath "Yes.  Please go on."
    Aristocrat "Tsk!"
    $ ClintPose = 4
    show clint smile
    stranger "Thank you, kind strangers.  I can see you’re a troupe that stands for virtue, just like me."
    stranger "Clint, archer, rogue, seducer of many--and at times, thief.  Though only from elite swine such as our Baron here.  Now, I may not look like much as I stand, but I assure you--I’m quite fetching in my full regalia."
    $ ClintPose = 4
    show clint neutral
    Clint "And yes, I have become a victim to the lycanthropic curse—a rather ghastly thing to deal with, I assure you.  But I avoid conflict in that form as best I can.  The proof is for your own eyes to see."
    Clint "I kept to my human form rather than transforming and, well, violently kiling them all.  Simpler, yes.  Pleasant?  I should say not."
    Aristocrat "You’re the one who’d be killed!"
    Clint "Ahem. This man has chased me all the way from the coast of Smegmalia all over his ill-gotten pearls."
    Clint "You see, he’s a baron who insists each family in his borough devote one of their children to his pearl his operation."
    $ ClintPose = 1
    show clint sneer
    Clint "He sends the poor souls down to the oysters with weights, then pulls them up with a rope. And he repeats this nasty business until the divers perish. Not a single one makes it back home, and none of them live long enough to reach puberty."
    
    
    $ DorikPose = 1
    $ DorikFireBeard = "visible"
    $ MuragPose = 1
    $ ClintPose = 3
    $ RodinPose = 2
    $ GildrathPose = 2
    show dorik angry
    show clint angry
    show murag angry
    show rodin angry
    show gildrath angry

    Aristocrat "That’s their own fault!"
    Rodin "Let him talk."
    Murag "Yeah, shut up you big jerk!"
    $ ClintPose = 2
    show clint flustered
    $ RodinPose = 1
    $ MuragPose = 1
    $ DorikPose = 2
    $ DorikFireBeard = "invisible"
    $ GildrathPose = 1
    show gildrath neutral
    show rodin neutral
    show dorik neutral
    show murag neutral
    Clint "Alright, I confess.  I stole his pearls and freed his latest crop of child-victims.  They took most of the pearls back to their impoverished families."
    Dorik "‘Most’?"
    $ ClintPose = 4
    show clint smile
    Clint "Well, I did keep a modest fee for myself.  One can’t live on virtue alone."
    Murag "I mean, yeah. You gotta eat."
    Clint "Right you are my dear orc!"
    
    pause 0.5
    show aristocrat shocked
    camera:
        subpixel True 
        linear 0.5 xpos -958 
        
    with Pause(0.5)
    camera:
        xpos -958

    Aristocrat "You see!  He admits it all!  He’s a thief and has destroyed my business!  Hand him over."
    Murag "Your business sounds gross and awful!"
    Aristocrat "How dare you!"
    $ RodinPose = 2
    $ MuragPose = 2
    $ ClintPose = 4
    $ DorikPose = 1
    $ DorikFireBeard = "visible"
    $ GildrathPose = 2

    show gildrath sneer
    show rodin sneer
    show dorik angry
    show murag sneer
    show clint neutral

    pause 0.5
    camera:
        subpixel True 
        linear 0.5 xpos 950
    with Pause(0.5)
    camera:
        xpos 950
    
    Dorik "Sounds like it needed to be destroyed!  And if you don’t get moving, by the gods, you’ll be next!"
    Aristocrat "But--!"
    Gildrath "You heard.  Your sort is not welcome in Hungwood."
    pause 0.5
    show aristocrat angry
    camera:
        subpixel True 
        linear 0.5 xpos -958 
        
    with Pause(0.5)
    camera:
        xpos -958

    Aristocrat "This is outrageous!  Boris!  Hugo!  Attack them!  Kill that nasty werewolf!"
    BANDH "..."
    show aristocrat shocked
    Aristocrat "What are you waiting for!  He’s a thief!  He’s scum!  And so are these bastards for protecting him!"
    Dorik "Watch it!"
    Boris "We were paid to help you catch the werewolf, not fight a whole band of adventurers--including a guardian and an orc."
    Hugo "And a human and dwarf.  This job ain’t worth my life."
    Boris "Yeah. Especially for the shit pay you’re giving us."
    show aristocrat angry
    Clint "I knew you were but hapless employees—that’s why I didn’t transform!"
    Aristocrat "Do as I order you!  I’ll have your heads!"
    Boris "Fuck you and fuck your pearl business. According to him you’re drowning kids. I didn’t know that when I answered your flyer."
    Hugo "And if you keep threatening us, you can find your way back through Shady Prick Forest by yourself!"
    Aristocrat "How dare you betray me!"
    Hugo "Yeah, yeah.  We better get going."
    Aristocrat "You haven’t heard the last of this!"
    hide ogre with dissolve
    Boris "C’mon."
    hide bear with dissolve
    show aristocrat shocked
    Aristocrat "Don’t leave me alone!  These woods are dangerous!"
    hide aristocrat with dissolve
    Aristocrat "Slow down!"
    $ RodinPose = 1
    $ MuragPose = 1
    $ ClintPose = 4
    $ DorikPose = 2
    $ DorikFireBeard = "invisible"
    $ GildrathPose = 1

    show gildrath neutral
    show rodin neutral
    show dorik neutral
    show murag neutral
    show clint smile
    pause 0.5
    camera:
        subpixel True 
        linear 0.5 xpos 950
    with Pause(0.5)
    camera:
        xpos 950

    Clint "Thank you, kind adventurers.  You saved me a great deal of...carnage."
    $ MuragPose = 2
    show murag smile
    Murag "You’re welcome!"
    $ ClintPose = 4
    show clint neutral
    Clint "It’s true I steal more than hearts on occasion, but I swear it’s only from the foulest of the elites.  The vile things they do to hoard their money will leave you appalled."
    $ ClintPose = 2
    show clint flustered
    Clint "Heh...though I suppose I hardly look like one who ran in elite circles.  It’s this blasted curse you see.  Fine clothes are torn to shreds with my transformation, so I have to make due with this."
    Rodin "It’s clear you were in the right.  And we’re happy to help."
    $ ClintPose = 6
    show clint thoughtful
    Clint "I don’t think I’ll be able to return to Smegmalia now.  Do you think I could settle here in Hungwood?  "
    Gildrath "Hungwood will only be safe for a brief while.  The heroes are gone, and enemies run rampant."
    $ ClintPose = 3
    show clint shocked 
    Clint "Is that what’s going on?!  I noticed there were more enemies than I’ve ever seen before.  I had to take my werewolf form again and again to fight them!"
    $ RodinPose = 4
    show rodin thoughtful
    Rodin "So...you’re an adventurer yourself?"
    $ ClintPose = 4
    show clint smile
    Clint "I’m more of a lover than a fighter—but one must keep their skills honed to razor sharpness to steal from the elite marks I target.  And I do like helping those in need from time to time."
    $ ClintPose = 4
    show clint neutral
    Dorik "We could use a werewolf to tear things apart on our mission to rescue the heroes."
    Murag "Yeah!  And he has a bow and arrow too.  I bet he uses it.  I mean--why else would he have it?"
    $ ClintPose = 4
    show clint smile 
    Clint "Well, I only resort to the violence of my werewolf side against enemies.  I can also take out enemies from a distance.  I’m quite a fine archer."
    $ ClintPose = 4
    show clint neutral
    $ RodinPose = 1
    show rodin neutral
    Gildrath "If you were sincere about your desire to help others, then would you join us?  The world is in peril without its heroes."
    $ MuragPose = 2
    show murag smile
    Murag "It’ll be fun!"
    $ RodinPose = 3
    show rodin flustered
    Rodin "...It will be dangerous.  But turning away from this crisis will only lead to our demise anyway."
    $ ClintPose = 5
    $ DorikPose = 1
    show clint thoughtful
    show dorik sneer
    Dorik "As dangerous as it is, these blasted enemies must be destroyed!  And that creep knight who’s behind it all, too!"
    $ RodinPose = 1
    show rodin neutral
    Clint "Well...I do owe you a debt for saving me.  And it’s not as if I have anywhere else to go at the moment."
    $ ClintPose = 4
    show clint smile
    Clint "Adding saving the world to my list of achievements is bound to bring more lovers to my bed!  Count me in!"
    Murag "Ha ha!"
    Gildrath "Thank you.  We will not take your help for granted."
    Rodin "And we’ll do our best to make sure we all make it back in one piece."
    Dorik "We’ll be in one piece—but not our enemies!"
    Gildrath "There is much to tell you.  We’ll fill you in as we continue purging the village of enemies."
    Clint "Lovely!  And perhaps I can regale you with a story or two also—or even a song?"
    Murag "Oh!  I like him!"
    $ RodinPose = 3
    show rodin shocked
    Rodin "We have enemies!  The song will have to wait!"
    $ MuragPose = 1
    $ ClintPose = 3
    $ DorikPose = 5
    $ GildrathPose = 3

    show dorik shocked
    show murag shocked
    show gildrath shocked
    show clint shocked
    pause 0.5
    $ allies = [rodin, dorik, murag, gildrath]
    $ all_allies = [rodin, murag, dorik, gildrath, clint]
    $ gildrath.clear_all_debuffs() 
    $ dorik.clear_all_debuffs() 
    $ rodin.clear_all_debuffs() 
    $ clint.clear_all_debuffs() 
    $ murag.clear_all_debuffs() 
    $ battle_y_offset = 0

    $ reset_effects()
    python:
        for ally in allies:
            ally.reset_all_cooldowns()

    $ current_hex_id = 64
    $ current_neighbors = WORLD_HEXES[current_hex_id]["neighbors"]
    $ visited_hexes = set()

    $ rodin.alive = True
    $ rodin.set_pose("idle")
    $ rodin.hp = rodin.get_stat('hp_max')
    $ rodin.mp = rodin.get_stat('mp_max')
    $ rodin.lp = 0
    $ rodin.lusted_out = False
    $ rodin.clear_all_status()

    $ murag.alive = True
    $ murag.set_pose("idle")
    $ murag.hp = murag.get_stat('hp_max')
    $ murag.mp = murag.get_stat('mp_max')
    $ murag.lp = 0
    $ murag.lusted_out = False
    $ murag.clear_all_status()

    $ gildrath.alive = True
    $ gildrath.set_pose("idle")
    $ gildrath.hp = gildrath.get_stat('hp_max')
    $ gildrath.mp = gildrath.get_stat('mp_max')
    $ gildrath.lp = 0
    $ gildrath.lusted_out = False
    $ gildrath.clear_all_status()

    $ clint.alive = True
    $ clint.set_pose("idle")
    $ clint.hp = clint.get_stat('hp_max')
    $ clint.mp = clint.get_stat('mp_max')
    $ clint.lp = 0
    $ clint.lusted_out = False
    $ clint.clear_all_status()
    
    $ dorik.alive = True
    $ dorik.set_pose("idle")
    $ dorik.hp = dorik.get_stat('hp_max')
    $ dorik.mp = dorik.get_stat('mp_max')
    $ dorik.lp = 0
    $ dorik.lusted_out = False
    $ dorik.clear_all_status()

    $ battle_context = "Clint_tutorial"

    camera:
        xpos 0
    call screen party_select with dissolve
    
    scene bg villagehomesright
    $ rat = Ratenemy()
    $ ratb = RatenemyB()
    $ balor = balorenemy()

    $ enemies = [rat, balor, ratb]

    play music "BattleMedium.mp3" fadein 2.0
    $ quick_menu = False
    $ battle_y_offset = 160
    
    call battle(allies, enemies, lust_battle=False) from _call_battle_20

    $ battle_context = None
    $ battle_y_offset = 0
    $ reset_effects()
    
    python:
        final_of_battle(all_allies)
        defeated_enemies = [e for e in enemies if (not e.alive) or getattr(e, "lusted_out", False)]
        xp_reward = sum(e.xp_reward for e in defeated_enemies) # XP total somado
        rewards = []

        if xp_reward > 0:
            party_gain_xp(xp_reward)
            add_reward("xp", xp_reward)
            
        for e in defeated_enemies:
            give_loot_for_enemy(e, rewards, inventario)
        rewards = consolidate_rewards(rewards)

    if battle_result == "victory":
        hide screen turn_order_display
        hide screen actor_overlay
        play sound "69_Enemy_death_01.mp3"

        $ total_items = len(rewards)
        $ last_index = total_items - 1
        $ anim_time = 2.0
        $ delay_per_item = 0.5
        $ total_time = (last_index * delay_per_item) + anim_time
        play sound "LootSound03.mp3"
        show screen reward_list_center(rewards)

        pause total_time
        hide screen reward_list_center
        battlesign "The Enemies has been vanquished!"
        hide screen battle_sprites with dissolve

    elif battle_result == "defeat":
        hide screen turn_order_display
        play sound "17_Def_buff_01.mp3"
        battlesign "The party succumbed to their injuries."
        hide screen battle_sprites with dissolve
        jump game_over

    elif battle_result == "escape":
        hide screen turn_order_display
        hide screen battle_sprites with Dissolve(0.5)
        hide screen actor_overlay
        pause 0.5
        battlesign "You escaped the enemy."
        play sound "51_Flee_02.mp3"

    $ quick_menu = True
    hide screen turn_order_display
    hide screen battle_sprites
    hide screen actor_overlay
    hide screen show_floating_number

    $ tutorial_step = 14
    call screen map_tutorial_overlay
    
    $ unlocked_keys = True
    scene MAP_hungwood_example
    python:
        objectives = [
            {"desc": _("Get the First half of the key."), "done": camp_scene_1_done},
        ]

        if all([camp_scene_1_done]):
            objectives.append({"desc": _("Get the Second half of the key."), "done": camp_scene_2_done})
        if all([camp_scene_1_done, camp_scene_2_done]):
            objectives.append({"desc": _("Enter in the cave."), "done": enter_cave})

        renpy.show_screen("mission_update", _("Clear Hungwood"), objectives, "main")
        renpy.pause (1.0, hard=True)
    call mapa1 from _call_mapa1



















screen map_tutorial_overlay():
    zorder 125
    modal True

    if tutorial_step == 14:
        key "dismiss" action SetVariable("tutorial_step", 15)
        add "map_tutorial1"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 650 ypos 160
            padding (50, 40)
            text "Check your party’s status here.\nClick to continue." textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 800 ypos 75
        text "Tutorial" xpos 870 ypos 125 color "#000000" size 36 font gui.roman
    
    elif tutorial_step == 15:
        key "dismiss" action SetVariable("tutorial_step", 151)
        add "map_tutorial4"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 650 ypos 160
            padding (50, 40)
            text """Click here to expand and check the \nstatus of your party members.\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 780 ypos 75
        text "Tutorial" xpos 850 ypos 125 color "#000000" size 36 font gui.roman

    elif tutorial_step == 151:
        key "dismiss" action SetVariable("tutorial_step", 16)
        add "map_tutorial5"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 650 ypos 160
            padding (50, 40)
            text """Click on hero portraits to open their inventory for heal or change their gear.\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 780 ypos 75
        text "Tutorial" xpos 850 ypos 125 color "#000000" size 36 font gui.roman

    elif tutorial_step == 16:
        key "dismiss" action SetVariable("tutorial_step", 17)
        add "map_tutorial1"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 600 ypos 210
            padding (50, 40)
            xmaximum 800
            text """Click ‘Quests’ to track your current objectives.\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 820 ypos 125
        text "Tutorial" xpos 890 ypos 175 color "#000000" size 36 font gui.roman
    
    elif tutorial_step == 17:
        key "dismiss" action SetVariable("tutorial_step", 18)
        add "map_tutorial1"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 600 ypos 210
            padding (50, 40)
            xmaximum 800
            text """Click ‘Inventory’ to open your party inventory.\n\nSwitch between the different party members to:\n* Equip your gear.\n* Use items on them.\n* See their skill-tree.\n\n\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 820 ypos 125
        text "Tutorial" xpos 900 ypos 175 color "#000000" size 36 font gui.roman

    elif tutorial_step == 18:
        key "dismiss" action SetVariable("tutorial_step", 19)
        add "map_tutorial1"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 600 ypos 210
            padding (50, 40)
            xmaximum 800
            text """Click ‘Party’ to change your party line-up before battles.\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 840 ypos 125
        text "Tutorial" xpos 920 ypos 175 color "#242424" size 36 font gui.roman

    elif tutorial_step == 19:
        key "dismiss" action SetVariable("tutorial_step", 20)
        add "tutorial2"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 580 ypos 700
            padding (50, 40)
            text """Your party is currently in Hungwood Village.\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 790 ypos 620
        text "Tutorial" xpos 860 ypos 670 color "#000000" size 36 font gui.roman

    elif tutorial_step == 20:
        key "dismiss" action Return()
        add "tutorial3"
        frame:
            background Frame("tuto_frame", 15, 15)
            xpos 650 ypos 760
            padding (50, 40)
            text """You can move to any adjacent cell.\nClick to continue.""" textalign 0.5 xalign 0.5 yalign 0.5 color "#000000" size 32 font gui.skill_buttons
        add "tutorialflag.png" xpos 780 ypos 680
        text "Tutorial" xpos 850 ypos 730 color "#000000" size 36 font gui.roman





















label debugdev:
    $ allies = [rodin]
    $ rodin.alive = True
    $ rodin.set_pose("idle")
    $ rodin.hp = rodin.get_stat('hp_max')
    $ rodin.mp = rodin.get_stat('mp_max')
    $ gildrath.alive = True
    $ gildrath.set_pose("idle")
    $ gildrath.hp = gildrath.get_stat('hp_max')
    $ gildrath.mp = gildrath.get_stat('mp_max')
    $ clint.alive = True
    $ clint.set_pose("idle")
    $ clint.hp = clint.get_stat('hp_max')
    $ clint.mp = clint.get_stat('mp_max')
    $ murag.alive = True
    $ murag.set_pose("idle")
    $ murag.hp = murag.get_stat('hp_max')
    $ murag.mp = murag.get_stat('mp_max')
    $ dorik.alive = True
    $ dorik.set_pose("idle")
    $ dorik.hp = dorik.get_stat('hp_max')
    $ dorik.mp = dorik.get_stat('mp_max')
    $ gildrath.clear_all_debuffs() 
    $ dorik.clear_all_debuffs() 
    $ rodin.clear_all_debuffs() 
    $ clint.clear_all_debuffs() 
    $ murag.clear_all_debuffs() 
    python:
        for ally in all_allies:
            ally.reset_all_cooldowns()

    show screen menushorts
    scene bg mountain
    "DEBUG DEV Fights tests"
    $ all_allies = [rodin, murag, dorik, gildrath, clint]
    

    $ battle_y_offset = 0
    $ active_murag = True
    $ active_clint = True
    $ active_gildrath = True
    $ active_dorik = True
    $ active_rodin = True
    "Debug: Add options of fight"
    "Line to open inventory or change party if want 1"
    "Line to open inventory or change party if want 2"
    "Line to open inventory or change party if want 3"
    "Line to open inventory or change party if want 4"
    "Line to open inventory or change party if want 5"
    "Line to open inventory or change party if want 6"
    "Line to open inventory or change party if want 7"
    "Line to open inventory or change party if want 8"
    return







#Lust Attacks
#Rodin
#Tease:  Hello, Beautiful.
#Be Submissive:  Don’t make me beg.
#Be Dominant:  Someone like you deserves to be punished.

#Dorik
#Tease:  
#Dorik "Let’s cut to the fun part, hm?
#Be Submissive:  
#Dorik "I wouldn’t mind kneeling at your crotch for a bit.
##Be Dominant:  
#Dorik "You know you want it, Slut.

#Murag
#Tease:  
#Murag "Hiya cutie!
#Be Submissive:  
#Murag "You’re so big and muscly.  
#Be Dominant:  
#Murag "You’re a bad boy, aren’t you?  

#Gildrath
#Tease:  
#Gildrath "Come here.
#Be Submissive:  
#Gildrath "Let me soothe you.
#Be Dominant:  
#Gildrath "Kneel.

#Clint
#Tease:  
#Clint: There’s so many funner things to do than fighting.
#Be Submissive:  
#Clint "Let me worship you.
#Be Dominant:  
#Clint "Daddy likes his cock slaves on their knees.



