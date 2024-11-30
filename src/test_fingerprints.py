import unittest
import new_fingerprint_functions as nf

ver_get_data = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [['-1',
   '33',
   '..',
   '43',
   'TTAATCCGACTTTGA',
   'CAAC',
   'CGG',
   'GATG',
   'GACCTCTTACAGGTG'],
  ['-0.3',
   '38',
   '..',
   '48',
   'CCGACTTTGACAACC',
   'GGG',
   'ATGGA',
   'CCT',
   'CTTACAGGTGGGAGA'],
  ['-2.5',
   '46',
   '..',
   '56',
   'GACAACCGGGATGGA',
   'CCT',
   'CTTAC',
   'AGG',
   'TGGGAGAGACGGAAG'],
  ['-3.4',
   '45',
   '..',
   '57',
   'TGACAACCGGGATGG',
   'ACCT',
   'CTTAC',
   'AGGT',
   'GGGAGAGACGGAAGT']]}

ver_get_data_multi = {'FC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD':
                      [['-8.2', '14', '..', '24', 'xxATGAAAGCATTCT', 'GGCG', 'TAA', 'CGCC', 'GCGTTGCTCGCGGTT'], ['-6.9', '13', '..', '25', 'xxxATGAAAGCATTC', 'TGGCG', 'TAA', 'CGCCG', 'CGTTGCTCGCGGTTT'], ['-3.4', '12', '..', '26', 'xxxxATGAAAGCATT', 'CTGGCG', 'TAA', 'CGCCGC', 'GTTGCTCGCGGTTTC']], 
                      'NC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD':
                      [['-9.2', '14', '..', '24', 'xxATGAAAGCATTCT', 'GGCG', 'TAA', 'CGCC', 'GCGTTGCTCGCGGTT'], ['-6.9', '13', '..', '25', 'xxxATGAAAGCATTC', 'TGGCG', 'TAA', 'CGCCG', 'CGTTGCTCGCGGTTT'], ['-3.4', '12', '..', '26', 'xxxxATGAAAGCATT', 'CTGGCG', 'TAA', 'CGCCGC', 'GTTGCTCGCGGTTTC']], 
                      'MC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD':
                      [['-1.2', '14', '..', '24', 'xxATGAAAGCATTCT', 'GGCG', 'TAA', 'CGCC', 'GCGTTGCTCGCGGTT'], ['-6.9', '13', '..', '25', 'xxxATGAAAGCATTC', 'TGGCG', 'TAA', 'CGCCG', 'CGTTGCTCGCGGTTT'], ['-3.4', '12', '..', '26', 'xxxxATGAAAGCATT', 'CTGGCG', 'TAA', 'CGCCGC', 'GTTGCTCGCGGTTTC']]}

ver_pal = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [[33,
   36,
   40,
   43],
  [38, 40, 46, 48],
  [45, 48, 54, 57],
  [46, 48, 54, 56]]}

ver_pal_multi = {'FC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD': 
                 [[12, 17, 21, 26], [13, 17, 21, 25], [14, 17, 21, 24]], 
                 'NC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD': 
                 [[12, 17, 21, 26], [13, 17, 21, 25], [14, 17, 21, 24]], 
                 'MC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD': 
                 [[12, 17, 21, 26], [13, 17, 21, 25], [14, 17, 21, 24]]}


ver_rel = 'X'


serial_pal = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [[33,
   36,
   40,
   43],
  [38, 40, 46, 48],
  [45, 48, 54, 57],
  [46, 48, 54, 56],
  [46, 50, 55, 59],
  [47, 52, 57, 62],
  [47, 53, 58, 64],
  [72, 77, 81, 86],
  [73, 77, 81, 85],
  [74, 77, 81, 84],
  [80, 83, 88, 91]]}

IOS_seqname = 'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD'

ver_rel_S = 'S'

ver_rel_O = 'O'

# palindromes with overlapping relationship
overlapping_pal = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [[33,
   36,
   40,
   43],
  [37, 39, 45, 48]]}

ver_rel_I = 'I'

# palindromes with inclusive relationship
inclusive_pal = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [
  [42, 45, 57, 60],
  [46, 48, 54, 56]]}


ver_graph = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': {0: [2,
   3],
  1: [],
  2: [],
  3: []}}

