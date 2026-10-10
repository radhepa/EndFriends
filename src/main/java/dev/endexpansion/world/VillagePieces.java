package dev.endexpansion.world;

import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.Identifier;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.StructureManager;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.StructurePiece;
import net.minecraft.world.level.levelgen.structure.TemplateStructurePiece;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePieceSerializationContext;
import net.minecraft.world.level.levelgen.structure.pieces.StructurePiecesBuilder;
import net.minecraft.world.level.levelgen.structure.templatesystem.BlockIgnoreProcessor;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplateManager;

/** The pieces of an End village: its ground first, then the planned tiles on top. */
public final class VillagePieces {
    /** How far above an islet's top the ground piece clears away old terrain. */
    static final int CLEAR = 48;

    private VillagePieces() {}

    static void addPieces(StructurePiecesBuilder builder, StructureTemplateManager templates, VillageLayout layout, BlockPos start, Rotation rotation) {
        builder.addPiece(new GroundPiece(layout, start, rotation));
        for (var tile : layout.tiles()) {
            BlockPos off = tile.offset();
            BlockPos turned = turn(off.getX() - layout.centerX(), off.getZ() - layout.centerZ(), rotation);
            builder.addPiece(new TilePiece(templates, tile.template(), start.offset(turned.getX(), off.getY(), turned.getZ()), rotation));
        }
        if (!layout.residents().isEmpty()) builder.addPiece(new ResidentPiece(layout, start, rotation));
    }

    /** A layout-space position (from the centre, y from the floor) in the world. */
    static BlockPos place(BlockPos start, BlockPos local, Rotation rotation) {
        BlockPos turned = turn(local.getX(), local.getZ(), rotation);
        return start.offset(turned.getX(), local.getY(), turned.getZ());
    }

    /** Layout-space (x, z) relative to the centre, turned as the templates are turned. */
    static BlockPos turn(int x, int z, Rotation rotation) {
        return StructureTemplate.transform(new BlockPos(x, 0, z), Mirror.NONE, rotation, BlockPos.ZERO);
    }

    static Rotation inverse(Rotation rotation) {
        return switch (rotation) {
            case CLOCKWISE_90 -> Rotation.COUNTERCLOCKWISE_90;
            case COUNTERCLOCKWISE_90 -> Rotation.CLOCKWISE_90;
            default -> rotation;
        };
    }

    /**
     * The village's islets. For each planned column it clears old terrain above the islet's top,
     * then lays end stone from the top down until it meets the island below or, over the void,
     * until the islet's underside ends.
     */
    public static final class GroundPiece extends StructurePiece {
        private final BlockPos origin;
        private final Rotation rotation;
        private final int width, depth, centerX, centerZ;
        private final byte[] tops, depths;

        GroundPiece(VillageLayout layout, BlockPos origin, Rotation rotation) {
            this(origin, rotation, layout.width(), layout.depth(), layout.centerX(), layout.centerZ(), layout.topBytes(), layout.depthBytes());
        }

        private GroundPiece(BlockPos origin, Rotation rotation, int width, int depth, int centerX, int centerZ, byte[] tops, byte[] depths) {
            super(EndVillages.GROUND_PIECE, 0, box(origin, rotation, width, depth, centerX, centerZ, tops, depths));
            this.origin = origin;
            this.rotation = rotation;
            this.width = width;
            this.depth = depth;
            this.centerX = centerX;
            this.centerZ = centerZ;
            this.tops = tops;
            this.depths = depths;
        }

        public GroundPiece(CompoundTag tag) {
            super(EndVillages.GROUND_PIECE, tag);
            this.origin = new BlockPos(tag.getIntOr("OX", 0), tag.getIntOr("OY", 0), tag.getIntOr("OZ", 0));
            this.rotation = tag.read("Rot", Rotation.LEGACY_CODEC).orElse(Rotation.NONE);
            this.width = tag.getIntOr("W", 0);
            this.depth = tag.getIntOr("D", 0);
            this.centerX = tag.getIntOr("CX", 0);
            this.centerZ = tag.getIntOr("CZ", 0);
            this.tops = tag.getByteArray("Tops").orElse(new byte[0]);
            this.depths = tag.getByteArray("Depths").orElse(new byte[0]);
        }

        private static BoundingBox box(BlockPos origin, Rotation rotation, int width, int depth, int centerX, int centerZ, byte[] tops, byte[] depths) {
            int low = Integer.MAX_VALUE, high = Integer.MIN_VALUE;
            for (int i = 0; i < tops.length; i++) {
                if (tops[i] == VillageLayout.NONE) continue;
                low = Math.min(low, tops[i] - (depths[i] & 0xFF));
                high = Math.max(high, tops[i]);
            }
            if (low > high) low = high = 0;
            BlockPos a = turn(-centerX, -centerZ, rotation), b = turn(width - 1 - centerX, depth - 1 - centerZ, rotation);
            return new BoundingBox(origin.getX() + Math.min(a.getX(), b.getX()), origin.getY() + low - 1, origin.getZ() + Math.min(a.getZ(), b.getZ()),
                    origin.getX() + Math.max(a.getX(), b.getX()), origin.getY() + high + CLEAR, origin.getZ() + Math.max(a.getZ(), b.getZ()));
        }

