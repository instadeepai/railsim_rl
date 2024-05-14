

# JAVA Part: 

def reset(): -> state
- > The simulation of Railsim would start. Reset() fuynction would be called by the python code

def getAction(state): -> action
- > Get action from RL corresponding to particular state


# Python Part: 

next_state = None

# Callback function called by the JAVA code
def onGetActionCall(state):
    global.next_state = state
    with torch.no_grad():
        action = rlModel(state)
    return action
    

def reset() -> tuple(state, info):
    state, info = java.RailSim.reset()
    return state, info

# This function would be called by the trainer of RLLib. 
def step(action) -> state, reward, terminated, truncated, info
    
    # Wait until next_state is not received  
    while (global.next_state == None):
        pass
    state = next_state
    global.next_state = None
    return state