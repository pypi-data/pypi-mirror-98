"""

preparation.py

preparation class is used to initialize the input and working
environment for validation analysis.

Copyright [2013] EMBL - European Bioinformatics Institute
Licensed under the Apache License, Version 2.0 (the
"License"); you may not use this file except in
compliance with the License. You may obtain a copy of
the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied. See the License for the
specific language governing permissions and limitations
under the License.

"""

__author__ = 'Zhe Wang'
__email__ = 'zhe@ebi.ac.uk'
__date__ = '2018-07-24'


import os
import sys
import psutil
import timeit
import json
import glob
import argparse
import mrcfile
import numpy as np
import xml.etree.ElementTree as ET

if sys.version_info[0] == 2:
    from TEMPy.MapParser import MapParser
    from TEMPy.StructureParser import mmCIFParser
    from TEMPy.EMMap import Map
else:
    from TEMPy.protein.structure_parser import mmCIFParser
    from TEMPy.maps.map_parser import MapParser
    from TEMPy.maps.em_map import Map
from Bio.PDB import MMCIFParser
from Bio.PDB.mmcifio import MMCIFIO
from Bio.PDB.PDBIO import Select
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from emda.core import iotools
from emda import emda_methods
from va.validationanalysis import ValidationAnalysis
from va.version import __version__

try:
    from PATHS import MAP_SERVER_PATH
except ImportError:
    MAP_SERVER_PATH = None


class NotDisordered(Select):
    """

        Class used to select non-disordered atom from biopython structure instance

    """

    def accept_atom(self, atom):
        """
            Accept only atoms that at "A"
        :param atom: atom instance from biopython library
        :return: True or False
        """
        if (not atom.is_disordered()) or atom.get_altloc() == "A":
            atom.set_altloc(" ")
            return True
        else:
            return False


