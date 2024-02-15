################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/proj.c 

SRC_OBJS += \
./src/proj.doj 

C_DEPS += \
./src/proj.d 


# Each subdirectory must supply rules for building sources it contributes
src/proj.doj: ../src/proj.c
	@echo 'Building file: $<'
	@echo 'Invoking: CrossCore SHARC C/C++ Compiler'
	cc21k -c -file-attr ProjectName="proj" -proc ADSP-21489 -flags-compiler --no_wrap_diagnostics -si-revision 0.2 -g -DCORE0 -DDO_CYCLE_COUNTS -D_DEBUG @includes-8a64c013a45a8f7de8bd84ed222e691f.txt -structs-do-not-overlap -no-const-strings -no-multiline -warn-protos -double-size-32 -swc -gnu-style-dependencies -MD -Mo "src/proj.d" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