        @Override
        protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
            tag.putInt("OX", origin.getX());
            tag.putInt("OY", origin.getY());
            tag.putInt("OZ", origin.getZ());
            tag.store("Rot", Rotation.LEGACY_CODEC, rotation);
            tag.putInt("W", width);
            tag.putInt("D", depth);
            tag.putInt("CX", centerX);
            tag.putInt("CZ", centerZ);
            tag.putByteArray("Tops", tops);
            tag.putByteArray("Depths", depths);
        }

        /** The village start: the centre column at the village floor. */
        public BlockPos origin() {
            return origin;
        }

        public Rotation rotation() {
            return rotation;
        }

        /** Index into the ground arrays for a world column, or -1 outside the plan. */
        public int column(int x, int z) {
            BlockPos local = turn(x - origin.getX(), z - origin.getZ(), inverse(rotation));
            int lx = local.getX() + centerX, lz = local.getZ() + centerZ;
            if (lx < 0 || lz < 0 || lx >= width || lz >= depth) return -1;
            int i = lz * width + lx;
            return tops[i] == VillageLayout.NONE ? -1 : i;
        }

        public String describe(int x, int z) {
            int i = column(x, z);
            BlockPos local = turn(x - origin.getX(), z - origin.getZ(), inverse(rotation));
            return "local " + (local.getX() + centerX) + "," + (local.getZ() + centerZ) + " of " + width + "x" + depth + " index " + i
                    + (i >= 0 ? " top " + tops[i] + " depth " + (depths[i] & 0xFF) : "") + " (" + tops.length + " columns)";
        }

        /** Whether a world position lies on (or just over) one of the islets. */
        public boolean covers(BlockPos pos) {
            if (!boundingBox.isInside(pos)) return false;
            return column(pos.getX(), pos.getZ()) >= 0;
        }

        @Override
        public void postProcess(WorldGenLevel level, StructureManager structures, ChunkGenerator generator, RandomSource random,
                                BoundingBox chunk, ChunkPos chunkPos, BlockPos reference) {
            BlockState stone = Blocks.END_STONE.defaultBlockState(), air = Blocks.AIR.defaultBlockState();
            var pos = new BlockPos.MutableBlockPos();
            int minX = Math.max(chunk.minX(), boundingBox.minX()), maxX = Math.min(chunk.maxX(), boundingBox.maxX());
            int minZ = Math.max(chunk.minZ(), boundingBox.minZ()), maxZ = Math.min(chunk.maxZ(), boundingBox.maxZ());
            for (int x = minX; x <= maxX; x++) {
                for (int z = minZ; z <= maxZ; z++) {
                    int i = column(x, z);
                    if (i < 0) continue;
                    int top = origin.getY() + tops[i], under = depths[i] & 0xFF;
                    int surface = Math.min(level.getHeight(Heightmap.Types.WORLD_SURFACE_WG, x, z), top + CLEAR);
                    for (int y = top + 1; y < surface; y++) {
                        pos.set(x, y, z);
                        if (!level.getBlockState(pos).isAir()) level.setBlock(pos, air, 2);
                    }
                    for (int y = top; y >= top - under && y > level.getMinY(); y--) {
                        pos.set(x, y, z);
                        BlockState here = level.getBlockState(pos);
                        if (y < top && !here.isAir() && !here.canBeReplaced()) break;
                        level.setBlock(pos, stone, 2);
                    }
                }
            }
        }
    }

    /** One tile of the planned village, a template turned with the whole village. */
    public static final class TilePiece extends TemplateStructurePiece {
        TilePiece(StructureTemplateManager templates, Identifier template, BlockPos position, Rotation rotation) {
            super(EndVillages.TILE_PIECE, 0, templates, template, template.toString(), settings(rotation), position);
        }

        public TilePiece(StructureTemplateManager templates, CompoundTag tag) {
            super(EndVillages.TILE_PIECE, tag, templates, location -> settings(tag.read("Rot", Rotation.LEGACY_CODEC).orElse(Rotation.NONE)));
        }

        /** Air in a tile is placed (it carves sunken rooms and doorways); the block states are final. */
        private static StructurePlaceSettings settings(Rotation rotation) {
            return new StructurePlaceSettings().setRotation(rotation).setKnownShape(true).setIgnoreEntities(false)
                    .addProcessor(BlockIgnoreProcessor.STRUCTURE_BLOCK);
        }

        @Override
        protected void addAdditionalSaveData(StructurePieceSerializationContext context, CompoundTag tag) {
            super.addAdditionalSaveData(context, tag);
            tag.store("Rot", Rotation.LEGACY_CODEC, placeSettings.getRotation());
        }

        @Override
        protected void handleDataMarker(String marker, BlockPos position, ServerLevelAccessor level, RandomSource random, BoundingBox chunk) {
        }
    }
}
