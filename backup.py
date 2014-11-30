def uniformCostSearch(problem):
    
    """
    Search the node of least total cost first.
    
    Code written by: 
        Nike Lambooy
        Nicky Lenaers
        
    UCS takes O(b^(C*/e)) time with
        b  = maximum branching factor
        C* = cost of optimal solution
        e  = some positive bound

    UCS takes O(b^(C*/e)) space.
    """
    
    # Initialize PriorityQueue() instance for fringe (Source: College 2, Slide 37)
    fringe = util.PriorityQueue()
    visited = util.Stack()
    parents = util.Queue()
    actions = util.Queue()
    
    # Push first state with priority zero
    fringe.push(problem.getStartState(), 0)
    
    smallest = fringe.pop()
    
    while not problem.isGoalState(smallest):
        
        # First item is lowerst-cost item in the heap
        successors = problem.getSuccessors(smallest)
        
        # Got successors, so mark as visited
        visited.push(smallest)
        
        # Build actions
        del actions.list[:]
        state = smallest        
        
        # Build actions
        while state != problem.getStartState():

            for index in xrange(len(parents.list)):

                if state == parents.list[index][0]:

                    actions.push(parents.list[index][2])
                    state = parents.list[index][1]
        
        totalcost = problem.getCostOfActions(actions.list)
        
        # Loop over successors using xrange loading lazingly
        for index in reversed(xrange(len(successors))):
            
            cost = 0
            
            # If successor is already seen
            for j in range(len(fringe.heap)):
                if successors[index][0] in fringe.heap[j]:
                    cost = fringe.heap[j][0]
            
            if successors[index][0] not in visited.list and cost < totalcost + successors[index][2]:
                
                # Addition of cost-so-far and cost of successor being pushed to the fringe heap
                fringe.push(successors[index][0], totalcost + successors[index][2])
                parents.push([successors[index][0], smallest, successors[index][1]])
        
        # Get the highest priority item from the priority queueu
        smallest = fringe.pop()
    
    actions.list.append(parents.list[0][2])
    
    return actions.list