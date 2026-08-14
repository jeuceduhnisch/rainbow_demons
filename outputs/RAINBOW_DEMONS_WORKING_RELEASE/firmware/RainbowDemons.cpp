#include "daisy_patch_sm.h"

#include <cmath>
#include <cstddef>
#include <cstdint>

using namespace daisy;
using namespace daisy::patch_sm;

// Independent clean-room firmware for the Rainbow Demons Patch SM instrument.
// See the release README for the independent-design disclaimer.
namespace
{
constexpr float  kSampleRate     = 48000.0f;
constexpr size_t kMaxSamples     = static_cast<size_t>(kSampleRate * 30.0f);
constexpr size_t kMinPhrase      = 512;
constexpr float  kResetHoldMs    = 1200.0f;
constexpr float  kCrossfade      = 192.0f;
constexpr float  kSliceAutoDeadZone = 0.03f;

enum class Mode { Tape, Slice, Scatter };
enum class Option { Reverse, Alternate, Forward };
enum class Quantize { Octave, Free, Semitone };

struct Controls
{
    float time;       // DIR 1: playback speed and direction
    float feedback;
    float head2;      // Mode 3 DIR 2, normalized to match the other heads
    float mix;
    float q;          // pitch quantization strength/interval set
    float length;     // LEN B: delay/phrase/slice length
    Mode mode;
    Option option;
    Quantize quantize;
};

struct Head
{
    float position;
    float rate;
};

DaisyPatchSM patch;
Switch record_button;
Switch reset_button;
Switch3 mode_switch;
Switch3 option_switch;
Switch3 quantize_switch;
GPIO record_led;
GPIO status_led;

float DSY_SDRAM_BSS buffer[kMaxSamples];

// Build with RAINBOW_DEMONS_DIAGNOSTIC_NO_SDRAM_WRITE to test external-memory
// writes are coupling into the analog input. Normal builds are unchanged.
#ifndef RAINBOW_DEMONS_DIAGNOSTIC_NO_SDRAM_WRITE
#define RAINBOW_DEMONS_CAPTURE_WRITE(sample) (buffer[capture_position++] = (sample))
#else
#define RAINBOW_DEMONS_CAPTURE_WRITE(sample) (++capture_position)
#endif

Mode current_mode = Mode::Tape;
size_t write_position = 0;
size_t phrase_samples = 0;
size_t capture_position = 0;
bool phrase_ready = false;
uint32_t mode_generation = 1;
uint32_t phrase_generation = 0;
bool capturing = false;
bool previous_record_pressed = false;
bool reset_hold_latched = false;
bool slice_record_override = false;
bool slice_auto_capture = false;
int32_t slice_auto_countdown = -1;
float tape_position = 0.0f;
size_t tape_valid_samples = 0;
size_t previous_tape_length = 0;
bool tape_initialized = false;
float tape_filter_state = 0.0f;
float tape_wow = 0.0f;
float tape_wow_target = 0.0f;
uint32_t tape_wow_counter = 0;
float slice_position = 0.0f;
float slice_start = 0.0f;
Head scatter_heads[3] = {{0.0f, 1.0f}, {0.0f, 1.0f}, {0.0f, 1.0f}};
uint32_t random_state = 0x43543532u;
int32_t activity_samples = 0;

inline float Clamp(float x, float lo, float hi)
{
    return x < lo ? lo : (x > hi ? hi : x);
}

float CalibrateMixPot(float raw)
{
    // MIX is wired to conditioned CV_8 rather than a native unipolar ADC.
    // Allow for op-amp/rail and pot tolerance. Audio calibration of this built
    // unit measured its conditioned CW endpoint near 0.66, well below the
    // nominal rail. Use asymmetric endpoints and retain a little margin so
    // both ends land on exact digital dry/wet values.
    const float conditioned = Clamp((raw - 0.015f) * (1.0f / 0.92f), 0.0f, 1.0f);
    constexpr float dry_endpoint = 0.08f;
    constexpr float wet_endpoint = 0.62f;
    return Clamp((conditioned - dry_endpoint)
                     * (1.0f / (wet_endpoint - dry_endpoint)),
                 0.0f,
                 1.0f);
}

float CalibrateMode3Head2Pot(float raw)
{
    // Two on-panel measurements placed conditioned values 0.28 at 10:30 and
    // 0.50 at 2 o'clock. Interpolating between them puts physical noon near
    // 0.375. Map that point to the stopped-head value while retaining the
    // complete reverse/forward travel at both ends.
    const float conditioned = CalibrateMixPot(raw);
    constexpr float measured_center = 0.375f;
    if(conditioned <= measured_center)
        return 0.5f * conditioned / measured_center;
    return 0.5f
           + 0.5f * (conditioned - measured_center)
                 / (1.0f - measured_center);
}

inline float SoftClip(float x)
{
    return x / (1.0f + std::fabs(x));
}

float RandomUnit()
{
    random_state = random_state * 1664525u + 1013904223u;
    return static_cast<float>((random_state >> 8) & 0x00ffffffu)
           * (1.0f / 16777215.0f);
}

Mode ReadMode()
{
    const int p = mode_switch.Read();
    if(p == Switch3::POS_UP) return Mode::Tape;
    if(p == Switch3::POS_DOWN) return Mode::Scatter;
    return Mode::Slice;
}

Option ReadOption()
{
    const int p = option_switch.Read();
    if(p == Switch3::POS_UP) return Option::Forward;
    if(p == Switch3::POS_DOWN) return Option::Reverse;
    return Option::Alternate;
}

Quantize ReadQuantize()
{
    const int p = quantize_switch.Read();
    if(p == Switch3::POS_UP) return Quantize::Semitone;
    if(p == Switch3::POS_DOWN) return Quantize::Octave;
    return Quantize::Free;
}

Controls ReadControls()
{
    // Preserve the already-built carrier wiring exactly:
    // TIME/ADC_9, FILTER/ADC_10, FLUTTER/ADC_11,
    // FEEDBACK/CV_7 and MIX/CV_8. The five panel CV inputs remain CV_1..CV_5.
    const float time_p = Clamp(patch.GetAdcValue(ADC_9), 0.0f, 1.0f);
    const float q_p    = Clamp(patch.GetAdcValue(ADC_10), 0.0f, 1.0f);
    const float len_p  = Clamp(patch.GetAdcValue(ADC_11), 0.0f, 1.0f);
    const float fb_p   = Clamp(patch.GetAdcValue(CV_7), 0.0f, 1.0f);
    const float mix_p  = CalibrateMixPot(patch.GetAdcValue(CV_8));

    const float cv1 = Clamp(patch.GetAdcValue(CV_1), -1.0f, 1.0f);
    const float cv2 = Clamp(patch.GetAdcValue(CV_2), -1.0f, 1.0f);
    const float cv3 = Clamp(patch.GetAdcValue(CV_3), -1.0f, 1.0f);
    const float cv4 = Clamp(patch.GetAdcValue(CV_4), -1.0f, 1.0f);
    // CV_5 is the jack physically located under FLUTTER on this reused board,
    // not a normalled MIX CV. Do not let its unpatched offset prevent the Mix
    // pot from reaching either endpoint.

    Controls c;
    c.time     = Clamp(time_p + 0.25f * cv1, 0.0f, 1.0f);
    c.q        = Clamp(q_p + 0.50f * cv2, 0.0f, 1.0f);
    c.length   = Clamp(len_p + 0.50f * cv3, 0.0f, 1.0f);
    c.feedback = Clamp(fb_p + 0.50f * cv4, 0.0f, 0.985f);
    // In Mode 3 FEEDBACK becomes DIR 2.  Its own center correction puts the
    // stopped head at physical noon; increasing clockwise matches DIR 1/3.
    c.head2    = Clamp(CalibrateMode3Head2Pot(fb_p) + 0.50f * cv4,
                       0.0f,
                       1.0f);
    // Physical panel convention: CCW=dry and CW=wet. CalibrateMixPot supplies
    // hard digital endpoints despite the conditioned CV_8 pot wiring.
    c.mix      = mix_p;
    c.mode     = ReadMode();
    c.option   = ReadOption();
    c.quantize = ReadQuantize();
    return c;
}

float Wrap(float p, float length)
{
    if(length <= 1.0f) return 0.0f;
    while(p < 0.0f) p += length;
    while(p >= length) p -= length;
    return p;
}

float ReadBuffer(float p, size_t length)
{
    if(length < 2) return 0.0f;
    p = Wrap(p, static_cast<float>(length));
    const size_t i0 = static_cast<size_t>(p);
    const size_t i1 = (i0 + 1) % length;
    const float f = p - static_cast<float>(i0);
    return buffer[i0] + (buffer[i1] - buffer[i0]) * f;
}

float ReadLoopCrossfaded(float p, float start, float length, size_t storage_length)
{
    if(length < 2.0f) return 0.0f;
    p = Wrap(p, length);
    float y = ReadBuffer(start + p, storage_length);
    const float fade = Clamp(length * 0.08f, 8.0f, kCrossfade);
    if(p > length - fade)
    {
        const float x = (p - (length - fade)) / fade;
        const float beginning = ReadBuffer(start + p - length, storage_length);
        y += (beginning - y) * x;
    }
    return y;
}

float RateFromKnob(float knob, Quantize quantize, Option option)
{
    // Each DIR control spans -4x to +4x with a stationary head at noon.
    float raw_rate = (knob - 0.5f) * 8.0f;
    float direction = raw_rate < 0.0f ? -1.0f : 1.0f;
    if(option == Option::Reverse) direction = -1.0f;
    else if(option == Option::Forward) direction = 1.0f;

    const float magnitude = std::fabs(raw_rate);
    if(magnitude < 0.015f) return 0.0f;
    float semitones = 12.0f * (std::log(magnitude) / std::log(2.0f));
    if(quantize == Quantize::Semitone)
        semitones = std::floor(semitones + 0.5f);
    else if(quantize == Quantize::Octave)
        semitones = std::floor(semitones / 12.0f + 0.5f) * 12.0f;
    const float speed = quantize == Quantize::Free
                            ? magnitude : std::pow(2.0f, semitones / 12.0f);
    return direction * Clamp(speed, 0.25f, 4.0f);
}

float QuantizedRate(const Controls& c)
{
    return RateFromKnob(c.time, c.quantize, c.option);
}

float Mode3HeadRate(float knob, Quantize quantize, Option option)
{
    // Retain the established control landmarks: stop at noon and about 1x at
    // 1:30. Raising the original magnitude to 1.5 keeps unity fixed while
    // extending the endpoints to 1/8x..8x (-3 through +3 octaves).
    const float raw_rate = (knob - 0.5f) * 8.0f;
    float direction = raw_rate < 0.0f ? -1.0f : 1.0f;
    if(option == Option::Reverse) direction = -1.0f;
    else if(option == Option::Forward) direction = 1.0f;

    const float original_magnitude = std::fabs(raw_rate);
    if(original_magnitude < 0.015f) return 0.0f;
    const float magnitude = original_magnitude * std::sqrt(original_magnitude);
    float semitones = 12.0f * (std::log(magnitude) / std::log(2.0f));
    if(quantize == Quantize::Semitone)
        semitones = std::floor(semitones + 0.5f);
    else if(quantize == Quantize::Octave)
        semitones = std::floor(semitones / 12.0f + 0.5f) * 12.0f;
    const float speed = quantize == Quantize::Free
                            ? magnitude : std::pow(2.0f, semitones / 12.0f);
    return direction * Clamp(speed, 0.125f, 8.0f);
}

size_t LengthSamples(float length, float minimum_seconds, float maximum_seconds)
{
    const float seconds = minimum_seconds
                          * std::pow(maximum_seconds / minimum_seconds, length);
    return static_cast<size_t>(Clamp(seconds * kSampleRate,
                                     static_cast<float>(kMinPhrase),
                                     static_cast<float>(kMaxSamples)));
}

size_t SteppedTapeLength(float normalized)
{
    // LEN B moves through 31.25 ms * 2^n: 31, 62, 125, 250, 500 ms,
    // then 1, 2, 4 and 8 seconds. The hard jumps are part of the instrument.
    const int step = static_cast<int>(Clamp(normalized, 0.0f, 0.9999f) * 9.0f);
    return static_cast<size_t>(0.03125f * kSampleRate
                               * static_cast<float>(1u << step));
}

float LoFiQuantize(float x)
{
    // Roughly 11-bit audio after saturation: audible texture without turning
    // quiet passages into a harsh bitcrusher.
    return std::floor(Clamp(x, -1.0f, 1.0f) * 1024.0f + 0.5f) * (1.0f / 1024.0f);
}

void ResetHeads()
{
    tape_position = 0.0f;
    tape_initialized = false;
    tape_filter_state = 0.0f;
    slice_position = 0.0f;
    slice_start = 0.0f;
    scatter_heads[0] = {0.0f, 1.0f};
    scatter_heads[1] = {phrase_samples * 0.333f, 1.0f};
    scatter_heads[2] = {phrase_samples * 0.667f, 1.0f};
    activity_samples = static_cast<int32_t>(0.03f * kSampleRate);
}

void ResetSliceAutomation()
{
    slice_record_override = false;
    slice_auto_capture = false;
    slice_auto_countdown = -1;
}

void ClearMemory()
{
    phrase_samples = 0;
    capture_position = 0;
    write_position = 0;
    phrase_ready = false;
    phrase_generation = 0;
    capturing = false;
    tape_valid_samples = 0;
    previous_tape_length = 0;
    ResetSliceAutomation();
    ResetHeads();
}

void BeginCapture()
{
    capture_position = 0;
    phrase_samples = 0;
    phrase_ready = false;
    phrase_generation = 0;
    capturing = true;
    ResetHeads();
}

void EndCapture()
{
    capturing = false;
#ifdef RAINBOW_DEMONS_DIAGNOSTIC_NO_SDRAM_WRITE
    // The diagnostic deliberately leaves SDRAM untouched. Do not declare an
    // unwritten phrase playable when Record is released.
    phrase_samples = 0;
    phrase_ready = false;
    ResetHeads();
#else
    if(capture_position >= kMinPhrase)
    {
        phrase_samples = capture_position;
        phrase_generation = mode_generation;
        phrase_ready = true;
        ResetHeads();
    }
#endif
}

void OnModeChanged(Mode next)
{
    ++mode_generation;
    if(mode_generation == 0) mode_generation = 1;
    current_mode = next;
    // Each mode starts as a separate instrument with an empty buffer. This
    // prevents a Mode 2 phrase or Mode 3 loop leaking into the next mode.
    ClearMemory();
}

float SliceAutoAmount(float feedback)
{
    return Clamp((feedback - kSliceAutoDeadZone)
                     / (0.985f - kSliceAutoDeadZone),
                 0.0f,
                 1.0f);
}

int32_t SliceAutoWaitSamples(float feedback)
{
    const float amount = SliceAutoAmount(feedback);
    // Mean idle time falls exponentially from roughly 12 seconds to 0.35
    // seconds. Randomizing around that mean keeps the captures asynchronous.
    const float mean_seconds = 12.0f * std::pow(0.35f / 12.0f, amount);
    const float seconds = mean_seconds * (0.55f + 0.90f * RandomUnit());
    return static_cast<int32_t>(seconds * kSampleRate);
}

int32_t SliceAutoWindowSamples(float feedback)
{
    // FEEDBACK is a density control: clockwise means both less idle time and
    // shorter fragments. Each target duration is randomized by +/-50%.
    const float amount = SliceAutoAmount(feedback);
    const float center_seconds = 2.5f * std::pow(0.12f / 2.5f, amount);
    const float seconds = Clamp(center_seconds * (0.5f + RandomUnit()),
                                0.06f,
                                3.75f);
    return static_cast<int32_t>(seconds * kSampleRate);
}

void ProcessSliceAutomation(const Controls& c, size_t block_size)
{
    if(c.feedback <= kSliceAutoDeadZone || slice_record_override)
    {
        if(slice_auto_capture && capturing) EndCapture();
        slice_auto_capture = false;
        slice_auto_countdown = -1;
        return;
    }

    if(slice_auto_countdown < 0)
        slice_auto_countdown = SliceAutoWaitSamples(c.feedback);
    slice_auto_countdown -= static_cast<int32_t>(block_size);
    if(slice_auto_countdown > 0) return;

    if(slice_auto_capture)
    {
        // ProcessSlice may already have ended the capture at its four-second
        // safety limit; EndCapture is only needed for the normal random end.
        if(capturing) EndCapture();
        slice_auto_capture = false;
        slice_auto_countdown = SliceAutoWaitSamples(c.feedback);
    }
    else
    {
        BeginCapture();
        slice_auto_capture = true;
        slice_auto_countdown = SliceAutoWindowSamples(c.feedback);
    }
}

float ProcessTape(float input, const Controls& c)
{
    const size_t delay_length = SteppedTapeLength(c.length);
    float rate = QuantizedRate(c);

    if(!tape_initialized || previous_tape_length != delay_length)
    {
        write_position %= delay_length;
        tape_position = static_cast<float>((write_position + 1) % delay_length);
        previous_tape_length = delay_length;
        tape_initialized = true;
    }

    // A freely moving read head produces the characteristic pitch/reverse delay.
    float wet = tape_valid_samples >= delay_length
                    ? ReadLoopCrossfaded(tape_position, 0.0f,
                                        static_cast<float>(delay_length), delay_length)
                    : 0.0f;

    // Fixed, very slow speed wander and a one-pole bandwidth limit supply the
    // imperfect converter/tape feel without sacrificing pitch tracking.
    if(++tape_wow_counter >= 2400)
    {
        tape_wow_counter = 0;
        tape_wow_target = (RandomUnit() * 2.0f - 1.0f) * 0.012f;
    }
    tape_wow += (tape_wow_target - tape_wow) * 0.0008f;
    rate += tape_wow;

    const float cutoff = 0.015f + 0.42f * c.q * c.q;
    tape_filter_state += cutoff * (wet - tape_filter_state);
    wet = LoFiQuantize(tape_filter_state);
    buffer[write_position] = LoFiQuantize(
        SoftClip(input * 1.15f + wet * c.feedback * 1.35f));
    write_position = (write_position + 1) % delay_length;
    if(tape_valid_samples < delay_length) ++tape_valid_samples;

    tape_position = Wrap(tape_position + rate, static_cast<float>(delay_length));
    return wet;
}

float ProcessSlice(float input, const Controls& c)
{
    if(capturing)
    {
        const size_t limit = static_cast<size_t>(4.0f * kSampleRate);
        if(capture_position < limit) RAINBOW_DEMONS_CAPTURE_WRITE(LoFiQuantize(SoftClip(input)));
        if(capture_position >= limit) EndCapture();
        return input;
    }
    if(!phrase_ready || phrase_generation != mode_generation) return 0.0f;

    const size_t requested = LengthSamples(c.length, 0.010f, 4.0f);
    const float slice_length = static_cast<float>(requested < phrase_samples
                                                    ? requested : phrase_samples);
    const float rate = QuantizedRate(c);
    const float wet = ReadLoopCrossfaded(slice_position, slice_start,
                                         slice_length, phrase_samples);
    slice_position += rate;
    if(slice_position >= slice_length || slice_position < 0.0f)
    {
        slice_position = rate < 0.0f ? slice_length - 1.0f : 0.0f;
        const float available = static_cast<float>(phrase_samples) - slice_length;
        // Q also raises the probability/range of asynchronous random jumps.
        if(RandomUnit() < (0.12f + 0.85f * c.q))
            slice_start = RandomUnit() * (available > 0.0f ? available : 0.0f);
        activity_samples = static_cast<int32_t>(0.02f * kSampleRate);
    }
    return wet;
}

float ProcessScatter(float input, const Controls& c)
{
    if(capturing)
    {
        const size_t limit = static_cast<size_t>(8.0f * kSampleRate);
        if(capture_position < limit) RAINBOW_DEMONS_CAPTURE_WRITE(LoFiQuantize(SoftClip(input)));
        if(capture_position >= limit) EndCapture();
        return input;
    }
    if(!phrase_ready || phrase_generation != mode_generation) return 0.0f;

    const int heads = 1 + static_cast<int>(Clamp(c.length, 0.0f, 0.9999f) * 3.0f);
    const float loop_length = static_cast<float>(phrase_samples);
    const float rates[3] = {
        Mode3HeadRate(c.time, c.quantize, c.option),
        Mode3HeadRate(c.head2, c.quantize, c.option),
        Mode3HeadRate(c.q, c.quantize, c.option)};
    float wet = 0.0f;
    for(int h = 0; h < heads; ++h)
    {
        wet += ReadLoopCrossfaded(scatter_heads[h].position, 0.0f,
                                  loop_length, phrase_samples);
        const float rate = rates[h] * scatter_heads[h].rate;
        scatter_heads[h].position = Wrap(scatter_heads[h].position + rate, loop_length);

        // Quantized modes occasionally produce musical random steps. Free mode
        // stays fully manual and behaves like a straightforward multi-head tape loop.
        if(c.quantize != Quantize::Free
           && RandomUnit() < (0.0000015f + 0.0000015f * static_cast<float>(heads)))
        {
            const int step = static_cast<int>(RandomUnit() * 9.0f) - 4;
            scatter_heads[h].rate = std::pow(2.0f, step / 12.0f);
            scatter_heads[h].position = RandomUnit() * loop_length;
            activity_samples = static_cast<int32_t>(0.02f * kSampleRate);
        }
    }
    return wet / static_cast<float>(heads);
}

void AudioCallback(AudioHandle::InputBuffer in,
                   AudioHandle::OutputBuffer out,
                   size_t size)
{
    patch.ProcessAllControls();
    record_button.Debounce();
    reset_button.Debounce();
    const Controls c = ReadControls();

    if(c.mode != current_mode) OnModeChanged(c.mode);

    const bool record_pressed = record_button.Pressed();
    const bool record_trigger = patch.gate_in_1.Trig();
    if(c.mode != Mode::Tape)
    {
        // The panel button retains hold-to-record behavior.
        if(record_pressed && !previous_record_pressed)
        {
            if(c.mode == Mode::Slice)
            {
                slice_record_override = true;
                slice_auto_capture = false;
                slice_auto_countdown = -1;
            }
            BeginCapture();
        }
        if(!record_pressed && previous_record_pressed && capturing) EndCapture();

        // REC CV is clock-friendly: successive rising edges alternate between
        // starting a fresh capture and stopping it for immediate playback.
        // Ignore trigger edges while the physical button is held so the two
        // control methods cannot fight over the capture state.
        if(record_trigger && !record_pressed)
        {
            bool start_fresh = false;
            if(c.mode == Mode::Slice)
            {
                // A Patch SM gate input cannot sense an inserted cable at 0 V.
                // The first received edge therefore latches external priority
                // until Reset is pressed or the mode is changed.
                start_fresh = !slice_record_override;
                slice_record_override = true;
                slice_auto_capture = false;
                slice_auto_countdown = -1;
            }
            if(start_fresh) BeginCapture();
            else if(capturing) EndCapture();
            else BeginCapture();
        }

        if(c.mode == Mode::Slice && !record_pressed)
            ProcessSliceAutomation(c, size);
    }
    previous_record_pressed = record_pressed;

    const bool reset_trigger = patch.gate_in_2.Trig();
    if(reset_button.RisingEdge() || reset_trigger)
    {
        if(c.mode == Mode::Slice && slice_auto_capture && capturing)
            EndCapture();
        ResetHeads();
        if(c.mode == Mode::Slice) ResetSliceAutomation();
    }
    if(reset_button.Pressed() && reset_button.TimeHeldMs() >= kResetHoldMs)
    {
        if(!reset_hold_latched)
        {
            ClearMemory();
            reset_hold_latched = true;
        }
    }
    else if(!reset_button.Pressed()) reset_hold_latched = false;

    for(size_t i = 0; i < size; ++i)
    {
        const float input = Clamp(IN_L[i], -2.0f, 2.0f);
        float wet = 0.0f;
        if(c.mode == Mode::Tape) wet = ProcessTape(input, c);
        else if(c.mode == Mode::Slice) wet = ProcessSlice(input, c);
        else wet = ProcessScatter(input, c);

        float y;
        if(capturing)
            y = input; // transparent live monitoring while recording a phrase
        else if(c.mix <= 0.0f)
            y = input; // true digital dry: no wet leakage and no DSP waveshaping
        else if(c.mix >= 1.0f)
            y = SoftClip(wet); // true digital wet: no direct-signal leakage
        else
            y = SoftClip(input * (1.0f - c.mix) + wet * c.mix);
        OUT_L[i] = y;
        OUT_R[i] = y;
        if(activity_samples > 0) --activity_samples;
    }

    record_led.Write(capturing);
    status_led.Write((c.mode == Mode::Tape || phrase_ready) && activity_samples <= 0);
    patch.SetLed(c.mode == Mode::Tape || phrase_ready);
}
} // namespace

int main(void)
{
    patch.Init();
    patch.SetAudioSampleRate(kSampleRate);
    patch.SetAudioBlockSize(16);

    // These pins exactly match the already-built carrier and existing guide.
    record_button.Init(DaisyPatchSM::D1);
    reset_button.Init(DaisyPatchSM::D2);
    mode_switch.Init(DaisyPatchSM::D7, DaisyPatchSM::D10);
    option_switch.Init(DaisyPatchSM::D3, DaisyPatchSM::D4);
    quantize_switch.Init(DaisyPatchSM::D5, DaisyPatchSM::D6);
    record_led.Init(DaisyPatchSM::B8, GPIO::Mode::OUTPUT);
    status_led.Init(DaisyPatchSM::B7, GPIO::Mode::OUTPUT);
    record_led.Write(false);
    status_led.Write(false);
    patch.SetLed(false);
    ClearMemory();
    patch.StartAudio(AudioCallback);
    while(true) {}
}
