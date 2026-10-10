package dev.endexpansion.world;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.Base64;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.resources.Identifier;

/**
 * One finished village plan, written by {@code tools/villages/plan.py}.
 *
 * <p>Layout space: x east, z south, y up, with y = 0 the village floor (the top layer of the
 * central islet). {@code center} is the column that lands on the structure's start. The plan is
 * cut into {@code tiles}, each a template placed with its minimum corner at {@code offset}.
 *
 * <p>{@code ground} describes the floating islets the village brings with it: for every column of
 * the {@code width} x {@code depth} plan, the y of its top layer and how deep its underside hangs
 * when nothing lies below. Both are bytes (base64), {@link #NONE} where there is no islet.
 *
 * <p>{@code residents} is the roster ({@code tools/villages/roster.py}): who lives here, their job,
 * where they sleep (or stand guard) and where they work, in layout space from the centre.
 */
public record VillageLayout(String name, int width, int depth, int minY, int maxY, int centerX, int centerZ,
                            List<Tile> tiles, String tops, String depths, List<Resident> residents) {
    public static final int NONE = -128;

    public record Tile(Identifier template, BlockPos offset) {
        public static final Codec<Tile> CODEC = RecordCodecBuilder.create(i -> i.group(
            Identifier.CODEC.fieldOf("template").forGetter(Tile::template),
            BlockPos.CODEC.fieldOf("offset").forGetter(Tile::offset)
        ).apply(i, Tile::new));
    }

    /** One resident or animal: an entity id in this mod, a job ("" for none), home and work spots. */
    public record Resident(String type, String job, BlockPos home, Optional<BlockPos> work) {
        public static final Codec<Resident> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("type").forGetter(Resident::type),
            Codec.STRING.optionalFieldOf("job", "").forGetter(Resident::job),
            BlockPos.CODEC.fieldOf("home").forGetter(Resident::home),
            BlockPos.CODEC.optionalFieldOf("work").forGetter(Resident::work)
        ).apply(i, Resident::new));
    }

    public static final Codec<VillageLayout> CODEC = RecordCodecBuilder.create(i -> i.group(
        Codec.STRING.fieldOf("name").forGetter(VillageLayout::name),
        Codec.intRange(1, 512).fieldOf("width").forGetter(VillageLayout::width),
        Codec.intRange(1, 512).fieldOf("depth").forGetter(VillageLayout::depth),
        Codec.INT.fieldOf("min_y").forGetter(VillageLayout::minY),
        Codec.INT.fieldOf("max_y").forGetter(VillageLayout::maxY),
        Codec.INT.fieldOf("center_x").forGetter(VillageLayout::centerX),
        Codec.INT.fieldOf("center_z").forGetter(VillageLayout::centerZ),
        Tile.CODEC.listOf().fieldOf("tiles").forGetter(VillageLayout::tiles),
        Codec.STRING.fieldOf("tops").forGetter(VillageLayout::tops),
        Codec.STRING.fieldOf("depths").forGetter(VillageLayout::depths),
        Resident.CODEC.listOf().optionalFieldOf("residents", List.of()).forGetter(VillageLayout::residents)
    ).apply(i, VillageLayout::new));

    /** spire, stead, crossing or citadel: the part of the layout's name before the underscore. */
    public String kind() {
        int cut = name.indexOf('_');
        return cut < 0 ? name : name.substring(0, cut);
    }

    public byte[] topBytes() {
        return Base64.getDecoder().decode(tops);
    }

    public byte[] depthBytes() {
        return Base64.getDecoder().decode(depths);
    }
}
