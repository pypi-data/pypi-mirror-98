# -*- coding:utf-8 -*-
#
# Copyright (C) 2019-2020 Alibaba Group Holding Limited


from __future__ import print_function
import os
import sys
import shutil

import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

try:
    import SCons.Script as SCons
except:
    import scons
    for path in scons.__path__:
        sys.path.append(path)
        import SCons.Script as SCons

from .log import logger
from .toolchain import *
from .qemu import *


# cpu models defines
CkcoreCPU = ['c807', 'c807f', 'c810', 'c810t', 'c810tv', 'c810v', 'c860', 'c860v', 'ck800', 'ck801', 'ck801t', 'ck802', 'ck802j', 'ck802t', 'ck803', 'ck803e', 'ck803ef', 'ck803efh', 'ck803efhr1', 'ck803efhr2', 'ck803efhr3', 'ck803efht', 'ck803efhtr1', 'ck803efhtr2', 'ck803efhtr3', 'ck803efr1', 'ck803efr2', 'ck803efr3', 'ck803eft', 'ck803eftr1', 'ck803eftr2', 'ck803eftr3', 'ck803eh', 'ck803ehr1', 'ck803ehr2', 'ck803ehr3', 'ck803eht', 'ck803ehtr1', 'ck803ehtr2', 'ck803ehtr3', 'ck803er1', 'ck803er2', 'ck803er3', 'ck803et', 'ck803etr1', 'ck803etr2', 'ck803etr3', 'ck803f', 'ck803fh', 'ck803fhr1', 'ck803fhr2', 'ck803fhr3', 'ck803fr1', 'ck803fr2', 'ck803fr3', 'ck803ft', 'ck803ftr1', 'ck803ftr2', 'ck803ftr3', 'ck803h', 'ck803hr1', 'ck803hr2', 'ck803hr3', 'ck803ht', 'ck803htr1', 'ck803htr2', 'ck803htr3', 'ck803r1', 'ck803r2', 'ck803r3', 'ck803s', 'ck803se', 'ck803sef', 'ck803seft', 'ck803sf', 'ck803st', 'ck803t', 'ck803tr1', 'ck803tr2', 'ck803tr3', 'ck804', 'ck804e', 'ck804ef', 'ck804efh', 'ck804efht', 'ck804eft', 'ck804eh', 'ck804eht', 'ck804et', 'ck804f', 'ck804fh', 'ck804ft', 'ck804h', 'ck804ht', 'ck804t', 'ck805', 'ck805e', 'ck805ef', 'ck805eft', 'ck805et', 'ck805f', 'ck805ft', 'ck805t', 'ck807', 'ck807e', 'ck807ef', 'ck807f', 'ck810', 'ck810e', 'ck810ef', 'ck810eft', 'ck810et', 'ck810f', 'ck810ft', 'ck810ftv', 'ck810fv', 'ck810t', 'ck810tv', 'ck810v', 'ck860', 'ck860f', 'ck860fv', 'ck860v', 'e801', 'e802', 'e802t', 'e803', 'e803t', 'e804d', 'e804df', 'e804dft', 'e804dt', 'e804f', 'e804ft', 'i805', 'i805f', 'r807', 'r807f', 's802', 's802t', 's803', 's803t']
RiscvCPU = ['rv32emc', 'rv32ec', 'rv32i', 'rv32iac', 'rv32im', 'rv32imac', 'rv32imafc', 'rv64imac', 'rv64imacxcki', 'rv64imafdc', 'e902', 'e902m', 'e902t', 'e902mt', 'e906', 'e906f', 'e906fd', 'c906', 'c906fd', 'c906fdv', 'c906v', 'c910', 'c910v']
ArmCPU = ['arm1020e', 'arm1020t', 'arm1022e', 'arm1026ej-s', 'arm10e', 'arm10tdmi', 'arm1136j-s', 'arm1136jf-s', 'arm1156t2-s',
                            'arm1156t2f-s', 'arm1176jz-s', 'arm1176jzf-s', 'arm2', 'arm250', 'arm3', 'arm6', 'arm60', 'arm600', 'arm610', 'arm620',
                            'arm7', 'arm70', 'arm700', 'arm700i', 'arm710', 'arm7100', 'arm710c', 'arm710t', 'arm720', 'arm720t', 'arm740t', 'arm7500',
                            'arm7500fe', 'arm7d', 'arm7di', 'arm7dm', 'arm7dmi', 'arm7m', 'arm7tdmi', 'arm7tdmi-s', 'arm8', 'arm810', 'arm9', 'arm920',
                            'arm920t', 'arm922t', 'arm926ej-s', 'arm940t', 'arm946e-s', 'arm966e-s', 'arm968e-s', 'arm9e', 'arm9tdmi', 'cortex-a12',
                            'cortex-a15', 'cortex-a17', 'cortex-a32', 'cortex-a35', 'cortex-a5','cortex-a53', 'cortex-a57', 'cortex-a7', 'cortex-a72',
                            'cortex-a73', 'cortex-a8', 'cortex-a9', 'cortex-m0', 'cortex-m0.small-multiply', 'cortex-m0plus', 'cortex-m0plus.small-multiply',
                            'cortex-m1', 'cortex-m1.small-multiply', 'cortex-m23', 'cortex-m3', 'cortex-m33', 'cortex-m33+nodsp', 'cortex-m4', 'cortex-m7',
                            'cortex-r4', 'cortex-r4f', 'cortex-r5', 'cortex-r52', 'cortex-r7', 'cortex-r8']

