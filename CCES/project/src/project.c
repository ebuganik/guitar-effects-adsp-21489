/*****************************************************************************
 * project.c
 *****************************************************************************/
#include <sys/platform.h>
#include "adi_initialize.h"
#include "project.h"
#include "audio.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <cycle_count.h>

#define SAMPLE_RATE 11025
#define NUM_SAMPLES 43155
/*LFO parameters*/
#define DEPTH 0.5
#define RATE 1.0
#define PI 3.1415926535
#define lfo(i) (1+DEPTH*sinf(2.0*PI*i*RATE/SAMPLE_RATE))
/* Za potencijalnu alokaciju unutar funkcija koje se pozivaju, da budu dostupni*/
/* Dodati jos optimizacionih metoda*/


int index, uid = 999;
float* buffer;
#pragma section("seg_hp2")
static char extra_heap[512000];
/*za 43 155 odmjeraka, 43 155 * 4 = 172 620*/
#pragma optimize_for_speed
/* Odredjivanje broja procesorskih ciklusa*/

	cycle_t start_count;
	cycle_t stop_count;
	cycle_t stats;

void delay_effect(const float *audio_data, float *audio_output, float delay_s, float amplitude)
{
	/* 5 725 867 cycles, 14.314 ms prvobitno*/
	int delay_samples = floor(SAMPLE_RATE*delay_s);
	/*printf("%d", delay_samples);*/
	float *x_delayed = (float*)heap_calloc(index, delay_samples+ NUM_SAMPLES, sizeof(float));
	/*#pragma vector_for(1000)*/
	/*#pragma SIMD_for*/
	/*for (int i = delay_samples; i < delay_samples + NUM_SAMPLES; i++)
	{
		x_delayed[i] = audio_data[i-delay_samples];
	}
	*/

	/*#pragma no_vectorization*/
	/*#pragma SIMD_for*/
	int i, l;
	/* 5 294 299 cycles, 13.23 ms*/
	/* sa optimize for speed 3 783 865, 9.46 ms*/
	for(i=0,l=delay_samples; i<NUM_SAMPLES; i++, l++)
	{
		x_delayed[l] = audio_data[l-delay_samples];
		audio_output[i] = audio_data[i] + amplitude * x_delayed[i];
	}
	/* oslobodi koristen prostor za pomocni signal*/
	heap_free(index, x_delayed);
}

void echo_effect(const float *audio_data, float *audio_output, int stages, float delay_s, float amplitude)
{
	/*Da li omoguciti upotrebu funkcije delay_effect?*/
	float stage_amp;
	int delay_samples = floor(SAMPLE_RATE*delay_s);
	float* delayed_x = (float*)heap_calloc(index, delay_samples+NUM_SAMPLES, sizeof(float));
	/*#pragma SIMD_for*/
    	/* objedinjene dvije petlje koje idu do NUM_SAMPLES*/
	int i, l; /* this way 15 354 017 cycles, 38.38 ms*/
	for(i=0,l=delay_samples; i<NUM_SAMPLES; i++,l++)
	{
		audio_output[i] = audio_data[i];
		delayed_x[l] = audio_data[l-delay_samples];
	}
	/* sa optimize for speed 10 499 029, time 26.24 ms*/
	/*#pragma SIMD_for*/

	/*for(int i=delay_samples; i<NUM_SAMPLES+delay_samples; i++)
	{
		delayed_x[i] = audio_data[i-delay_samples];
	}*/

	/*#pragma no_vectorization*/
	/*#pragma vector_for(1000)*/

	for(int i=1; i<stages+1; i++)
	{
		stage_amp = amplitude/i;  /* prvobitno 15 569 809 cycles, time 38 ms*/
		for(int k=0; k<NUM_SAMPLES; k++)
			{
			/*stage_amp = amplitude/i; 20 748 289 cycles, time 51.87 ms*/
			audio_output[k] += stage_amp*delayed_x[k];
			}
	}

	/*int k, l;
	#pragma SIMD_for
	for(int i=1; i<stages+1; i++)
	{    17 727 553 cycles, 44.31 ms
		stage_amp = amplitude/i;
		for(k=0, l=delay_samples; k<NUM_SAMPLES; k++, l++)
		{
			delayed_x[l] = audio_data[l-delay_samples];
			audio_output[k] += stage_amp*delayed_x[k];
		}
	}*/

	/*for(int i=1; i < stages+1; i++)
	{
	    stage_amp=amplitude/i;

	    int k = 0;
	    while (k < NUM_SAMPLES)
	    {
	        audio_output[k]+=stage_amp*delayed_x[k];
	        k++;
	    }
	}*/

		/*int i=stages+1; 26 mil. cycles, bad

		while(i--)
		{
			for(int k=0; k<NUM_SAMPLES; k++)
			{

			stage_amp=amplitude/i;
			audio_output[k]+=stage_amp*delayed_x[k];
			}
		}*/


	heap_free(index, delayed_x);
}

/*Ovo moze i u define --  ima li razlike kakve?*/
/*float lfo(int i)
{
	return 1+DEPTH*sinf(2.0*PI*i*RATE/SAMPLE_RATE);
}*/

