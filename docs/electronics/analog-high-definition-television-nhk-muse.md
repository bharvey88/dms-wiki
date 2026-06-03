# Analog High-Definition Television : NHK MUSE

!!! note "Source"
    Mirrored from [Analog High-Definition Television : NHK MUSE](https://dallasmakerspace.org/wiki/Analog_High-Definition_Television_:_NHK_MUSE) on the Dallas Makerspace wiki (CC BY-SA 3.0).

Presented as two sessions, first a lecture, then a demonstration of the MUSE system using a Hi-Vision LaserDisc source.

## Slides for Lecture Session

- [![](https://dallasmakerspace.org/w/images/thumb/4/45/MUSE_00_intro.png/120px-MUSE_00_intro.png)](https://dallasmakerspace.org/wiki/File:MUSE_00_intro.png)

  Title Card

- [![](https://dallasmakerspace.org/w/images/thumb/5/56/MUSE_01_whatis.png/120px-MUSE_01_whatis.png)](https://dallasmakerspace.org/wiki/File:MUSE_01_whatis.png)

  Just what are we talking about here, anyway?

- [![](https://dallasmakerspace.org/w/images/thumb/5/54/MUSE_02_screen_formats.png/120px-MUSE_02_screen_formats.png)](https://dallasmakerspace.org/wiki/File:MUSE_02_screen_formats.png)

  The blue rectangle represents NTSC television, 483 visible lines with 4:3 aspect ratio ; the green represents Hi-Vision, 1035 visible lines, 16:9, with the dark green areas being parts of the Hi-Vision picture which are not transmitted in the MUSE system.

- [![](https://dallasmakerspace.org/w/images/thumb/d/de/MUSE_03_fundamentals.png/120px-MUSE_03_fundamentals.png)](https://dallasmakerspace.org/wiki/File:MUSE_03_fundamentals.png)

  What is television supposed to do, anyway, and how does Hi-Vision achieve it better than NTSC does?

- [![](https://dallasmakerspace.org/w/images/thumb/a/a6/MUSE_04_raster.png/120px-MUSE_04_raster.png)](https://dallasmakerspace.org/wiki/File:MUSE_04_raster.png)

  Since there is no practicable way of transmitting the value of every point in the picture all at once, the points are sampled successively over the course of one frame period. Until recently, the most common way of doing this was to trace an electron beam across a light-sensitive or light-emitting screen, using electric or magnetic fields. By precise control of timing, the image as seen at the receiver is a good duplicate of that at the transmitter.

- [![](https://dallasmakerspace.org/w/images/thumb/4/4b/MUSE_05_interlace.png/120px-MUSE_05_interlace.png)](https://dallasmakerspace.org/wiki/File:MUSE_05_interlace.png)

  Because the eye is more sensitive to flicker than to motion, the picture only needs to be scanned about 24 times each second, but dividing it into two interdigitated sets of lines scanned in succession 48 or more times a second reduces the sensation of flicker to tolerable levels.

- [![](https://dallasmakerspace.org/w/images/thumb/7/79/MUSE_06_color_rgb.png/120px-MUSE_06_color_rgb.png)](https://dallasmakerspace.org/wiki/File:MUSE_06_color_rgb.png)

  Any full-colour image can be adequately represented by a combination of three primary-colour images, red, green, and blue.

- [![](https://dallasmakerspace.org/w/images/thumb/a/a9/MUSE_07_color_ypbpr.png/120px-MUSE_07_color_ypbpr.png)](https://dallasmakerspace.org/wiki/File:MUSE_07_color_ypbpr.png)

  For efficiency in transmission, a colour image can be separated into a monochrome image and two colour difference images, weighted sums of the primary colour images which correlate less. The colour differences can then be transmitted at reduced resolution, as the eye is less sensitive to colour detail than brightness detail.

- [![](https://dallasmakerspace.org/w/images/thumb/d/d2/MUSE_08_spectrum.png/120px-MUSE_08_spectrum.png)](https://dallasmakerspace.org/wiki/File:MUSE_08_spectrum.png)

  The raster scan structure causes the energy in the video signal to cluster at integer multiples of the line frequency, and around those multiples at integer multiples of the field frequency.

- [![](https://dallasmakerspace.org/w/images/thumb/5/53/MUSE_09_chronology.png/120px-MUSE_09_chronology.png)](https://dallasmakerspace.org/wiki/File:MUSE_09_chronology.png)

  The meaning of "high definition television" has changed over time.

- [![](https://dallasmakerspace.org/w/images/thumb/3/3a/MUSE_10_signal_format.png/120px-MUSE_10_signal_format.png)](https://dallasmakerspace.org/wiki/File:MUSE_10_signal_format.png)

  The transmitted signal, after MUSE processing, is very clearly a video signal, but one which has been "mangled". Green represents the vertical synchronizing signal, black the horizontal synchronizing signal, orange the digital audio signal, yellow the luminance video signal, and red and blue the colour-difference video signals.

- [![](https://dallasmakerspace.org/w/images/thumb/d/db/MUSE_11_block_diagram.png/120px-MUSE_11_block_diagram.png)](https://dallasmakerspace.org/wiki/File:MUSE_11_block_diagram.png)

  The MUSE encoder is quite complicated.

- [![](https://dallasmakerspace.org/w/images/thumb/9/9c/MUSE_12_interframe_subsampling.png/120px-MUSE_12_interframe_subsampling.png)](https://dallasmakerspace.org/wiki/File:MUSE_12_interframe_subsampling.png)

  Elements marked "A" are transmitted in the first frame, elements marked "B" in the second frame, in a "dot interlacing" process. In stationary picture areas, this is a lossless process.

- [![MUSE 13 interframe subsampling A.png](https://dallasmakerspace.org/w/images/thumb/9/9d/MUSE_13_interframe_subsampling_A.png/120px-MUSE_13_interframe_subsampling_A.png)](https://dallasmakerspace.org/wiki/File:MUSE_13_interframe_subsampling_A.png)

- [![MUSE 14 interframe subsampling B.png](https://dallasmakerspace.org/w/images/thumb/2/22/MUSE_14_interframe_subsampling_B.png/120px-MUSE_14_interframe_subsampling_B.png)](https://dallasmakerspace.org/wiki/File:MUSE_14_interframe_subsampling_B.png)

- [![](https://dallasmakerspace.org/w/images/thumb/6/66/MUSE_15_still_image.png/120px-MUSE_15_still_image.png)](https://dallasmakerspace.org/wiki/File:MUSE_15_still_image.png)

  Transformation of original luminance signal into transmitted (bandwidth-reduced) luminance signal in still-image areas.

- [![](https://dallasmakerspace.org/w/images/thumb/9/9e/MUSE_16_moving_image.png/120px-MUSE_16_moving_image.png)](https://dallasmakerspace.org/wiki/File:MUSE_16_moving_image.png)

  Processing in moving-image areas, relying on intraframe subsampling.

- [![](https://dallasmakerspace.org/w/images/thumb/5/5d/MUSE_17_audio.png/120px-MUSE_17_audio.png)](https://dallasmakerspace.org/wiki/File:MUSE_17_audio.png)

  MUSE supports two digital audio formats, using an unsophisticated type of bitrate reduction, for a total of four possible audio channels.

- [![](https://dallasmakerspace.org/w/images/thumb/4/4d/MUSE_18_frequencies.png/120px-MUSE_18_frequencies.png)](https://dallasmakerspace.org/wiki/File:MUSE_18_frequencies.png)

  MUSE has been transmitted by satellite, using a wide frequency deviation and low carrier-to-noise ratio, and recorded on optical disc, with an narrow deviation and high CNR, with roughly equivalent signal-to-noise ratio, after demodulation, in both cases.
