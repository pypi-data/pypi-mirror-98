"""
classes used by mummichog

"""

import numpy as np
# mummichog uses nx 1.x
import networkx as nx

# will redo evaluation of empCpd
primary_ions = ['M+H[1+]', 'M+Na[1+]', 'M-H2O+H[1+]', 'M-H[-]', 'M-2H[2-]', 'M-H2O-H[-]']
# weighting function of isotopic derivatives and adducts
dict_weight_adduct = {
            'M[1+]': 5, 
            'M+H[1+]': 5,
            'M+2H[2+]': 3,
            'M+3H[3+]': 1,
            'M(C13)+H[1+]': 2,
            'M(C13)+2H[2+]': 1,
            'M(C13)+3H[3+]': 1,
            'M(S34)+H[1+]': 1,
            'M(Cl37)+H[1+]': 1,
            'M+Na[1+]': 3, 
            'M+H+Na[2+]': 2,
            'M+K[1+]': 2, 
            'M+H2O+H[1+]': 1, 
            'M-H2O+H[1+]': 1, 
            'M-H4O2+H[1+]': 1,
            'M-NH3+H[1+]': 1,
            'M-CO+H[1+]': 1,
            'M-CO2+H[1+]': 1,
            'M-HCOOH+H[1+]': 1,
            'M+HCOONa[1+]': 1,
            'M-HCOONa+H[1+]': 1,
            'M+NaCl[1+]': 1, 
            'M-C3H4O2+H[1+]': 1,
            'M+HCOOK[1+]': 1,
            'M-HCOOK+H[1+]': 1,
            # negative
            'M-H[-]': 5,
            'M-2H[2-]': 3,
            'M(C13)-H[-]': 2,
            'M(S34)-H[-]': 1,
            'M(Cl37)-H[-]': 1,
            'M+Na-2H[-]': 2,
            'M+K-2H[-]': 1,
            'M-H2O-H[-]': 1,
            'M+Cl[-]': 1,
            'M+Cl37[-]': 1,
            'M+Br[-]': 1,
            'M+Br81[-]': 1,
            'M+ACN-H[-]': 1,
            'M+HCOO[-]': 1,
            'M+CH3COO[-]': 1,
            'M-H+O[-]': 1,
                    }

#
# -----------------------------------------------------------------------------
#
# classes for theoretical metabolic models

class metabolicPathway:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.rxns = []
        self.ecs = []
        self.ec_num = 0
        self.cpds = []
        self.cpd_num = 0
        
        self.selected_features = []
        self.combined_pvalue = 0    # -log10()
        
    def str_import(self, s):
        '''
        function to import pathway from plain text;
        excluding currency metabolites.
        Not used for now.
        '''
        a = s.rstrip().split('\t')
        self.id = a[0]
        self.name = a[1]
        self.rxns = a[2].split(';')
        self.ecs = a[3].split(';')
        self.ec_num = int(a[4])
        cpds = a[5].split(';')
        self.cpds = [x for x in cpds if x not in currency]
        self.cpd_num = len(self.cpds)
        
    def json_import(self, j):
        '''
        function to import pathway from JSON format.
        '''
        self.id = j['id']
        self.name = j['name']
        self.rxns = j['rxns']
        self.ecs = j['ecs']
        self.ec_num = len(j['ecs'])
        self.cpds = j['cpds']
        self.cpd_num = len(j['cpds'])


class metabolicNetwork:
    '''
    Metabolite-centric metabolic model 
    Theoretical model, not containing user data
    '''
    def __init__(self, MetabolicModel):
        '''
        Initiation of metabolic network model.
        Building Compound index.
        Parsing input files.
        Matching m/z - Compound.
        
        MetabolicModel['Compounds'] are subset of cpds in network/pathways with mw.
        Not all in total_cpd_list has mw.
        '''
        #print_and_loginfo( "Loading metabolic network %s..." %MetabolicModel.version ) # version from metabolic model
        
        self.MetabolicModel = MetabolicModel
        self.network = self.build_network(MetabolicModel['cpd_edges'])
        
        self.version = MetabolicModel['version']
        self.Compounds = MetabolicModel['Compounds']
        self.metabolic_pathways = MetabolicModel['metabolic_pathways']
        self.dict_cpds_def = MetabolicModel['dict_cpds_def']
        self.cpd2pathways = MetabolicModel['cpd2pathways']
        self.edge2enzyme = MetabolicModel['edge2enzyme']
        self.total_cpd_list = self.network.nodes()
        
        
    def build_network(self, edges):
        return nx.from_edgelist( edges )
        

    def get_pathways(self):
        pass
 

