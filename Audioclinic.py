# ==========================================
# Final Project: Ansh's Digital Audio Clinic
# ==========================================
# A GUI-based hearing test simulation. 
# Disclaimer: Educational purposes only!

import tkinter as tk
import numpy as np
import sounddevice as sd

# Decided to wrap everything in a class. Tried using standard functions at first, 
# but passing the score and window frame around got way too messy with global variables.
class AudioClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ansh's Digital Audio Clinic")
        self.root.geometry("850x650")
        self.root.minsize(800, 600) # prevent it from squishing too small
        
        # --- Color Theme ---
        # Using a custom colorblind-friendly dark theme I found online (Okabe-Ito style)
        # so the red/green buttons don't blend together for colorblind users.
        self.app_bg = "#0f172a"      
        self.card_bg = "#1e293b"     
        self.text_main = "#f8fafc"   
        self.text_muted = "#cbd5e1"  
        self.title_color = "#38bdf8" 
        
        self.btn_neutral = "#38bdf8" # Sky Blue
        self.btn_neutral_h = "#0ea5e9" # Hover state
        
        self.btn_yes = "#2dd4bf"     # Teal (replaces green)
        self.btn_yes_h = "#14b8a6"
        
        self.btn_no = "#fb923c"      # Orange (replaces red)
        self.btn_no_h = "#f97316"
        
        self.root.configure(bg=self.app_bg)
        
        # keep track of user's points
        self.score = 0
        self.progress_width = 0
        
        # Top progress bar setup
        self.prog_canvas = tk.Canvas(self.root, width=850, height=15, bg=self.app_bg, highlightthickness=0)
        self.prog_canvas.pack(side="top", fill="x")
        self.prog_bar = self.prog_canvas.create_rectangle(0, 0, 0, 15, fill=self.btn_yes, outline="")
        
        # Outer Container
        self.container = tk.Frame(self.root, bg=self.app_bg)
        self.container.pack(expand=True, fill="both")
        
        # Inner white/gray card to make it look like a modern app
        self.content = tk.Frame(self.container, bg=self.card_bg)
        self.content.pack(expand=True, fill="both", padx=60, pady=50)
        
        # boot up the first screen
        self.show_welcome()

    # --- Utility Functions ---
    
    def clear_screen(self):
        # Destroys all widgets in the content frame so we have a blank slate for the next screen
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_progress(self, percentage):
        # Calculate how many pixels wide the bar should be based on window size
        target_width = (percentage / 100) * self.root.winfo_width()
        if target_width == 0:  # fallback bug fix: window width is 0 before it fully loads
            target_width = (percentage / 100) * 850
        self._animate_bar(self.progress_width, target_width)

    def _animate_bar(self, current, target):
        # smoothly moves the bar instead of snapping instantly
        if current < target:
            current += 10
            if current > target:
                current = target
            self.progress_width = current
            self.prog_canvas.coords(self.prog_bar, 0, 0, current, 15)
            self.root.after(10, self._animate_bar, current, target)

    def play_tone(self, frequency, duration, volume=0.5, ear="both"):
        # Note: I originally wanted to play mp3 files, but realized standard audio libraries 
        # were crashing or complex. I asked Gemini how to synthesize audio natively in Python 
        # and it gave me this math approach using numpy to generate a sine wave. 
        # Basically, we map out the wave mathematically and send the array to sounddevice!
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = volume * np.sin(2 * np.pi * frequency * t)
        
        # Pan the audio to specific ears
        if ear == "left":
            stereo_wave = np.column_stack((wave, np.zeros_like(wave)))
        elif ear == "right":
            stereo_wave = np.column_stack((np.zeros_like(wave), wave))
        else:
            stereo_wave = np.column_stack((wave, wave))
            
        sd.play(stereo_wave, sample_rate)
        sd.wait() # wait for sound to finish before moving on

    def create_flat_button(self, parent, text, default_color, hover_color, command, width=15):
        # Note: Standard Tkinter buttons looked completely broken on Mac because Apple forces 
        # its own pill-shaped gray styles and ignores background colors. I used Gemini to help 
        # me write this custom function. It uses a clickable Label widget to fake a button, 
        # allowing me to keep my custom flat colors and add hover animations.
        btn = tk.Label(parent, text=text, bg=default_color, fg="#0f172a", font=("Arial", 16, "bold"), width=width, pady=10, cursor="hand2")
        
        def on_enter(e):
            btn['background'] = hover_color
        def on_leave(e):
            btn['background'] = default_color
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda event: command()) # triggers the actual click action
        
        return btn

    # --- UI Screens ---
    
    def show_welcome(self):
        self.clear_screen()
        self.set_progress(0)
        
        # using wraplength=650 so text doesn't cut off on smaller monitors
        tk.Label(self.content, text="Welcome to Ansh's Digital Audio Clinic!", font=("Arial", 28, "bold"), bg=self.card_bg, fg=self.title_color, wraplength=650, justify="center").pack(pady=(60, 20))
        tk.Label(self.content, text="Disclaimer: This program is built for Educational and Reference Purposes. Do not compare its results to a Professional Alternative.", font=("Arial", 16), bg=self.card_bg, fg=self.text_muted, wraplength=650, justify="center").pack(pady=10)
        
        self.create_flat_button(self.content, "Start Clinic", self.btn_neutral, self.btn_neutral_h, self.question_1).pack(pady=60)

    def question_1(self):
        self.clear_screen()
        self.set_progress(10)
        
        tk.Label(self.content, text="Question 1:", font=("Arial", 20, "bold"), bg=self.card_bg, fg=self.title_color).pack(pady=(60, 10))
        tk.Label(self.content, text="Do you have a ringing or buzzing sound in your ear(s)?", font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=650, justify="center").pack(pady=20)
        
        btn_frame = tk.Frame(self.content, bg=self.card_bg)
        btn_frame.pack(pady=40)
        self.create_flat_button(btn_frame, "Yes", self.btn_yes, self.btn_yes_h, lambda: self.q1_response("Y"), width=10).pack(side="left", padx=20)
        self.create_flat_button(btn_frame, "No", self.btn_no, self.btn_no_h, lambda: self.q1_response("N"), width=10).pack(side="right", padx=20)

    def q1_response(self, ans):
        self.clear_screen()
        if ans == "Y":
            msg = "Got it. This may or may not be a symptom of hearing loss."
        else:
            msg = "Good. But often times subtle or gradual hearing loss does not trigger tinnitus."
            
        tk.Label(self.content, text=msg, font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=600, justify="center").pack(pady=80)
        self.create_flat_button(self.content, "Continue", self.btn_neutral, self.btn_neutral_h, self.question_2).pack(pady=20)

    def question_2(self):
        self.clear_screen()
        self.set_progress(20)
        
        tk.Label(self.content, text="Question 2:", font=("Arial", 20, "bold"), bg=self.card_bg, fg=self.title_color).pack(pady=(40, 10))
        q2_text = "Do you have trouble hearing? (e.g., feeling like you're under water, asking people to repeat themselves, or needing to increase the volume on devices)"
        tk.Label(self.content, text=q2_text, font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=650, justify="center").pack(pady=20)
        
        btn_frame = tk.Frame(self.content, bg=self.card_bg)
        btn_frame.pack(pady=30)
        self.create_flat_button(btn_frame, "Yes", self.btn_yes, self.btn_yes_h, lambda: self.q2_response("Y"), width=10).pack(side="left", padx=20)
        self.create_flat_button(btn_frame, "No", self.btn_no, self.btn_no_h, lambda: self.q2_response("N"), width=10).pack(side="right", padx=20)

    def q2_response(self, ans):
        self.clear_screen()
        if ans == "Y":
            tk.Label(self.content, text="Noted. Let's head to the audio test.", font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=600, justify="center").pack(pady=80)
            self.create_flat_button(self.content, "Continue", self.btn_neutral, self.btn_neutral_h, self.setup_test).pack(pady=20)
        else:
            tk.Label(self.content, text="Excellent! If you don't have trouble hearing, chances are low, but follow earphone discipline. Cheers!!", font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=650, justify="center").pack(pady=40)
            tk.Label(self.content, text="Do you still want to proceed to the test?", font=("Arial", 18, "bold"), bg=self.card_bg, fg=self.title_color).pack(pady=20)
            
            btn_frame = tk.Frame(self.content, bg=self.card_bg)
            btn_frame.pack(pady=20)
            self.create_flat_button(btn_frame, "Yes", self.btn_yes, self.btn_yes_h, self.setup_test, width=10).pack(side="left", padx=20)
            self.create_flat_button(btn_frame, "No", self.btn_no, self.btn_no_h, self.root.quit, width=10).pack(side="right", padx=20)

    def setup_test(self):
        self.clear_screen()
        self.set_progress(30)
        
        tk.Label(self.content, text="Loading Test.......", font=("Arial", 22, "bold"), bg=self.card_bg, fg=self.title_color).pack(pady=20)
        
        inst = ("Get ready for the test. Start Note:\n\n"
                "1. Be in somewhere silent.\n"
                "2. Connect headphones/earphones with noise isolation.\n"
                "3. Optional: Turn on Active Noise Cancellation if available.")
        
        tk.Label(self.content, text=inst, font=("Arial", 16), bg=self.card_bg, fg=self.text_main, justify="left", wraplength=600).pack(pady=20)
        
        btn_frame = tk.Frame(self.content, bg=self.card_bg)
        btn_frame.pack(pady=40)
        self.create_flat_button(btn_frame, "I'm Ready", self.btn_yes, self.btn_yes_h, lambda: self.run_audio_test(1), width=15).pack(side="left", padx=10)
        self.create_flat_button(btn_frame, "Need a minute", self.btn_no, self.btn_no_h, self.wait_minute, width=15).pack(side="right", padx=10)

    def wait_minute(self):
        # simple holding screen if they need time to plug in headphones
        self.clear_screen()
        tk.Label(self.content, text="Waiting...\nSet up your audio and click Continue when ready.", font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=600, justify="center").pack(pady=80)
        self.create_flat_button(self.content, "Continue", self.btn_neutral, self.btn_neutral_h, lambda: self.run_audio_test(1)).pack(pady=20)

    # --- Core Audio Testing Loop ---

    def run_audio_test(self, test_num, boosted=False):
        self.clear_screen()
        
        # Put all the tests in a list of tuples so I don't have to copy/paste the UI code 6 times.
        # This matches how real audiograms check both ears independently.
        test_sequence = [
            (1000, "left", "Test 1: 1000Hz (Left Ear)"),
            (1000, "right", "Test 2: 1000Hz (Right Ear)"),
            (4000, "left", "Test 3: 4000Hz (Left Ear)"),
            (4000, "right", "Test 4: 4000Hz (Right Ear)"),
            (8000, "left", "Test 5: 8000Hz (Left Ear)"),
            (8000, "right", "Test 6: 8000Hz (Right Ear)")
        ]
        
        # if we pass the length of the list, move to results!
        if test_num > len(test_sequence):
            self.show_results()
            return
            
        freq, ear, title = test_sequence[test_num - 1]
        
        # math to fill the remaining 70% of the progress bar
        current_progress = 30 + (test_num * 10)
        self.set_progress(current_progress)
            
        vol = 1.0 if boosted else 0.1
        vol_text = "Boosting the level..." if boosted else f"Now playing {freq}Hz in {ear.capitalize()} ear."

        tk.Label(self.content, text=title, font=("Arial", 22, "bold"), bg=self.card_bg, fg=self.title_color).pack(pady=30)
        tk.Label(self.content, text=vol_text, font=("Arial", 18), bg=self.card_bg, fg=self.text_main, wraplength=600, justify="center").pack(pady=10)
        
        self.create_flat_button(self.content, "🔊 Play Sound", self.btn_neutral, self.btn_neutral_h, lambda: self.play_tone(freq, 2.0, vol, ear)).pack(pady=30)
        
        tk.Label(self.content, text="Do you hear it?", font=("Arial", 18, "bold"), bg=self.card_bg, fg=self.text_main).pack(pady=10)
        
        btn_frame = tk.Frame(self.content, bg=self.card_bg)
        btn_frame.pack(pady=10)
        self.create_flat_button(btn_frame, "Yes", self.btn_yes, self.btn_yes_h, lambda: self.test_response(test_num, boosted, "Y"), width=10).pack(side="left", padx=20)
        self.create_flat_button(btn_frame, "No", self.btn_no, self.btn_no_h, lambda: self.test_response(test_num, boosted, "N"), width=10).pack(side="right", padx=20)

    def test_response(self, test_num, boosted, ans):
        if ans == "Y":
            # get full point for hearing it, half point if we had to boost it
            self.score += 0.5 if boosted else 1.0
            self.run_audio_test(test_num + 1)
        else:
            if not boosted:
                # try again with high volume
                self.run_audio_test(test_num, boosted=True)
            else:
                # missed it completely, move on
                self.run_audio_test(test_num + 1)

    # --- Final Results ---
    
    def show_results(self):
        self.clear_screen()
        self.set_progress(100)
        
        tk.Label(self.content, text="Test Results", font=("Arial", 26, "bold"), bg=self.card_bg, fg=self.title_color).pack(pady=(40, 20))
        
        # Max score is 6 since we test 3 frequencies across 2 ears
        if self.score == 6:
            res = "Your hearing seems to be in fantastic shape! Keep up the good earphone discipline. Cheers!!"
            res_color = self.btn_yes
        elif self.score >= 4:
            res = "Your hearing is decent, but you might be missing some subtle frequencies. Remember to keep your volume at safe levels."
            res_color = "#fcd34d" # warm yellow for contrast against the dark background
        else:
            res = "You missed several frequencies during the test. Since this is just an educational tool, you might want to visit a real audiologist!"
            res_color = self.btn_no # use the orange/red failure color
            
        tk.Label(self.content, text=res, font=("Arial", 18, "bold"), bg=self.card_bg, fg=res_color, wraplength=650, justify="center").pack(pady=30)
        
        tk.Label(self.content, text="Thank you for visiting Ansh's Digital Audio Clinic!", font=("Arial", 16, "italic"), bg=self.card_bg, fg=self.text_muted, wraplength=600, justify="center").pack(pady=30)
        
        self.create_flat_button(self.content, "Finish & Exit", self.btn_neutral, self.btn_neutral_h, self.root.quit).pack(pady=20)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioClinicApp(root)
    root.mainloop()