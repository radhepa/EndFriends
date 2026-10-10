package dev.endexpansion.world;

import dev.endexpansion.EndExpansion;
import dev.endexpansion.entity.Settler;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.StructureManager;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.StructurePiece;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;

/**
 * A village's people and animals. Each one is spawned, once, when the chunk holding their home is
 * generated, already knowing their village, job, bed (or post) and workplace.
 */
public final class ResidentPiece extends StructurePiece {
    private final String kind;
    private final BlockPos center;
    private final List<VillageLayout.Resident> residents;

    ResidentPiece(VillageLayout layout, BlockPos start, Rotation rotation) {
        this(layout.kind(), start, layout.residents().stream().map(r -> new VillageLayout.Resident(r.type(), r.job(),
                VillagePieces.place(start, r.home(), rotation), r.work().map(w -> VillagePieces.place(start, w, rotation)))).toList());
    }

    private ResidentPiece(String kind, BlockPos center, List<VillageLayout.Resident> residents) {
        super(EndVillages.RESIDENT_PIECE, 0, box(center, residents));
        this.kind = kind;
        this.center = center;
        this.residents = residents;
    }

    public ResidentPiece(CompoundTag tag) {
        super(EndVillages.RESIDENT_PIECE, tag);
        this.kind = tag.getStringOr("Kind", "spire");
        this.center = tag.read("Center", BlockPos.CODEC).orElse(BlockPos.ZERO);
        this.residents = tag.read("Residents", VillageLayout.Resident.CODEC.listOf()).orElse(List.of());
    }

    private static BoundingBox box(BlockPos center, List<VillageLayout.Resident> residents) {
        List<BlockPos> all = new ArrayList<>();
        all.add(center);
        residents.forEach(r -> all.add(r.home()));
        return BoundingBox.encapsulatingPositions(all).orElseThrow();
    }

    @Override
    protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
        tag.putString("Kind", kind);
        tag.store("Center", BlockPos.CODEC, center);
        tag.store("Residents", VillageLayout.Resident.CODEC.listOf(), residents);
    }

    public Settlement settlement() {
        return Settlement.of(kind, center);
    }

    public List<VillageLayout.Resident> residents() {
        return residents;
    }

    @Override
    public void postProcess(WorldGenLevel level, StructureManager structures, ChunkGenerator generator, RandomSource random,
                            BoundingBox chunk, ChunkPos chunkPos, BlockPos reference) {
        Settlement settlement = null;
        for (var r : residents) {
            if (!chunk.isInside(r.home())) continue;
            var type = BuiltInRegistries.ENTITY_TYPE.getOptional(EndExpansion.id(r.type()));
            if (type.isEmpty()) {
                EndExpansion.LOG.warn("Unknown resident type {} in a {} village", r.type(), kind);
                continue;
            }
            if (!(type.get().create(level.getLevel(), EntitySpawnReason.STRUCTURE) instanceof Mob mob)) continue;
            if (settlement == null) settlement = settlement();
            BlockPos home = r.home();
            mob.snapTo(home.getX() + 0.5, home.getY(), home.getZ() + 0.5, random.nextFloat() * 360.0F, 0.0F);
            mob.setPersistenceRequired();
            mob.finalizeSpawn(level, level.getCurrentDifficultyAt(home), EntitySpawnReason.STRUCTURE, null);
            if (mob instanceof Settler settler) settler.settle(settlement, r.job(), home, r.work().orElse(null));
            level.addFreshEntityWithPassengers(mob);
        }
    }

    /** For tests and tools: where a layout's residents land for a start and rotation. */
    public static List<VillageLayout.Resident> placed(VillageLayout layout, BlockPos start, Rotation rotation) {
        return new ResidentPiece(layout, start, rotation).residents;
    }
}
