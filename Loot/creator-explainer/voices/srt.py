# Build loot-secure-the-bag.srt from the VO placement in audio/mix.py and the phrase pauses
# measured on each line (voices/pauses.json; Higgsfield TTS returns no word timings).
import os
here = os.path.dirname(os.path.abspath(__file__))
VO = {'d01': 0.40, 'd02': 6.00, 'd03': 10.25, 'd04': 16.95, 'd05': 23.75, 'd06': 30.20, 'd07': 35.45, 'd08': 41.00, 'd09': 46.05, 'd10': 52.40}
PH = {
 'd01': [(0, 2.17, "Brands don't want perfect ads anymore."), (2.41, 3.18, "They want raw."), (3.38, 4.19, "They want real."), (4.36, 5.28, "They want you.")],
 'd02': [(0, 0.74, "This is LOOT."), (0.79, 2.42, "Brands drop paid video missions."), (2.48, 3.06, "You film them."), (3.18, 3.77, "You get paid.")],
 'd03': [(0, 1.38, "Step one: enlist."), (1.71, 2.55, "Pick a codename,"), (2.61, 4.05, "build your hunter profile,"), (4.05, 6.28, "and once we approve you, the full app unlocks.")],
 'd04': [(0, 1.65, "Step two: hit the Loot tab."), (1.9, 3.94, "Every contract shows the brand, the brief,"), (4.13, 6.4, "and a guaranteed reward, before you film a thing.")],
 'd05': [(0, 1.24, "Every brief comes loaded:"), (1.4, 4.33, "hooks, scripts, scene-by-scene shots, do's and don'ts."), (4.54, 6.12, "Just copy, and shoot.")],
 'd06': [(0, 1.17, "Tap Secure the Bag."), (1.41, 4.64, "Once the brand locks you in, the money's pre-funded and held for you.")],
 'd07': [(0, 1.68, "Step three: drop the loot."), (1.9, 5.19, "Shoot it, open the Studio, and transmit your video to the brand.")],
 'd08': [(0, 0.92, "On beginner missions,"), (0.97, 2.95, "reshoots only happen for technical glitches,"), (3.22, 4.57, "and we verify them first.")],
 'd09': [(0, 1.70, "Step four: bag secured."), (1.99, 3.85, "Approved videos get paid into your Stash,"), (4.09, 5.88, "and you withdraw straight to UPI.")],
 'd10': [(0, 1.63, "No boss. No schedule."), (1.81, 2.62, "Just the mission."), (2.67, 4.20, "Read the rules, don't get banned…"), (4.44, 5.39, "and secure the bag.")],
}
def ts(t): m = int(t // 60); s = t % 60; return f'00:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}'.replace(',1000', ',999')
cues = [(VO[k] + a, VO[k] + b + 0.12, txt) for k in VO for a, b, txt in PH[k]]
with open(os.path.join(os.path.dirname(here), 'loot-secure-the-bag.srt'), 'w') as f:
    for i, (a, b, txt) in enumerate(cues, 1):
        if i < len(cues): b = min(b, cues[i][0] - 0.02)
        f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{txt}\n\n')
print(len(cues), 'cues')
