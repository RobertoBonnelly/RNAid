import unittest
import data_mining as dm
import fingerprint as fing

ver_get_data = [['-8.2', '14', '..', '24', 'xxATGAAAGCATTCT', 'GGCG','TAA', 'CGCC', 'GCGTTGCTCGCGGTT'], ['-6.9', '13', '..', '25', 'xxxATGAAAGCATTC', 'TGGCG', 'TAA', 'CGCCG', 'CGTTGCTCGCGGTTT'], ['-3.4', '12', '..', '26', 'xxxxATGAAAGCATT', 'CTGGCG', 'TAA', 'CGCCGC', 'GTTGCTCGCGGTTTC']]

ver_pal = [[12, 17, 21, 26], [13, 17, 21, 25], [14, 17, 21, 24]]

ver_rel = 'X'

ver_graph = {0:[], 1:[], 2:[]}

ver_path = [[0]]

ver_dag = [0]
## add a file that is empty, a file that does not exist, a file with a different format
## if a file has multiple sequences

# add multiple relations hairpins to enhance relations test

# pal test can only deal when a hairpin file has 1 sequence

# check all possible positions for each relation

# add multiple sequence possibility for get_data function

class testFing(unittest.TestCase):

    def test_get_data(self):
        self.assertEqual(dm.get_data('../test_data.out')[1], ver_get_data)
        self.assertEqual(dm.get_data('../test_data_empty.out')[1], [])
        self.assertEqual(dm.get_data('../test_data_compempty.out'), None)

    def test_pal(self):
        self.assertEqual(fing.palindromes(ver_get_data), ver_pal)
    
    def test_rel(self):
        self.assertEqual(fing.relation(ver_pal[0], ver_pal[1]), ver_rel)

    def test_graph(self):
        self.assertEqual(fing.pgraph(ver_pal), ver_graph)
    
    def test_path(self):
        self.assertEqual(fing.path(ver_graph, 0), ver_path)

    def test_pal(self):
        self.assertEqual(fing.dag(ver_path), ver_dag)