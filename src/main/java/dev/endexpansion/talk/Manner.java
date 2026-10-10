package dev.endexpansion.talk;

import java.util.Locale;

/**
 * How someone behaves while you talk to them, from their personality (see {@link StoryBook}).
 * Most stand still for as long as you like; some can't, by nature or by station.
 */
public enum Manner {
    /** Stands still for as long as you like. */
    STEADY,
    /** Keeps a step of distance and backs off if you crowd them. */
    SHY,
    /** Paces a step or two while talking, but stays. */
    RESTLESS,
    /** After a while excuses themselves and goes back to what they were doing (not with close friends). */
    BUSY,
    /** Chorrin: blinks a short hop now and then while talking, and carries on from there. */
    FLIGHTY,
    /** The Court: ends the audience after a while unless your Favor is high enough. */
    PROUD;

    public static Manner of(String id) {
        try {
            return valueOf(id.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException e) {
            return STEADY;
        }
    }
}
