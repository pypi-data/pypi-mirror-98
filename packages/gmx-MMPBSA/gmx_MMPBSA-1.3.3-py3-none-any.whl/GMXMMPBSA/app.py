# ##############################################################################
#                           GPLv3 LICENSE INFO                                 #
#                                                                              #
#  Copyright (C) 2020  Mario S. Valdes-Tresanco and Mario E. Valdes-Tresanco   #
#  Copyright (C) 2014  Jason Swails, Bill Miller III, and Dwight McGee         #
#                                                                              #
#   Project: https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA                  #
#                                                                              #
#   This program is free software; you can redistribute it and/or modify it    #
#  under the terms of the GNU General Public License version 3 as published    #
#  by the Free Software Foundation.                                            #
#                                                                              #
#  This program is distributed in the hope that it will be useful, but         #
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY  #
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License    #
#  for more details.                                                           #
# ##############################################################################

import sys
from os.path import split
import shutil
from pathlib import Path
import logging
from PyQt5.QtWidgets import QApplication
# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
# rootLogger = logging.getLogger(__name__)
# logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger(__name__)
log_file = Path('gmx_MMPBSA.log')
if log_file.exists():
    log_file.unlink()

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)-7s] %(message)s",
    handlers=[
        logging.FileHandler("gmx_MMPBSA.log"),
        logging.StreamHandler()])

try:
    from GMXMMPBSA.exceptions import GMXMMPBSA_ERROR, InputError, CommandlineError
    from GMXMMPBSA.infofile import InfoFile
    from GMXMMPBSA import main
    from GMXMMPBSA.analyzer import GMX_MMPBSA_ANA
    from GMXMMPBSA.commandlineparser import anaparser
except ImportError:
    import os
    amberhome = os.getenv('AMBERHOME') or '$AMBERHOME'
    logging.error('Could not import Amber Python modules. Please make sure '
                      'you have sourced %s/amber.sh (if you are using sh/ksh/'
                      'bash/zsh) or %s/amber.csh (if you are using csh/tcsh)' %
                      (amberhome, amberhome))
    raise ImportError('Could not import Amber Python modules. Please make sure '
                      'you have sourced %s/amber.sh (if you are using sh/ksh/'
                      'bash/zsh) or %s/amber.csh (if you are using csh/tcsh)' %
                      (amberhome, amberhome))


def gmxmmpbsa():

    # Adapted to run with MPI ?
    if len(sys.argv) > 1 and sys.argv[1] in ['MPI', 'mpi']:
        args = sys.argv
        args.pop(1)  # remove mpi arg before passed it to app
        try:
            from mpi4py import MPI
        except ImportError:
            GMXMMPBSA_ERROR('Could not import mpi4py package! Use serial version or install mpi4py.')
    else:
        # If we're not running "gmx_MMPBSA MPI", bring MPI into the top-level namespace
        # (which will overwrite the MPI from mpi4py, which we *want* to do in serial)
        from GMXMMPBSA.fake_mpi import MPI
        args = sys.argv
    # Set up error/signal handlers
    main.setup_run()

    # Instantiate the main MMPBSA_App
    app = main.MMPBSA_App(MPI)

    # Read the command-line arguments
    try:
        app.get_cl_args(args[1:])
    except CommandlineError as e:
        sys.stderr.write('%s: %s' % (type(e).__name__, e) + '\n')
        sys.exit(1)
    logging.info('Started')

    # Perform our MMPBSA --clean now
    if app.FILES.clean:
        sys.stdout.write('Cleaning temporary files and quitting.\n')
        app.remove(0)
        sys.exit(0)

    # See if we wanted to print out our input file options
    if app.FILES.infilehelp:
        app.input_file.print_contents(sys.stdout)
        sys.exit(0)

    # If we're not rewriting output do whole shebang, otherwise load info and parms
    # Throw up a barrier before and after running the actual calcs
    if not app.FILES.rewrite_output:
        try:
            app.read_input_file()
        except InputError as e:
            sys.stderr.write('%s: %s' % (type(e).__name__, e) + '\n')
            sys.stderr.write('  Enter `%s --help` for help\n' %
                             (split(sys.argv[0])[1]))
            sys.exit(1)
        app.process_input()
        app.check_for_bad_input()
        app.loadcheck_prmtops()
        app.file_setup()
        app.run_mmpbsa()
    # If we are rewriting output, load the info and check prmtops
    else:
        info = InfoFile(app)
        info.read_info()
        app.loadcheck_prmtops()

    # Now we parse the output, print, and finish
    app.parse_output_files()
    app.write_final_outputs()
    app.finalize()



def gmxmmpbsa_ana():
    app = QApplication(sys.argv)
    try:
        parser = anaparser.parse_args(sys.argv[1:])
    except CommandlineError as e:
        sys.stderr.write('%s: %s' % (type(e).__name__, e) + '\n')
        sys.exit(1)
    path = Path(parser.path).absolute()
    if not path.exists():
        print('Path not found')
        sys.exit(1)
    app.setApplicationName('gmx_MMPBSA Analyzer (gmx_MMPBSA_ana)')
    w = GMX_MMPBSA_ANA(path.as_posix())
    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':


    logging.info('Finished')

    # gmxmmpbsa()
    gmxmmpbsa_ana()