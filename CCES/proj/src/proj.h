/*****************************************************************************
 * project.h
 *****************************************************************************/

#ifndef __PROJ_H__
#define __PROJ_H__

typedef float float32_t;

void delay_effect(const float32_t *audio_input, float32_t *audio_output, float32_t delay_s, float32_t amplitude);
void echo_effect(const float32_t *audio_data, float32_t *audio_output, int stages, float32_t delay_s, float32_t amplitude);
void tremolo_effect(const float32_t *audio_data, float32_t *audio_output);
void flanger_effect(const float32_t *audio_data, float32_t *audio_output, float32_t delay_s);
void bit_crusher_effect(const float32_t *audio_data, float32_t *audio_output, unsigned int bit_depth);
void initSRU(void);
void turnOff(void);
void delay_cycles(unsigned int delayCount);
void write_samples(const char *outputFile, float32_t *audio_output, int arr_size);

#endif /* __PROJ_H__ */