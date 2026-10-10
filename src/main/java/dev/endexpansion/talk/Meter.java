package dev.endexpansion.talk;

/**
 * How closeness is counted: friendship with Shulkin and Chorrin (ten chorus blossoms) or a
 * Citadel's Favor (ten eyes). Each has eleven levels, 0 to 10, reached at these points.
 */
public enum Meter {
    BLOSSOM("blossom", new int[] {0, 20, 45, 75, 110, 150, 195, 245, 300, 360, 425}),
    EYE("eye", new int[] {0, 8, 18, 30, 45, 62, 82, 105, 130, 158, 190});

    public final String id;
    private final int[] thresholds;

    Meter(String id, int[] thresholds) {
        this.id = id;
        this.thresholds = thresholds;
    }

    public int level(int points) {
        int level = 0;
        while (level < 10 && points >= thresholds[level + 1]) level++;
        return level;
    }

    /** Points at which a level begins. */
    public int floor(int level) {
        return thresholds[Math.clamp(level, 0, 10)];
    }

    /** Points at which the next level begins (the top level's own floor at 10). */
    public int next(int level) {
        return thresholds[Math.clamp(level + 1, 0, 10)];
    }

    /** The most points worth keeping: a little past the top level. */
    public int cap() {
        return thresholds[10] + 50;
    }
}
