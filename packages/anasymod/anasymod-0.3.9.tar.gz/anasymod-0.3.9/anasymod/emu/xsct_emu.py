import shutil
import re

from pathlib import Path

from anasymod.generators.xsct import XSCTTCLGenerator

from anasymod.templates.xsct_build import TemplXSCTBuild
from anasymod.templates.xsct_program import TemplXSCTProgram
from anasymod.config import EmuConfig

class XSCTEmulation(XSCTTCLGenerator):
    """
    Generate and execute Vivado TCL scripts to generate a bitstream, run an emulation of FPGA for non-interactive mode,
    or launch an FPGA emulation for interactive mode and pass the handle for interactive control.
    """

    def __init__(self, pcfg: EmuConfig, top_module, project_root, content):
        super().__init__(pcfg=pcfg)
        self.top_module = top_module
        self.project_root = project_root
        self.content = content

        self.err_str = re.compile('^(Failed)')

    @property
    def impl_dir(self):
        return (
            Path(self.project_root) /
            f'{self.pcfg.vivado_config.project_name}.runs' /
            'impl_1'
        )

    @property
    def bit_path(self):
        return self.impl_dir / f'{self.top_module}.bit'

    @property
    def tcl_path(self):
        if self.pcfg.board.is_ultrascale:
            return self.impl_dir / 'psu_init.tcl'
        else:
            return self.impl_dir / 'ps7_init.tcl'

    @property
    def hw_path(self):
        if self.pcfg.xsct_config.version_year < 2020:
            return self.impl_dir / f'{self.top_module}.sysdef'
        else:
            return self.impl_dir / f'{self.top_module}.xsa'

    def build(self, create=True, copy_files=True, build=True):
        # determine SDK path
        sdk_path = (Path(self.project_root) /
                    f'{self.pcfg.vivado_config.project_name}.sdk')

        # clear the SDK directory
        if create:
            shutil.rmtree(sdk_path, ignore_errors=True)
            sdk_path.mkdir(exist_ok=True, parents=True)

        # copy over the firmware sources
        if copy_files:
            src_path = sdk_path / 'sw' / 'src'
            src_path.mkdir(exist_ok=True, parents=True)
            for src in self.content.firmware_files:
                if src.files is not None:
                    for file_ in src.files:
                        shutil.copy(str(file_), str(src_path / Path(file_).name))

        # determine the processor name
        if self.pcfg.board.is_ultrascale:
            proc_name = 'psu_cortexa53_0'
        else:
            proc_name = 'ps7_cortexa9_0'

        # generate the build script
        self.write(
            TemplXSCTBuild(
                sdk_path=sdk_path,
                hw_path=self.hw_path,
                version_year=self.pcfg.xsct_config.version_year,
                version_number=self.pcfg.xsct_config.version_number,
                proc_name=proc_name,
                create=create,
                build=build
            ).text
        )

        # run the build script while checking for errors
        err_str = re.compile(r'(: error:)|(make.*: \*\*\* .* Error \d+)')
        self.run('sdk.tcl', err_str=err_str)

    def program(self, **kwargs):
        # determine SDK path
        sdk_path = (Path(self.project_root) /
                    f'{self.pcfg.vivado_config.project_name}.sdk')

        # generate the build script
        self.write(
            TemplXSCTProgram(
                sdk_path=sdk_path,
                bit_path=self.bit_path,
                hw_path=self.hw_path,
                tcl_path=self.tcl_path,
                is_ultrascale=self.pcfg.board.is_ultrascale,
                xsct_install_dir=self.pcfg.xsct_config.xsct_install_dir,
                no_rev_check=self.pcfg.board.no_rev_check,
                pcfg=self.pcfg,
                **kwargs
            ).text
        )

        # run the programming script. xsct appears to return an error code
        # when the FPGA board is not plugged in or is not powered up, so
        # parsing for errors doesn't appear to be necessary in this case)
        self.run('program.tcl', err_str=self.err_str)
