from networkx.utils import powerlaw_sequence
import networkx as nx
import numpy as np
import random
import sys
import networkx as nx
import warnings as _warnings

class Comlib():

    def __init__(self, name):
        self.name = name

    def fixed_generate_community(self, number_of_communities, proba_inner, erdos_nodes_num = 100):
        list_of_communities = [nx.erdos_renyi_graph(erdos_nodes_num, proba_inner) for i in range(number_of_communities)]
        return list_of_communities

    def unite_list_to_one(self, list_of_communities):
        current_graph = nx.Graph()
        if (len(list_of_communities) != 0):
            current_graph = list_of_communities[0]

        for i in range(1,len(list_of_communities)):
            current_graph = nx.disjoint_union(current_graph, list_of_communities[i])
    
        return current_graph 

    def connect_communities_by_edge(self, graph_with_isolated_components, G_configurated_no_comm, erdos_nodes_num = 100):
        count_edges_avg_outer_deg = np.array([0 for i in range(len(graph_with_isolated_components))]) #array for computing average outer degree (between communities) 
        for u,v in G_configurated_no_comm.edges():
            i = np.random.choice(erdos_nodes_num-1)
            j = np.random.choice(erdos_nodes_num-1)
            graph_with_isolated_components.add_edge(erdos_nodes_num*u + i, erdos_nodes_num*v + j)
            count_edges_avg_outer_deg[erdos_nodes_num*u + i] += 1
            count_edges_avg_outer_deg[erdos_nodes_num*v + j] += 1
        #average_degree = len(np.nonzero(count_edges_avg_outer_deg)[0])/np.sum(count_edges_avg_outer_deg)
        #for i in range(number_of_communities - 1):
        #    graph_with_isolated_components.add_edge(20*i, 20*(i+1)) #100 is equal to number of nodes in one component
        return graph_with_isolated_components #, average_degree


    #The code below in this cell is taken from previous implementation of networkx 
    def create_degree_sequence(self, n, sfunction=None, max_tries=50, **kwds):
        _warnings.warn("create_degree_sequence() is deprecated",
                   DeprecationWarning)
        """ Attempt to create a valid degree sequence of length n using
        specified function sfunction(n,**kwds).

        Parameters
        ----------
        n : int
            Length of degree sequence = number of nodes
        sfunction: function
            Function which returns a list of n real or integer values.
            Called as "sfunction(n,**kwds)".
        max_tries: int
            Max number of attempts at creating valid degree sequence.

        Notes
        -----
        Repeatedly create a degree sequence by calling sfunction(n,**kwds)
        until achieving a valid degree sequence. If unsuccessful after
        max_tries attempts, raise an exception.
    
        For examples of sfunctions that return sequences of random numbers,
        see networkx.Utils.

        Examples
        --------
        >>> from networkx.utils import uniform_sequence, create_degree_sequence
        >>> seq=create_degree_sequence(10,uniform_sequence)
        """
        tries=0
        max_deg=n
        while tries < max_tries:
            trialseq=sfunction(n,**kwds)
            # round to integer values in the range [0,max_deg]
            seq=[min(max_deg, max( int(round(s)),0 )) for s in trialseq]
            # if graphical return, else throw away and try again
            if is_valid_degree_sequence(seq):
                return seq
            tries+=1
        raise nx.NetworkXError(\
              "Exceeded max (%d) attempts at a valid sequence."%max_tries)

    def is_valid_degree_sequence_erdos_gallai(self, deg_sequence):
        """Returns True if deg_sequence is a valid degree sequence.
    
        A degree sequence is valid if some graph can realize it. 
        Validation proceeds via the Erdős-Gallai algorithm.
        
        Worst-case run time is: O( n**2 )
    
        Parameters
        ----------
        deg_sequence : list
            A list of integers where each element specifies the degree of a node
            in a graph.

        Returns
        -------
         valid : bool
            True if deg_sequence is a valid degree sequence and False if not.
    
        References
        ----------
        [EG1960]_, [choudum1986]_    

        """
        # some simple tests 
        if deg_sequence==[]:
            return True # empty sequence = empty graph 
        if not nx.utils.is_list_of_ints(deg_sequence):
            return False   # list of ints
        if min(deg_sequence)<0:
            return False      # each int not negative
        if sum(deg_sequence)%2:
            return False      # must be even

        n = len(deg_sequence)
        deg_seq = sorted(deg_sequence,reverse=True)
        sigk = [i for i in range(1, len(deg_seq)) if deg_seq[i] < deg_seq[i-1]]
        for k in sigk:
            sum_deg = sum(deg_seq[0:k])
            sum_min = k*(k-1) + sum([min([k,deg_seq[i]]) 
                                     for i in range(k,n)])
            if sum_deg>sum_min:
                return False
        return True

    def is_valid_degree_sequence_havel_hakimi(self, deg_sequence):
        """Returns True if deg_sequence is a valid degree sequence.
        
        A degree sequence is valid if some graph can realize it. 
        Validation proceeds via the Havel-Hakimi algorithm.
        
        Worst-case run time is: O( n**(log n) )
        
        Parameters
        ----------
        deg_sequence : list
            A list of integers where each element specifies the degree of a node
            in a graph.
    
        Returns
        -------
        valid : bool
            True if deg_sequence is a valid degree sequence and False if not.
        
        References
        ----------
        [havel1955]_, [hakimi1962]_, [CL1996]_
    
        """
        # some simple tests 
        if deg_sequence==[]:
            return True # empty sequence = empty graph 
        if not nx.utils.is_list_of_ints(deg_sequence):
            return False   # list of ints
        if min(deg_sequence)<0:
            return False      # each int not negative
        if sum(deg_sequence)%2:
            return False      # must be even
    
        # successively reduce degree sequence by removing node of maximum degree
        # as in Havel-Hakimi algorithm
            
        s=deg_sequence[:]  # copy to s
        while s:      
            s.sort()    # sort in increasing order
            if s[0]<0: 
                return False  # check if removed too many from some node

            d=s.pop()             # pop largest degree 
            if d==0: return True  # done! rest must be zero due to ordering
    
            # degree must be <= number of available nodes
            if d>len(s):   return False
    
            # remove edges to nodes of next higher degrees
            #s.reverse()  # to make it easy to get at higher degree nodes.
            for i in range(len(s)-1,len(s)-(d+1),-1):
                s[i]-=1
    
        # should never get here b/c either d==0, d>len(s) or d<0 before s=[]
        return False

    def is_valid_degree_sequence(self, deg_sequence, method='hh'):
        """Returns True if deg_sequence is a valid degree sequence.
    
        A degree sequence is valid if some graph can realize it.
        
        Parameters
        ----------
        deg_sequence : list
            A list of integers where each element specifies the degree of a node
            in a graph.
        method : "eg" | "hh"
            The method used to validate the degree sequence.  
            "eg" corresponds to the Erdős-Gallai algorithm, and 
            "hh" to the Havel-Hakimi algorithm.
    
        Returns
        -------
        valid : bool
            True if deg_sequence is a valid degree sequence and False if not.
        
        References
        ----------
        Erdős-Gallai
            [EG1960]_, [choudum1986]_
        
        Havel-Hakimi
            [havel1955]_, [hakimi1962]_, [CL1996]_
    
        """
        if method == 'eg':
            valid = is_valid_degree_sequence_erdos_gallai(deg_sequence)
        elif method == 'hh':
            valid = is_valid_degree_sequence_havel_hakimi(deg_sequence)
        else:
            msg = "`method` must be 'eg' or 'hh'"
            raise nx.NetworkXException(msg)
        
        return valid

    def generate_powerlaw_partial(self, Graph, percentage):
        if percentage > 1 or percentage < 0:
            print('Enter percentage between 0 and 1')
            return
        
        nodes_in_subgraph = []
    
        arr_of_nodes = np.array(list(Graph.nodes()))
        number_of_vertices = int(len(Graph.nodes())*percentage)
        for i in range(number_of_vertices):
            elem = np.random.choice(arr_of_nodes)             
            nodes_in_subgraph.append(elem)
            tmp_res = np.where(arr_of_nodes == elem)
            arr_of_nodes = np.delete(arr_of_nodes, tmp_res[0][0])
        x = create_degree_sequence(number_of_vertices, powerlaw_sequence)
        G_subgraph_percentage = nx.configuration_model(x)
        return G_subgraph_percentage, nodes_in_subgraph
    
    def relabelling_nodes(self, Graph, list_for_mapping):
        G_relabelled = nx.relabel_nodes(Graph, dict(zip(list(Graph.nodes()), list_for_mapping)))
        return G_relabelled
    
    def merge_relabelled_with_erdos_communities(self, G_relabelled_partial, G_erdos_communities):
        for (u,v) in G_relabelled_partial.edges():
            if (u,v) not in G_erdos_communities.edges():
                G_erdos_communities.add_edge(u,v)
        return G_erdos_communities 

