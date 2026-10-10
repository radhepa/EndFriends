package dev.endexpansion.mixin;

import dev.endexpansion.EndExpansion;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.RandomSource;
import net.minecraft.world.RandomizableContainer;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.levelgen.structure.BoundingBox;
import net.minecraft.world.level.levelgen.structure.TemplateStructurePiece;
import net.minecraft.world.level.levelgen.structure.structures.EndCityPieces;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.level.storage.loot.LootTable;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * One End ship in five was a Court envoy's: its left-hand chest (beside the elytra) also holds a pair
 * of Enderman Eyes. The ship is chosen from its position, so both its chests agree.
 */
@Mixin(EndCityPieces.EndCityPiece.class)
public abstract class EndShipEyesMixin extends TemplateStructurePiece {
    /** The ship template's left chest marker, in template space. */
    private static final BlockPos ENVOY_CHEST = new BlockPos(5, 5, 7);
    private static final ResourceKey<LootTable> ENVOY = ResourceKey.create(Registries.LOOT_TABLE, EndExpansion.id("chests/envoy_ship"));
    private static final long SALT = 0x5EA1ED_E7E5L;

    private EndShipEyesMixin() {
        super(null, 0, null, null, null, null, null);
    }

    @Inject(method = "handleDataMarker", at = @At("TAIL"))
    private void endexpansion$envoyEyes(String marker, BlockPos position, ServerLevelAccessor level, RandomSource random, BoundingBox chunk,
                                        CallbackInfo ci) {
        if (!marker.startsWith("Chest") || !"ship".equals(templateName)) return;
        if (!position.equals(StructureTemplate.calculateRelativePosition(placeSettings, ENVOY_CHEST).offset(templatePosition))) return;
        BlockPos chest = position.below();
        if (!chunk.isInside(chest) || RandomSource.create(templatePosition.asLong() ^ SALT).nextInt(5) != 0) return;
        RandomizableContainer.setBlockEntityLootTable(level, random, chest, ENVOY);
    }
}