void tremolo_effect(const float *audio_data, float *audio_output)
{
	/* prvobitno 5 502 229 cycles, 13.75 ms sa funkcijom lfo_function*/
	/*#pragma SIMD_for*/
	/* sa optimize for speed 4 531 237*/
	for(int i=0; i<NUM_SAMPLES; i++)
	{
		/*audio_output[i] = audio_data[i]*lfo(i);*/
		/*bez poziva funkcije lfo_function, 4 890 865 cycles, 12 ms*/
		/* sa optimize for speed 3 883 922, 9.7 ms*/
		/*audio_output[i] = audio_data[i]*1+DEPTH*sinf(2.0*PI*i*RATE/SAMPLE_RATE);*/

		/*funkcija u define 4 962 790*/
		/*sa optimize for speed 3 883 948*/
		audio_output[i] = audio_data[i]*lfo(i);
	}

}
/* Nedostaje jos optimizovanja!*/
void flanger_effect(const float *audio_data, float *audio_output, float delay_s)
{
	/* prvobitno 5 753 874, 14 ms*/
	/* optimize for speed 4 315 444, 10 ms*/
	int d;
	int delay_samples = floor(delay_s*SAMPLE_RATE);
	for(int i=0; i<NUM_SAMPLES; i++)
{
		/*d = (int)(delay_samples*(1 + sinf(2.0*PI* i * RATE/SAMPLE_RATE)));*/
		/* poziv funkcije lfo, depth 1.0, 6 473 105, 16.1 ms*/
		/* optimize for speed 4 890 849, 12.2 ms*/
		d = (int)(delay_samples*lfo(i));
		if(d<i)
		{
			/* depth kao zasebna vrijednost*/
			audio_output[i]= audio_data[i]+ DEPTH*audio_data[i-d];
		}
		else
		{
			audio_output[i] = audio_data[i];
		}
	}
}

void bit_crusher_effect(const float *audio_data, float *audio_output, int D, int bit_depth)
{
	/* nova velicina niza je NUM_SAMPLES/D*/
	/* naivna implementacija - 1 966 165*/
	/* optimize for speed 1 459 699*/

	int i, j;
	/*int max_value = powf(2,bit_depth);*/
	 unsigned int max_value = 1<<bit_depth;
	 /*1 450 520*/
	/*#pragma no_vectorization nema efekta*/
	/*#pragma SIMD_for nema efekta */
	for(i = 0, j = 0; i < NUM_SAMPLES; i += D, j++)
	{
		audio_output[j] = audio_data[i];
		/* 791 209 cycles*/
		audio_output[j] /= (float)max_value;
	}
	/*#pragma no_vectorization nema efekta*/
	/*#pragma SIMD_for*/
	/*for (i=0; i<j; i++)
	{
		audio_output[i] /= (float)max_value;
	}*/
}


int main()
{
	/**
	 * Initialize managed drivers and/or services that have been added to 
	 * the project.
	 * @return zero on success 
	 */

	/* Implementirati nesto da se ne mora rucno otkomentarisati poziv neke od funkcija*/

	/* Pracenje vremena izvrsavanja*/

	volatile clock_t clock_start;
	volatile clock_t clock_stop;

	adi_initComponents();
	float *audio_output = 0;
	FILE *fp;
	unsigned int length;

	double secs;

	index = heap_install(extra_heap, sizeof(extra_heap), uid);

	if (index<0)
	{
		printf("Installation failed!\n");
		return -1;
	}
	/*Bit Crusher effect parameters*/
		int dec_fac = 3;
		int bit_depth = 3;
	audio_output = (float*)heap_calloc(index, NUM_SAMPLES, sizeof(float));
	/* SETTING DEFAULT PARAMETERS */
	/* Delay effect parameters*/
	int delay_time = 2.0;
	float delay_amp = 2.0;
	/* Echo effect parameters*/
	int stages = 3;
	float stage_delay = 0.2;
	float stage_amp = 1.0;
	/*Tremolo effect parameters  - LFO*/
	/*Flanger effect parameters*/
	float flanger_delay = 0.001;
	clock_start = clock();
	START_CYCLE_COUNT(start_count);
	delay_effect(audio_data, audio_output, delay_time, delay_amp);
	/*echo_effect(audio_data, audio_output, stages, stage_delay, stage_amp);*/
	/*tremolo_effect(audio_data, audio_output);*/
	/*flanger_effect(audio_data, audio_output, flanger_delay);*/
	/*bit_crusher_effect(audio_data, audio_output, dec_fac,bit_depth);*/
	STOP_CYCLE_COUNT(stop_count,start_count);
	clock_stop = clock();
	PRINT_CYCLES("Cycles number: ",stop_count);
	secs = ((double)(clock_stop - clock_start))/CLOCKS_PER_SEC;
	printf("Time taken is %e seconds\n", secs);

	/*Writing to a file*/

    fp = fopen("audio_output.txt", "w");
    if (fp == NULL)
    {
    	printf("Error while opening .txt file!\n");
    	return -1;
    }
    else printf("Writing to .txt file ...\n");

    /* ova vrijednost da se azurira zavisno od velicine niza audio_output*/
	/*spor upis u fajl, rjesenje? */
	
	char* outputValue = (char*)heap_calloc(index, NUM_SAMPLES, sizeof(char));
	
	char outputArr[10000];
	int ind = 0;
	for (int i = 0; i<NUM_SAMPLES; i++){
		ind+=sprintf(outputValue+ind, "%.6f\n", audio_output[i]);

	}
	//printf("output:%s", outputArr);
	fprintf(fp, "%s", outputValue);

    //for(int i=0; i<NUM_SAMPLES/dec_fac; i++)
    //{
    //	fprintf(fp, "%f\n", audio_output[i]);
    //}

    fclose(fp);

    printf("File closed!\n");

    heap_free(index, audio_output);
    printf("Heap free\n");
	return 0;
}





