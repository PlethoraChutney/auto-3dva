import argparse
import os
from glob import glob
from chimera import runCommand as rc

cryosparc_dir = '/goliath/processing/BaconguisLab/posert/cryosparc'
output_dir = '/troll/scratch/sw/troll_web/3dva'

class Component:
  def __init__(self, job_string, id, map_location):
    self.job_string = job_string
    self.id = id
    self.map_location = map_location

  def __repr__(self):
    return 'Component {} with maps at {}'.format(self.id, self.map_location)

  def make_movie(self):
    rc('windowsize 1200 1200')
    print('Opening {}'.format(self.map_location))
    rc('vseries open {}*.mrc'.format(self.map_location))
    rc('vol #0 step 1')
    rc('movie record')
    rc('vseries play #0 direction oscillate loop false normalize truei cacheFrames 30')
    rc('wait 77')
    rc('vseries stop #0')
    rc('movie stop')
    try:
      os.makedirs('{}/{}'.format(output_dir, self.job_string))
    except OSError as e:
      pass
    rc('movie encode {}/{}_component{}.mp4'.format(output_dir, self.job_string, self.id))
    rc('wait 300')
    rc('vseries close #0')

def get_maps(job_string):
  components = []

  job_glob = glob('{}/{}/*component*/'.format(cryosparc_dir, job_string))
  for directory in job_glob:
    components.append(Component(job_string, directory[-3:-1], directory))

  return components

def main(args):
  job_string = args.job.replace('J', '/J')

  components = get_maps(job_string)
  print(components)
  for comp in components:
    comp.make_movie()


  

parser = argparse.ArgumentParser(
  description = 'Process 3DVA jobs into movies without downloading .mrc files',
)

parser.add_argument(
  'job',
  type = str.upper,
  help = 'Project and job number for 3DVA display job, e.g., \"P11J54\"'
)

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)
