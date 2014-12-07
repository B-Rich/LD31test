from random import shuffle
from datastructures import *

class Graph :
    def __init__(self,size,start_point,end_point,min_steps=1) :

        self.start_point = start_point
        self.end_point = end_point
        self.size = size

        # generates the path from start_point to end_point with a random walk of length >= min_steps
        ok = False
        while not ok :
            # initializes the graph structure
            self.nodes = {}
            self.edges = []
            for x in xrange(size[0]) :
                for y in xrange(size[1]) :
                    self.nodes[(x,y)] = {'candidate':True, 'color':'white'}    
    
            ok = self.randomWalk(start_point,end_point) and len(self.edges) >= min_steps

        # generates the misleading paths by connecting leftover nodes to the main path
        while len([n for n in self.nodes if self.nodes[n]['color'] == 'white']) > 0 :
            nodes_in_path = [n for n in self.nodes if self.nodes[n]['color'] != 'white' and len([y for y in self.neighbors(n) if self.nodes[y]['color'] == 'white'])>0]
            shuffle(nodes_in_path)
            new_x = nodes_in_path[0]
            choices = [y for y in self.neighbors(new_x) if self.nodes[y]['color'] == 'white']
            shuffle(choices)
            new_y = choices[0]
            self.nodes[new_y]['color'] = 'grey'
            self.edges.append( (new_x,new_y) )


        '''
        leftovers = [n for n in self.nodes if n['color'] == 'white']
        while len(leftovers) == 0 :
            choices = [n for n in self.nodes if len([y for y in self.neighbors(n) self.nodes[y]['color']!='white'])>0'''

    def neighbors(self,node) :
        x,y = node
        nbors = [(x+b,y) for b in [-1,+1] if x+b >= 0 and x+b < self.size[0]]
        nbors += [(x,y+b) for b in [-1,+1] if y+b >= 0 and y+b < self.size[1]]
        return nbors

    def randomWalk(self,sp,ep) :

        # the 'random' in 'randomWalk'
        choices = [n for n in self.neighbors(sp) if self.nodes[n]['candidate'] and self.nodes[n]['color'] == 'white']
        shuffle(choices)

        self.nodes[sp]['color'] = 'black'

        for c in choices :
            if c == ep : # we made it!
                self.nodes[ep]['color'] = 'black'
                self.edges.append((sp,c))
                return True
            elif not self.randomWalk(c,ep) : # all the paths passing through candidate c lead to a dead end
                self.nodes[c]['candidate'] = False
                self.nodes[c]['color'] = 'white'
            else :
                self.edges.append((sp,c))
                return True
            
        # dead end :(
        return False
    
    def pp(self) :
        s1 = ''
        s2 = ''
        for x in xrange(self.size[0]) :
            for y in xrange(self.size[1]) :
                if self.nodes[(x,y)]['color'] == 'black' :
                    s1+='#'
                else :
                    s1+=' '
                if self.nodes[(x,y)]['candidate'] :
                    s2 += '*'
                else :
                    s2 += ' '
            s1 +='\n'
            s2+='\n'
        print s1
        print ""
        print s2
        print "EDGES: " + str(self.edges)
                

    def graphToMatrix(self) :

        matrix = {}

        for x in xrange(self.size[0]*2 + 2) :
            for y in xrange(self.size[1]*2 + 2) :
                if (x*y)%2 == 0 :
                    matrix[(x,y)] = 1
                else :
                    matrix[(x,y)] = 0

        for n1,n2 in self.edges :
            x1,y1 = (n1[0]*2 + 1, n1[1]*2 + 1)
            x2,y2 = (n2[0]*2 + 1, n2[1]*2 + 1)

            if x1 == x2 :
                matrix[(x1,max(y1,y2)-1)] = 0
            elif y1 == y2 :
                matrix[(max(x1,x2)-1),y1] = 0
            
            else :
                raise ValueError("Diagonal edges?")

        return matrix


if __name__ == '__main__' :
    g = Graph((26,20),(0,0),(25,19))
    
    matrix = g.graphToMatrix()
    s = ''
    for y in xrange(max(map(lambda x:x[1],matrix.keys()))) :
        for x in xrange(max(map(lambda x:x[0],matrix.keys()))) :
        
            if matrix[(x,y)] == 0 :
                s += ' '
            else : 
                s += '#'
        s += '\n'
        
    g = GameMapData()
    l = LevelData()
    l.matrix = matrix
    g.levels[0] = l
    g.save("level.dat")
    print s