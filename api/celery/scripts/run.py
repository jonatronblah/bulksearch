from pippi import dsp, noise
import random
from io import BytesIO


def generate():

    pluckout = dsp.win('pluckout')

    def makehat(length=dsp.MS*80):
        lowhz = dsp.win('rnd', 9000, 11000)
        highhz = dsp.win('rnd', 12000, 14000)
        return noise.bln('sine', length, lowhz, highhz).env(pluckout) * 0.5


    lfo = dsp.win('sinc', 0.1, 1) # Hat lengths between 100ms and 1s over a sinc window
    time_lfo = dsp.win('rnd', 0.07, 0.1) # Time increments between 1ms and 200ms over a sinc curve
    length = 10
    out = dsp.buffer(length=length)

    elapsed = 0
    while elapsed < length: 
        pos = elapsed / length # position in the buffer between 0 and 1
        hatlength = lfo.interp(pos) # Sample the current interpolated position in the curve to get the hat length
        hat = makehat(hatlength)
        out.dub(hat, elapsed) # Finally, we dub the hat into the output buffer at the current time
        beat = time_lfo.interp(pos)
        elapsed += beat # and move our position forward again a half second so we can do it all again!
    spooled = BytesIO()
    out.write(spooled)
    spooled.seek(0)
    return spooled

###
# write wav to a file like object and return it via task
# user uses id to trigger streaming

'''elapsed = 0
while elapsed < length: 
    pos = elapsed / length
    beat = time_lfo.interp(pos)
    elapsed += beat 
    print(beat)'''
