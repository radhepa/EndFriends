package dev.endexpansion.world;

import dev.endexpansion.talk.DialogueBank;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import org.jspecify.annotations.Nullable;

/**
 * The village (or Citadel) a mob belongs to: its kind (spire, stead, crossing, citadel), its centre,
 * its name, and a key that stays the same for the life of the world (Court Favor is kept per key).
 */
public record Settlement(String kind, BlockPos center, String name) {
    /** For mobs that came from a spawn egg or a spawner: no village, a place name made up on the spot. */
    public static Settlement wild(String people, BlockPos at, RandomSource random) {
        String kind = switch (people) {
            case "chorrin" -> "stead";
            case "court" -> "citadel";
            default -> "spire";
        };
        return new Settlement("wild", at, place(kind, random));
    }

    public static Settlement of(String kind, BlockPos center) {
        return new Settlement(kind, center, place(kind, RandomSource.create(center.asLong() * 31 + kind.hashCode())));
    }

    /** Court Favor and outlawry are kept per Citadel under this key. */
    public String key() {
        return kind + "@" + center.getX() + "," + center.getY() + "," + center.getZ();
    }

    public boolean isWild() {
        return kind.equals("wild");
    }

    /** A village name from the people's bank: Spires and Crossings from the Shulkin places, Steads from the Chorrin's. */
    static String place(String kind, RandomSource random) {
        String bank = switch (kind) {
            case "stead" -> "chorrin";
            case "citadel" -> "court";
            default -> "shulkin";
        };
        List<String> places = DialogueBank.get(bank).places();
        String name = places.isEmpty() ? "the outer islands" : places.get(random.nextInt(places.size()));
        return kind.equals("crossing") ? "the Crossing below " + strip(name) : name;
    }

    private static String strip(String place) {
        return place.startsWith("the ") ? place.substring(4) : place;
    }

    public static @Nullable Settlement read(String kind, @Nullable BlockPos center, String name) {
        return center == null || kind.isEmpty() ? null : new Settlement(kind, center, name);
    }
}
