package dev.endexpansion.mixin;

import dev.endexpansion.world.VillageGrounds;
import net.minecraft.core.BlockPos;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.chunk.ChunkGenerator;
import net.minecraft.world.level.levelgen.feature.ChorusPlantFeature;
import net.minecraft.world.level.levelgen.feature.EndIslandFeature;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Wild chorus and small floating islands skip End villages. */
@Mixin({ChorusPlantFeature.class, EndIslandFeature.class})
public abstract class VillageFeatureMixin {
    @Inject(method = "place", at = @At("HEAD"), cancellable = true)
    private void endexpansion$keepOutOfVillages(WorldGenLevel level, ChunkGenerator generator, RandomSource random, BlockPos origin,
                                                CallbackInfoReturnable<Boolean> cir) {
        if (VillageGrounds.occupied(origin)) cir.setReturnValue(false);
    }
}
