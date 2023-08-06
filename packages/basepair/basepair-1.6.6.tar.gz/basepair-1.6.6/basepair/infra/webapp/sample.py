'''Sample webapp api wrapper'''

# App imports
from .abstract import Abstract

class Sample(Abstract):
  '''Webapp Sample class'''
  def __init__(self, cfg):
    super(Sample, self).__init__(cfg)
    self.endpoint += 'samples/'