class PreParation:

    def __init__(self):
        """

            Initialization of objects for Validation analysis

        """
        self.args = self.read_para()
        self.emdid = self.args.emdid
        self.json = self.args.j
        methoddict = {'tomography': 'tomo', 'twodcrystal': 'crys', 'singleparticle': 'sp',
                      'subtomogramaveraging': 'subtomo', 'helical': 'heli', 'crystallography': 'crys',
                      'single particle': 'sp', 'subtomogram averaging': 'subtomo'}
        if self.emdid:
            self.mapname = 'emd_{}.map'.format(self.emdid)
            self.subdir = self.folders(self.emdid)
            self.dir = '{}{}/va/'.format(MAP_SERVER_PATH, self.subdir)
            filepath = '{}{}/va/{}'.format(MAP_SERVER_PATH, self.subdir, self.mapname)
            try:
                inputdict = self.read_header()
                if os.path.isfile(filepath):
                    # Read header file
                    inputdict = self.read_header()
                    self.model = inputdict['fitmodels']
                    self.contourlevel = inputdict['reccl']
                    if len(inputdict['halfmaps']) == 2:
                        self.evenmap = inputdict['halfmaps'][0]
                        self.oddmap = inputdict['halfmaps'][1]
                    else:
                        self.evenmap = None
                        self.oddmap = None
                    self.pid = inputdict['fitpid']
                self.method = (inputdict['method']).lower()
                self.resolution = inputdict['resolution']
                self.masks = inputdict['masks'] if inputdict['masks'] is not None else self.collectmasks()
                self.modelmap = True
            except:
                print('No proper header information.')


            self.run = self.args.run
            self.fscfile = self.findfscxml()
            self.platform = 'emdb'
            if self.args.p in ['emdb', 'wwpdb']:
                self.platform = self.args.p
            else:
                print('Please use "emdb" or "wwpdb" as platform argument.')

        elif self.json:
            self.mapname, self.dir, self.model, self.contourlevel, self.evenmap, self.oddmap, \
            self.fscfile, self.method, self.resolution, self.masks, self.run, self.platform, \
            self.modelmap = self.read_json(self.json)
            self.method = methoddict[self.method.lower()]

        else:

            self.mapname = self.args.m
            self.model = self.args.f
            self.pid = self.args.pid
            self.emdid = self.args.emdid
            self.evenmap = self.args.hmeven
            self.oddmap = self.args.hmodd
            #self.contourlevel = float(self.args.cl) if self.args.cl else None
            self.contourlevel = self.read_contour()
            self.run = self.args.run
            self.dir = self.args.d + '/'
            self.method = methoddict[self.args.met.lower()] if self.args.met is not None else None
            self.resolution = self.args.s
            self.platform = 'emdb'
            if self.args.p in ['emdb', 'wwpdb']:
                self.platform = self.args.p
            else:
                print('Please use "emdb" or "wwpdb" as platform argument.')

            # self.masks = self.collectmasks()
            if self.args.ms is not None:
                self.masks = {self.dir + i: float(j) for i, j in zip(self.args.ms, self.args.mscl)}
            else:
                self.masks = {}
            self.fscfile = self.findfscxml()
            self.modelmap = True if self.args.modelmap else False


    def findfscxml(self):
        """

            Find the fsc.xml file if exist

        :return:
        """

        fscxmlre = '*_fsc.xml'
        fscxmlarr = glob.glob(self.dir + fscxmlre)
        if not fscxmlarr:
            print('No fsc.xml file can be read for FSC information.')
            return None
        elif len(fscxmlarr) > 1:
            print('There are more than one FSC files in the folder. Please make sure only one exist.')
            return None
        else:
            filefsc = os.path.basename(fscxmlarr[0])
            return filefsc



    def read_json(self, injson):
        """

            Load input arguments from JSON file

        :return: dictornary which contains correspdong parameters for the pipeline
        """

        if injson:
            with open(injson, 'r') as f:
                args = json.load(f)
            argsdata = args['inputs']
            map = argsdata['map']
            assert map is not None, "There must be a map needed in the input JSON file."
            assert argsdata['workdir'] is not None, "Working directory must be provided in the input JSON file."
            workdir = str(argsdata['workdir'] + '/')
            if 'contour_level' in argsdata and argsdata['contour_level'] is not None:
                cl = argsdata['contour_level']
            else:
                print('There is no contour level.')
                cl = None

            if 'evenmap' in argsdata and argsdata['evenmap'] is not None:
                evenmap = argsdata['evenmap']
            else:
                print('There is no evnemap.')
                evenmap = None

            if 'oddmap' in argsdata and argsdata['oddmap'] is not None:
                oddmap = argsdata['oddmap']
            else:
                print('There is no oddmap.')
                oddmap = None

            if 'fscfile' in argsdata and argsdata['fscfile'] is not None:
                fscfile = argsdata['fscfile']
            else:
                print('There is no fsc file.')
                fscfile = None

            if 'method' in argsdata and argsdata['method'] is not None:
                method = argsdata['method']
            else:
                print('There is no method information.')
                method = None

            if 'resolution' in argsdata and argsdata['resolution'] is not None:
                resolution = argsdata['resolution']
            else:
                print('There is no resolution information.')
                resolution = None

            if 'runs' in argsdata and argsdata['runs'] is not None:
                runs = argsdata['runs']
            else:
                runs = 'all'

            if 'models' in argsdata and argsdata['models'] is not None:
                models = [argsdata['models'][item]['name'] for item in argsdata['models'] if item is not None]
            else:
                models = None

            if 'masks' in argsdata and argsdata['masks'] is not None:
                masks = {workdir + argsdata['masks'][item]['name']: argsdata['masks'][item]['contour']
                          for item in argsdata['masks']}
            else:
                masks = {}

            if 'platform' in argsdata and argsdata['platform'] in ['emdb', 'wwpdb']:
                platform = str(argsdata['platform'])
            else:
                print('There is no platform information.')
                platform = 'emdb'

            if 'modelmap' in argsdata and argsdata['modelmap'] == True:
                modelmap = True
            else:
                modelmap = False
                print('Model map and related calculations will not be done. Please specify modelmap in input json.')

            # masks = { workdir + argsdata['masks'][item]['name']: argsdata['masks'][item]['contour'] for item in argsdata['masks']}

            return (map, workdir, models, cl, evenmap, oddmap, fscfile,
                    method, resolution, masks, runs, platform, modelmap)
        else:
            print('Input JSON needed.')


    def runs(self):
        """

            Check parameters for -run

        :return: dictornary contains binary value of each parameter of -run
        """

        # If only one argument, it will be string type and should be converted to lower letters directly
        # For more than one arguments, it will be list type
        if isinstance(self.run, str):
            runs = self.run.lower()
        else:
            runs = [x.lower() for x in self.run]
        if runs[0] == 'validation':
            return ['projection', 'central', 'surface', 'volume', 'density', 'raps', 'largestvariance', 'mask',
                    'inclusion','fsc']
        else:
            resdict = {'all': False, 'projection': False, 'central': False, 'surface': False, 'density': False,
                       'volume': False, 'fsc': False, 'raps': False, 'mapmodel': False, 'inclusion': False,
                       'largestvariance': False, 'mask': False, 'symmetry': False, 'ccc': False, 'smoc': False,
                       'emrigner': False}
            for key in resdict.keys():
                if key in runs:
                    resdict[key] = True
            # If -run has arguments but do not fit with any above, set to all to True
            if True not in resdict.values():
                resdict['all'] = False

            runlist = []

            # not for OneDep for now: mmfsc, symmetry, qscore, some projectioins
            if self.mapname is not None:
                runlist.extend(['projection', 'central', 'surface', 'volume', 'density', 'raps', 'largestvariance',
                                'mask', 'fsc', 'mmfsc', 'ccc', 'symmetry', 'qscore'
                                ])

            if self.masks is None:
                runlist.remove('mask')

            if self.model is not None and self.contourlevel is not None:
                runlist.extend(['inclusion'])
            else:
                sys.stderr.write('REMINDER: Contour level or model needed for atom and residue inclusion.\n')


            # if self.evenmap is not None and self.oddmap is not None:
            #     runlist.extend(['fsc'])

            # if self.method is not None and self.resolution is not None:
            #     runlist.extend(['symmetry'])

            if runs[0] == 'all' or runs == 'all':
                finallist = runlist
            else:
                finallist = list(set(runlist) & set(runs))

            return finallist


    @staticmethod
    def folders(emdid):
        """

            Folders' path for the one entry with its ids

        :return: Dictionary key: id value: subpath of that entry
        """


        breakdigits = 2
        emdbidmin = 4
        if len(emdid) >= emdbidmin and isinstance(emdid, str):
            topsubpath = emdid[:breakdigits]
            middlesubpath = emdid[breakdigits:-breakdigits]
            subpath = os.path.join(topsubpath, middlesubpath, emdid)

            return subpath
        else:
            return None

    def read_header(self):
        """

            When "-emdid" is give, we search the input information for validation analysis
            inside the header file and return a dictionary

        :return:
        """

        headerfile = '{}{}/va/emd-{}.xml'.format(MAP_SERVER_PATH, self.subdir, self.emdid)
        headerdict = {}
        if os.path.isfile(headerfile):
            tree = ET.parse(headerfile)
            root = tree.getroot()

            # Fitted models
            deposition = root.find('deposition')
            title = deposition.find('title').text
            fitlist = deposition.find('fittedPDBEntryIdList')
            fitmodel = []
            modelcount = 0
            fitpid = []
            if fitlist is not None:
                for child in fitlist.iter('fittedPDBEntryId'):
                    fitmodel.append(child.text + '.cif')
                    fitpid.append(child.text)

            # Recommended contour level
            map = root.find('map')
            contourtf = map.find('contourLevel')
            reccl = None
            if contourtf is not None:
                reccl = "{0:.3f}".format(float(map.find('contourLevel').text))

            # Half maps
            halfmapsfolder = '{}{}/va/*_half_map_*.map'.format(MAP_SERVER_PATH, self.subdir)
            halfmaps = glob.glob(halfmapsfolder)

            # check when there is fitted models for tomography data, do not count the fitted model
            # for calculating atom inclusion, residue inclusion or map model view
            processing = root.find('processing')
            method = processing.find('method').text
            headerdict['fitmodels'] = None if method == 'tomography' else fitmodel


            # Got the resolution value from the header
            reconstruction = processing.find('reconstruction')
            preresolution = reconstruction.find('resolutionByAuthor')
            if preresolution is None:
                resolution = None
            else:
                resolution = preresolution.text


            # Masks
            supplement = root.find('supplement')
            maskset = supplement.find('maskSet') if supplement is not None else None
            masks = {}
            if maskset is not None:
                for child in maskset.iter('mask'):
                    # masks.append(self.dir + child.find('file').text)
                    # Here as there is no mask value from the header, I use 1.0 for all masks
                    masks[self.dir + child.find('file').text] = 1.0
            methoddict = {'tomography': 'tomo', 'twoDCrystal': '2dcrys', 'singleParticle': 'sp',
                          'subtomogramAveraging': 'subtomo', 'helical': 'heli'}

            headerdict['fitmodels'] = fitmodel if fitmodel else None
            headerdict['fitpid'] = fitpid
            headerdict['reccl'] = reccl
            headerdict['halfmaps'] = halfmaps
            headerdict['method'] = methoddict[method]
            headerdict['resolution'] = resolution
            headerdict['masks'] = masks if masks else None


            return headerdict

        else:
            print('Header file: %s does not exit.' % headerfile)
            raise OSError('Header file does not exist.')


    @staticmethod
    def read_para():
        """

            Read arguments


        """

        assert len(sys.argv) > 1, ('There has to be arguments for the command.\n \
               Usage: mainva.py [-h] -m [M] -d [D] [-f [F]] [-pid [PID]] [-hm [HM]] [-cl [CL]]\n \
               or:    mainva.py -emdid <EMDID>\n \
               or:    mainva.py -j <input.json>')
        methodchoices = ['tomography', 'twodcrystal', 'crystallography', 'singleparticle', 'single particle',
                         'subtomogramaveraging', 'subtomogram averaging', 'helical']

        parser = argparse.ArgumentParser(description='Input density map(name) for Validation Analysis')
        #parser = mainparser.add_mutually_exclusive_group(required = True)
        parser.add_argument('--version', '-V', action='version', version='va: {version}'.format(version=__version__),
                            help='Version')
        parser.add_argument('-f', nargs='*',
                            help='Structure model file names. Multiple model names can be used with space separated.')
        parser.add_argument('-pid', nargs='?', help='PDB ID which needed while "-f" in use.')
        parser.add_argument('-hmeven', nargs='?', help='Half map.')
        parser.add_argument('-hmodd', nargs='?', help='The other half map.')
        parser.add_argument('-cl', nargs='?', help='The recommended contour level .')
        parser.add_argument('-run', nargs='*', help='Run customized validation analysis.', default='all')
        parser.add_argument('-met', nargs='?', help='EM method: tomography-tomo, twoDCrystal-2dcrys, singleParticle-sp, '
                                                    'subtomogramAveraging-subtomo, helical-heli',
                            choices=methodchoices)
        parser.add_argument('-s', nargs='?', help='Resolution of the map.')
        parser.add_argument('-ms', nargs='*', help='All masks')
        parser.add_argument('-mscl', nargs='*', help='Contour level corresponding to the masks.')
        parser.add_argument('-p', nargs='?', type=str, help='Platform to run the data either wwpdb or emdb', default='emdb')
        parser.add_argument('-i', '--modelmap', help='If specified then model map will be produce or vice versa',
                            action='store_true')
        requiredname = parser.add_argument_group('required arguments')
        requiredname2 = parser.add_argument_group('alternative required arguments')
        requiredname3 = parser.add_argument_group('alternative required arguments')
        requiredname.add_argument('-m', nargs='?', help='Density map file')
        requiredname.add_argument('-d', nargs='?', help='Directory of all input files')
        requiredname2.add_argument('-emdid', nargs='?', help='EMD ID with which can run without other parameters.')
        requiredname3.add_argument('-j', nargs='?', help='JSON file which has all arguments.')
        args = parser.parse_args()
        checkpar = (isinstance(args.m, type(None)) and isinstance(args.f, type(None)) and
                    isinstance(args.pid, type(None)) and isinstance(args.hmeven, type(None)) and
                    isinstance(args.cl, type(None)) and isinstance(args.hmodd, type(None)) and
                    isinstance(args.emdid, type(None)) and isinstance(args.run, type(None)) and
                    isinstance(args.j, type(None)) and isinstance(args.ms, type(None)) and
                    isinstance(args.mscl, type(None)) and isinstance(args.p, type(None)) and
                    isinstance(args.modelmap, type(None)))

        if checkpar:
            print('There has to be arguments for the command. \n \
                  usage: mainva.py [-h] [-m [M]] [-d [D]] [-f [F]] [-pid [PID]] [-hm [HM]] [-cl [CL]]'
                  '[-i/--modelmap] [-run [all]/[central...]]\n \
                  or   : mainva.py [-emdid [EMDID]] [-run [-run [all]/[central...]]] \n \
                  or   : mainva.py [-j] <input.json>')
            sys.exit()
        return args


    def collectmasks(self):
        """
            todo: Collect masks information if exist return list of mask with full path
            else None(This can be used for unittest, here as the each masks need to corresponding to a contour level
            so the masks' full path and its corresponding contour level need to be generated by reading mmcif file
            and put into a dictionary.

        :return:
        """
        maskstr = ['mask', 'msk']
        globresult = glob.glob(self.dir+'*.map')
        if globresult:
            maskresult = [s for s in globresult for b in maskstr if b in s]
            maskdict = {mask: 1.0 for mask in maskresult}
            print('!!! Be careful the masks were only taken from the folder instead of the header. Header missing the '
                  'corresponding information. For all masks we assume proper contour is 1.0')
            return maskdict
        else:
            return {}



        # Function inside here should do:
        # 1) look for mmcif file from self.workdir ( are their only one mmcif even for multiple fitted model)
        # 2) put mask full path and its corresponding contour level into a dictionary
        # For ccpem and individual user put either contour level contained inside a single file with certain name
        # or make it readable from the file name

        # return maskresult

    def read_contour(self):
        """

            If contour level is not offer,  we need either pid or emdid to get the recommended contour level info
            If contour level is not given by user, estimate a reasonable contour level (Todo)

        :return: contour level

        """

        # if self.emdid:
        #     headfile = '{}EMD-{}/header/emd-{}.xml'.format(HEADER_PATH, self.emdid, self.emdid)
        #     tree = ET.parse(headfile)
        #     root = tree.getroot()
        #     map = root.find('map')
        #     reccl = float(map.find('contourLevel').text)
        #
        #     return reccl
        # elif self.args.cl:
        if self.args.cl:

            return float(self.args.cl)

        else:
            # Todo: Add a estimated contour level function here
            return None


    def swap_axes(self, header):
        """

            Swap the axes to make the data arranged as z, y, z by indices

        :param header:
        :return:
        """



    def frommrc_totempy(self, fullmapname):
        """
            Transfer the mrcfile map object to TEMPy map object

        :param fullmapname:
        :return: TEMPy map object
        """

        mrcmap = mrcfile.mmap(fullmapname, mode='r')
        mrcheader = mrcmap.header
        mapdata = mrcmap.data.astype('float')
        crs = (mrcheader.mapc, mrcheader.mapr, mrcheader.maps)
        reversecrs = crs[::-1]
        nstarts = (mrcheader.nxstart, mrcheader.nystart, mrcheader.nzstart)
        stdcrs = (3, 2, 1)
        diffcrs = tuple(x-y for x,y in zip(reversecrs, stdcrs))
        if diffcrs != (0, 0, 0):
            if 1 in diffcrs and -1 in diffcrs:
                mapdata = np.swapaxes(mapdata, diffcrs.index(-1), diffcrs.index(1))
            if -2 in diffcrs and 2 in diffcrs:
                mapdata = np.swapaxes(mapdata, diffcrs.index(-2), diffcrs.index(2))
            if 1 in diffcrs and -2 in diffcrs:
                mapdata = np.swapaxes(np.swapaxes(mapdata, 0, 1), 1, 2)
            if -1 in diffcrs and 2 in diffcrs:
                mapdata = np.swapaxes(np.swapaxes(mapdata, 1, 2), 0, 1)
            # mapdata = np.swapaxes(mapdata, 0, 2)

        # mapdata = np.swapaxes(np.swapaxes(mapdata, 0, 2), 1, 2)
        tempyheader = MapParser.readMRCHeader(fullmapname)

        # nx, ny, nz and nxstart, nystart, nzstart haver to be changed accordingly to the data
        tempyheader = list(tempyheader)
        tempyheader[0] = mapdata.shape[2]
        tempyheader[1] = mapdata.shape[1]
        tempyheader[2] = mapdata.shape[0]
        tempyheader[3] = mrcheader.mode.item(0)
        tempyheader[4] = nstarts[0].item(0)
        tempyheader[5] = nstarts[1].item(0)
        tempyheader[6] = nstarts[2].item(0)
        tempyheader[7] = mrcheader.mx.item(0)
        tempyheader[8] = mrcheader.my.item(0)
        tempyheader[9] = mrcheader.mz.item(0)
        tempyheader[10] = mrcheader.cella.x.item(0)
        tempyheader[11] = mrcheader.cella.y.item(0)
        tempyheader[12] = mrcheader.cella.z.item(0)
        tempyheader[13:16] = mrcheader.cellb.tolist()
        tempyheader[16] = crs[0].item(0)
        tempyheader[17] = crs[1].item(0)
        tempyheader[18] = crs[2].item(0)
        tempyheader[19] = mrcheader.dmin.item(0)
        tempyheader[20] = mrcheader.dmax.item(0)
        tempyheader[21] = mrcheader.dmean.item(0)
        tempyheader[22] = mrcheader.ispg.item(0)
        tempyheader[23] = mrcheader.nsymbt.item(0)

        # tempyheader[24] = mrcheader.extra1.item(0)
        # tempyheader[25] = mrcheader.exttyp.item(0)
        # tempyheader[26] = mrcheader.nversion.item(0)
        # tempyheader[27] = mrcheader.extra2.item(0)

        tempyheader[49] = mrcheader.origin.x.item(0)
        tempyheader[50] = mrcheader.origin.y.item(0)
        tempyheader[51] = mrcheader.origin.z.item(0)
        tempyheader[52:55] = ['M', 'A', 'P']

        tempyheader[56] = mrcheader.machst
        tempyheader[57] = mrcheader.rms.item(0)
        # tempyheader[58] = mrcheader.nlabl.item(0)
        # tempyheader[59] = mrcheader.label.item(0)



        # tempyheader[13] = mrcheader.cellb.x.item(0)
        # tempyheader[14] = mrcheader.cellb.y.item(0)
        # tempyheader[15] = mrcheader.cellb.z.item(0)
        # here also keep the nstarts position according to original crs order as in __getindices it automaticlly
        # adjust the calculation based on the
        # tempyheader[4] = int(nstarts[crs.index(1)])
        # tempyheader[5] = int(nstarts[crs.index(2)])
        # tempyheader[6] = int(nstarts[crs.index(3)])
        tempyheader = tuple(tempyheader)
        origin = (float(mrcheader.origin.x), float(mrcheader.origin.y), float(mrcheader.origin.z))
        apix = (mrcheader.cella.x/mrcheader.mx, mrcheader.cella.y/mrcheader.my, mrcheader.cella.z/mrcheader.mz)[0]

        finalmap = Map(mapdata, origin, apix, fullmapname, header=tempyheader)

        # inputmap.fullMap = np.swapaxes(np.swapaxes(mrcfile.mmap(fullmapname).data, 0, 2), 1, 2)
        # print(inputmap.fullMap.shape)
        # print(inputmap.fullMap[1, 3, 66])

        return finalmap

    def read_map(self):
        """

            Read maps

        """

        start = timeit.default_timer()

        try:
            if self.emdid:
                #fullmapname = '{}EMD-{}/map/{}'.format(MAP_SERVER_PATH, self.emdid, self.mapname)
                fullmapname = '{}{}/va/{}'.format(MAP_SERVER_PATH, self.subdir, self.mapname)
                mapsize = os.stat(fullmapname).st_size
                # TEMPy way of reading MRC file which does not work well with the 2D crystall data, switch off
                # for now, when it is updated could be changed back

                # inputmap = MapParser.readMRC(fullmapname)

                # Use mrcfile to load all map related data
                inputmap = self.frommrc_totempy(fullmapname)
                self.primarymapmean = inputmap.mean()
                self.primarymapstd = inputmap.std()
                nancheck = np.isnan(inputmap.fullMap).any()
                assert not nancheck, 'There is NaN value in the map, please check.'
                mapdimension = inputmap.map_size()
                end = timeit.default_timer()

                print('Read map time: %s' % (end - start))
                print('------------------------------------')

                return inputmap, mapsize, mapdimension
            elif os.path.exists(self.dir) and self.mapname is not None:
                #print "selfmap:%s" % (self.mapname)
                fullmapname = self.dir + self.mapname
                if not os.path.isfile(fullmapname):
                    fullmapname = self.mapname
                mapsize = os.stat(fullmapname).st_size
                # Swith off using the TEMPy to read map and using the mrcfile loaded information for reading map
                # inputmap = MapParser.readMRC(fullmapname)
                inputmap = self.frommrc_totempy(fullmapname)
                self.primarymapmean = inputmap.mean()
                self.primarymapstd = inputmap.std()
                nancheck = np.isnan(inputmap.fullMap).any()
                assert not nancheck, 'There is NaN value in the map, please check.'
                mapdimension = inputmap.map_size()

                end = timeit.default_timer()
                print('Read map time: %s' % (end - start))
                print('------------------------------------')

                return inputmap, mapsize, mapdimension
            else:
                print('------------------------------------')
                print('Folder: %s does not exist.' % self.dir)
                exit()
        except:
            print('Map does not exist or corrupted.')
            sys.stderr.write('Error: {} \n'.format(sys.exc_info()[1]))
            print('------------------------------------')
            exit()

    def hasdisorder_atom(self, structure):

        ress = structure.get_residues()
        disorder_flag = False
        for res in ress:
            if res.is_disordered() == 1:
                disorder_flag = True
                return disorder_flag
        return disorder_flag

    def _structure_tomodel(self, pid, curmodelname):
        """
            Take structure object and output the used model object

        :param pid: String of anything or pdbid
        :param curmodelname: String of the model name
        :return: TEMPy model instance which will be used for the whole calculation
        """

        p = MMCIFParser()
        io = MMCIFIO()
        orgfilename = curmodelname
        structure = p.get_structure(pid, curmodelname)
        if len(structure.get_list()) > 1:
            orgmodel = curmodelname + '_org.cif'
            os.rename(curmodelname, orgmodel)
            # firstmodel = curmodelname + '_firstmodel' + '.cif'
            fstructure = structure[0]
            io.set_structure(fstructure)
            io.save(curmodelname)
            usedframe = p.get_structure('first', curmodelname)
            print('!!!There are multiple models in the cif file. Here we only use the first for calculation.')
        else:
            usedframe = structure

        # io.set_structure(usedframe)
        if self.hasdisorder_atom(usedframe):
            curmodelname = curmodelname + '_Alt_A.cif'
            io.set_structure(usedframe)
            print('There are alternative atom in the model here we only use A for calculations and saved as {}'
                  .format(curmodelname))
            io.save(curmodelname, select=NotDisordered())
            newstructure = p.get_structure(pid, curmodelname)
        else:
            # curmodelname = curmodelname[:-4] + '_resaved.cif'
            # io.save(curmodelname)
            newstructure = usedframe
        # newstructure = p.get_structure(pid, curmodelname)
        tmodel = mmCIFParser._biommCIF_strcuture_to_TEMpy(curmodelname, newstructure, hetatm=True)
        tmodel.filename = orgfilename

        return tmodel

    def change_cifname(self):
        """
            If there is *_org.cif exist in the va folder, then change it back to the orignal file name

        :return:
        """

        for file in os.listdir(self.dir):
            if file.endswith('_org.cif'):
                print('{} to {}'.format(file, file[:-8]))
                os.rename(self.dir + '/' + file, self.dir + '/' + file[:-8])

    def read_model(self):
        """

            Read models if '-f' argument is used

        """

        start = timeit.default_timer()
        if self.model is not None:
            modelname = self.model
            # Todo: 1)modelname could be multiple models here using just the first model
            #       2)after 'else', the path should be a path on server or a folder I ust to store all files
            #         right now just use the same value as before 'else'
            ## commented area can be deleted after fully test (below)
            # if self.emdid:
            #     # Real path is comment out for the reason that the folder on server is not ready yet
            #     # Here use the local folder VAINPUT_DIR for testing purpose
            #     #fullmodelname = MAP_SERVER_PATH + modelname[0] if self.emdid is None else MAP_SERVER_PATH + modelname[0]
            #     fullmodelname = [ VAINPUT_DIR + curmodel if self.emdid is None else MAP_SERVER_PATH + self.subdir + '/va/' + curmodel for curmodel in modelname ]
            # else:
            #     fullmodelname = [ VAINPUT_DIR + curmodel if self.emdid is None else VAINPUT_DIR + curmodel for curmodel in modelname ]
            # fullmodelname = [ self.dir + curmodel if self.emdid is None else MAP_SERVER_PATH + self.subdir + '/va/' + curmodel for curmodel in modelname ]
            fullmodelname = []
            if self.emdid is None:
                for curmodel in modelname:
                    if not os.path.isfile(self.dir + curmodel) and os.path.isfile(curmodel):
                        fullmodelname.append(curmodel)
                    elif os.path.isfile(self.dir + curmodel):
                        fullmodelname.append(self.dir + curmodel)
                    else:
                        print('Something wrong with the input model name or path: {}.'.format(self.dir + curmodel))
            else:
                fullmodelname = [MAP_SERVER_PATH + self.subdir + '/va/' + curmodel for curmodel in modelname]

            try:
                modelsize = [os.stat(curmodelname).st_size for curmodelname in fullmodelname]
                #pid = self.pid
                pids = [os.path.basename(model)[:-4] for model in fullmodelname]
                # inputmodel = [mmCIFParser.read_mmCIF_file(pid, curmodelname, hetatm=True) for pid, curmodelname in zip(pids, fullmodelname)]
                inputmodel = []
                p = MMCIFParser()
                io = MMCIFIO()
                for pid, curmodelname in zip(pids, fullmodelname):
                    # structure = p.get_structure(pid, curmodelname)
                    # print(structure)
                    # structure[0] here when cif has multiple models, only use the first one for calculation
                    tmodel = self._structure_tomodel(pid, curmodelname)
                    # if len(structure.get_list()) > 1:
                    #     io.set_structure(structure[0])
                    #     orgmodel = curmodelname[:-4] + '_org' + '.cif'
                    #     # self.model = [os.path.basename(firstmodel) if (os.path.basename(curmodelname) == m) else m for m in self.model]
                    #     os.rename(curmodelname, orgmodel)
                    #     print('!!!There are multiple models in the cif file. Here we only use the first for calculation.')
                    #     if self.hasdisorder_atom(structure[0]):
                    #         usedmodel = curmodelname[:-4] + '_Alt_A.cif'
                    #         io.save(usedmodel, select=NotDisordered())
                    #     else:
                    #         io.save(curmodelname)
                    #     newstructure = p.get_structure(pid, curmodelname)
                    #     tmodel = mmCIFParser._biommCIF_strcuture_to_TEMpy(curmodelname, newstructure, hetatm=True)
                    #     tmodel.filename = '/Users/zhe/Downloads/alltempmaps/D_6039242/moriginalfile.cif'
                    #     # tmodel = mmCIFParser._biommCIF_strcuture_to_TEMpy(curmodelname, structure[0], hetatm=True)
                    # else:
                    #     print('fine here')
                    #     io.set_structure(structure)
                    #     if self.hasdisorder_atom(structure):
                    #         curmodelname = curmodelname[:-4] + '_Alt_A.cif'
                    #         io.save(curmodelname, select=NotDisordered())
                    #     else:
                    #         io.save(curmodelname)
                    #     newstructure = p.get_structure(pid, curmodelname)
                    #     tmodel = mmCIFParser._biommCIF_strcuture_to_TEMpy(curmodelname, newstructure, hetatm=True)
                    #     tmodel.filename = '/Users/zhe/Downloads/alltempmaps/D_6039242/moriginalfile.cif'
                    #     print(tmodel)
                    #     print(dir(tmodel))
                    #     exit(0)
                        # tmodel = mmCIFParser._biommCIF_strcuture_to_TEMpy(curmodelname, structure, hetatm=True)

                    # tmodel = mmCIFParser.read_mmCIF_file(pid, curmodelname, hetatm=True)
                    inputmodel.append(tmodel)

                # Split each model mmcif file to a chain mmcif file
                # tempdict = self.cifchains(fullmodelname)
                # chaindict = self.updatechains(tempdict)
                # tchaindict = self.chainmaps(chaindict)

                end = timeit.default_timer()
                print('Read model time: %s' % (end - start))
                print('------------------------------------')

                return inputmodel, pids, modelsize
            except:
                print('File: %s does not exist or corrupted.' % fullmodelname)
                print('------------------------------------')
                exit()
        else:
            print('No model is given.')
            inputmodel = None
            pid = None
            modelsize = None

            return inputmodel, pid, modelsize

    def cifchains(self, fullmodelname):
        """

            For each model in fullmodelname, split each chain into a single mmcif file

        :param fullmodelname: a list of model file full names
        :return: a dirtornary which key as model and value as a list of chain cif file names
        """

        parser = MMCIFParser()
        chaindict = {}
        for model in fullmodelname:
            modelname = os.path.basename(model)
            structure = parser.get_structure(modelname, model)
            singlechainfiles = []
            io = MMCIFIO()
            for chain in structure.get_chains():
                io.set_structure(chain)
                name = '{}{}_chain_{}.cif'.format(self.dir, modelname, chain.id)
                print(name)
                singlechainfiles.append(name)
                io.save(name)
            chaindict[model] = singlechainfiles
        print('Each chain cif files saved')

        return chaindict

    def updatechains(selfs, chaindict):
        """

            As Refmac need the symmetry in the chain to produce the model map, here we reload the model and each chain
            to a dictornary and save again to each chain so to produce the chain map

        :param chaindict:
        :return:
        """

        for (model, chains) in chaindict.items():
            model_dict = MMCIF2Dict(model)
            io = MMCIFIO()
            for chain in chains:
                chain_dict = MMCIF2Dict(chain)
                if '_symmetry.space_group_name_H-M' in model_dict.keys():
                    chain_dict['_symmetry.space_group_name_H-M'] = model_dict['_symmetry.space_group_name_H-M']
                else:
                    chain_dict['_symmetry.space_group_name_H-M'] = 'P 1'
                io.set_dict(chain_dict)
                io.save(chain)

        return chaindict


    def chainmaps(self, chaindict):
        """

            Produce all the chain maps based on the chain model mmcifs

        :param chaindict: dictionary from function cifchains
        :return:
        """

        unit_cell, arr, origin = iotools.read_map(self.dir + self.mapname)
        dim = list(arr.shape)

        finaldict = {}
        for (key, value) in chaindict.items():
            modelmaps = []
            errlist = []
            for chainfile in value:
                print(chainfile)
                try:
                    chainfilename = os.path.basename(chainfile)
                    modelmapname = '{}{}_chainmap.map'.format(self.dir, chainfilename)
                    modelmap = emda_methods.model2map(chainfile, dim, float(self.resolution),
                                                      unit_cell, maporigin=origin)
                    emda_methods.write_mrc(modelmap, modelmapname, unit_cell, map_origin=origin)
                    modelmaps.append(modelmapname)
                except:
                    err = 'Simulating model({}) map error:{}.'.format(model, sys.exc_info()[1])
                    errlist.append(err)
                    sys.stderr.write(err + '\n')

                if errlist:
                    try:
                        chainfilename = os.path.basename(chainfile)
                        modelmapname = '{}{}_chainmap.map'.format(self.dir, chainfilename)
                        modelmap = emda_methods.model2map(chainfile, dim, float(self.resolution),
                                                          unit_cell, lig=True, maporigin=origin)
                        emda_methods.write_mrc(modelmap, modelmapname, unit_cell, map_origin=origin)
                        modelmaps.append(modelmapname)
                        print('Model map produced without the ligand description.')
                    except:
                        err = 'Simulating model({}) map error:{}.'.format(model, sys.exc_info()[1])
                        errlist.append(err)
                        sys.stderr.write(err + '\n')
            finaldict[key] = modelmaps

        return finaldict

    def modelstomaps(self):
        """

            Conver all models to corresponding maps and write it out

        :return:
        """

        if not self.model or not self.modelmap:
            print('If there is no model given or no modelmap in json or command line, model map will not be produced.')
        else:
            # get map cell and dimension info,
            # 1) using mrcfile to only read the header to get the information
            # but need to take correct order of crs corresponding to the cell grid size ...
            # start = timeit.default_timer()
            # primarymapheader = mrcfile.open(self.dir + self.mapname, mode=u'r', permissive=False, header_only=True)
            # end = timeit.default_timer()
            # print(primarymapheader.print_header())
            # print('mrcfile use:{}s to read the map data'.format(end - start))

            # 2) currently direcctly use emda to avoid self formating the dimension and so on
            # but it may take more time to load a large map than using mrcfile just for header info but durable for now
            # only do it for single particle as electron crystalography does not need model map FSC calculation
            if self.method == 'sp' and self.resolution:
                unit_cell, arr, origin = iotools.read_map(self.dir + self.mapname)
                dim = list(arr.shape)

                modelmaps = []
                errlist = []
                # for each model produce a model map
                for model in self.model:
                    try:
                        modelmapname = '{}{}_modelmap.map'.format(self.dir, model)
                        modelmap = emda_methods.model2map(self.dir + model, dim, float(self.resolution), unit_cell,
                                                          maporigin=origin)
                        emda_methods.write_mrc(modelmap, modelmapname, unit_cell, map_origin=origin)
                        modelmaps.append(modelmapname)
                    except:
                        err = 'Simulating model({}) map error:{}.'.format(model, sys.exc_info()[1])
                        errlist.append(err)
                        sys.stderr.write(err + '\n')

                    if errlist:
                        try:
                            modelmapname = '{}{}_modelmap.map'.format(self.dir, model)
                            modelmap = emda_methods.model2map(self.dir + model, dim, float(self.resolution), unit_cell,
                                                              lig=True, maporigin=origin)
                            emda_methods.write_mrc(modelmap, modelmapname, unit_cell, map_origin=origin)
                            modelmaps.append(modelmapname)
                            print('Model map produced without the ligand description.')
                        except:
                            err = 'Simulating model({}) map error:{}.'.format(model, sys.exc_info()[1])
                            errlist.append(err)
                            sys.stderr.write(err + '\n')
                print(modelmaps)
                return modelmaps, errlist
            else:
                print("No model map is produced as this is either not a single particle entry or nothing specified "
                      "for method -m (please use: -m sp) or resolution not specified -s (please use: -s <value>).")

        return None, None

    def combinemap(self, oddobj, evenobj, rawmapfullname):
        """
            Calculate rawmap from two half-maps and scale to primary map range.
            Apply primary map mean and std over the normalized raw map (mean=0, std=1)

        :param oddobj: odd map TEMPy instance
        :param evenobj: even map TEMPy instance
        :param rawmapfullname: string of raw map full name
        :return: raw map TEMPy instance
        """
        oddmap = oddobj.copy()
        rawmap = oddmap.normalise()
        normevenmap = evenobj.normalise()
        rawmap.fullMap += normevenmap.fullMap
        rawmap = rawmap.normalise()
        rawmap.fullMap = rawmap.fullMap * self.primarymapstd + self.primarymapmean
        rawmap.filename = rawmapfullname
        rawmap.update_header()
        rawmap.write_to_MRC_file(rawmapfullname)

        return rawmap

    def read_halfmaps(self):
        """

            Read two half maps for FSC calculation

        :return:
        """

        halfeven = None
        halfodd = None
        rawmap = None
        twomapsize = 0.
        if self.emdid:
            mapone = MAP_SERVER_PATH + self.subdir + '/va/' + 'emd_' + self.emdid + '_half_map_1.map'
            maptwo = MAP_SERVER_PATH + self.subdir + '/va/' + 'emd_' + self.emdid + '_half_map_2.map'
            rawmapname = '{}{}/va/emd_{}_rawmap.map'.format(MAP_SERVER_PATH, self.subdir, self.emdid)
            if os.path.isfile(mapone) and os.path.isfile(maptwo):
                try:
                    halfodd = self.frommrc_totempy(mapone)
                    halfeven = self.frommrc_totempy(maptwo)
                    rawmap = self.combinemap(halfodd, halfeven, rawmapname)
                    twomapsize = halfodd.map_size() + halfeven.map_size()
                except IOError as e:
                    print(e)
                    exit()
            else:
                halfeven = None
                halfodd = None
                rawmap = None
                twomapsize = 0.
                print('No half maps for this entry.')
        else:
            if self.evenmap is not None and self.oddmap is not None:
                try:
                    rawmapname = '{}{}_{}_rawmap.map'.format(self.dir, self.oddmap, self.evenmap)
                    halfodd = self.frommrc_totempy(self.dir + self.oddmap)
                    halfeven = self.frommrc_totempy(self.dir + self.evenmap)
                    rawmap = self.combinemap(halfodd, halfeven, rawmapname)
                    twomapsize = halfodd.map_size() + halfeven.map_size()
                except IOError as maperr:
                    print(maperr)
                    exit()
            elif self.evenmap is None and self.oddmap is None:
                print('REMINDER: Both half maps needed for FSC calculation!')
                halfeven = None
                halfodd = None
                rawmap = None
                twomapsize = 0.
            else:
                raise IOError('Another half map is needed for FSC calculation.')

        return halfeven, halfodd, rawmap, twomapsize







        # if self.evenmap is not None and self.oddmap is not None and self.emdid is None:
        #     try:
        #         halfeven = MapParser.readMRC(VAINPUT_DIR + self.evenmap)
        #         halfodd = MapParser.readMRC(VAINPUT_DIR + self.oddmap)
        #     except IOError as maperr:
        #         print maperr
        #         exit()
        # elif self.evenmap is not None and self.oddmap is not None and self.emdid:
        #     try:
        #         halfeven = MapParser.readMRC(self.evenmap)
        #         halfodd = MapParser.readMRC(self.oddmap)
        #     except IOError as maperr:
        #         print maperr
        #         exit()
        # elif self.evenmap is None and self.oddmap is None:
        #     print 'REMINDER: Both half maps needed for FSC calculation!'
        #     halfeven = None
        #     halfodd = None
        # elif self.emdid:
        #     halfeven = MapParser.readMRC(MAP_SERVER_PATH + 'EMD_' + self.emdid + '/other/' + 'emd_'+ self.emdid + '_half_map_1.map')
        #     halfodd = MapParser.readMRC(MAP_SERVER_PATH + 'EMD_' + self.emdid + '/other/' + 'emd_'+ self.emdid + '_half_map_2.map')
        # else:
        #     raise IOError('Another half map is needed for FSC calculation.')
        #
        # return halfeven, halfodd


    def merge_jsons(self):
        """

            Merge all generated json files to one file

        :return: None
        """

        # workdir = '{}{}/va/'.format(MAP_SERVER_PATH, self.subdir())
        jsonfiles = glob.glob(self.dir + '*.json')
        jsonfiles = [jfile for jfile in jsonfiles if 'all.json' not in jfile]

        fuldata = {}

        filename = os.path.basename(self.mapname) if self.emdid is None else self.emdid

        for tfile in jsonfiles:
            if os.path.getsize(tfile) > 0:
                with open(tfile, 'r') as f:
                    if f is not None:
                        data = json.load(f)
                        datakeys = list(data.keys())
                        if datakeys[0] != filename:
                            fuldata[datakeys[0]] = list(data.values())[0]
            else:
                sys.stderr.write('The {} is empty!\n'.format(tfile))

        finaldata = dict()
        if self.emdid is not None:
            finaldata[self.emdid] = fuldata
            output = '{}emd_{}_all.json'.format(self.dir, self.emdid)
        else:
            finaldata[filename] = fuldata
            output = '{}{}_all.json'.format(self.dir, filename)
        with open(output, 'w') as out:
            json.dump(finaldata, out)

        return None

    def write_recl(self):
        """

            Write recl into a json file

        :return: None
        """

        if self.contourlevel is not None:
            dictrecl = dict()
            dictrecl['recl'] = self.contourlevel
            lastdict = dict()
            lastdict['recommended_contour_level'] = dictrecl
            # filename = self.mapname if self.emdid is None else self.emdid
            filename = self.mapname
            # if self.emdid is not None:
            #     output = '{}emd_{}_recl.json'.format(self.workdir, filename)
            # else:
            #     output = '{}{}_recl.json'.format(self.workdir, filename)
            output = '{}{}_recl.json'.format(self.dir, os.path.basename(filename))
            with open(output, 'w') as out:
                json.dump(lastdict, out)

        return None

    def write_version(self):
        """

            Write version

        :return: None
        """
        versiondict = dict()
        versiondict['version'] = __version__
        filename = self.mapname
        output = '{}{}_version.json'.format(self.dir, os.path.basename(filename))
        with open(output, 'w') as out:
            json.dump(versiondict, out)

        return None


    def finiliszejsons(self):
        """



        :return:
        """

        start = timeit.default_timer()
        self.write_recl()
        self.write_version()
        self.merge_jsons()
        stop = timeit.default_timer()
        print('Merge JSONs: %s' % (stop - start))
        print('------------------------------------')

    #@staticmethod
    def memmsg(self, mapsize):
        """

            Memory usage reminder based on memory prediction

        :return:
        """
        # When there is no emdid given, we use one level above the given "dir" to save the memory prediction file
        # input.csv. If emdid is given, we use the. self.dir is like /abc/cde/ so it needs to used os.path.dirname()
        # twice.

        if self.emdid:
            vout = MAP_SERVER_PATH
        else:
            vout = os.path.dirname(os.path.dirname(self.dir)) + '/'
        if os.path.isfile(vout + 'input.csv') and os.path.getsize(vout + 'input.csv') > 0:
            mempred = ValidationAnalysis.mempred(vout + 'input.csv', 2 * mapsize)
            if mempred == 0 or mempred is None:
                print('No memory prediction.')
                return None
            else:
                print('The memory you may need is %s M' % mempred)
                assert mempred < psutil.virtual_memory().total / 1024 / 1024, \
                    'The memory needed to run may exceed the total memory you have on the machine.'
                return mempred
        else:
            print('No memory data available for prediction yet')
            return None



