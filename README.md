# This is the Iterated Prisoner's Dilemma

# Coding agents
The stuff needed will be in the SimulationFramework folder
you can put you're agents inside the agents folder. To get started
you can simply just copy over tit_for_tat_agent.py as that will have
many of the actions you'd want.

Look at abstract_agent.py or other examples to see exactly what you need.
Essentially though, you will need to create the decide method and have it 
return either DecisionEnum.COOPERATE or DecisionEnum.DEFECT and that's 
all you need to do.

# Visualizing
If you'd like a neat animation, go into GameSection folder, and then into exports. Click on the exe
to get into the visualization. Then click start afterwards it will bring up the menu to select a txt
file. Make sure you select the output of the file, and it will then play a little animation.
Press the reset button in the bottom left to restart.

If you'd like to build the exe from source, download Godot 4.5 and drag the folder into the editor to have Godot recognize the project. Then either export it or play it in the godot editor with the top right actions in its menu.