class Builder(object):
    def __init__(self, solution):
        self.toolchain_path = ''
        self.qemu_path = ''
        self.PREFIX = 'csky-abiv2-elf'
        if solution.toolchain_prefix:
            self.PREFIX = solution.toolchain_prefix
        self.SIZE = lambda: self.PREFIX + '-size'
        self.OBJDUMP = lambda: self.PREFIX + '-objdump'
        self.OBJCOPY = lambda: self.PREFIX + '-objcopy'
        self.STRIP = lambda: self.PREFIX + '-strip'
        self.AS = lambda: self.PREFIX + '-gcc'
        self.CC = lambda: self.PREFIX + '-gcc'
        self.CXX = lambda: self.PREFIX + '-g++'
        self.AR = lambda: self.PREFIX + '-ar'
        self.LINK = lambda: self.PREFIX + '-g++'

        self.solution = solution

        self.env = SCons.Environment(tools=['default', 'objcopy', 'objdump', 'product'],
                                     toolpath=[os.path.dirname(
                                         __file__) + '/site_tools'],
                                     AS=self.AS(),
                                     CC=self.CC(),
                                     CXX=self.CXX(),
                                     AR=self.AR(),
                                     LINK=self.CXX(),
                                     OBJCOPY=self.OBJCOPY(),
                                     OBJDUMP=self.OBJDUMP(),
                                     ARFLAGS='-rc',
                                     )

        # self.env.Decider(decide_if_changed)
        self.env.Decider('timestamp-newer')
        # self.env.Decider('make')
        # self.env.Decider('MD5')

        self.env.PrependENVPath('TERM', "xterm-256color")
        self.env.PrependENVPath('PATH', os.getenv('PATH'))

        if SCons.GetOption('verbose'):
            self.env.Replace(
                ARCOMSTR='AR $TARGET',
                ASCOMSTR='AS $TARGET',
                ASPPCOMSTR='AS $TARGET',
                CCCOMSTR='CC $TARGET',
                CXXCOMSTR='CXX $TARGET',
                LINKCOMSTR = 'LINK $TARGET',
                INSTALLSTR='INSTALL $TARGET',
                BINCOMSTR="Generating $TARGET",
            )

        self.set_cpu(self.solution.cpu_name)
        if self.solution.LINKFLAGS:
            linkflags = self.solution.LINKFLAGS
        else:
            if self.solution.cpu_name.lower().startswith('ck'):
                linkflags = ['-lm', '-Wl,-ckmap="yoc.map"', '-Wl,-zmax-page-size=1024']
            else:
                linkflags = ['-lm', '-Wl,-Map="yoc.map"', '-Wl,-zmax-page-size=1024']
        self.env.AppendUnique(
            ASFLAGS=self.solution.ASFLAGS,
            CCFLAGS=self.solution.CCFLAGS,
            CXXFLAGS=self.solution.CXXFLAGS,
            LINKFLAGS=linkflags,
        )

        self.env.Replace(AS=self.AS(),
                        CC=self.CC(),
                        CXX=self.CXX(),
                        AR=self.AR(),
                        LINK=self.CXX(),
                        OBJCOPY=self.OBJCOPY(),
                        OBJDUMP=self.OBJDUMP())

    def set_cpu(self, cpu):
        flags = ['-MP', '-MMD', '-g', '-Os', '-Wno-main']
        self.CPU = cpu.lower()
        if self.CPU in CkcoreCPU:
            if not self.PREFIX:
                self.PREFIX = 'csky-abiv2-elf'
            flags.append('-mcpu=' + self.CPU)
            if 'f' in self.CPU:
                flags.append('-mhard-float')
            if self.CPU == 'ck803ef':
                flags.append('-mhigh-registers')
                flags.append('-mdsp')
        elif self.CPU in RiscvCPU:
            if not self.PREFIX:
                self.PREFIX = 'riscv64-unknown-elf'
            elif not self.PREFIX.startswith('riscv'):
                self.PREFIX = 'riscv64-unknown-elf'
            if self.CPU == 'rv32emc':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32e')
            if self.CPU == 'rv32ec':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32e')
            if self.CPU == 'rv32i':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'rv32iac':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'rv32im':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'rv32imac':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'rv32imafc':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=ilp32f')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'rv64imac':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=lp64')
                flags.append('-mcmodel=medany')
            if self.CPU == 'rv64imacxcki':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=lp64')
                flags.append('-mcmodel=medany')
            if self.CPU == 'rv64imafdc':
                flags.append('-march=' + self.CPU)
                flags.append('-mabi=lp64d')
                flags.append('-mcmodel=medany')
            if self.CPU == 'e902':
                flags.append('-march=rv32ecxtheadse')
                flags.append('-mabi=ilp32e')
            if self.CPU == 'e902m':
                flags.append('-march=rv32emcxtheadse')
                flags.append('-mabi=ilp32e')
            if self.CPU == 'e902t':
                flags.append('-march=rv32ecxtheadse')
                flags.append('-mabi=ilp32e')
            if self.CPU == 'e902mt':
                flags.append('-march=rv32emcxtheadse')
                flags.append('-mabi=ilp32e')
            if self.CPU == 'e906':
                flags.append('-march=rv32imacxtheade')
                flags.append('-mabi=ilp32')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'e906f':
                flags.append('-march=rv32imafcxtheade')
                flags.append('-mabi=ilp32f')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'e906fd':
                flags.append('-march=rv32imafdcxtheade')
                flags.append('-mabi=ilp32d')
                flags.append('-mcmodel=medlow')
            if self.CPU == 'c906':
                flags.append('-march=rv64imacxtheadc')
                flags.append('-mabi=lp64')
                flags.append('-mcmodel=medlow')
                flags.append('-mtune=c906')
            if self.CPU == 'c906fd':
                flags.append('-march=rv64imafdcvxtheadc')
                flags.append('-mabi=lp64d')
                flags.append('-mcmodel=medany')
                flags.append('-mtune=c906')
            if self.CPU == 'c906fdv':
                flags.append('-march=rv64imafdcvxtheadc')
                flags.append('-mabi=lp64dv')
                flags.append('-mcmodel=medany')
                flags.append('-mtune=c906')
            if self.CPU == 'c906v':
                flags.append('-march=rv64imafdcvxtheadc')
                flags.append('-mabi=lp64dv')
                flags.append('-mcmodel=medany')
                flags.append('-mtune=c906')
            if self.CPU == 'c910':
                flags.append('-march=rv64imafdcvxtheadc')
                flags.append('-mabi=lp64d')
                flags.append('-mcmodel=medany')
                flags.append('-mtune=c910')
            if self.CPU == 'c910v':
                flags.append('-march=rv64imafdcvxtheadc')
                flags.append('-mabi=lp64dv')
                flags.append('-mcmodel=medany')
                flags.append('-mtune=c910')
        elif self.CPU in ArmCPU:
            if not self.PREFIX:
                self.PREFIX = 'arm-none-eabi'
            elif not self.PREFIX.startswith('arm'):
                self.PREFIX = 'arm-none-eabi'
            flags.append('-mcpu=' + self.CPU)
        else:
            logger.error(
                'error cpu `%s`, please make sure your cpu mode' % self.CPU)
            exit(0)

        self.env.AppendUnique(
            ASFLAGS=flags, CCFLAGS=flags,
            CXXFLAGS=flags, LINKFLAGS=flags
        )

    def clone_component(self, component):
        def var_convert(defs):
            if type(defs) == dict:
                vars = {}
                for k, v in defs.items():
                    if type(v) == str:
                        vars[k] = '\\"' + v + '\\"'
                    else:
                        vars[k] = v
                return vars
            else:
                return defs

        env = self.env.Clone()

        if component.build_config.cflag:
            env.AppendUnique(CCFLAGS=component.build_config.cflag.split())
            env.AppendUnique(CCFLAGS=component.build_config.cflag.split())
        if component.build_config.cxxflag:
            env.AppendUnique(CPPFLAGS=component.build_config.cxxflag.split())
        if component.build_config.asmflag:
            env.AppendUnique(ASFLAGS=component.build_config.asmflag.split())

        env.AppendUnique(CPPPATH=component.build_config.internal_include)
        env.AppendUnique(CPPPATH=self.solution.global_includes)
        env.AppendUnique(CPPDEFINES=var_convert(self.solution.defines))
        env.AppendUnique(CPPDEFINES=var_convert(component.build_config.define))

        # when dummy, use qemu platform
        if self.solution.variables.get('vendor') == 'dummy':
            if self.qemu_path == '':
                qemu = QemuYoC()
                path = qemu.check_qemu(self.solution.variables.get('arch'))
                if path:
                    self.qemu_path = os.path.dirname(path)
            if self.qemu_path:
                env.PrependENVPath('PATH', self.qemu_path)
            else:
                put_string("Not found qemu for %s, please check it." % self.solution.variables.get('arch'), level='error')
                exit(-1)

        if self.toolchain_path == '':
            tool = ToolchainYoC()
            path = tool.check_toolchain(self.PREFIX)
            if path:
                self.toolchain_path = os.path.dirname(path)

        if self.toolchain_path:
            env.PrependENVPath('PATH', self.toolchain_path)
        else:
            put_string("Not found toolchain: `%s`, please check it." % self.PREFIX, level='error')
            exit(-1)

        return env

    def build_component(self, component):
        env = self.clone_component(component)

        sources = []
        for fn in component.source_files:
            f_list = env.Glob(fn)
            if f_list:
                for f in f_list:
                    if f not in sources:
                        sources.append(f)

        job = env.StaticLibrary(os.path.join(
            self.solution.lib_path, component.name), sources)

        env.Default(job)

        if component.type == 'solution':
            linkflags = ' -Wl,--whole-archive -l' + \
                ' -l'.join(self.solution.libs) + ' -l' + component.name + ' -Wl,--no-whole-archive'
            linkflags += ' -nostartfiles -Wl,--gc-sections'
            linkflags += ' -T ' + self.solution.ld_script
            cname = 'yoc'  # component.name
            env.AppendUnique(LINKFLAGS=linkflags.split())
            env.AppendUnique(LIBPATH=self.solution.libpath)
            job = env.Program(target=cname + '.elf', source=[])

            # add recompiled file check.
            env.Depends(job, self.solution.depend_libs)
            env.Depends(job, self.solution.ld_script)
            env.Default(job)

            jobs = []
            dirname = os.path.dirname(env.GetBuildPath("output_xxxd"))
            if env['ELF_FILE']:
                output = os.path.join(dirname, env['ELF_FILE'])
                jj = env.InstallAs(output, job[0])
                jobs.append(jj)

            if env['OBJCOPY_FILE']:
                output = os.path.join(dirname, env['OBJCOPY_FILE'])
                jj = env.Binary(source=job[0], target=output)
                jobs.append(jj)

            if env['OBJDUMP_FILE']:
                output = os.path.join(dirname, env['OBJDUMP_FILE'])
                jj = env.Dump(source=job[0], target=output)
                jobs.append(jj)

            env.Default(jobs)

    def build_image(self, elf=None, objcopy=None, objdump=None, product=None):
        component = self.solution.solution_component
        env = self.clone_component(component)

        source_name = os.path.join('out', component.name, 'yoc.elf')
        if elf and os.path.isfile(source_name):
            shutil.copy2(source_name, elf)


        if objcopy:
            job1 = env.Binary(source=source_name, target=objcopy)
            env.Default(job1)

        if objdump:
            job2 = env.Dump(source=source_name, target=objdump)
            env.Default(job2)
        if product:
            job3 = env.Zip(source='generated/data/config.yaml',
                        target="generated/images.zip", PATH='generated/data')
            job4 = env.Hex(source='generated/images.zip', PATH='generated')
            env.Default(job3)
            env.Default(job4)


def decide_if_changed(dependency, target, prev_ni, repo_node=None):
    # put_string(dependency, prev_ni)
    if not prev_ni:
        return True
    if dependency.get_timestamp() != prev_ni.timestamp:
        return True

    return False
