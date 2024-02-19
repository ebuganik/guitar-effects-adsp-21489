/*****************************************************************************
 * project.c
 *****************************************************************************/
#include <sys/platform.h>
#include <def21489.h>
#include <sru21489.h>
#include <SYSREG.h>
#include "adi_initialize.h"
#include "project.h"
#include "audio.h"
#include "builtins.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <cycle_count.h>

#define SAMPLE_RATE 11025
#define DEC_FAC 3
/*LFO parameters*/
#define DEPTH 0.7
#define RATE 5.0

#define PI 3.14159265358979
/*#define lfo(i) (1+DEPTH*sinf(2.0*PI*i*RATE/SAMPLE_RATE))*/

/*#pragma optimize_for_speed*/

	cycle_t start_count;
	cycle_t stop_count;

#pragma section("seg_sram")
float32_t audio_w_effect[NUM_SAMPLES];
#pragma section("seg_sram")
float32_t temp_array[NUM_SAMPLES];
#pragma section("seg_sram")
float32_t audio_dec_effect[NUM_SAMPLES/DEC_FAC];


void delay_effect(const float32_t* restrict audio_input, float32_t* restrict audio_output, float32_t delay_s, float32_t gain)
{
	/* naive implementation*/
	/*int delay_samples = (int)(delay_s*SAMPLE_RATE);*/
	int delay_samples = conv_fix(delay_s*SAMPLE_RATE);
	int i,k;

  for(k=0, i = delay_samples; i < NUM_SAMPLES; i++, k++)
  {
	  temp_array[i] = audio_input[i-delay_samples];
	  /*  delayed_value = gain*temp_array[k];*/
	  audio_output[k] = audio_input[k]+gain*temp_array[k];
	  /*audio_output[k] = audio_input[k]+delayed_value;*/
  }
 /* for(k=0; k<NUM_SAMPLES; k++)
  {
	  audio_output[k] = audio_input[k]+amplitude*temp_array[k];
  }*/
}

void echo_effect(const float32_t* restrict audio_data, float32_t* restrict audio_output, uint32_t stages, float32_t delay_s, float32_t gain)

{
		/*naive implementation*/
		float32_t stage_amp;
		/*int delay_samples = (int)(SAMPLE_RATE*delay_s);*/
		int delay_samples = conv_fix(delay_s*SAMPLE_RATE);
		int i,k;
/*#pragma loop_unroll 10*/
		for(i=0, k=delay_samples; i<NUM_SAMPLES; i++, k++)
		{
			audio_output[i] = audio_data[i];
			temp_array[k] = audio_data[k-delay_samples];
		}
		/*for(k=delay_samples; k<NUM_SAMPLES; k++)
		{
			temp_array[k] = audio_data[k-delay_samples];
		}*/
	__builtin_assert(stages> 1); /*for stages = 1, it's better to call delay function*/
/*#pragma vector_for(10)*/
/*#pragma loop_unroll 10*/
	for(i=1; i<stages+1; i++)
		{
			/*stage_amp = (float32_t)(gain/i);*/
			stage_amp = gain*frecipsf((float32_t)i);
/*#pragma vector_for(10)*/
			for(k=0; k<NUM_SAMPLES; k++)
				{
				audio_output[k]+=stage_amp*temp_array[k];
				}
		}

}

/*inline float32_t lfo(int i) {return 1+DEPTH*sinf(2.0*PI*i*RATE/SAMPLE_RATE);}*/