class Mmodule:
    '''
    Metabolites by their connection in metabolic network.
    A module is a subgraph, while modularity is calculated in 
    the background of reference hsanet.
    
    
    need to record sig EmpCpds
    
    '''
    def __init__(self, network, subgraph, TrioList):
        '''
        TrioList (seeds) format: [(M.row_number, EmpiricalCompounds, Cpd), ...]
        to keep tracking of where the EmpCpd came from (mzFeature).
        
        network is the total parent metabolic network
        '''
        self.network = network
        self.num_ref_edges = self.network.number_of_edges()
        self.num_ref_nodes = self.network.number_of_nodes()
        self.graph = subgraph
        
        seed_cpds = [x[2] for x in TrioList]
        self.shave(seed_cpds)
        self.nodestr = self.make_nodestr()
        self.N_seeds = len(seed_cpds)
        self.A = self.activity_score(seed_cpds, self.get_num_EmpCpd(TrioList))
    
    def activity_score(self, seed_cpds, num_EmpCpd):
        '''
        A * (Ns/Nm)
        A = Newman-Girvan modularity score
        Ns = number of input cpds in module M
        Nm = number of total cpds in M
        Ns/Nm can be corrected as (Ns/total input size)/(Nm/network size), however,
        this normalization factor holds the same in permutations. 
        Use 100 here for network size/total input size.
        
        To reduce bias towards larger modules in Q:
        np.sqrt(len(seed_cpds)/Nm) * 
        
        Ns is now controlled by number of empiricalCompounds
        '''
        Ns = num_EmpCpd
        Nm = float(self.graph.number_of_nodes())
        if Nm > 0:
            self.compute_modularity()
            return np.sqrt(self.N_seeds/Nm) *self.Q * (Ns/Nm) * 100
        else:
            return 0
        
        
    def get_num_EmpCpd(self, TrioList):
        new = []
        subgraph_nodes = self.graph.nodes()
        for x in TrioList:
            if x[2] in subgraph_nodes:
                new.append(x[1])
                
        return len(set(new))
        
        
    def compute_modularity(self):
        '''
        To compute Newman-Girvan modularity for a single module,
        in reference to the whole network.
        '''
        m = self.num_ref_edges
        Nodes = self.graph.nodes()
        expected = 0
        for ii in Nodes:
            for jj in Nodes:
                if ii != jj:
                    expected += self.network.degree(ii) * self.network.degree(jj)
                    
        expected /= (4.0 * m)
        self.Q = (self.graph.number_of_edges() - expected) / m
    
    def test_compute_modularity(self):
        '''
        Alternative modularity measure as 
        edges in module over all edges on the same nodes
        '''
        m = float(self.graph.number_of_edges())
        expected = 0
        for ii in self.graph.nodes(): expected += self.network.degree(ii)
        self.Q = 2 * m * (np.sqrt(self.graph.number_of_nodes())) / expected
        
        
    def shave(self, seed_cpds):
        '''
        shave off nodes that do not connect seeds, i.e.
        any node with degree = 1 and is not a seed, iteratively.
        '''
        nonseeds = [x for x in self.graph.nodes() if x not in seed_cpds]
        excessive = [x for x in nonseeds if self.graph.degree(x)==1]
        while excessive:
            for x in excessive: self.graph.remove_node(x)
            nonseeds = [x for x in self.graph.nodes() if x not in seed_cpds]
            excessive = [x for x in nonseeds if self.graph.degree(x)==1]


    def make_nodestr(self):
        '''
        create an identifier using nodes in sorted order
        '''
        Nodes = self.graph.nodes()
        Nodes.sort()
        return ''.join(Nodes)

    def export_network_txt(self, met_model, filename):
        '''
        To use .txt for Cytoscape 3, no need for .sif any more.
        Edges are strings now as switching to JSON compatible.
        '''
        s = 'SOURCE\tTARGET\tENZYMES\n'
        for e in self.graph.edges():
            s += e[0] + '\t' + e[1] + '\t' + met_model.edge2enzyme.get(','.join(sorted(e)), '') + '\n'
        
        out = open(filename, 'w')
        out.write(s)
        out.close()



