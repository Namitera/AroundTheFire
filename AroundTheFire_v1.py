from manim import *
import numpy as np
import soundfile as sf
import os

class AroundTheFire(Scene):
    def construct(self):

        def generate_tone(freq, duration=2.0, samplerate=44100, folder="sounds"):
            os.makedirs(folder, exist_ok=True)
            t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
            wave = 0.5 * np.sin(2 * np.pi * freq * t)
            filename = os.path.join(folder, f"{(freq)}Hz.wav")
            sf.write(filename, wave, samplerate)
            print(f"Saved {filename}")

        # Generate a few common frequencies
        # for f in [220, 440, 880, 1000, 2000]:
        #     generate_tone(f)


        def generate_frequency_sweep(start_freq, end_freq, duration=2.0, samplerate=44100, folder="sounds", filename=None):
            os.makedirs(folder, exist_ok=True)
            t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
            # Linear interpolation of frequency
            freqs = np.linspace(start_freq, end_freq, len(t))
            # Phase integration to get waveform
            phase = 2 * np.pi * np.cumsum(freqs) / samplerate
            wave = 0.5 * np.sin(phase)

            if filename is None:
                filename = f"{int(start_freq)}to{int(end_freq)}Hz_{duration:.1f}s.wav"
            path = os.path.join(folder, filename)
            sf.write(path, wave, samplerate)
            print(f"Saved: {path}")
            return path

        # Example: 440 Hz to 880 Hz over 2 seconds
        # generate_frequency_sweep(440, 880, duration=2.0)



    

        f = ValueTracker(1)
        frequency = DecimalNumber(1.0, num_decimal_places=2)
        frequency.add_updater(lambda m: m.set_value(f.get_value()).next_to(text1, RIGHT))
        amplitude = 10


        axes = Axes(
            x_range=[-10, 10, 3],
            y_range=[-16, 16, 2],
            x_length=13.5,
            y_length=7.5,
            axis_config={"include_tip": False},
        )
        axes.center()

        noteGraph = axes.plot(lambda x: np.sin(x), color = RED)
        noteGraph.add_updater(lambda m: m.become(axes.plot(lambda x: amplitude * np.sin(f.get_value() * x), color=GREEN)))

        text1 = MathTex(r"f=")
        text1.to_corner(UP + LEFT)
        text2 = MathTex(r"Hz")
        text2.next_to(text1, RIGHT * 7)
        self.wait(frozen_frame=False)

        self.play(Write(axes), Write(text1), Write(text2), Write(frequency), Write(noteGraph))

        # generate_tone(329.63, duration=0.375)
        # self.add_sound("sounds/329.63Hz.wav", time_offset=0)
        # self.play(f.animate.set_value(329.63), run_time=0.375)

        # generate_tone(293.66, duration=0.125)
        # self.add_sound("sounds/293.66Hz.wav", time_offset=0)
        # self.play(f.animate.set_value(293.66), run_time=0.125)

        # generate_tone(329.63, duration=0.25)
        # self.add_sound("sounds/329.63Hz.wav", time_offset=0)


        # Define a list of (frequency, duration) tuples
        tones = [
            (329.63, 0.375),
            (293.66, 0.125),
            (329.63, 0.25),
            (369.99, 0.25),
            (392, 0.375),
            (369.99, 0.125),
            (392, 0.25),
            (329.63, 0.25),
            (369.99, 0.375),
            (329.63, 0.125),
            (369.99, 0.25),
            (293.66, 0.25),
            (293.66, 0.5),
            (277.18, 0.5),
            (329.63, 0.375),
            (293.66, 0.125),
            (329.63, 0.25),
            (369.99, 0.25),
            (392, 0.375),
            (369.99, 0.125),
            (392, 0.25),
            (440, 0.25),
            (493.88, 0.375),
            (440, 0.125),
            (493.88, 0.25),
            (587.33, 0.25),
            (440, 1)
            # Add more tones as needed
        ]

        for freq, dur in tones:
            generate_tone(freq, duration=dur*2)
            self.add_sound(f"sounds/{freq}Hz.wav", time_offset=0)
            # Assign a specific color to each frequency (example mapping)
            freq_colors = {
                329.63: "#16a085",
                293.66: "#1abc9c",
                369.99: "#27ae60",
                392: "#2ecc71",
                277.18: "#3498db",
                440: "#f1c40f",
                493.88: "#f39c12",
                587.33: "#e74c3c",
            }
            color = freq_colors.get(freq, WHITE)
            noteGraph.clear_updaters()
            noteGraph.add_updater(lambda m: m.become(axes.plot(lambda x: amplitude * np.sin(f.get_value() * x), color=color)))
            self.play(f.animate.set_value(freq), rate_func=rate_functions.exponential_decay, run_time=dur*2)
        
