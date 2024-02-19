################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL := ${ComSpec}

-include ../makefile.init

RM := clean

# All of the sources participating in the build are defined here
-include sources.mk
-include system/startup_ldf/subdir.mk
-include system/sru/subdir.mk
-include system/subdir.mk
-include src/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(DSP_DEPS)),)
-include $(DSP_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
LINKER_LOG_OUTPUTS += \
linker_log.xml \

OBJS := $(SRC_OBJS)
# Quote makefile variable : OBJS 
OBJS := $(subst \ ,@, $(OBJS))
OBJS := $(foreach var, $(OBJS), "$(subst @, ,$(var))")
# Quote makefile variable : DSP_DEPS 
DSP_DEPS := $(subst \ ,@, $(DSP_DEPS))
DSP_DEPS := $(foreach var, $(DSP_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : CC_DEPS 
CC_DEPS := $(subst \ ,@, $(CC_DEPS))
CC_DEPS := $(foreach var, $(CC_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : C++_DEPS 
C++_DEPS := $(subst \ ,@, $(C++_DEPS))
C++_DEPS := $(foreach var, $(C++_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : C_UPPER_DEPS 
C_UPPER_DEPS := $(subst \ ,@, $(C_UPPER_DEPS))
C_UPPER_DEPS := $(foreach var, $(C_UPPER_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : CXX_DEPS 
CXX_DEPS := $(subst \ ,@, $(CXX_DEPS))
CXX_DEPS := $(foreach var, $(CXX_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : ASM_DEPS 
ASM_DEPS := $(subst \ ,@, $(ASM_DEPS))
ASM_DEPS := $(foreach var, $(ASM_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : S_DEPS 
S_DEPS := $(subst \ ,@, $(S_DEPS))
S_DEPS := $(foreach var, $(S_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : C_DEPS 
C_DEPS := $(subst \ ,@, $(C_DEPS))
C_DEPS := $(foreach var, $(C_DEPS), "$(subst @, ,$(var))")
# Quote makefile variable : CPP_DEPS 
CPP_DEPS := $(subst \ ,@, $(CPP_DEPS))
CPP_DEPS := $(foreach var, $(CPP_DEPS), "$(subst @, ,$(var))")

# All Target
all: project.dxe

# Tool invocations
project.dxe: $(LDF_SRCS) $(SRC_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: CrossCore SHARC Linker'
	cc21k -proc ADSP-21489 -si-revision 0.2 -T C:/Users/User/OneDrive/Desktop/workspace/project/system/startup_ldf/app.ldf -no-mem -L C:/Users/User/OneDrive/Desktop/workspace/project/Debug/system/startup_ldf -flags-link -MDCORE0,-MDDEBUG -add-debug-libpaths -o project.dxe @input-file.txt
	@echo 'Finished building target: $@'
	@echo ' '

linker_log.xml: project.dxe $(LDF_SRCS) $(SRC_OBJS)

# Other Targets
clean:
	-$(RM) $(DXE) $(DSP_DEPS) $(CC_DEPS) $(LINKER_LOG_OUTPUTS) $(C++_DEPS) $(OBJS) $(C_UPPER_DEPS) $(CXX_DEPS) $(ASM_DEPS) $(S_DEPS) $(C_DEPS) $(CPP_DEPS)  project.dxe
	-@echo ' '

.PHONY: all clean dependents

-include ../makefile.targets