ver_graph_multi = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': {0: [2,
   3,
   4,
   5,
   6,
   7,
   8,
   9,
   10],
  1: [7, 8, 9, 10],
  2: [7, 8, 9, 10],
  3: [7, 8, 9, 10],
  4: [7, 8, 9, 10],
  5: [7, 8, 9, 10],
  6: [7, 8, 9, 10],
  7: [],
  8: [],
  9: [],
  10: []},
 'AACY023852401.1:c427-367 Marine metagenome ctg_1101668659752, whole genome shotgun sequence FORWARD': {0: [4,
   5,
   6],
  1: [4, 5, 6],
  2: [4, 5, 6],
  3: [4, 5, 6],
  4: [6],
  5: [],
  6: []},
 'CT978603.1:1340859-1340915 Synechococcus sp. RCC307 genomic DNA sequence FORWARD': {0: [14,
   15,
   16],
  1: [14, 15, 16],
  2: [13, 14, 15, 16],
  3: [13, 14, 15, 16],
  4: [11, 12, 13, 14, 15, 16],
  5: [11, 12, 13, 14, 15, 16],
  6: [11, 12, 13, 14, 15, 16],
  7: [11, 12, 13, 14, 15, 16],
  8: [11, 12, 13, 14, 15, 16],
  9: [11, 12, 13, 14, 15, 16],
  10: [11, 12, 13, 14, 15, 16],
  11: [16],
  12: [],
  13: [],
  14: [],
  15: [],
  16: []}}

ver_path = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [[0,
   2,
   7],
  [0, 2, 8],
  [0, 2, 9],
  [0, 2, 10],
  [0, 3, 7],
  [0, 3, 8],
  [0, 3, 9],
  [0, 3, 10],
  [0, 4, 7],
  [0, 4, 8],
  [0, 4, 9],
  [0, 4, 10],
  [0, 5, 7],
  [0, 5, 8],
  [0, 5, 9],
  [0, 5, 10],
  [0, 6, 7],
  [0, 6, 8],
  [0, 6, 9],
  [0, 6, 10],
  [0, 7],
  [0, 8],
  [0, 9],
  [0, 10]],
 'AACY023852401.1:c427-367 Marine metagenome ctg_1101668659752, whole genome shotgun sequence FORWARD': [[0,
   4,
   6],
  [0, 5],
  [0, 6]],
 'CT978603.1:1340859-1340915 Synechococcus sp. RCC307 genomic DNA sequence FORWARD': [[0,
   14],
  [0, 15],
  [0, 16]]}

ver_dag = {'CP001344.1:2330090-2330186 Cyanothece sp. PCC 7425, complete genome FORWARD': [0,
  2,
  7],
 'AACY023852401.1:c427-367 Marine metagenome ctg_1101668659752, whole genome shotgun sequence FORWARD': [0,
  4,
  6],
 'CT978603.1:1340859-1340915 Synechococcus sp. RCC307 genomic DNA sequence FORWARD': [0,
  14]}
## a file that does not exist, a file with a different format

# add multiple relations hairpins to enhance relations test

# pal test can only deal when a hairpin file has 1 sequence

# check all possible positions for each relation

# add multiple sequence possibility for get_data function

class testFing(unittest.TestCase):

    def test_get_data(self):
        self.assertEqual(nf.get_data('../test_sequence_1.fasta.out'), ver_get_data)
        self.assertEqual(nf.get_data('../test_data_empty.out'), {'NC_000913.3:c645003-644197 rna [organism=Escherichia coli str. K-12 substr. MG1655] [GeneID=949065] [chromosome=] FORWARD':[]})
        self.assertEqual(nf.get_data('../test_data_compempty.out'), {})
        self.assertEqual(nf.get_data('../test_multi.out'), ver_get_data_multi)

    def test_pal(self):
        self.assertEqual(nf.new_palindromes(ver_get_data), ver_pal)
        self.assertEqual(nf.new_palindromes(ver_get_data_multi), ver_pal_multi)
    
    def test_rel(self):
        self.assertEqual(nf.relation(ver_pal[IOS_seqname][0], ver_pal[IOS_seqname][1]), ver_rel)
        self.assertEqual(nf.relation(serial_pal[IOS_seqname][0], serial_pal[IOS_seqname][2]), ver_rel_S)
        self.assertEqual(nf.relation(overlapping_pal[IOS_seqname][0], overlapping_pal[IOS_seqname][1]), ver_rel_O)
        self.assertEqual(nf.relation(inclusive_pal[IOS_seqname][0], inclusive_pal[IOS_seqname][1]), ver_rel_I)

    def test_graph(self):
        self.assertEqual(nf.new_pgraph(nf.new_palindromes(nf.get_data('../test_sequence_1.fasta.out'))), ver_graph)
        self.assertEqual(nf.new_pgraph(nf.new_palindromes(nf.get_data('../test_sequence_multi.fasta.out'))), ver_graph_multi)
    
    def test_path(self):
        self.assertEqual(nf.new_pathsfunc(nf.new_pgraph(nf.new_palindromes(nf.get_data('../test_sequence_multi.fasta.out'))), 0), ver_path)

    def test_pal(self):
        self.assertEqual(nf.new_dag(ver_path), ver_dag)