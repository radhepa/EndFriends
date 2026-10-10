package dev.endexpansion.court;

import com.mojang.serialization.Codec;
import dev.endexpansion.EndExpansion;
import dev.endexpansion.talk.Bond;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.UUIDUtil;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.datafix.DataFixTypes;
import net.minecraft.world.level.saveddata.SavedData;
import net.minecraft.world.level.saveddata.SavedDataType;

/**
 * Each Citadel's Favor with each player, kept for good (the Eyes must be carried on every visit,
 * but the Court remembers what you have done). One {@link Bond} per Citadel per player.
 */
public final class CourtFavor extends SavedData {
    private static final Codec<Map<String, Map<UUID, Bond>>> MAPS =
            Codec.unboundedMap(Codec.STRING, Codec.unboundedMap(UUIDUtil.STRING_CODEC, Bond.CODEC));
    private static final Codec<CourtFavor> CODEC = MAPS.xmap(CourtFavor::new, f -> f.favor);
    private static final SavedDataType<CourtFavor> TYPE =
            new SavedDataType<>(EndExpansion.id("court_favor"), CourtFavor::new, CODEC, DataFixTypes.SAVED_DATA_COMMAND_STORAGE);

    private final Map<String, Map<UUID, Bond>> favor = new HashMap<>();

    public CourtFavor() {}

    private CourtFavor(Map<String, Map<UUID, Bond>> loaded) {
        loaded.forEach((citadel, players) -> favor.put(citadel, new HashMap<>(players)));
    }

    public static CourtFavor get(MinecraftServer server) {
        return server.getDataStorage().computeIfAbsent(TYPE);
    }

    /** A player's standing with one Citadel; changes to it are saved with the world. */
    public Bond bond(String citadel, UUID player) {
        setDirty();
        return favor.computeIfAbsent(citadel, k -> new HashMap<>()).computeIfAbsent(player, k -> new Bond());
    }
}
