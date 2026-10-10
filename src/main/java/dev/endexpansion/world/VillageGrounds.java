package dev.endexpansion.world;

import net.minecraft.core.BlockPos;
import net.minecraft.core.SectionPos;
import net.minecraft.world.level.StructureManager;

/**
 * Keeps wild chorus and stray floating islands out of End villages.
 *
 * <p>Vegetation is decorated after structures, so wild chorus would otherwise sprout on paths and
 * in doorways. While a chunk is being decorated, {@code ChunkGeneratorDecorationMixin} lends this
 * class the region's structure manager, and {@code VillageFeatureMixin} asks before each plant or
 * island. Planted groves are part of the village's own templates.
 */
public final class VillageGrounds {
    private static final ThreadLocal<StructureManager> DECORATING = new ThreadLocal<>();

    private VillageGrounds() {}

    public static void begin(StructureManager manager) {
        DECORATING.set(manager);
    }

    public static void end() {
        DECORATING.remove();
    }

    public static boolean occupied(BlockPos origin) {
        var manager = DECORATING.get();
        if (manager == null) return false;
        var starts = manager.startsForStructure(SectionPos.blockToSectionCoord(origin.getX()), SectionPos.blockToSectionCoord(origin.getZ()),
                structure -> structure instanceof EndVillageStructure);
        for (var start : starts) {
            var box = start.getBoundingBox();
            if (origin.getX() < box.minX() - 3 || origin.getX() > box.maxX() + 3 || origin.getZ() < box.minZ() - 3 || origin.getZ() > box.maxZ() + 3) continue;
            for (var piece : start.getPieces()) {
                if (piece instanceof VillagePieces.GroundPiece ground) {
                    for (int dx = -2; dx <= 2; dx += 2)
                        for (int dz = -2; dz <= 2; dz += 2)
                            if (ground.covers(origin.offset(dx, 0, dz))) return true;
                } else if (piece.getBoundingBox().isInside(origin)) {
                    return true;
                }
            }
        }
        return false;
    }
}
