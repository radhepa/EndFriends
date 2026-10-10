package dev.endexpansion.talk;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * What one resident (or one Citadel's Court) knows of one player: points toward the next level,
 * whether they have met, what was talked about and given today, when the player last hurt them and
 * how much of a grudge they still hold (it fades a step each day, or with an apology or a gift they
 * love). The Court also keeps the player's service task and whether the Lord has given them a hound.
 */
public final class Bond {
    public static final Codec<Bond> CODEC = RecordCodecBuilder.create(i -> i.group(
        Codec.INT.optionalFieldOf("points", 0).forGetter(b -> b.points),
        Codec.BOOL.optionalFieldOf("met", false).forGetter(b -> b.met),
        Codec.LONG.optionalFieldOf("day", -1L).forGetter(b -> b.day),
        Codec.STRING.listOf().optionalFieldOf("topics", List.of()).forGetter(b -> new ArrayList<>(b.topics)),
        Codec.INT.optionalFieldOf("gifts", 0).forGetter(b -> b.gifts),
        Codec.BOOL.optionalFieldOf("greeted", false).forGetter(b -> b.greeted),
        Codec.LONG.optionalFieldOf("hurt_until", 0L).forGetter(b -> b.hurtUntil),
        Codec.STRING.optionalFieldOf("task", "").forGetter(b -> b.task),
        Codec.BOOL.optionalFieldOf("hound", false).forGetter(b -> b.hound),
        Codec.INT.optionalFieldOf("grudge", 0).forGetter(b -> b.grudge),
        Codec.BOOL.optionalFieldOf("apologized", false).forGetter(b -> b.apologized)
    ).apply(i, Bond::new));
    public static final int MAX_GRUDGE = 5;

    public int points;
    public boolean met;
    /** The day (overworld days since the world began) the daily counts below belong to. */
    public long day;
    public final Set<String> topics;
    public int gifts;
    public boolean greeted;
    public long hurtUntil;
    public String task;
    public boolean hound;
    /** Blows not yet made up for; while there is one they won't stay to talk. */
    public int grudge;
    /** Said sorry today. */
    public boolean apologized;

    public Bond() {
        this(0, false, -1L, List.of(), 0, false, 0L, "", false, 0, false);
    }

    private Bond(int points, boolean met, long day, List<String> topics, int gifts, boolean greeted, long hurtUntil, String task, boolean hound,
                 int grudge, boolean apologized) {
        this.points = points;
        this.met = met;
        this.day = day;
        this.topics = new HashSet<>(topics);
        this.gifts = gifts;
        this.greeted = greeted;
        this.hurtUntil = hurtUntil;
        this.task = task;
        this.hound = hound;
        this.grudge = grudge;
        this.apologized = apologized;
    }

    /** Starts a new day's counts when the day has turned. */
    public void today(long today) {
        if (day == today) return;
        if (day >= 0 && today > day) grudge = (int) Math.max(0, grudge - Math.min(MAX_GRUDGE, today - day));
        day = today;
        topics.clear();
        gifts = 0;
        greeted = false;
        apologized = false;
    }
}
