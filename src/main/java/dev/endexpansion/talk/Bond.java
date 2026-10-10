package dev.endexpansion.talk;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * What one resident (or one Citadel's Court) knows of one player: points toward the next level,
 * whether they have met, what was talked about and given today, and when the player last hurt them.
 * The Court also keeps the player's service task and whether the Lord has given them a hound.
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
        Codec.BOOL.optionalFieldOf("hound", false).forGetter(b -> b.hound)
    ).apply(i, Bond::new));

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

    public Bond() {
        this(0, false, -1L, List.of(), 0, false, 0L, "", false);
    }

    private Bond(int points, boolean met, long day, List<String> topics, int gifts, boolean greeted, long hurtUntil, String task, boolean hound) {
        this.points = points;
        this.met = met;
        this.day = day;
        this.topics = new HashSet<>(topics);
        this.gifts = gifts;
        this.greeted = greeted;
        this.hurtUntil = hurtUntil;
        this.task = task;
        this.hound = hound;
    }

    /** Starts a new day's counts when the day has turned. */
    public void today(long today) {
        if (day == today) return;
        day = today;
        topics.clear();
        gifts = 0;
        greeted = false;
    }
}
