/*****************************************************************************
 * project.h
 *****************************************************************************/

#ifndef __PROJECT_H__
#define __PROJECT_H__

/* Add your custom header content here */

void delay_effect(const float *audio_data, float *audio_output, float delay_s, float amplitude);
void echo_effect(const float *audio_data, float *audio_output, int stages, float delay_s, float amplitude);
float lfo_function(int i);
void tremolo_effect(const float *audio_data, float *audio_output);
void flanger_effect(const float *audio_data, float *audio_output, float delay_s);
void bit_crusher_effect(const float *audio_data, float *audio_output, int D, int bit_depth);

#endif /* __PROJECT_H__ */
