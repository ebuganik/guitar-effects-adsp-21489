################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/project.c 

SRC_OBJS += \
./src/project.doj 

C_DEPS += \
./src/project.d 


# Each subdirectory must supply rules for building sources it contributes
src/project.doj: ../src/project.c
	@echo 'Building file: $<'
	@echo 'Invoking: CrossCore SHARC C/C++ Compiler'
	cc21k -c -file-attr ProjectName="project" -proc ADSP-21489 -flags-compiler --no_wrap_diagnostics -si-revision 0.2 -g -DCORE0 -DDO_CYCLE_COUNTS -D_DEBUG @includes-053fdfe95a233f7c8fb9f4a93ec8a990.txt -structs-do-not-overlap -no-const-strings -no-multiline -warn-protos -double-size-32 -swc -gnu-style-dependencies -MD -Mo "src/project.d" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


