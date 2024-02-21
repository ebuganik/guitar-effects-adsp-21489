/**
 *
 * 	Header file with function declarations.
 */

#ifndef __PROJ_H__
#define __PROJ_H__

typedef float float32_t;

void delay_effect(const float32_t* restrict audio_input, float32_t* restrict audio_output, float32_t delay_s, float32_t gain);
void echo_effect(const float32_t* audio_data,  float32_t *audio_output, uint32_t stages, float32_t delay_s, float32_t gain);
void tremolo_effect(const float32_t* audio_data, float32_t* audio_output, float32_t depth, float32_t rate);
void flanger_effect(const float32_t *audio_data,  float32_t *audio_output, float32_t delay_s, float32_t rate, float32_t gain);
void bitcrusher_effect(const float32_t *audio_data, float32_t *audio_output, uint32_t bit_depth);
void initSRU(void);
void turnOff(void);
void delay_cycles(uint32_t delayCount);
int write_samples(const char *outputFile, float32_t *audio_output, int arr_size);

#endif  /*__PROJ_H__*/