#
# -----------------------------------------------------------------------------
#
# classes for data structure from MS

class MassFeature:
    '''
    Data model, to store info per input feature
    row_number is used as unique ID. A string like "row23" is used instead of integer for two reasons:
    to enforce unique IDs in string not in number, and for clarity throughout the code;
    to have human friendly numbering, starting from 1 not 0.
    '''
    def __init__(self, row_number, mz, retention_time, p_value, statistic, CompoundID_from_user=''):
        self.row_number = row_number        # Unique ID
        self.mz = mz
        self.retention_time = retention_time
        self.retention_time_rank = 0

        self.p_value = p_value
        self.statistic = statistic
        self.CompoundID_from_user = CompoundID_from_user
        
        self.matched_Ions = []
        self.matched_Compounds = []
        self.matched_EmpiricalCompounds = []
        
        self.is_significant = False
        
        # for future use
        self.peak_quality = 0
        self.database_match = []

    def make_str_output(self):
        return '\t'.join( [str(x) for x in [self.row_number, self.mz, self.retention_time, 
                            self.p_value, self.statistic, self.CompoundID_from_user,
                            ]] ) 


class EmpiricalCompound:
    '''
    Carryover from mummichog 2.

    to be updated from .core
    
    and move annotation to mass2chem
    
    '''
    def __init__(self, listOfFeatures):
        '''
        Initiation using 
        listOfFeatures = [[retention_time, row_number, ion, mass, compoundID], ...]
        This will be merged and split later to get final set of EmpCpds.
        '''
        self.listOfFeatures = listOfFeatures
        self.listOfFeatures.sort(key=lambda x: x[1])
        self.str_row_ion = self.__make_str_row_ion__()          # also a unique ID
        self.__unpack_listOfFeatures__()
        
        self.EID = ''
        self.chosen_compounds = []
        self.face_compound = ''
        
        self.evidence_score = 0
        self.primary_ion_present = False
        self.statistic = 0
    
    def __make_str_row_ion__(self):
        '''
        feature order is fixed now after sorting by row_number
        '''
        return ";".join([x[1]+'_'+x[2] for x in self.listOfFeatures])
    
    
    def __unpack_listOfFeatures__(self):
        
        self.compounds = list(set([x[4] for x in self.listOfFeatures]))
        self.massfeature_rows = [x[1] for x in self.listOfFeatures]
        self.ions = dict([x[2:4] for x in self.listOfFeatures])
        self.row_to_ion = dict( [x[1:3] for x in self.listOfFeatures] )
        
        
    def join(self, E):
        '''
        join another instance with identical ions.
        str_row_ion must be the same to be joined.
        '''
        for c in E.compounds:
            if c not in self.compounds:
                self.compounds.append(c)
        
        
    def evaluate(self):
        '''
        test if EmpCpds has any of primary_ions as defined in config.py, 
        ['M+H[1+]', 'M+Na[1+]', 'M-H2O+H[1+]', 'M-H[-]', 'M-2H[2-]', 'M-H2O-H[-]']
        
        evidence_score is combining weight scores from multiple adducts.
        
        No need to separate ionMode upfront ("positive", "negative")
        Bad ones should not be used for downstream analysis...
        
        '''
        
        if set(self.ions.keys()).intersection(primary_ions):
            self.primary_ion_present = True
        
        for x in self.ions.keys(): 
            self.evidence_score += dict_weight_adduct[x]
            
            
    def update_chosen_cpds(self, cpd):
        if cpd not in self.chosen_compounds:
            self.chosen_compounds.append(cpd)

    def designate_face_cpd(self):
        '''
        When there are more than one compounds suggested by pathway and module analysis,
        one is arbitrarily designated as "face compound".
        '''
        self.face_compound = self.chosen_compounds[-1]

    def get_mzFeature_of_highest_statistic(self, dict_mzFeature):
        '''
        Take highest abs(statistic) among all matched ions,
        which will give statistic value for downstream output.
        '''
        all = [dict_mzFeature[r] for r in self.massfeature_rows]
        all.sort(key=lambda m: abs(m.statistic))
        self.mzFeature_of_highest_statistic = all[-1]
