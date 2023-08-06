import os.path
import subprocess

from anasymod.generators.vivado import VivadoTCLGenerator
from anasymod.generators.codegen import CodeGenerator
from anasymod.util import back2fwd

from anasymod.templates.dbg_hub import TemplDbgHub
from anasymod.templates.ext_clk import TemplExtClk
from anasymod.templates.clk_wiz import TemplClkWiz
from anasymod.templates.execute_FPGA_sim import TemplEXECUTE_FPGA_SIM
from anasymod.templates.ila import TemplILA
from anasymod.templates.zynq_gpio import TemplZynqGPIO
from anasymod.targets import FPGATarget
from anasymod.enums import FPGASimCtrl
from anasymod.sim_ctrl.ctrlapi import CtrlApi

class VivadoEmulation(VivadoTCLGenerator):
    """
    Generate and execute Vivado TCL scripts to generate a bitstream, run an emulation of FPGA for non-interactive mode,
    or launch an FPGA emulation for interactive mode and pass the handle for interactive control.
    """

    def __init__(self, target: FPGATarget):
        super().__init__(target=target)

    def build(self):
        #subst drive
        drive = 'V:'
        # Check if on-chip memory is sufficient on selected FPGA board
        if self.target.prj_cfg.board.bram is not None:
            bits_per_sample = 0
            probes = (self.target.str_cfg.digital_probes + self.target.str_cfg.analog_probes +
                      [self.target.str_cfg.time_probe] + [self.target.str_cfg.dec_cmp])
            for probe in probes:
                bits_per_sample += int(probe.width)
            if (bits_per_sample * self.target.prj_cfg.ila_depth) > (self.target.prj_cfg.board.bram * 8):
                raise(f'ERROR: Number ob samples to be recorded does not fit on FPGA board, please either select a '
                      f'board with more block memory, or change the ila_depth')
        else:
            print(f'WARNING: Check for sufficient BRAM could not be conducted, '
                  f'not enough information given in board definition!')

        scfg = self.target.str_cfg
        """ type : StructureConfig """
        project_root = self.target.project_root
        # under Windows there is the problem with path length more than 146 characters, that's why we have to use
        # subst command to substitute project directory to a drive letter
        if os.name == 'nt':
            if len(back2fwd(self.target.project_root)) > 80:

                project_root = self.subst_path(drive=drive)

        # create a new project
        self.create_project(
            project_name=self.target.prj_cfg.vivado_config.project_name,
            project_directory=project_root,
            full_part_name=self.target.prj_cfg.board.full_part_name,
            board_part=self.target.prj_cfg.board.board_part,
            force=True
        )

        # add all source files to the project (including header files)
        self.add_project_sources(content=self.target.content)

        # define the top module
        self.set_property('top', f"{{{self.target.cfg.top_module}}}", '[current_fileset]')

        # set define variables
        self.add_project_defines(content=self.target.content, fileset='[current_fileset]')

        # specify the level of flattening to use
        self.set_property(
            'STEPS.SYNTH_DESIGN.ARGS.FLATTEN_HIERARCHY',
            self.target.prj_cfg.cfg.flatten_hierarchy,
            '[get_runs synth_1]'
        )

        # append user constraints
        for xdc_file in self.target.content.xdc_files:
            for file in xdc_file.files:
                self.writeln(f'read_xdc "{back2fwd(file)}"')

        if not self.target.cfg.custom_top:
            # write constraints to file
            constrs = CodeGenerator()
            # generate constraints for external clk
            constrs.use_templ(TemplExtClk(target=self.target))
            # generate clock wizard IP core
            self.use_templ(TemplClkWiz(target=self.target))

            # Add IP cores necessary for control interface
            ip_core_templates = self.target.ctrl.add_ip_cores(scfg=scfg, ip_dir=self.target.ip_dir)
            for ip_core_template in ip_core_templates:
                self.use_templ(ip_core_template)

            ## Add constraints for additional generated emu_clks
            constrs.writeln('create_generated_clock -name emu_clk -source [get_pins clk_gen_i/clk_wiz_0_i/clk_out1] -divide_by 2 [get_pins gen_emu_clks_i/buf_emu_clk/I]')

            for k in range(scfg.num_gated_clks):
                constrs.writeln(f'create_generated_clock -name clk_other_{k} -source [get_pins clk_gen_i/clk_wiz_0_i/clk_out1] -divide_by 4 [get_pins gen_emu_clks_i/buf_{k}/I]')

            # Setup ILA for signal probing - only of at least one probe is defined
            if len(scfg.analog_probes + scfg.digital_probes + [scfg.time_probe]) != 0:
                self.use_templ(TemplILA(target=self.target, depth=self.target.prj_cfg.ila_depth))
    
            # Setup Debug Hub
            constrs.use_templ(TemplDbgHub(target=self.target))

            # Add false paths for Zynq control signals.  This is necessary in some cases
            # to provide timing violations, since the ARM core is running on a different
            # clock that the emulator circuitry.  This is a real problem, but is handled
            # in firmware with handshaking and very short delays.
            if self.target.cfg.fpga_sim_ctrl == FPGASimCtrl.UART_ZYNQ:
                constrs.writeln('set_false_path -through [get_pins sim_ctrl_gen_i/zynq_gpio_i/*]')

            # write master constraints to file and add to project
            master_constr_path = os.path.join(self.target.prj_cfg.build_root, 'constrs.xdc')
            constrs.write_to_file(master_constr_path)
            self.add_files([master_constr_path], fileset='constrs_1')

        # read user-provided IPs
        self.writeln('# Custom user-provided IP cores')
        for xci_file in self.target.content.xci_files:
            for file in xci_file.files:
                self.writeln(f'read_ip "{back2fwd(file)}"')

        # read user-provided TCL scripts
        self.writeln('# Custom user-provided TCL scripts')
        for tcl_file in self.target.content.tcl_files:
            for file in tcl_file.files:
                self.writeln(f'source "{back2fwd(file)}"')

        # upgrade IPs as necessary
        self.writeln('if {[get_ips] ne ""} {')
        self.writeln('    upgrade_ip [get_ips]')
        self.writeln('}')

        # generate all IPs
        self.writeln('generate_target all [get_ips]')

        # create additional Hardware for control interface
        if self.target.cfg.fpga_sim_ctrl == FPGASimCtrl.UART_ZYNQ:
            self.use_templ(TemplZynqGPIO(is_ultrascale=scfg.is_ultrascale))

        # launch the build and wait for it to finish
        num_cores = min(int(self.target.prj_cfg.vivado_config.num_cores), 8)
        self.writeln(f'launch_runs impl_1 -to_step write_bitstream -jobs {num_cores}')
        self.writeln('wait_on_run impl_1')

        # re-generate the LTX file
        # without this step, the ILA probes are sometimes split into individual bits
        impl_dir = os.path.join(
            project_root,
            f'{self.target.prj_cfg.vivado_config.project_name}.runs',
            'impl_1',
        )

        ltx_file_path = os.path.join(
            impl_dir, f"{self.target.cfg.top_module}.ltx"
        )

        self.writeln('open_run impl_1')
        self.writeln(f'write_debug_probes -force {{{back2fwd(ltx_file_path)}}}')

        # export the XSA if this is a more recent version of vivado
        if self.version_year >= 2020:
            xsa_file_path = os.path.join(impl_dir, f'{self.target.cfg.top_module}.xsa')
            xsa_file_path = back2fwd(xsa_file_path)
            self.writeln(f'write_hw_platform -fixed -include_bit -force -file {{{xsa_file_path}}}')

        #remove and restore drive substitutions
        if self.subst:
            self.writeln('exec subst ' + self.subst + ' /d')
            if self.old_subst:
                self.writeln('exec subst ' + self.subst + ' ' + self.old_subst)

        # run bitstream generation
        ret_error = self.run(filename=r"bitstream.tcl", stack=self.target.prj_cfg.cfg.vivado_stack, return_error=True)
        if os.name == 'nt':
            if ret_error:
                #remove and restore drive substitutions
                if self.subst:
                    try:
                        subprocess.call(f'subst {drive} /d', shell=True)
                    except:
                        print(f'WARNING: Removing mapped drive:{drive} did not work.')
                    if self.old_subst:
                        try:
                            subprocess.call(f'subst {drive} {self.old_subst}', shell=True)
                        except:
                            print(f'WARNING: Mapping of drive:{drive} to network path: {self.old_subst} did not work.')


    def run_FPGA(self, **kwargs):
        """
        Run the FPGA in non-interactive mode. This means FPGA will run for a specified
        duration; all specified signals will be captured and dumped to a file.

        See anasymod/templates/execute_FPGA_sim.py for keyword arguments.
        """

        self.use_templ(TemplEXECUTE_FPGA_SIM(target=self.target, **kwargs))
        self.run(filename='run_FPGA.tcl', interactive=False)

    def launch_FPGA(self, server_addr: str) -> CtrlApi:
        """
        Run the FPGA in interactive mode. This means FPGA will be programmed and
        control interfaces prepared. After that interactive communication with FPGA
        is possible.

        :param server_addr: Hardware server address for HW server launched by Vivado
        """

        self.target.ctrl_api._initialize()
        self.target.ctrl_api._setup_ctrl(server_addr=server_addr)

        # return ctrl object to user for further interactive commands
        return self.target.ctrl_api
