package dev.endexpansion.world;

import dev.endexpansion.EndExpansion;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceType;

/**
 * Registers the End village structure type and its pieces. The villages themselves are data:
 * {@code data/endexpansion/worldgen/structure/*.json}, written by {@code tools/villages/compile.py}
 * with every layout's tiles and islets.
 */
public final class EndVillages {
    public static final StructurePieceType GROUND_PIECE = Registry.register(BuiltInRegistries.STRUCTURE_PIECE,
            EndExpansion.id("village_ground"), (StructurePieceType.ContextlessType) VillagePieces.GroundPiece::new);
    public static final StructurePieceType TILE_PIECE = Registry.register(BuiltInRegistries.STRUCTURE_PIECE,
            EndExpansion.id("village_tile"), (StructurePieceType.StructureTemplateType) VillagePieces.TilePiece::new);
    public static final StructurePieceType RESIDENT_PIECE = Registry.register(BuiltInRegistries.STRUCTURE_PIECE,
            EndExpansion.id("village_residents"), (StructurePieceType.ContextlessType) ResidentPiece::new);

    private EndVillages() {}

    public static void register() {
        Registry.register(BuiltInRegistries.STRUCTURE_TYPE, EndExpansion.id("village"), EndVillageStructure.TYPE);
    }
}
