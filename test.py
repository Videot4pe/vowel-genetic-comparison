import unittest
from analysis.distance import getDistance
from analysis.tract import getVocalTractParams, getF1, getF2, getF1F0, getF1F2, getF2F0, getDF1F2 
from utils.files import loadFormantsFolder
from analysis.formants import extractFormants
import parselmouth

class DistanceTestCase(unittest.TestCase):
  def testEmpty(self):
    with self.assertRaises(Exception):
      getDistance([], [], [])

  def testDifferentLen(self):
    with self.assertRaises(Exception):
      getDistance([1, 2, 3], [1, 2, 3], [1, 2])
    
  def testSameSound(self):
    res = getDistance([1, 1, 1], [1, 1, 1], [1, 1, 1])
    self.assertEqual(res, 0)
  
  def testManhattan(self):
    res = getDistance([1, 1, 1], [1, 1, 1], [2, 2, 2])
    self.assertEqual(res, 3)

class FilesTestCase(unittest.TestCase):
  def testFileNotFound(self):
    with self.assertRaises(FileNotFoundError):
      loadFormantsFolder('../good-config')
      
  def testOnlyWavFiles(self):
    files = loadFormantsFolder('../src')
    self.assertEqual(files, {})
    
  def testFormantsWrongPath(self):
    with self.assertRaises(parselmouth.PraatError):
      extractFormants('../good-config')

class VocalTractTestCase(unittest.TestCase):
  def testNotAllFormants(self):
    with self.assertRaises(Exception):
      getVocalTractParams([1, 2, None])
      
  def testZeroF0F1(self):
    with self.assertRaises(Exception):
      getF1(0, 4)
      
  def testZeroF0F2(self):
    with self.assertRaises(Exception):
      getF2(0, 2)
    
  def testZeroF2(self):
    with self.assertRaises(Exception):
      getDF1F2(1, 0)
      
  def testF1(self):
    res = getF1(2, 4)
    self.assertEqual(res, 2)
    
  def testF2(self):
    res = getF2(2, 4)
    self.assertEqual(res, 2)
  
  def testF1F2(self):
    res = getF1F2(7, 3)
    self.assertEqual(res, 4)
  
  def testF1F0(self):
    res = getF1F0(3, 7)
    self.assertEqual(res, 4)

  def testF2F0(self):
    res = getF2F0(3, 7)
    self.assertEqual(res, 4)