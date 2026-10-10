package dev.endexpansion.entity;

import dev.endexpansion.world.Settlement;
import net.minecraft.core.BlockPos;
import org.jspecify.annotations.Nullable;

/** A mob a village spawns with a place in it: its village, job, bed or post, and workplace. */
public interface Settler {
    void settle(Settlement settlement, String job, BlockPos home, @Nullable BlockPos work);

    /** The village or Citadel it belongs to (a made-up one for spawn eggs). */
    Settlement settlement();
}
