from anasymod.templates.templ import JinjaTempl
from anasymod.config import EmuConfig
from anasymod.generators.gen_api import SVAPI, ModuleInst
from anasymod.structures.structure_config import StructureConfig
from anasymod.sim_ctrl.datatypes import DigitalSignal


class ModuleEmuClks(JinjaTempl):
    def __init__(self, scfg: StructureConfig, pcfg: EmuConfig):
        super().__init__(trim_blocks=True, lstrip_blocks=True)

        gated_clks = []

        #####################################################
        # Create module interface
        #####################################################
        self.module_ifc = SVAPI()

        module = ModuleInst(api=self.module_ifc, name="gen_emu_clks")
        module.add_input(scfg.emu_clk_2x)
        module.add_output(scfg.emu_clk)

        for derived_clk in scfg.clk_derived:
            if derived_clk.abspath_gated_clk is not None:
                gated_clks.append(derived_clk.name)

        # add IOs for default oscillator if used
        self.use_default_oscillator = scfg.use_default_oscillator
        if scfg.use_default_oscillator:
            module.add_input(DigitalSignal(name=f'clk_val_default_osc', width=1, abspath=''))
            module.add_output(DigitalSignal(name=f'clk_default_osc', width=1, abspath=''))

        for gated_clk in gated_clks:
            module.add_input(DigitalSignal(name=f'clk_val_{gated_clk}', width=1, abspath=''))
            module.add_output(DigitalSignal(name=f'clk_{gated_clk}', width=1, abspath=''))

        module.generate_header()

        #####################################################
        # Generate other clks
        #####################################################
        self.generated_clks = SVAPI()

        if gated_clks:
            for gated_clk in gated_clks:
                self.generated_clks.gen_signal(DigitalSignal(name=f'clk_unbuf_{gated_clk}', width=1, abspath=''), default_value=0)
            self.generated_clks.writeln(f'always @(posedge emu_clk_2x) begin')
            self.generated_clks.indent()
            for gated_clk in gated_clks:
                self.generated_clks.writeln(f"if (emu_clk_unbuf == 1'b0) begin")
                self.generated_clks.indent()
                self.generated_clks.writeln(f'clk_unbuf_{gated_clk} <= clk_val_{gated_clk};')
                self.generated_clks.dedent()
                self.generated_clks.writeln(f'end else begin')
                self.generated_clks.indent()
                self.generated_clks.writeln(f"clk_unbuf_{gated_clk} <= clk_unbuf_{gated_clk};")
                self.generated_clks.dedent()
                self.generated_clks.writeln(f'end')
            self.generated_clks.dedent()
            self.generated_clks.writeln(f'end')
            self.generated_clks.writeln(f'')
            self.generated_clks.writeln(f'`ifndef SIMULATION_MODE_MSDSL')
            self.generated_clks.indent()
            for k, gated_clk in enumerate(gated_clks):
                self.generated_clks.writeln(f'BUFG buf_{k} (.I(clk_unbuf_{gated_clk}), .O(clk_{gated_clk}));')
            self.generated_clks.dedent()
            self.generated_clks.writeln(f'`else')
            self.generated_clks.indent()
            for gated_clk in gated_clks:
                self.generated_clks.writeln(f'assign clk_{gated_clk} = clk_unbuf_{gated_clk};')
            self.generated_clks.dedent()
            self.generated_clks.writeln(f'`endif')

    TEMPLATE_TEXT = '''
`timescale 1ns/1ps

`default_nettype none

{{subst.module_ifc.text}}

// generate emu_clk
logic emu_clk_unbuf = 0;

always @(posedge emu_clk_2x) begin
    emu_clk_unbuf <= ~emu_clk_unbuf;
end
`ifndef SIMULATION_MODE_MSDSL
    BUFG buf_emu_clk (.I(emu_clk_unbuf), .O(emu_clk));
`else
    assign emu_clk = emu_clk_unbuf;
`endif

{% if subst.use_default_oscillator %}
// Handle default oscillator
logic clk_unbuf_default_osc = 0;
always @(posedge emu_clk_2x) begin
    clk_unbuf_default_osc <= (~emu_clk_unbuf) & clk_val_default_osc;
end
`ifndef SIMULATION_MODE_MSDSL
    BUFG buf_default_osc (.I(clk_unbuf_default_osc), .O(clk_default_osc));
`else
    assign clk_default_osc = clk_unbuf_default_osc;
`endif
{% endif %}

// generate other clocks
{{subst.generated_clks.text}}
endmodule
 
`default_nettype wire
'''

def main():
    print(ModuleEmuClks(scfg=StructureConfig(prj_cfg=EmuConfig(root='test', cfg_file=''))).render())

if __name__ == "__main__":
    main()
