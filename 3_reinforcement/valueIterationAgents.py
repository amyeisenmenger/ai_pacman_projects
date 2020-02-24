# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        # Write value iteration code here
        states = mdp.getStates()
        for _ in range(0,self.iterations):
          # create temporary values for for k iteration update
            tempValues = util.Counter()
            # loop over states to find max q value
            for state in states:
                if not mdp.isTerminal(state):
                    actions = mdp.getPossibleActions(state)
                    tempValues[state] = max([self.getQValue(state,action) for action in actions])
            # set values to k iteration update values
            self.values = tempValues




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # "*** YOUR CODE HERE ***"
        qValue = 0
        # get the transition states and their probabilities from the mdp
        transitionStates =  self.mdp.getTransitionStatesAndProbs(state, action)
        # loop over possible new states and calculate their value
        # add their value to the state's q value

        for nextStateTransition in transitionStates:
            nextState = nextStateTransition[0]
            transitionProbability = nextStateTransition[1]
            reward = self.mdp.getReward(state, action, nextState)
            qValue += transitionProbability*(reward + self.discount*self.getValue(nextState))
        return qValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        # if state is terminal return none
        if self.mdp.isTerminal(state):
            return None
        # get action with max q value
        actions = self.mdp.getPossibleActions(state)
        qValues = [self.getQValue(state,action) for action in actions]

        maxQValIndex = qValues.index(max(qValues))
        optimalAction = actions[maxQValIndex]
        return optimalAction


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