void tremolo_effect(const float32_t* restrict audio_data, float32_t* restrict audio_output)
{
	int i;
/*#pragma SIMD_for*/
/*#pragma no_vectorization*/
	for(i=0; i<NUM_SAMPLES; i++)
	{
		audio_output[i] = audio_data[i]*1+DEPTH*sinf(2.0*PI*i*RATE/SAMPLE_RATE);
		/*call for function in define or inline*/
		/*audio_output[i] = audio_data[i]*lfo(i);*/
	}

}
void flanger_effect(const float32_t* restrict audio_data, float32_t* restrict audio_output, float32_t delay_s, float32_t rate, float32_t gain)
{

	int i,d;
	int delay_samples = conv_fix(delay_s*SAMPLE_RATE);
	float32_t lfo_w = 2.0*PI*rate/SAMPLE_RATE;
	for(i = 0 ; i<NUM_SAMPLES; i++)
{
		/*d = (int)(delay_samples*(1 + sinf(2.0*PI* i * rate/SAMPLE_RATE)));*/
		d = (int)(delay_samples*(1 + sinf(lfo_w*i)));
		/*if(d<i)*/
		if(expected_true(i-d > 0))
		{
			/*audio_output[i]= audio_data[i]+ DEPTH*audio_data[i-d];*/
			audio_output[i]= audio_data[i]+ gain*audio_data[i-d];
		}
		else
		{
			audio_output[i] = audio_data[i];
		}
	}
}
void bitcrusher_effect(const float32_t* restrict audio_data, float32_t* restrict audio_output, uint32_t bit_depth)
{

	int i, j;
	/*uint32_t max_value = powf(2,bit_depth);*/
	uint32_t  max_value = 1<<bit_depth;

	for(i = 0, j = 0; i < NUM_SAMPLES; i += DEC_FAC, j++)
	{
		/*audio_output[j] = audio_data[i];*/
		/* Built-in functions for floating point and integer type*/
		/*audio_output[j] = (int)(max_value*audio_data[i])/((float32_t)max_value);*/
		audio_output[j] = conv_fix(max_value*audio_data[i])*frecipsf((float32_t)max_value);
	}
	/*for (i=0; i<j; i++)
	{
		audio_output[i] = (int)(max_value*audio_output[i])/(float32_t)max_value;
	}*/
}

int main(int argc, char *argv[])
{
	/**
	 * Initialize managed drivers and/or services that have been added to
	 * the project.
	 * @return zero on success
	 */
	adi_initComponents();
	FILE *fp;
	double secs;
	volatile clock_t clock_start;
	volatile clock_t clock_stop;
	int arr_size = sizeof(audio_w_effect)/sizeof(audio_w_effect[0]);
	int dec_arr_size = sizeof(audio_dec_effect)/sizeof(audio_dec_effect[0]);
	initSRU();
	turnOff();

	/**SETTING DEFAULT PARAMETERS**/
	delay_cycles(3500000);
	sysreg_bit_set(sysreg_FLAGS, FLG4);

	/* Delay effect*/
	float32_t delay_time = 0.5;
	float32_t delay_amp = 0.5;

	/*Echo effect*/
	uint32_t stages = 3;
	float32_t stage_delay = 0.2;
	float32_t gain = 1.0;

	/* Tremolo effect*/
	float32_t lfo_depth = 0.7;
	float32_t lfo_rate = 5.0;

	/*Flanger effect*/
	float32_t flanger_delay = 0.001;
	float32_t flanger_rate = 2.0;
	float32_t amplitude = 0.8;

	/*Bit Crusher effect*/
	uint32_t bit_depth = 3;


	/**FUNCTION CALL**/
	delay_cycles(3500000);
	sysreg_bit_set(sysreg_FLAGS, FLG5);
	/*clock_start = clock();*/
	START_CYCLE_COUNT(start_count);
	/*delay_cycles(3500000);*/
	/*sysreg_bit_set(sysreg_FLAGS, FLG6);*/
	/*delay_effect(audio_data, audio_w_effect, delay_time, delay_amp);*/
	/*tremolo_effect(audio_data, audio_w_effect);*/
	echo_effect(audio_data, audio_w_effect, stages, delay_time, gain);
	/*bitcrusher_effect(audio_data, audio_dec_effect, bit_depth);*/
	/*flanger_effect(audio_data, audio_w_effect, flanger_delay, flanger_rate, amplitude);*/
	/*delay_cycles(3500000);*/
	/*SRU(HIGH,DAI_PB03_I);*/
	STOP_CYCLE_COUNT(stop_count,start_count);
	/*clock_stop = clock();*/
	PRINT_CYCLES("Cycles number: ",stop_count);
	/*secs = ((double)(clock_stop - clock_start))/CLOCKS_PER_SEC;*/
	/*printf("Time taken to proceed function is %e seconds\n", secs);*/

	/**WRITING TO FILE**/
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB04_I);
	START_CYCLE_COUNT(start_count);
	printf("\nWriting samples to file, number of samples is %d \n", arr_size);
	write_samples("audio_w_echo.txt", audio_w_effect, arr_size);
	STOP_CYCLE_COUNT(stop_count,start_count);
	PRINT_CYCLES("Cycles number: ",stop_count);
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB17_I);
	printf("Program ends.\n");
	return 0;
	}

