package dev.endexpansion.world;

import com.mojang.serialization.Codec;
import com.mojang.serialization.MapCodec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.level.levelgen.structure.StructureType;

/**
 * An End village: one of a few pre-planned layouts, turned to a random side, set on the outer
 * islands. The layout's own islets are built under it, so a village can perch on an island's rim
 * and reach out over the void; only its centre has to stand on real land.
 */
public final class EndVillageStructure extends Structure {
    /**
     * Site survey around the start: samples {@code step} apart out to {@code radius}. At least
     * {@code minLand} of them must be land, and the median land height (the village floor) must lie
     * between {@code minY} and {@code maxY}. Sites closer than {@code minDistance} blocks to the
     * world's centre (the Dragon's island) are skipped.
     */
    public record Survey(int radius, int step, float minLand, int minY, int maxY, int minDistance) {
        public static final Survey DEFAULT = new Survey(12, 4, 0.6f, 40, 120, 1000);
        public static final Codec<Survey> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.intRange(0, 64).optionalFieldOf("radius", DEFAULT.radius).forGetter(Survey::radius),
            Codec.intRange(1, 32).optionalFieldOf("step", DEFAULT.step).forGetter(Survey::step),
            Codec.floatRange(0, 1).optionalFieldOf("min_land", DEFAULT.minLand).forGetter(Survey::minLand),
            Codec.INT.optionalFieldOf("min_y", DEFAULT.minY).forGetter(Survey::minY),
            Codec.INT.optionalFieldOf("max_y", DEFAULT.maxY).forGetter(Survey::maxY),
            Codec.intRange(0, 100000).optionalFieldOf("min_distance", DEFAULT.minDistance).forGetter(Survey::minDistance)
        ).apply(i, Survey::new));
    }

    public static final MapCodec<EndVillageStructure> CODEC = RecordCodecBuilder.mapCodec(i -> i.group(
        settingsCodec(i),
        VillageLayout.CODEC.listOf().fieldOf("layouts").forGetter(s -> s.layouts),
        Survey.CODEC.optionalFieldOf("survey", Survey.DEFAULT).forGetter(s -> s.survey)
    ).apply(i, EndVillageStructure::new));
    public static final StructureType<EndVillageStructure> TYPE = () -> CODEC;

    private final List<VillageLayout> layouts;
    private final Survey survey;

    /** Why sites were turned down or taken, counted for the game test. */
    public static final java.util.Map<String, java.util.concurrent.atomic.AtomicInteger> VERDICTS = new java.util.concurrent.ConcurrentHashMap<>();

    private static Optional<Integer> verdict(String reason, Optional<Integer> result) {
        VERDICTS.computeIfAbsent(reason, k -> new java.util.concurrent.atomic.AtomicInteger()).incrementAndGet();
        return result;
    }

    public EndVillageStructure(StructureSettings settings, List<VillageLayout> layouts, Survey survey) {
        super(settings);
        this.layouts = layouts;
        this.survey = survey;
    }

    public List<VillageLayout> layouts() {
        return layouts;
    }

    @Override
    public StructureType<?> type() {
        return TYPE;
    }

    /** The y of the top solid block, or below the world where the column is void. */
    private static int top(GenerationContext c, int x, int z) {
        return c.chunkGenerator().getFirstOccupiedHeight(x, z, Heightmap.Types.WORLD_SURFACE_WG, c.heightAccessor(), c.randomState());
    }

    /** The village floor at this site, or empty when the site is too small, too high or too low. */
    Optional<Integer> floor(GenerationContext c, int cx, int cz) {
        if ((long) cx * cx + (long) cz * cz < (long) survey.minDistance() * survey.minDistance()) return verdict("too close to the centre", Optional.empty());
        int land = c.heightAccessor().getMinY() + 4;
        int r = survey.radius(), step = survey.step(), samples = 0, found = 0;
        int[] heights = new int[(2 * r / step + 1) * (2 * r / step + 1)];
        for (int dx = -r; dx <= r; dx += step) {
            for (int dz = -r; dz <= r; dz += step) {
                if (dx * dx + dz * dz > r * r) continue;
                samples++;
                int y = top(c, cx + dx, cz + dz);
                if (y > land) heights[found++] = y;
            }
        }
        if (found == 0 || found < samples * survey.minLand()) return verdict("land " + found * 10 / Math.max(samples, 1) * 10 + "%", Optional.empty());
        int[] sorted = Arrays.copyOf(heights, found);
        Arrays.sort(sorted);
        int floor = sorted[found / 2];
        return floor < survey.minY() || floor > survey.maxY() ? verdict("floor " + floor / 10 * 10, Optional.empty()) : verdict("accepted", Optional.of(floor));
    }

    @Override
    protected Optional<GenerationStub> findGenerationPoint(GenerationContext context) {
        if (layouts.isEmpty()) return Optional.empty();
        int cx = context.chunkPos().getMiddleBlockX(), cz = context.chunkPos().getMiddleBlockZ();
        var floor = floor(context, cx, cz);
        if (floor.isEmpty()) return Optional.empty();
        var layout = layouts.get(context.random().nextInt(layouts.size()));
        var rotation = Rotation.getRandom(context.random());
        var start = new BlockPos(cx, floor.get(), cz);
        return Optional.of(new GenerationStub(start, builder -> VillagePieces.addPieces(builder, context.structureTemplateManager(), layout, start, rotation)));
    }
}