void write_samples(const char *outputFile, float32_t *audio_output, int arr_size)
	{
	FILE *fp = fopen(outputFile, "w");
	int half_samples = arr_size/2;
	int i = 0;
	/*printf("%d", half_samples);*/
	/*unsigned int arr_size = sizeof(audio_output)/sizeof(audio_output[0]);*/
	/*printf("%d", arr_size);*/

	if(fp == NULL) {
		printf("File couldn't be opened!\n");
	}else
		{
		printf("File opened!\n");
		SRU(HIGH,DAI_PB15_I);
		}

	for(int i=0; i<arr_size;i++)
	{
		fprintf(fp, "%f\n", audio_output[i]);
		if(i>=half_samples)
		{
			SRU(HIGH,DAI_PB16_I);
		}
	}

	fclose(fp);
	printf("File closed!\n");

	}

void initSRU(void)
	{
		//** LED01**//
		SRU(HIGH,DPI_PBEN06_I);
		SRU(FLAG4_O,DPI_PB06_I);
		//** LED02**//
		SRU(HIGH,DPI_PBEN13_I);
		SRU(FLAG5_O,DPI_PB13_I);
		//** LED03**//
		SRU(HIGH,DPI_PBEN14_I);
		SRU(FLAG6_O,DPI_PB14_I);
		//** LED04**//
		SRU(HIGH,DAI_PBEN03_I);
		SRU(HIGH,DAI_PB03_I);
		//** LED05**//
		SRU(HIGH,DAI_PBEN04_I);
		SRU(HIGH,DAI_PB04_I);
		//** LED06**//
		SRU(HIGH,DAI_PBEN15_I);
		SRU(HIGH,DAI_PB15_I);
		//** LED07**//
		SRU(HIGH,DAI_PBEN16_I);
		SRU(HIGH,DAI_PB16_I);
		//** LED08**//
		SRU(HIGH,DAI_PBEN17_I);
		SRU(HIGH,DAI_PB17_I);
		//Setting flag pins as outputs
		sysreg_bit_set(sysreg_FLAGS,(FLG4O|FLG5O|FLG6O));
		//Setting HIGH to flag pins
		sysreg_bit_set(sysreg_FLAGS,(FLG4|FLG5|FLG6));
}

void turnOff(void)
{
	//turn off LEDs
	sysreg_bit_clr(sysreg_FLAGS, FLG4);
	sysreg_bit_clr(sysreg_FLAGS, FLG5);
	sysreg_bit_clr(sysreg_FLAGS, FLG6);
	SRU(LOW,DAI_PB03_I);
	SRU(LOW,DAI_PB04_I);
	SRU(LOW,DAI_PB15_I);
	SRU(LOW,DAI_PB16_I);
	SRU(LOW,DAI_PB17_I);
}

void delay_cycles(uint32_t delayCount)
	{
/* delayCount = 1 => 38ns delay */
	while(delayCount--);
	}
